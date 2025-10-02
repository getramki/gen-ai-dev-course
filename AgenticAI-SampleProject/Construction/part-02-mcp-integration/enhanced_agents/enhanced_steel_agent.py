#!/usr/bin/env python3
"""
Enhanced Steel Agent with MCP Tool Integration
Extends Part 1 steel agent with FastMCP tools for advanced inventory and profit optimization
"""

from langgraph.graph import StateGraph, END
from langchain_aws import ChatBedrock
from typing import Dict, List, Optional, TypedDict
import httpx
import json
import sys
import os

# Define base classes (compatible with Part 1)
class SteelState(TypedDict):
    rfq_id: str
    quantity: float
    grade: str
    base_price: float
    storage_cost: float
    current_offer: Dict
    competitor_offers: List[Dict]
    current_cycle: int
    negotiation_complete: bool

class SteelAgent:
    """Base Steel Agent class"""
    def __init__(self):
        self.grade_costs = {"A": 500, "B": 400, "C": 300}
        self.grade_prices = {"A": 750, "B": 600, "C": 450}
        self.storage_cost_per_ton = 5
        self.inventory = {"A": 2000, "B": 3000, "C": 5000}
        self.llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            region_name="us-east-1"
        )
    
    def _finalize_terms(self, state):
        offer = state["current_offer"]
        offer["payment_terms"] = "net_30"
        offer["warranty"] = "12_months"
        state["negotiation_complete"] = True
        return state

class EnhancedSteelState(SteelState):
    inventory_analysis: Dict
    grade_optimization: Dict
    market_positioning: Dict
    delivery_analysis: Dict
    bulk_strategy: Dict

