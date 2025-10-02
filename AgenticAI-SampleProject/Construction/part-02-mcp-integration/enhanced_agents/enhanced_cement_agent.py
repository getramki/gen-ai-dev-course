#!/usr/bin/env python3
"""
Enhanced Cement Agent with MCP Tool Integration
Extends Part 1 cement agent with FastMCP tools for advanced margin optimization
"""

from langgraph.graph import StateGraph, END
from langchain_aws import ChatBedrock
from typing import Dict, List, Optional, TypedDict
import httpx
import json
import sys
import os

# Define base classes (compatible with Part 1)
class CementState(TypedDict):
    rfq_id: str
    quantity: float
    base_price: float
    cost_per_ton: float
    current_offer: Dict
    competitor_offers: List[Dict]
    current_cycle: int
    negotiation_complete: bool

class CementAgent:
    """Base Cement Agent class"""
    def __init__(self):
        self.base_cost = 120
        self.base_price = 180
        self.inventory = 5000
        self.llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            region_name="us-east-1"
        )
    
    def _analyze_competition(self, state):
        return state
    
    def _finalize_offer(self, state):
        offer = state["current_offer"]
        offer["payment_terms"] = "net_30"
        offer["quality_grade"] = "A"
        offer["warranty"] = "standard"
        state["negotiation_complete"] = True
        return state

class EnhancedCementState(CementState):
    mcp_margin_analysis: Dict
    pricing_strategy: Dict
    inventory_status: Dict
    competitive_response: Dict

