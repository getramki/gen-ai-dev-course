#!/usr/bin/env python3
"""
Enhanced Purchase Agent with MCP Tool Integration
Extends Part 1 purchase agent with FastMCP tools for advanced profit optimization
"""

from langgraph.graph import StateGraph, END
from langchain_aws import ChatBedrock
from typing import Dict, List, Optional, TypedDict
import httpx
import json
import sys
import os

# Define base classes (compatible with Part 1)
class PurchaseState(TypedDict):
    task_id: str
    requirements: Dict
    budget: float
    received_quotes: List[Dict]
    selected_suppliers: List[Dict]
    current_cycle: int
    negotiation_complete: bool

class PurchaseAgent:
    """Base Purchase Agent class"""
    def __init__(self):
        self.llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            region_name="us-east-1"
        )
    
    def _analyze_requirements(self, state):
        # Basic requirements analysis
        cement_qty = state["requirements"].get("cement_tons", 0)
        steel_qty = state["requirements"].get("steel_tons", 0)
        budget = state["budget"]
        
        state["requirements"]["target_cement_price"] = min(150, budget * 0.4 / cement_qty if cement_qty > 0 else 0)
        state["requirements"]["target_steel_price"] = min(600, budget * 0.6 / steel_qty if steel_qty > 0 else 0)
        return state
    
    def _evaluate_quotes(self, state):
        return state
    
    def _make_counter_offer(self, state):
        return state
    
    def _finalize_selection(self, state):
        return state
    
    def _should_negotiate(self, state):
        return "finalize"

class EnhancedPurchaseState(PurchaseState):
    mcp_analysis: Dict
    roi_projection: Dict
    budget_tracking: Dict
    supplier_performance: Dict

