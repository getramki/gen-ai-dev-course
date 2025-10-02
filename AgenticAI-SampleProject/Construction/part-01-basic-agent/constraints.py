from pydantic import BaseModel
from typing import Dict, Optional

class PurchaseConstraints(BaseModel):
    max_budget: float = 500000
    max_price_per_ton_cement: float = 200
    max_price_per_ton_steel: float = 800
    min_quality_grade: str = "A"
    max_delivery_days: int = 30
    approval_threshold: float = 50000

class SalesConstraints(BaseModel):
    min_margin: float = 0.15
    max_discount: float = 0.20
    min_order_quantity: float = 10
    payment_terms: str = "net_30"
    approval_threshold: float = 20000

class NegotiationLimits(BaseModel):
    max_cycles: int = 5
    cycle_adjustments: Dict[int, float] = {
        1: 1.0,    # No limit
        2: 0.10,   # 10% adjustment
        3: 0.05,   # 5% adjustment  
        4: 0.02,   # 2% adjustment
        5: 0.01    # 1% adjustment
    }
    
    def get_max_adjustment(self, cycle: int) -> float:
        return self.cycle_adjustments.get(cycle, 0.01)
    
    def is_final_cycle(self, cycle: int) -> bool:
        return cycle >= self.max_cycles