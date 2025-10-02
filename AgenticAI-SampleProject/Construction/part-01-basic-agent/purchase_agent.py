from langgraph.graph import StateGraph, END
from langchain_aws import ChatBedrock
from pydantic import BaseModel
from typing import Dict, List, Optional, TypedDict
from constraints import PurchaseConstraints
from negotiation_cycles import CycleManager

class PurchaseState(TypedDict):
    task_id: str
    requirements: Dict
    budget: float
    received_quotes: List[Dict]
    selected_suppliers: List[Dict]
    current_cycle: int
    negotiation_complete: bool

class PurchaseAgent:
    def __init__(self):
        self.constraints = PurchaseConstraints()
        self.cycle_manager = CycleManager()
        self.llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            region_name="us-east-1"
        )
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(PurchaseState)
        
        workflow.add_node("analyze_requirements", self._analyze_requirements)
        workflow.add_node("evaluate_quotes", self._evaluate_quotes)
        workflow.add_node("make_counter_offer", self._make_counter_offer)
        workflow.add_node("finalize_selection", self._finalize_selection)
        
        workflow.set_entry_point("analyze_requirements")
        workflow.add_edge("analyze_requirements", "evaluate_quotes")
        workflow.add_conditional_edges(
            "evaluate_quotes",
            self._should_negotiate,
            {"negotiate": "make_counter_offer", "finalize": "finalize_selection"}
        )
        workflow.add_edge("make_counter_offer", "evaluate_quotes")
        workflow.add_edge("finalize_selection", END)
        
        return workflow.compile()
    
    def _analyze_requirements(self, state: PurchaseState) -> PurchaseState:
        # LLM reasoning for procurement strategy
        total_budget = min(state["budget"], self.constraints.max_budget)
        cement_qty = state["requirements"].get("cement_tons", 0)
        steel_qty = state["requirements"].get("steel_tons", 0)
        
        strategy_prompt = f"""
        As Construction Co procurement agent, optimize this purchase:
        - Budget: ${total_budget:,}
        - Cement needed: {cement_qty} tons
        - Steel needed: {steel_qty} tons
        - Max cement price: ${self.constraints.max_price_per_ton_cement}/ton
        - Max steel price: ${self.constraints.max_price_per_ton_steel}/ton
        
        What should be our target prices to minimize total cost?
        """
        
        try:
            response = self.llm.invoke(strategy_prompt)
            state["procurement_reasoning"] = response.content
            print(f"\n🏢 Purchase Agent Strategy:\n{response.content}\n")
        except Exception as e:
            print(f"\n⚠️  LLM reasoning failed: {e}")
            state["procurement_reasoning"] = "LLM unavailable - using rule-based logic"
        
        # Calculate target prices for cost minimization
        target_cement_price = min(150, total_budget * 0.4 / cement_qty if cement_qty > 0 else 0)
        target_steel_price = min(600, total_budget * 0.6 / steel_qty if steel_qty > 0 else 0)
        
        state["requirements"]["target_cement_price"] = target_cement_price
        state["requirements"]["target_steel_price"] = target_steel_price
        
        return state
    
    def _evaluate_quotes(self, state: PurchaseState) -> PurchaseState:
        if not state["received_quotes"]:
            return state
        
        # Rank quotes by total cost (profit maximization = cost minimization)
        evaluated_quotes = []
        for quote in state["received_quotes"]:
            total_cost = (quote.get("cement_price", 0) * state["requirements"].get("cement_tons", 0) + 
                         quote.get("steel_price", 0) * state["requirements"].get("steel_tons", 0))
            
            if total_cost <= state["budget"]:
                evaluated_quotes.append({**quote, "total_cost": total_cost, "rank": total_cost})
        
        # Sort by lowest cost (best for purchase agent)
        evaluated_quotes.sort(key=lambda x: x["rank"])
        state["received_quotes"] = evaluated_quotes
        
        return state
    
    def _make_counter_offer(self, state: PurchaseState) -> PurchaseState:
        cycle = state["current_cycle"]
        max_adjustment = self.cycle_manager.limits.get_max_adjustment(cycle)
        
        # Counter with lower prices (aggressive cost reduction)
        best_quote = state["received_quotes"][0] if state["received_quotes"] else {}
        
        counter_cement = best_quote.get("cement_price", 200) * (1 - max_adjustment * 0.5)
        counter_steel = best_quote.get("steel_price", 800) * (1 - max_adjustment * 0.5)
        
        # Ensure within constraints
        counter_cement = max(counter_cement, self.constraints.max_price_per_ton_cement * 0.8)
        counter_steel = max(counter_steel, self.constraints.max_price_per_ton_steel * 0.8)
        
        state["counter_offer"] = {
            "cement_price": counter_cement,
            "steel_price": counter_steel,
            "cycle": cycle + 1
        }
        state["current_cycle"] = cycle + 1
        
        return state
    
    def _finalize_selection(self, state: PurchaseState) -> PurchaseState:
        if state["received_quotes"]:
            # Select lowest cost option within budget
            best_quote = state["received_quotes"][0]
            if best_quote["total_cost"] <= state["budget"]:
                state["selected_suppliers"] = [best_quote]
        
        state["negotiation_complete"] = True
        return state
    
    def _should_negotiate(self, state: PurchaseState) -> str:
        if state["current_cycle"] >= self.cycle_manager.limits.max_cycles:
            return "finalize"
        
        if not state["received_quotes"]:
            return "finalize"
        
        best_quote = state["received_quotes"][0]
        target_total = (state["requirements"]["target_cement_price"] * state["requirements"].get("cement_tons", 0) +
                       state["requirements"]["target_steel_price"] * state["requirements"].get("steel_tons", 0))
        
        # LLM reasoning for negotiation decision
        decision_prompt = f"""
        Should Construction Co continue negotiating?
        - Current best offer: ${best_quote['total_cost']:,.2f}
        - Our target total: ${target_total:,.2f}
        - Budget: ${state['budget']:,}
        - Cycle: {state['current_cycle']}/{self.cycle_manager.limits.max_cycles}
        
        Continue negotiating or accept current offer?
        """
        
        try:
            response = self.llm.invoke(decision_prompt)
            print(f"\n🤔 Purchase Agent Decision:\n{response.content}\n")
        except Exception as e:
            print(f"\n⚠️  LLM reasoning failed: {e}")
        
        if best_quote["total_cost"] > target_total * 1.1:  # 10% tolerance
            return "negotiate"
        
        return "finalize"
    
    def process_procurement(self, requirements: Dict, budget: float) -> Dict:
        initial_state = PurchaseState(
            task_id=f"procurement_{hash(str(requirements))}",
            requirements=requirements,
            budget=budget,
            received_quotes=[],
            selected_suppliers=[],
            current_cycle=1,
            negotiation_complete=False
        )
        
        result = self.graph.invoke(initial_state)
        return result