class EnhancedPurchaseAgent(PurchaseAgent):
    """Purchase agent enhanced with MCP tools for advanced cost optimization"""
    
    def __init__(self, mcp_server_url: str = "http://localhost:8000"):
        super().__init__()
        self.mcp_server_url = mcp_server_url
        self.graph = self._build_enhanced_graph()
    
    def _build_enhanced_graph(self) -> StateGraph:
        """Build enhanced workflow with MCP tool integration"""
        workflow = StateGraph(EnhancedPurchaseState)
        
        workflow.add_node("analyze_requirements", self._analyze_requirements_with_tools)
        workflow.add_node("calculate_total_cost", self._calculate_total_cost_mcp)
        workflow.add_node("track_budget", self._track_budget_mcp)
        workflow.add_node("analyze_suppliers", self._analyze_suppliers_mcp)
        workflow.add_node("calculate_roi", self._calculate_roi_mcp)
        workflow.add_node("evaluate_quotes", self._evaluate_quotes_enhanced)
        workflow.add_node("make_counter_offer", self._make_counter_offer)
        workflow.add_node("finalize_selection", self._finalize_selection_enhanced)
        
        workflow.set_entry_point("analyze_requirements")
        workflow.add_edge("analyze_requirements", "calculate_total_cost")
        workflow.add_edge("calculate_total_cost", "track_budget")
        workflow.add_edge("track_budget", "analyze_suppliers")
        workflow.add_edge("analyze_suppliers", "calculate_roi")
        workflow.add_edge("calculate_roi", "evaluate_quotes")
        workflow.add_conditional_edges(
            "evaluate_quotes",
            self._should_negotiate,
            {"negotiate": "make_counter_offer", "finalize": "finalize_selection"}
        )
        workflow.add_edge("make_counter_offer", "evaluate_quotes")
        workflow.add_edge("finalize_selection", END)
        
        return workflow.compile()
    
    async def _call_mcp_tool(self, tool_name: str, **kwargs) -> Dict:
        """Call MCP tool via HTTP"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.mcp_server_url}/tools/{tool_name}",
                    json=kwargs,
                    timeout=10.0
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"HTTP {response.status_code}: {response.text}"}
        except httpx.ConnectError:
            print(f"⚠️ MCP server not available at {self.mcp_server_url}")
            return {"error": "MCP server not available"}
        except Exception as e:
            print(f"⚠️ MCP tool call failed: {e}")
            return {"error": str(e)}
    
    def _analyze_requirements_with_tools(self, state: EnhancedPurchaseState) -> EnhancedPurchaseState:
        """Enhanced requirements analysis using MCP tools"""
        # LLM reasoning for procurement strategy
        cement_qty = state["requirements"].get("cement_tons", 0)
        steel_qty = state["requirements"].get("steel_tons", 0)
        budget = state["budget"]
        
        reasoning_prompt = f"""
        As Construction Co procurement agent, analyze this purchase requirement:
        - Budget: ${budget:,}
        - Cement needed: {cement_qty} tons
        - Steel needed: {steel_qty} tons
        
        What should be our procurement strategy to minimize costs while ensuring quality?
        Consider: budget allocation, target prices, supplier selection criteria.
        """
        
        try:
            response = self.llm.invoke(reasoning_prompt)
            print(f"\n🧠 Purchase Agent LLM Reasoning:\n{response.content}\n")
            state["llm_reasoning"] = response.content
        except Exception as e:
            print(f"\n⚠️ LLM reasoning failed: {e}")
            state["llm_reasoning"] = "LLM unavailable - using rule-based logic"
        
        # Call parent method
        state = super()._analyze_requirements(state)
        
        # Create project in MCP system
        project_data = {
            "project_id": state["task_id"],
            "name": f"Procurement {state['task_id']}",
            "budget": state["budget"]
        }
        
        try:
            import asyncio
            result = asyncio.run(self._call_mcp_tool("create_project", **project_data))
            state["mcp_analysis"] = result
            print(f"📊 MCP Project Created: {result.get('message', 'Success')}")
        except Exception as e:
            print(f"⚠️ MCP project creation failed: {e}")
            state["mcp_analysis"] = {"error": str(e)}
        
        return state
    
    def _calculate_total_cost_mcp(self, state: EnhancedPurchaseState) -> EnhancedPurchaseState:
        """Calculate total cost using MCP tools"""
        cement_qty = state["requirements"].get("cement_tons", 0)
        steel_qty = state["requirements"].get("steel_tons", 0)
        cement_price = state["requirements"].get("target_cement_price", 150)
        steel_price = state["requirements"].get("target_steel_price", 600)
        
        try:
            import asyncio
            result = asyncio.run(self._call_mcp_tool(
                "calculate_total_cost",
                cement_tons=cement_qty,
                cement_price=cement_price,
                steel_tons=steel_qty,
                steel_price=steel_price
            ))
            
            state["mcp_analysis"]["cost_analysis"] = result
            
            print(f"💰 MCP Cost Analysis:")
            print(f"   Total Cost: ${result.get('total_cost', 0):,.2f}")
            print(f"   Savings: ${result.get('savings', 0):,.2f} ({result.get('savings_percentage', 0):.1f}%)")
            print(f"   Within Constraints: {result.get('within_constraints', False)}")
            
        except Exception as e:
            print(f"⚠️ MCP cost calculation failed: {e}")
        
        return state
    
    def _track_budget_mcp(self, state: EnhancedPurchaseState) -> EnhancedPurchaseState:
        """Track budget utilization using MCP tools"""
        proposed_cost = state["mcp_analysis"].get("cost_analysis", {}).get("total_cost", 0)
        
        try:
            import asyncio
            result = asyncio.run(self._call_mcp_tool(
                "track_budget_utilization",
                project_id=state["task_id"],
                proposed_cost=proposed_cost
            ))
            
            state["budget_tracking"] = result
            
            print(f"📈 Budget Tracking:")
            print(f"   Utilization: {result.get('utilization_percentage', 0):.1f}%")
            print(f"   Status: {result.get('budget_status', 'unknown')}")
            print(f"   Remaining: ${result.get('projected_remaining', 0):,.2f}")
            
        except Exception as e:
            print(f"⚠️ Budget tracking failed: {e}")
            state["budget_tracking"] = {"error": str(e)}
        
        return state
    
    def _analyze_suppliers_mcp(self, state: EnhancedPurchaseState) -> EnhancedPurchaseState:
        """Analyze supplier performance using MCP tools"""
        # Analyze both cement and steel suppliers
        suppliers = ["ABC_Cement", "XYZ_Steel"]
        supplier_analysis = {}
        
        for supplier in suppliers:
            try:
                import asyncio
                result = asyncio.run(self._call_mcp_tool(
                    "analyze_supplier_performance",
                    supplier_name=supplier
                ))
                supplier_analysis[supplier] = result
                
                if "error" not in result:
                    print(f"🏭 {supplier} Performance:")
                    print(f"   Total Orders: {result.get('total_orders', 0)}")
                    print(f"   Total Value: ${result.get('total_value', 0):,.2f}")
                
            except Exception as e:
                print(f"⚠️ Supplier analysis failed for {supplier}: {e}")
                supplier_analysis[supplier] = {"error": str(e)}
        
        state["supplier_performance"] = supplier_analysis
        return state
    
    def _calculate_roi_mcp(self, state: EnhancedPurchaseState) -> EnhancedPurchaseState:
        """Calculate ROI projection using MCP tools"""
        investment = state["budget"]
        savings = state["mcp_analysis"].get("cost_analysis", {}).get("savings", 0)
        
        try:
            import asyncio
            result = asyncio.run(self._call_mcp_tool(
                "calculate_roi_projection",
                investment=investment,
                material_savings=savings,
                project_duration_months=12
            ))
            
            state["roi_projection"] = result
            
            print(f"📊 ROI Projection:")
            print(f"   ROI: {result.get('roi_percentage', 0):.1f}%")
            print(f"   Payback: {result.get('payback_period_months', 0):.1f} months")
            print(f"   Recommendation: {result.get('recommendation', 'unknown')}")
            
        except Exception as e:
            print(f"⚠️ ROI calculation failed: {e}")
            state["roi_projection"] = {"error": str(e)}
        
        return state
    
    def _evaluate_quotes_enhanced(self, state: EnhancedPurchaseState) -> EnhancedPurchaseState:
        """Enhanced quote evaluation with MCP insights and LLM reasoning"""
        
        # LLM reasoning for quote evaluation
        if state["received_quotes"]:
            quotes_summary = "\n".join([
                f"Quote {i+1}: ${quote.get('total_cost', 0):,.2f} (Supplier: {quote.get('supplier', 'Unknown')})"
                for i, quote in enumerate(state["received_quotes"][:3])  # Show top 3
            ])
            
            evaluation_prompt = f"""
            As Construction Co procurement agent, evaluate these quotes:
            {quotes_summary}
            
            Budget: ${state['budget']:,}
            MCP Analysis Available: {bool(state.get('mcp_analysis'))}
            
            Which quote should we select and why? Consider:
            - Total cost vs budget
            - MCP tool insights
            - Risk factors
            - Supplier reliability
            """
            
            try:
                response = self.llm.invoke(evaluation_prompt)
                print(f"\n🤔 Quote Evaluation Reasoning:\n{response.content}\n")
            except Exception as e:
                print(f"\n⚠️ Quote evaluation reasoning failed: {e}")
        # Call parent evaluation
        state = super()._evaluate_quotes(state)
        
        # Add MCP-based evaluation criteria
        if state["received_quotes"] and "mcp_analysis" in state:
            cost_analysis = state["mcp_analysis"].get("cost_analysis", {})
            budget_tracking = state.get("budget_tracking", {})
            
            for quote in state["received_quotes"]:
                # Add MCP scoring
                quote["mcp_score"] = 0
                
                # Budget compliance score
                if quote["total_cost"] <= budget_tracking.get("remaining", float('inf')):
                    quote["mcp_score"] += 30
                
                # Savings score
                max_budget = cost_analysis.get("max_budget", quote["total_cost"])
                savings_ratio = (max_budget - quote["total_cost"]) / max_budget if max_budget > 0 else 0
                quote["mcp_score"] += savings_ratio * 40
                
                # Constraint compliance score
                if cost_analysis.get("within_constraints", False):
                    quote["mcp_score"] += 30
                
                quote["mcp_recommendation"] = (
                    "highly_recommended" if quote["mcp_score"] >= 80 else
                    "recommended" if quote["mcp_score"] >= 60 else
                    "acceptable" if quote["mcp_score"] >= 40 else
                    "not_recommended"
                )
            
            # Re-sort by MCP score
            state["received_quotes"].sort(key=lambda x: x.get("mcp_score", 0), reverse=True)
        
        return state
    
    def _finalize_selection_enhanced(self, state: EnhancedPurchaseState) -> EnhancedPurchaseState:
        """Enhanced finalization with MCP insights"""
        # Call parent finalization
        state = super()._finalize_selection(state)
        
        # Add MCP-based final analysis
        if state["selected_suppliers"]:
            selected = state["selected_suppliers"][0]
            
            print(f"\n🎯 Final Selection with MCP Analysis:")
            print(f"   Selected Supplier: {selected.get('supplier', 'Unknown')}")
            print(f"   Total Cost: ${selected.get('total_cost', 0):,.2f}")
            print(f"   MCP Score: {selected.get('mcp_score', 0):.1f}/100")
            print(f"   MCP Recommendation: {selected.get('mcp_recommendation', 'unknown')}")
            
            # ROI summary
            roi_data = state.get("roi_projection", {})
            if "error" not in roi_data:
                print(f"   Projected ROI: {roi_data.get('roi_percentage', 0):.1f}%")
                print(f"   Payback Period: {roi_data.get('payback_period_months', 0):.1f} months")
        
        return state
    
    def process_procurement_enhanced(self, requirements: Dict, budget: float) -> Dict:
        """Enhanced procurement processing with MCP tools"""
        initial_state = EnhancedPurchaseState(
            task_id=f"enhanced_procurement_{hash(str(requirements))}",
            requirements=requirements,
            budget=budget,
            received_quotes=[],
            selected_suppliers=[],
            current_cycle=1,
            negotiation_complete=False,
            mcp_analysis={},
            roi_projection={},
            budget_tracking={},
            supplier_performance={}
        )
        
        result = self.graph.invoke(initial_state)
        return result