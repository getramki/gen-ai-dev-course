from langgraph.graph import StateGraph, END
from langchain_aws import ChatBedrock
from pydantic import BaseModel
from typing import Dict, List, Optional, TypedDict
from constraints import SalesConstraints
from negotiation_cycles import CycleManager

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
    def __init__(self):
        self.constraints = SalesConstraints()
        self.cycle_manager = CycleManager()
        self.base_cost = 120  # Cost per ton
        self.base_price = 180  # List price per ton (50% margin)
        self.inventory = 5000  # Available tons
        
        self.llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            region_name="us-east-1"
        )
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(CementState)
        
        workflow.add_node("calculate_initial_price", self._calculate_initial_price)
        workflow.add_node("analyze_competition", self._analyze_competition)
        workflow.add_node("optimize_margin", self._optimize_margin)
        workflow.add_node("finalize_offer", self._finalize_offer)
        
        workflow.set_entry_point("calculate_initial_price")
        workflow.add_edge("calculate_initial_price", "analyze_competition")
        workflow.add_conditional_edges(
            "analyze_competition",
            self._should_adjust_price,
            {"adjust": "optimize_margin", "finalize": "finalize_offer"}
        )
        workflow.add_edge("optimize_margin", "finalize_offer")
        workflow.add_edge("finalize_offer", END)
        
        return workflow.compile()
    
    def _calculate_initial_price(self, state: CementState) -> CementState:
        quantity = state["quantity"]
        
        # Volume-based pricing for profit maximization
        if quantity >= 1000:  # Bulk discount but maintain margin
            discount = min(0.15, self.constraints.max_discount * 0.75)
        elif quantity >= 500:
            discount = min(0.10, self.constraints.max_discount * 0.5)
        else:
            discount = 0.05
        
        # Ensure minimum margin maintained
        min_price = self.base_cost * (1 + self.constraints.min_margin)
        offered_price = max(min_price, self.base_price * (1 - discount))
        
        margin = (offered_price - self.base_cost) / offered_price
        
        state["current_offer"] = {
            "price_per_ton": offered_price,
            "total_price": offered_price * quantity,
            "margin": margin,
            "discount": discount,
            "delivery_days": 15
        }
        
        return state
    
    def _analyze_competition(self, state: CementState) -> CementState:
        # LLM reasoning for competitive analysis
        if state["competitor_offers"]:
            competitor_prices = [offer.get("price_per_ton", float('inf')) 
                               for offer in state["competitor_offers"]]
            lowest_competitor = min(competitor_prices)
            
            reasoning_prompt = f"""
            As ABC Cement Co sales agent, analyze this competitive situation:
            - Our cost: ${self.base_cost}/ton
            - Our current price: ${state['current_offer']['price_per_ton']:.2f}/ton
            - Competitor lowest: ${lowest_competitor:.2f}/ton
            - Minimum margin required: {self.constraints.min_margin:.1%}
            - Quantity: {state['quantity']} tons
            
            Should we adjust pricing? What's our competitive strategy?
            """
            
            try:
                response = self.llm.invoke(reasoning_prompt)
                state["llm_reasoning"] = response.content
                print(f"\n🧠 Cement Agent LLM Reasoning:\n{response.content}\n")
            except Exception as e:
                print(f"\n⚠️  LLM reasoning failed: {e}")
                state["llm_reasoning"] = "LLM unavailable - using rule-based logic"
            
            # Position slightly below competition while maintaining margin
            target_price = lowest_competitor * 0.98
            min_acceptable = self.base_cost * (1 + self.constraints.min_margin)
            
            if target_price >= min_acceptable:
                state["competitive_price"] = target_price
            else:
                state["competitive_price"] = min_acceptable
        
        return state
    
    def _optimize_margin(self, state: CementState) -> CementState:
        cycle = state["current_cycle"]
        max_adjustment = self.cycle_manager.limits.get_max_adjustment(cycle)
        
        current_price = state["current_offer"]["price_per_ton"]
        competitive_price = state.get("competitive_price", current_price)
        
        # Aggressive pricing in later cycles to close deal
        if cycle >= 4:
            # Final rounds - prioritize winning over maximum margin
            adjustment_factor = max_adjustment * 2
        else:
            # Early rounds - maintain higher margins
            adjustment_factor = max_adjustment * 0.5
        
        # Calculate new price balancing competition and margin
        new_price = min(current_price, competitive_price * (1 - adjustment_factor))
        min_price = self.base_cost * (1 + self.constraints.min_margin)
        final_price = max(new_price, min_price)
        
        quantity = state["quantity"]
        margin = (final_price - self.base_cost) / final_price
        
        state["current_offer"] = {
            "price_per_ton": final_price,
            "total_price": final_price * quantity,
            "margin": margin,
            "cycle": cycle,
            "delivery_days": max(10, 20 - cycle * 2)  # Faster delivery as incentive
        }
        
        return state
    
    def _finalize_offer(self, state: CementState) -> CementState:
        # LLM reasoning for final offer decision
        offer = state["current_offer"]
        
        decision_prompt = f"""
        As ABC Cement Co, finalize this offer:
        - Price: ${offer['price_per_ton']:.2f}/ton
        - Margin: {offer['margin']:.1%}
        - Quantity: {state['quantity']} tons
        - Cycle: {state['current_cycle']}
        
        Should we accept this deal? What terms should we offer?
        Consider: payment terms, delivery, warranty based on margin achieved.
        """
        
        try:
            response = self.llm.invoke(decision_prompt)
            state["final_reasoning"] = response.content
            print(f"\n🎯 Cement Agent Final Decision:\n{response.content}\n")
        except Exception as e:
            print(f"\n⚠️  LLM reasoning failed: {e}")
            state["final_reasoning"] = "LLM unavailable - using rule-based logic"
        
        # Payment terms based on margin achieved
        if offer["margin"] >= 0.20:
            payment_terms = "net_45"  # Better terms for higher margin
        elif offer["margin"] >= 0.15:
            payment_terms = "net_30"
        else:
            payment_terms = "net_15"  # Faster payment for lower margin
        
        offer["payment_terms"] = payment_terms
        offer["quality_grade"] = "A"
        offer["warranty"] = "standard"
        
        state["negotiation_complete"] = True
        return state
    
    def _should_adjust_price(self, state: CementState) -> str:
        if state["current_cycle"] >= self.cycle_manager.limits.max_cycles:
            return "finalize"
        
        # Adjust if competitors are significantly lower
        if "competitive_price" in state:
            current_price = state["current_offer"]["price_per_ton"]
            competitive_price = state["competitive_price"]
            
            if current_price > competitive_price * 1.05:  # 5% tolerance
                return "adjust"
        
        return "finalize"
    
    def generate_quote(self, rfq: Dict, competitor_offers: List[Dict] = None) -> Dict:
        initial_state = CementState(
            rfq_id=rfq.get("id", "rfq_001"),
            quantity=rfq.get("cement_tons", 100),
            base_price=self.base_price,
            cost_per_ton=self.base_cost,
            current_offer={},
            competitor_offers=competitor_offers or [],
            current_cycle=1,
            negotiation_complete=False
        )
        
        result = self.graph.invoke(initial_state)
        return result["current_offer"]