class EnhancedSteelAgent(SteelAgent):
    """Steel agent enhanced with MCP tools for advanced inventory and profit optimization"""
    
    def __init__(self, mcp_server_url: str = "http://localhost:8002"):
        super().__init__()
        self.mcp_server_url = mcp_server_url
        self.graph = self._build_enhanced_graph()
    
    def _build_enhanced_graph(self) -> StateGraph:
        """Build enhanced workflow with MCP tool integration"""
        workflow = StateGraph(EnhancedSteelState)
        
        workflow.add_node("calculate_inventory_costs", self._calculate_inventory_costs_mcp)
        workflow.add_node("optimize_grade_pricing", self._optimize_grade_pricing_mcp)
        workflow.add_node("analyze_market_position", self._analyze_market_position_mcp)
        workflow.add_node("calculate_delivery_impact", self._calculate_delivery_impact_mcp)
        workflow.add_node("evaluate_bulk_strategy", self._evaluate_bulk_strategy_mcp)
        workflow.add_node("finalize_terms", self._finalize_terms_enhanced)
        
        workflow.set_entry_point("calculate_inventory_costs")
        workflow.add_edge("calculate_inventory_costs", "optimize_grade_pricing")
        workflow.add_edge("optimize_grade_pricing", "analyze_market_position")
        workflow.add_edge("analyze_market_position", "calculate_delivery_impact")
        workflow.add_conditional_edges(
            "calculate_delivery_impact",
            self._should_evaluate_bulk,
            {"bulk": "evaluate_bulk_strategy", "finalize": "finalize_terms"}
        )
        workflow.add_edge("evaluate_bulk_strategy", "finalize_terms")
        workflow.add_edge("finalize_terms", END)
        
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
            print(f"⚠️ Steel MCP tool call failed: {e}")
            return {"error": str(e)}
    
    def _calculate_inventory_costs_mcp(self, state: EnhancedSteelState) -> EnhancedSteelState:
        """Calculate inventory carrying costs using MCP tools"""
        grade = state["grade"]
        quantity = state["quantity"]
        
        try:
            import asyncio
            result = asyncio.run(self._call_mcp_tool(
                "calculate_inventory_carrying_cost",
                grade=grade,
                quantity=quantity,
                months_projected=3
            ))
            
            state["inventory_analysis"] = result
            
            if "error" not in result:
                print(f"📦 Inventory Cost Analysis:")
                print(f"   Base Cost: ${result.get('base_cost_per_ton', 0):.2f}/ton")
                print(f"   Carrying Cost: ${result.get('carrying_cost_per_ton', 0):.2f}/ton")
                print(f"   Adjusted Cost: ${result.get('adjusted_cost_per_ton', 0):.2f}/ton")
                print(f"   Total Carrying Cost: ${result.get('total_carrying_cost', 0):,.2f}")
                
                # Update base cost with carrying costs
                state["cost_per_ton"] = result.get("adjusted_cost_per_ton", state["cost_per_ton"])
            
        except Exception as e:
            print(f"⚠️ Inventory cost calculation failed: {e}")
            state["inventory_analysis"] = {"error": str(e)}
        
        return state
    
    def _optimize_grade_pricing_mcp(self, state: EnhancedSteelState) -> EnhancedSteelState:
        """Optimize pricing by grade using MCP tools with LLM reasoning"""
        quantity = state["quantity"]
        grade = state["grade"]
        
        # LLM reasoning for grade-based pricing
        pricing_prompt = f"""
        As XYZ Steel Co sales agent, optimize pricing for this order:
        - Grade: {grade} steel
        - Quantity: {quantity} tons
        - Our cost: ${self.grade_costs.get(grade, 500)}/ton
        - Inventory: {self.inventory.get(grade, 0)} tons available
        
        What should be our pricing strategy for this grade and quantity?
        Consider: grade premium, volume discounts, inventory levels, profit margins.
        """
        
        try:
            response = self.llm.invoke(pricing_prompt)
            print(f"\n🧠 Steel Agent Grade Pricing Strategy:\n{response.content}\n")
            state["grade_reasoning"] = response.content
        except Exception as e:
            print(f"\n⚠️ Grade pricing reasoning failed: {e}")
            state["grade_reasoning"] = "LLM unavailable - using rule-based logic"
        
        # Determine urgency based on quantity and grade
        if quantity >= 200:
            urgency = "normal"
        elif grade == "A":
            urgency = "urgent"  # Premium grade often urgent
        else:
            urgency = "flexible"
        
        try:
            import asyncio
            result = asyncio.run(self._call_mcp_tool(
                "optimize_grade_pricing",
                quantity=quantity,
                grade=grade,
                urgency=urgency
            ))
            
            state["grade_optimization"] = result
            
            if "error" not in result:
                print(f"⚙️ Grade Pricing Optimization:")
                print(f"   Grade: {result.get('grade', 'unknown')}")
                print(f"   Final Price: ${result.get('final_price', 0):.2f}/ton")
                print(f"   Margin: {result.get('margin', 0):.1%}")
                print(f"   Total Profit: ${result.get('total_profit', 0):,.2f}")
                print(f"   Can Fulfill: {result.get('can_fulfill', False)}")
                
                # Update current offer with optimized pricing
                state["current_offer"] = {
                    "price_per_ton": result.get("final_price", 600),
                    "total_price": result.get("total_revenue", 0),
                    "margin": result.get("margin", 0.12),
                    "grade": grade,
                    "delivery_days": 20,
                    "inventory_available": result.get("available_inventory", 0)
                }
            
        except Exception as e:
            print(f"⚠️ Grade pricing optimization failed: {e}")
            state["grade_optimization"] = {"error": str(e)}
        
        return state
    
    def _analyze_market_position_mcp(self, state: EnhancedSteelState) -> EnhancedSteelState:
        """Analyze market positioning using MCP tools"""
        grade = state["grade"]
        
        # Extract competitor prices if available
        competitor_prices = []
        if state["competitor_offers"]:
            competitor_prices = [offer.get("price_per_ton", 0) for offer in state["competitor_offers"]]
        
        if competitor_prices:
            try:
                import asyncio
                result = asyncio.run(self._call_mcp_tool(
                    "analyze_market_positioning",
                    grade=grade,
                    competitor_prices=competitor_prices
                ))
                
                state["market_positioning"] = result
                
                if "error" not in result:
                    print(f"📊 Market Positioning Analysis:")
                    print(f"   Recommended Strategy: {result.get('recommended_strategy', 'unknown')}")
                    print(f"   Recommended Price: ${result.get('recommended_price', 0):.2f}/ton")
                    print(f"   Competitive Advantage: ${result.get('market_analysis', {}).get('competitor_min', 0) - result.get('recommended_price', 0):.2f}")
                    
                    # Adjust pricing based on market analysis
                    if result.get("recommended_price", 0) > 0:
                        quantity = state["quantity"]
                        state["current_offer"]["price_per_ton"] = result["recommended_price"]
                        state["current_offer"]["total_price"] = result["recommended_price"] * quantity
                        
                        # Recalculate margin with new price
                        cost = state["cost_per_ton"]
                        new_margin = (result["recommended_price"] - cost) / result["recommended_price"]
                        state["current_offer"]["margin"] = new_margin
                        state["current_offer"]["market_strategy"] = result.get("recommended_strategy", "unknown")
                
            except Exception as e:
                print(f"⚠️ Market positioning analysis failed: {e}")
                state["market_positioning"] = {"error": str(e)}
        else:
            print(f"📊 No competitors detected - maintaining premium positioning")
            state["market_positioning"] = {"strategy": "premium_position", "competitors": 0}
        
        return state
    
    def _calculate_delivery_impact_mcp(self, state: EnhancedSteelState) -> EnhancedSteelState:
        """Calculate delivery cost impact using MCP tools"""
        quantity = state["quantity"]
        distance_km = 150  # Default delivery distance
        urgency = "normal"
        
        try:
            import asyncio
            result = asyncio.run(self._call_mcp_tool(
                "calculate_delivery_cost_impact",
                quantity=quantity,
                distance_km=distance_km,
                urgency=urgency
            ))
            
            state["delivery_analysis"] = result
            
            if "error" not in result:
                print(f"🚚 Delivery Cost Analysis:")
                print(f"   Total Delivery Cost: ${result.get('costs', {}).get('total_delivery_cost', 0):.2f}")
                print(f"   Cost per Ton: ${result.get('costs', {}).get('cost_per_ton', 0):.2f}")
                
                pricing_options = result.get("pricing_options", {})
                absorb_recommended = pricing_options.get("absorb_cost", {}).get("recommended", False)
                
                if absorb_recommended:
                    print(f"   Strategy: Absorb delivery cost")
                    # Adjust margin to account for delivery cost
                    delivery_cost_per_ton = result.get("costs", {}).get("cost_per_ton", 0)
                    current_price = state["current_offer"]["price_per_ton"]
                    adjusted_cost = state["cost_per_ton"] + delivery_cost_per_ton
                    new_margin = (current_price - adjusted_cost) / current_price if current_price > 0 else 0
                    state["current_offer"]["adjusted_margin"] = new_margin
                else:
                    print(f"   Strategy: Pass through delivery cost")
                    additional_charge = result.get("costs", {}).get("total_delivery_cost", 0)
                    state["current_offer"]["delivery_charge"] = additional_charge
                    state["current_offer"]["total_price"] += additional_charge
            
        except Exception as e:
            print(f"⚠️ Delivery cost analysis failed: {e}")
            state["delivery_analysis"] = {"error": str(e)}
        
        return state
    
    def _evaluate_bulk_strategy_mcp(self, state: EnhancedSteelState) -> EnhancedSteelState:
        """Evaluate bulk discount strategy using MCP tools"""
        quantity = state["quantity"]
        grade = state["grade"]
        
        # For bulk evaluation, consider this as part of larger order
        quantities = [quantity]
        grades = [grade]
        
        try:
            import asyncio
            result = asyncio.run(self._call_mcp_tool(
                "calculate_bulk_discount_strategy",
                quantities=quantities,
                grades=grades
            ))
            
            state["bulk_strategy"] = result
            
            if "error" not in result:
                print(f"📈 Bulk Strategy Analysis:")
                order_summary = result.get("order_summary", {})
                pricing = result.get("pricing", {})
                
                print(f"   Total Quantity: {order_summary.get('total_quantity', 0)} tons")
                print(f"   Bulk Discount: {pricing.get('bulk_discount_rate', 0):.1%}")
                print(f"   Final Margin: {pricing.get('final_margin', 0):.1%}")
                print(f"   Recommendation: {result.get('recommendation', 'unknown')}")
                
                # Apply bulk pricing if beneficial
                if pricing.get("bulk_discount_rate", 0) > 0:
                    discounted_price = state["current_offer"]["price_per_ton"] * (1 - pricing["bulk_discount_rate"])
                    state["current_offer"]["price_per_ton"] = discounted_price
                    state["current_offer"]["total_price"] = discounted_price * quantity
                    state["current_offer"]["bulk_discount"] = pricing["bulk_discount_rate"]
                    state["current_offer"]["margin"] = pricing["final_margin"]
            
        except Exception as e:
            print(f"⚠️ Bulk strategy evaluation failed: {e}")
            state["bulk_strategy"] = {"error": str(e)}
        
        return state
    
    def _finalize_terms_enhanced(self, state: EnhancedSteelState) -> EnhancedSteelState:
        """Enhanced terms finalization with MCP insights and LLM reasoning"""
        
        # LLM reasoning for final terms
        offer = state["current_offer"]
        
        terms_prompt = f"""
        As XYZ Steel Co, finalize contract terms for this order:
        - Grade {offer.get('grade', 'B')}: ${offer.get('price_per_ton', 0):.2f}/ton
        - Quantity: {state['quantity']} tons
        - Margin: {offer.get('margin', 0):.1%}
        - Total Value: ${offer.get('total_price', 0):,.2f}
        
        What payment terms, delivery schedule, and warranty should we offer?
        Consider: margin achieved, order size, customer relationship, risk factors.
        """
        
        try:
            response = self.llm.invoke(terms_prompt)
            print(f"\n📄 Steel Agent Contract Terms Reasoning:\n{response.content}\n")
            state["terms_reasoning"] = response.content
        except Exception as e:
            print(f"\n⚠️ Contract terms reasoning failed: {e}")
            state["terms_reasoning"] = "LLM unavailable - using rule-based logic"
        
        # Call parent finalization
        state = super()._finalize_terms(state)
        
        offer = state["current_offer"]
        
        print(f"\n🎯 Final Steel Offer with MCP Analysis:")
        print(f"   Grade: {offer.get('grade', 'unknown')}")
        print(f"   Price: ${offer.get('price_per_ton', 0):.2f}/ton")
        print(f"   Total: ${offer.get('total_price', 0):,.2f}")
        print(f"   Margin: {offer.get('margin', 0):.1%}")
        
        # Add MCP insights to offer
        if "grade_optimization" in state and "error" not in state["grade_optimization"]:
            opt_data = state["grade_optimization"]
            offer["mcp_profit_projection"] = opt_data.get("total_profit", 0)
            offer["inventory_status"] = "available" if opt_data.get("can_fulfill", False) else "limited"
        
        if "market_positioning" in state and "error" not in state["market_positioning"]:
            market_data = state["market_positioning"]
            offer["market_strategy"] = market_data.get("recommended_strategy", "unknown")
        
        if "delivery_analysis" in state and "error" not in state["delivery_analysis"]:
            delivery_data = state["delivery_analysis"]
            offer["delivery_cost_per_ton"] = delivery_data.get("costs", {}).get("cost_per_ton", 0)
        
        if "bulk_strategy" in state and "error" not in state["bulk_strategy"]:
            bulk_data = state["bulk_strategy"]
            offer["bulk_eligible"] = bulk_data.get("recommendation") == "approve"
        
        # Add enhanced terms based on MCP analysis
        final_margin = offer.get("margin", 0.12)
        if final_margin >= 0.18:
            offer["payment_terms"] = "net_45"
            offer["warranty"] = "18_months"
        elif final_margin >= 0.15:
            offer["payment_terms"] = "net_30"
            offer["warranty"] = "12_months"
        else:
            offer["payment_terms"] = "net_15"
            offer["warranty"] = "6_months"
        
        return state
    
    def _should_evaluate_bulk(self, state: EnhancedSteelState) -> str:
        """Determine if bulk strategy evaluation is needed"""
        quantity = state["quantity"]
        if quantity >= 100:  # Evaluate bulk for orders >= 100 tons
            return "bulk"
        return "finalize"
    
    def generate_quote_enhanced(self, rfq: Dict, competitor_offers: List[Dict] = None) -> Dict:
        """Enhanced quote generation with MCP tools"""
        grade = rfq.get("steel_grade", "B")
        if grade not in self.grade_costs:
            grade = "B"  # Default to grade B
        
        initial_state = EnhancedSteelState(
            rfq_id=rfq.get("id", "rfq_001"),
            quantity=rfq.get("steel_tons", 50),
            grade=grade,
            base_price=self.grade_prices[grade],
            storage_cost=self.storage_cost_per_ton,
            current_offer={},
            competitor_offers=competitor_offers or [],
            current_cycle=1,
            negotiation_complete=False,
            inventory_analysis={},
            grade_optimization={},
            market_positioning={},
            delivery_analysis={},
            bulk_strategy={}
        )
        
        result = self.graph.invoke(initial_state)
        return result["current_offer"]