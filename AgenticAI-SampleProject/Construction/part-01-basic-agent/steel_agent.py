from langgraph.graph import StateGraph, END
from langchain_aws import ChatBedrock
from pydantic import BaseModel
from typing import Dict, List, Optional, TypedDict
from constraints import SalesConstraints
from negotiation_cycles import CycleManager

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
    def __init__(self):
        self.constraints = SalesConstraints()
        self.cycle_manager = CycleManager()
        
        # Grade-based pricing
        self.grade_costs = {"A": 500, "B": 400, "C": 300}
        self.grade_prices = {"A": 750, "B": 600, "C": 450}
        self.storage_cost_per_ton = 5  # Monthly storage cost
        self.inventory = {"A": 2000, "B": 3000, "C": 5000}
        
        self.llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            region_name="us-east-1"
        )
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(SteelState)
        
        workflow.add_node("calculate_base_price", self._calculate_base_price)
        workflow.add_node("optimize_inventory", self._optimize_inventory)
        workflow.add_node("competitive_pricing", self._competitive_pricing)
        workflow.add_node("finalize_terms", self._finalize_terms)
        
        workflow.set_entry_point("calculate_base_price")
        workflow.add_edge("calculate_base_price", "optimize_inventory")
        workflow.add_conditional_edges(
            "optimize_inventory",
            self._should_compete,
            {"compete": "competitive_pricing", "finalize": "finalize_terms"}
        )
        workflow.add_edge("competitive_pricing", "finalize_terms")
        workflow.add_edge("finalize_terms", END)
        
        return workflow.compile()
    
    def _calculate_base_price(self, state: SteelState) -> SteelState:
        grade = state["grade"]
        quantity = state["quantity"]
        
        base_cost = self.grade_costs[grade]
        base_price = self.grade_prices[grade]
        
        # Inventory carrying cost consideration
        months_in_inventory = 2  # Average storage time
        total_cost = base_cost + (self.storage_cost_per_ton * months_in_inventory)
        
        # Volume-based pricing for profit maximization
        if quantity >= 200:  # Large order
            discount = min(0.20, self.constraints.max_discount)
        elif quantity >= 100:
            discount = min(0.15, self.constraints.max_discount * 0.75)
        elif quantity >= 50:
            discount = min(0.10, self.constraints.max_discount * 0.5)
        else:
            discount = 0.05
        
        # Ensure minimum margin after storage costs
        min_price = total_cost * (1 + self.constraints.min_margin)
        offered_price = max(min_price, base_price * (1 - discount))
        
        margin = (offered_price - total_cost) / offered_price
        
        state["current_offer"] = {
            "price_per_ton": offered_price,
            "total_price": offered_price * quantity,
            "margin": margin,
            "discount": discount,
            "grade": grade,
            "delivery_days": 20
        }
        
        return state
    
    def _optimize_inventory(self, state: SteelState) -> SteelState:
        grade = state["grade"]
        quantity = state["quantity"]
        available = self.inventory[grade]
        
        # Inventory optimization for profit
        if available > 1000:  # High inventory - aggressive pricing
            inventory_factor = 0.95
        elif available < 500:  # Low inventory - premium pricing
            inventory_factor = 1.10
        else:
            inventory_factor = 1.0
        
        current_price = state["current_offer"]["price_per_ton"]
        optimized_price = current_price * inventory_factor
        
        # Ensure constraints still met
        total_cost = self.grade_costs[grade] + (self.storage_cost_per_ton * 2)
        min_price = total_cost * (1 + self.constraints.min_margin)
        final_price = max(optimized_price, min_price)
        
        margin = (final_price - total_cost) / final_price
        
        state["current_offer"].update({
            "price_per_ton": final_price,
            "total_price": final_price * quantity,
            "margin": margin,
            "inventory_factor": inventory_factor
        })
        
        return state
    
    def _competitive_pricing(self, state: SteelState) -> SteelState:
        cycle = state["current_cycle"]
        max_adjustment = self.cycle_manager.limits.get_max_adjustment(cycle)
        
        current_price = state["current_offer"]["price_per_ton"]
        
        # Analyze competition
        if state["competitor_offers"]:
            competitor_prices = [offer.get("price_per_ton", float('inf')) 
                               for offer in state["competitor_offers"]]
            lowest_competitor = min(competitor_prices)
            
            # Strategic pricing based on cycle
            if cycle <= 2:
                # Early cycles - maintain premium
                target_price = min(current_price, lowest_competitor * 1.02)
            else:
                # Later cycles - more aggressive
                target_price = min(current_price, lowest_competitor * 0.98)
        else:
            # No competition - slight reduction to encourage acceptance
            target_price = current_price * (1 - max_adjustment * 0.3)
        
        # Ensure minimum margin
        grade = state["grade"]
        total_cost = self.grade_costs[grade] + (self.storage_cost_per_ton * 2)
        min_price = total_cost * (1 + self.constraints.min_margin)
        final_price = max(target_price, min_price)
        
        quantity = state["quantity"]
        margin = (final_price - total_cost) / final_price
        
        state["current_offer"].update({
            "price_per_ton": final_price,
            "total_price": final_price * quantity,
            "margin": margin,
            "cycle": cycle
        })
        
        return state
    
    def _finalize_terms(self, state: SteelState) -> SteelState:
        offer = state["current_offer"]
        grade = state["grade"]
        
        # Enhanced terms based on margin achieved
        if offer["margin"] >= 0.18:
            payment_terms = "net_45"
            delivery_days = 25
        elif offer["margin"] >= 0.12:
            payment_terms = "net_30"
            delivery_days = 20
        else:
            payment_terms = "net_15"
            delivery_days = 15
        
        # Quality certifications by grade
        certifications = {
            "A": ["ISO_9001", "ASTM_A36"],
            "B": ["ISO_9001"],
            "C": ["basic_quality"]
        }
        
        offer.update({
            "payment_terms": payment_terms,
            "delivery_days": delivery_days,
            "certifications": certifications[grade],
            "warranty": "12_months" if grade == "A" else "6_months"
        })
        
        state["negotiation_complete"] = True
        return state
    
    def _should_compete(self, state: SteelState) -> str:
        if state["current_cycle"] >= self.cycle_manager.limits.max_cycles:
            return "finalize"
        
        # Compete if competitors present or margin too high
        if state["competitor_offers"] or state["current_offer"]["margin"] > 0.25:
            return "compete"
        
        return "finalize"
    
    def generate_quote(self, rfq: Dict, competitor_offers: List[Dict] = None) -> Dict:
        grade = rfq.get("steel_grade", "B")
        if grade not in self.grade_costs:
            grade = "B"  # Default to grade B
        
        initial_state = SteelState(
            rfq_id=rfq.get("id", "rfq_001"),
            quantity=rfq.get("steel_tons", 50),
            grade=grade,
            base_price=self.grade_prices[grade],
            storage_cost=self.storage_cost_per_ton,
            current_offer={},
            competitor_offers=competitor_offers or [],
            current_cycle=1,
            negotiation_complete=False
        )
        
        result = self.graph.invoke(initial_state)
        return result["current_offer"]