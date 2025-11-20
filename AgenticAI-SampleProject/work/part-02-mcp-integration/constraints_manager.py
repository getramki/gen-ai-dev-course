from pydantic import BaseModel
from typing import Dict, Any, Optional

# Constraint classes (copied from Part 1 to avoid import issues)
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

class ConstraintsManager:
    """Enhanced constraints manager with MCP tool integration"""
    
    def __init__(self):
        self.purchase_limits = PurchaseConstraints()
        self.sales_limits = SalesConstraints()
        self.negotiation_limits = NegotiationLimits()
    
    def validate_purchase_decision(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Validate purchase decisions against human-set limits"""
        result = {"valid": True, "violations": [], "adjusted_decision": decision.copy()}
        
        # Budget validation
        total_cost = decision.get("total_cost", 0)
        if total_cost > self.purchase_limits.max_budget:
            result["valid"] = False
            result["violations"].append(f"Exceeds max budget: ${total_cost:,.2f} > ${self.purchase_limits.max_budget:,.2f}")
        
        # Price per ton validation
        cement_price = decision.get("cement_price_per_ton", 0)
        steel_price = decision.get("steel_price_per_ton", 0)
        
        if cement_price > self.purchase_limits.max_price_per_ton_cement:
            result["valid"] = False
            result["violations"].append(f"Cement price too high: ${cement_price} > ${self.purchase_limits.max_price_per_ton_cement}")
            result["adjusted_decision"]["cement_price_per_ton"] = self.purchase_limits.max_price_per_ton_cement
        
        if steel_price > self.purchase_limits.max_price_per_ton_steel:
            result["valid"] = False
            result["violations"].append(f"Steel price too high: ${steel_price} > ${self.purchase_limits.max_price_per_ton_steel}")
            result["adjusted_decision"]["steel_price_per_ton"] = self.purchase_limits.max_price_per_ton_steel
        
        return result
    
    def validate_sales_offer(self, offer: Dict[str, Any], agent_type: str) -> Dict[str, Any]:
        """Validate sales offers against margin and discount limits"""
        result = {"valid": True, "violations": [], "adjusted_offer": offer.copy()}
        
        margin = offer.get("margin", 0)
        discount = offer.get("discount", 0)
        
        # Margin validation
        if margin < self.sales_limits.min_margin:
            result["valid"] = False
            result["violations"].append(f"Margin too low: {margin:.1%} < {self.sales_limits.min_margin:.1%}")
        
        # Discount validation
        if discount > self.sales_limits.max_discount:
            result["valid"] = False
            result["violations"].append(f"Discount too high: {discount:.1%} > {self.sales_limits.max_discount:.1%}")
            result["adjusted_offer"]["discount"] = self.sales_limits.max_discount
        
        return result
    
    def check_approval_required(self, transaction: Dict[str, Any], agent_type: str) -> bool:
        """Check if human approval is required for transaction"""
        if agent_type == "purchase":
            return transaction.get("total_cost", 0) > self.purchase_limits.approval_threshold
        elif agent_type == "sales":
            return transaction.get("total_value", 0) > self.sales_limits.approval_threshold
        
        return False
    
    def get_cycle_limits(self) -> Dict[str, Any]:
        """Get negotiation cycle limits for MCP tools"""
        return {
            "max_cycles": self.negotiation_limits.max_cycles,
            "cycle_adjustments": self.negotiation_limits.cycle_adjustments
        }