class EnhancedCementAgent(CementAgent):
    """Cement agent enhanced with MCP tools for advanced margin optimization"""
    
    def __init__(self, mcp_server_url: str = "http://localhost:8001"):
        super().__init__()
        self.mcp_server_url = mcp_server_url
        self.graph = self._build_enhanced_graph()
    
    def _build_enhanced_graph(self) -> StateGraph:
        """Build enhanced workflow with MCP tool integration"""
        workflow = StateGraph(EnhancedCementState)
        
        workflow.add_node("calculate_optimal_margin", self._calculate_optimal_margin_mcp)
        workflow.add_node("analyze_pricing_strategy", self._analyze_pricing_strategy_mcp)
        workflow.add_node("check_inventory", self._check_inventory_mcp)
        workflow.add_node("analyze_competition", self._analyze_competition_enhanced)
        workflow.add_node("calculate_competitive_response", self._calculate_competitive_response_mcp)
        workflow.add_node("finalize_offer", self._finalize_offer_enhanced)
        
        workflow.set_entry_point("calculate_optimal_margin")
        workflow.add_edge("calculate_optimal_margin", "analyze_pricing_strategy")
        workflow.add_edge("analyze_pricing_strategy", "check_inventory")
        workflow.add_edge("check_inventory", "analyze_competition")
        workflow.add_conditional_edges(
            "analyze_competition",
            self._should_calculate_response,
            {"calculate_response": "calculate_competitive_response", "finalize": "finalize_offer"}
        )
        workflow.add_edge("calculate_competitive_response", "finalize_offer")
        workflow.add_edge("finalize_offer", END)
        
        return workflow.compile()
    
    async def _call_mcp_tool(self, tool_name: str, **kwargs) -> Dict:
        """Call MCP tool via HTTP"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.mcp_server_url}/tools/{tool_name}",
                    json=kwargs,
                    timeout=30.0
                )
                return response.json()
        except Exception as e:
            print(f"⚠️ Cement MCP tool call failed: {e}")
            return {"error": str(e)}
    
    def _calculate_optimal_margin_mcp(self, state: EnhancedCementState) -> EnhancedCementState:
        """Calculate optimal margin using MCP tools with LLM reasoning"""
        quantity = state["quantity"]
        competitor_price = None
        
        if state["competitor_offers"]:
            competitor_prices = [offer.get("price_per_ton", float('inf')) for offer in state["competitor_offers"]]
            competitor_price = min(competitor_prices)
        
        # LLM reasoning for margin strategy
        margin_prompt = f"""
        As ABC Cement Co sales agent, determine optimal pricing strategy:
        - Order quantity: {quantity} tons
        - Our cost: ${self.base_cost}/ton
        - Competitor price: ${competitor_price or 'No competition'}
        - Market position: {'Competitive' if competitor_price else 'Market leader'}
        
        What should be our pricing strategy to maximize profit while staying competitive?
        Consider: margin targets, volume discounts, market positioning.
        """
        
        try:
            response = self.llm.invoke(margin_prompt)
            print(f"\n🧠 Cement Agent Pricing Strategy:\n{response.content}\n")
            state["pricing_reasoning"] = response.content
        except Exception as e:
            print(f"\n⚠️ Pricing reasoning failed: {e}")
            state["pricing_reasoning"] = "LLM unavailable - using rule-based logic"
        
        try:
            import asyncio
            result = asyncio.run(self._call_mcp_tool(
                "calculate_optimal_margin",
                quantity=quantity,
                competitor_price=competitor_price,
                grade="A"
            ))
            
            state["mcp_margin_analysis"] = result
            
            if "error" not in result:
                print(f"🧮 MCP Margin Analysis:")
                print(f"   Optimal Price: ${result.get('optimal_price', 0):.2f}/ton")
                print(f"   Optimal Margin: {result.get('optimal_margin', 0):.1%}")
                print(f"   Total Profit: ${result.get('total_profit', 0):,.2f}")
                print(f"   Competitive Advantage: ${result.get('competitive_advantage', 0):.2f}")
                
                # Update current offer with MCP recommendations
                state["current_offer"] = {
                    "price_per_ton": result.get("optimal_price", 180),
                    "total_price": result.get("total_revenue", 0),
                    "margin": result.get("optimal_margin", 0.2),
                    "discount": result.get("discount", 0),
                    "delivery_days": 15
                }
            
        except Exception as e:
            print(f"⚠️ MCP margin calculation failed: {e}")
            state["mcp_margin_analysis"] = {"error": str(e)}
        
        return state
    
    def _analyze_pricing_strategy_mcp(self, state: EnhancedCementState) -> EnhancedCementState:
        """Analyze pricing strategy using MCP tools"""
        quantity = state["quantity"]
        
        # Determine market conditions based on competition
        if state["competitor_offers"]:
            market_conditions = "competitive"
        else:
            market_conditions = "normal"
        
        try:
            import asyncio
            result = asyncio.run(self._call_mcp_tool(
                "analyze_pricing_strategy",
                order_size=quantity,
                market_conditions=market_conditions
            ))
            
            state["pricing_strategy"] = result
            
            if "error" not in result:
                print(f"📈 Pricing Strategy Analysis:")
                print(f"   Market Conditions: {result.get('market_conditions', 'unknown')}")
                print(f"   Strategy: {result.get('strategy', 'unknown')}")
                print(f"   Recommended Price: ${result.get('recommended_price', 0):.2f}/ton")
                print(f"   Expected Profit: ${result.get('total_profit', 0):,.2f}")
                
                # Adjust offer based on strategy
                if result.get("recommended_price", 0) > 0:
                    state["current_offer"]["price_per_ton"] = result["recommended_price"]
                    state["current_offer"]["total_price"] = result["recommended_price"] * quantity
                    state["current_offer"]["margin"] = result.get("final_margin", 0.2)
            
        except Exception as e:
            print(f"⚠️ Pricing strategy analysis failed: {e}")
            state["pricing_strategy"] = {"error": str(e)}
        
        return state
    
    def _check_inventory_mcp(self, state: EnhancedCementState) -> EnhancedCementState:
        """Check inventory availability using MCP tools"""
        quantity = state["quantity"]
        
        try:
            import asyncio
            result = asyncio.run(self._call_mcp_tool(
                "check_inventory_availability",
                quantity=quantity,
                grade="A"
            ))
            
            state["inventory_status"] = result
            
            if "error" not in result:
                print(f"📦 Inventory Status:")
                print(f"   Available: {result.get('available_quantity', 0)} tons")
                print(f"   Can Fulfill: {result.get('can_fulfill', False)}")
                print(f"   Carrying Cost: ${result.get('total_carrying_cost', 0):.2f}")
                print(f"   Inventory Status: {result.get('inventory_status', 'unknown')}")
                
                # Adjust pricing based on inventory levels
                if result.get("inventory_status") == "critical":
                    # Premium pricing for low inventory
                    current_price = state["current_offer"]["price_per_ton"]
                    state["current_offer"]["price_per_ton"] = current_price * 1.05
                    state["current_offer"]["total_price"] = state["current_offer"]["price_per_ton"] * quantity
                elif result.get("inventory_status") == "healthy":
                    # Competitive pricing for high inventory
                    current_price = state["current_offer"]["price_per_ton"]
                    state["current_offer"]["price_per_ton"] = current_price * 0.98
                    state["current_offer"]["total_price"] = state["current_offer"]["price_per_ton"] * quantity
            
        except Exception as e:
            print(f"⚠️ Inventory check failed: {e}")
            state["inventory_status"] = {"error": str(e)}
        
        return state
    
    def _analyze_competition_enhanced(self, state: EnhancedCementState) -> EnhancedCementState:
        """Enhanced competition analysis with MCP insights"""
        # Call parent method first
        state = super()._analyze_competition(state)
        
        # Add MCP-based competitive intelligence
        if state["competitor_offers"]:
            print(f"🏆 Enhanced Competitive Analysis:")
            print(f"   Competitors detected: {len(state['competitor_offers'])}")
            
            # Analyze our position
            our_price = state["current_offer"]["price_per_ton"]
            competitor_prices = [offer.get("price_per_ton", float('inf')) for offer in state["competitor_offers"]]
            
            if competitor_prices:
                min_competitor = min(competitor_prices)
                avg_competitor = sum(competitor_prices) / len(competitor_prices)
                
                print(f"   Our Price: ${our_price:.2f}/ton")
                print(f"   Competitor Min: ${min_competitor:.2f}/ton")
                print(f"   Competitor Avg: ${avg_competitor:.2f}/ton")
                
                if our_price <= min_competitor:
                    print(f"   Position: Price Leader ✅")
                elif our_price <= avg_competitor:
                    print(f"   Position: Competitive 📊")
                else:
                    print(f"   Position: Premium 💎")
        
        return state
    
    def _calculate_competitive_response_mcp(self, state: EnhancedCementState) -> EnhancedCementState:
        """Calculate competitive response using MCP tools"""
        if not state["competitor_offers"]:
            return state
        
        our_current_price = state["current_offer"]["price_per_ton"]
        
        try:
            import asyncio
            result = asyncio.run(self._call_mcp_tool(
                "calculate_competitive_response",
                competitor_offers=state["competitor_offers"],
                our_current_price=our_current_price
            ))
            
            state["competitive_response"] = result
            
            if "error" not in result:
                print(f"⚔️ Competitive Response Strategy:")
                print(f"   Strategy: {result.get('strategy', 'unknown')}")
                print(f"   Recommended Price: ${result.get('recommended_price', 0):.2f}/ton")
                print(f"   Price Change: ${result.get('price_change', 0):.2f}")
                print(f"   Risk Level: {result.get('risk_level', 'unknown')}")
                
                # Apply competitive response
                if result.get("recommended_price", 0) > 0:
                    quantity = state["quantity"]
                    state["current_offer"]["price_per_ton"] = result["recommended_price"]
                    state["current_offer"]["total_price"] = result["recommended_price"] * quantity
                    state["current_offer"]["margin"] = result.get("new_margin", 0.2)
                    state["current_offer"]["competitive_strategy"] = result.get("strategy", "unknown")
            
        except Exception as e:
            print(f"⚠️ Competitive response calculation failed: {e}")
            state["competitive_response"] = {"error": str(e)}
        
        return state
    
    def _finalize_offer_enhanced(self, state: EnhancedCementState) -> EnhancedCementState:
        """Enhanced offer finalization with MCP insights and LLM reasoning"""
        
        # LLM reasoning for final decision
        offer = state["current_offer"]
        
        decision_prompt = f"""
        As ABC Cement Co, finalize this offer:
        - Price: ${offer.get('price_per_ton', 0):.2f}/ton
        - Margin: {offer.get('margin', 0):.1%}
        - Quantity: {state['quantity']} tons
        - Competition: {len(state['competitor_offers'])} competitors
        
        Should we accept this deal? What terms should we offer?
        Consider: profitability, market share, customer relationship.
        """
        
        try:
            response = self.llm.invoke(decision_prompt)
            print(f"\n🎯 Cement Agent Final Decision:\n{response.content}\n")
            state["final_reasoning"] = response.content
        except Exception as e:
            print(f"\n⚠️ Final decision reasoning failed: {e}")
            state["final_reasoning"] = "LLM unavailable - using rule-based logic"
        
        # Call parent finalization
        state = super()._finalize_offer(state)
        
        # Add MCP-based final adjustments
        offer = state["current_offer"]
        
        print(f"\n🎯 Final Cement Offer with MCP Analysis:")
        print(f"   Price: ${offer.get('price_per_ton', 0):.2f}/ton")
        print(f"   Total: ${offer.get('total_price', 0):,.2f}")
        print(f"   Margin: {offer.get('margin', 0):.1%}")
        
        # Add MCP insights to offer
        if "mcp_margin_analysis" in state and "error" not in state["mcp_margin_analysis"]:
            mcp_data = state["mcp_margin_analysis"]
            offer["mcp_profit_projection"] = mcp_data.get("total_profit", 0)
            offer["mcp_competitive_advantage"] = mcp_data.get("competitive_advantage", 0)
        
        if "pricing_strategy" in state and "error" not in state["pricing_strategy"]:
            strategy_data = state["pricing_strategy"]
            offer["pricing_strategy"] = strategy_data.get("strategy", "unknown")
        
        if "inventory_status" in state and "error" not in state["inventory_status"]:
            inventory_data = state["inventory_status"]
            offer["inventory_impact"] = inventory_data.get("inventory_status", "unknown")
        
        # Record sale in MCP system
        try:
            import asyncio
            asyncio.run(self._call_mcp_tool(
                "record_sale",
                customer="Construction_Co",
                quantity=state["quantity"],
                price_per_ton=offer["price_per_ton"]
            ))
            print(f"   ✅ Sale recorded in MCP system")
        except Exception as e:
            print(f"   ⚠️ Failed to record sale: {e}")
        
        return state
    
    def _should_calculate_response(self, state: EnhancedCementState) -> str:
        """Determine if competitive response calculation is needed"""
        if state["competitor_offers"] and len(state["competitor_offers"]) > 0:
            return "calculate_response"
        return "finalize"
    
    def generate_quote_enhanced(self, rfq: Dict, competitor_offers: List[Dict] = None) -> Dict:
        """Enhanced quote generation with MCP tools"""
        initial_state = EnhancedCementState(
            rfq_id=rfq.get("id", "rfq_001"),
            quantity=rfq.get("cement_tons", 100),
            base_price=self.base_price,
            cost_per_ton=self.base_cost,
            current_offer={},
            competitor_offers=competitor_offers or [],
            current_cycle=1,
            negotiation_complete=False,
            mcp_margin_analysis={},
            pricing_strategy={},
            inventory_status={},
            competitive_response={}
        )
        
        result = self.graph.invoke(initial_state)
        return result["current_offer"]