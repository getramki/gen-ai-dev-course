from pydantic import BaseModel
from typing import Dict, List, Optional
from constraints import NegotiationLimits

class NegotiationState(BaseModel):
    task_id: str
    current_cycle: int = 1
    participants: List[str] = []
    offers: Dict[str, Dict] = {}
    best_offer: Optional[Dict] = None
    is_finalized: bool = False
    finalization_reason: str = ""

class CycleManager:
    def __init__(self):
        self.limits = NegotiationLimits()
        self.active_negotiations: Dict[str, NegotiationState] = {}
    
    def start_negotiation(self, task_id: str, participants: List[str]) -> NegotiationState:
        state = NegotiationState(task_id=task_id, participants=participants)
        self.active_negotiations[task_id] = state
        return state
    
    def add_offer(self, task_id: str, agent_id: str, offer: Dict) -> bool:
        if task_id not in self.active_negotiations:
            return False
        
        state = self.active_negotiations[task_id]
        if state.is_finalized:
            return False
        
        state.offers[agent_id] = {**offer, "cycle": state.current_cycle}
        return True
    
    def advance_cycle(self, task_id: str) -> bool:
        if task_id not in self.active_negotiations:
            return False
        
        state = self.active_negotiations[task_id]
        if state.is_finalized:
            return False
        
        state.current_cycle += 1
        
        if self.limits.is_final_cycle(state.current_cycle):
            self._finalize_negotiation(task_id, "max_cycles_reached")
        
        return True
    
    def _finalize_negotiation(self, task_id: str, reason: str):
        state = self.active_negotiations[task_id]
        state.is_finalized = True
        state.finalization_reason = reason
        
        # Select best offer based on agent type logic
        if state.offers:
            state.best_offer = min(state.offers.values(), 
                                 key=lambda x: x.get("total_price", float('inf')))
    
    def should_continue(self, task_id: str) -> bool:
        if task_id not in self.active_negotiations:
            return False
        
        state = self.active_negotiations[task_id]
        return not state.is_finalized and state.current_cycle <= self.limits.max_cycles