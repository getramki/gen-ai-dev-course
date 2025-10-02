#!/usr/bin/env python3
"""
FastMCP Server for Cement Company Tools
Provides margin analysis, pricing optimization, and inventory management tools
"""

import sys
import os

# Add parent directory to path for constraints_manager
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

# Use FastAPI directly instead of FastMCP
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

class ToolRequest(BaseModel):
    """Request model for tool calls"""
    pass

class MockMCP:
    def __init__(self, name):
        self.name = name
        self.tools = {}
        self._app = None
        
    def tool(self):
        def decorator(func):
            self.tools[func.__name__] = func
            return func
        return decorator
        
    @property
    def app(self):
        if self._app is None:
            self._app = FastAPI(title=self.name)
            
            @self._app.post("/tools/{tool_name}")
            async def call_tool(tool_name: str, request: dict):
                if tool_name in self.tools:
                    try:
                        return self.tools[tool_name](**request)
                    except Exception as e:
                        return {"error": str(e)}
                return {"error": f"Tool {tool_name} not found"}
            
            @self._app.get("/")
            async def root():
                return {"message": f"{self.name} is running", "tools": list(self.tools.keys())}
                
        return self._app

# Use MockMCP instead of FastMCP
mcp = MockMCP("Cement Company Tools Server")
from typing import Dict, List, Any
from constraints_manager import ConstraintsManager
import sqlite3
import json
from datetime import datetime, timedelta

# MCP server initialized above
constraints_mgr = ConstraintsManager()

# Initialize database
def init_db():
    conn = sqlite3.connect('cement_company.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            grade TEXT PRIMARY KEY,
            quantity REAL,
            cost_per_ton REAL,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_history (
            id TEXT PRIMARY KEY,
            customer TEXT,
            quantity REAL,
            price_per_ton REAL,
            margin REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert initial inventory
    cursor.execute("INSERT OR REPLACE INTO inventory VALUES ('A', 5000, 120, ?)", (datetime.now(),))
    cursor.execute("INSERT OR REPLACE INTO inventory VALUES ('B', 3000, 100, ?)", (datetime.now(),))
    
    conn.commit()
    conn.close()

@mcp.tool()
def calculate_optimal_margin(quantity: float, competitor_price: float = None, grade: str = "A") -> Dict[str, Any]:
    """Calculate optimal margin for maximum profit within constraints"""
    
    conn = sqlite3.connect('cement_company.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT cost_per_ton FROM inventory WHERE grade = ?", (grade,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return {"error": f"Grade {grade} not found in inventory"}
    
    cost_per_ton = result[0]
    base_price = 180  # Standard list price
    
    # Volume-based margin optimization
    if quantity >= 1000:
        target_margin = 0.18  # Lower margin for volume
    elif quantity >= 500:
        target_margin = 0.22
    else:
        target_margin = 0.25  # Higher margin for small orders
    
    # Competitive adjustment
    if competitor_price:
        competitive_price = competitor_price * 0.98  # Beat by 2%
        competitive_margin = (competitive_price - cost_per_ton) / competitive_price
        
        # Use competitive margin if it's above minimum
        if competitive_margin >= constraints_mgr.sales_limits.min_margin:
            target_margin = min(target_margin, competitive_margin)
    
    # Ensure minimum margin constraint
    final_margin = max(target_margin, constraints_mgr.sales_limits.min_margin)
    optimal_price = cost_per_ton / (1 - final_margin)
    
    # Calculate discount from list price
    discount = (base_price - optimal_price) / base_price if optimal_price < base_price else 0
    
    # Validate against constraints
    offer = {"margin": final_margin, "discount": discount}
    validation = constraints_mgr.validate_sales_offer(offer, "cement")
    
    return {
        "grade": grade,
        "quantity": quantity,
        "cost_per_ton": cost_per_ton,
        "optimal_price": optimal_price,
        "optimal_margin": final_margin,
        "discount": discount,
        "total_revenue": optimal_price * quantity,
        "total_profit": (optimal_price - cost_per_ton) * quantity,
        "competitive_advantage": competitor_price - optimal_price if competitor_price else 0,
        "within_constraints": validation["valid"],
        "constraint_violations": validation["violations"]
    }

@mcp.tool()
def analyze_pricing_strategy(order_size: float, market_conditions: str = "normal") -> Dict[str, Any]:
    """Analyze pricing strategy based on market conditions and order size"""
    
    base_margin = 0.20
    
    # Market condition adjustments
    market_multipliers = {
        "high_demand": 1.15,  # Premium pricing
        "normal": 1.0,
        "competitive": 0.95,  # Aggressive pricing
        "recession": 0.90     # Survival pricing
    }
    
    multiplier = market_multipliers.get(market_conditions, 1.0)
    adjusted_margin = base_margin * multiplier
    
    # Volume-based adjustments
    if order_size >= 1000:
        volume_discount = 0.03
    elif order_size >= 500:
        volume_discount = 0.02
    else:
        volume_discount = 0
    
    final_margin = max(adjusted_margin - volume_discount, constraints_mgr.sales_limits.min_margin)
    
    # Calculate pricing tiers
    cost = 120  # Base cost
    price = cost / (1 - final_margin)
    
    return {
        "market_conditions": market_conditions,
        "order_size": order_size,
        "base_margin": base_margin,
        "market_adjustment": multiplier,
        "volume_discount": volume_discount,
        "final_margin": final_margin,
        "recommended_price": price,
        "profit_per_ton": price - cost,
        "total_profit": (price - cost) * order_size,
        "strategy": "premium" if final_margin > 0.22 else "competitive" if final_margin > 0.18 else "aggressive"
    }

@mcp.tool()
def check_inventory_availability(quantity: float, grade: str = "A") -> Dict[str, Any]:
    """Check inventory availability and calculate carrying costs"""
    
    conn = sqlite3.connect('cement_company.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT quantity, cost_per_ton, last_updated FROM inventory WHERE grade = ?", (grade,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return {"error": f"Grade {grade} not found"}
    
    available, cost_per_ton, last_updated = result
    
    # Calculate carrying costs (storage, insurance, etc.)
    carrying_cost_per_month = 2.5  # $2.5 per ton per month
    months_in_storage = 2  # Average storage time
    total_carrying_cost = carrying_cost_per_month * months_in_storage
    
    # Inventory turnover analysis
    can_fulfill = available >= quantity
    remaining_after_sale = available - quantity if can_fulfill else available
    inventory_turnover = quantity / available if available > 0 else 0
    
    return {
        "grade": grade,
        "requested_quantity": quantity,
        "available_quantity": available,
        "can_fulfill": can_fulfill,
        "remaining_inventory": remaining_after_sale,
        "inventory_turnover": inventory_turnover,
        "carrying_cost_per_ton": total_carrying_cost,
        "total_carrying_cost": total_carrying_cost * quantity,
        "adjusted_cost": cost_per_ton + total_carrying_cost,
        "inventory_status": "critical" if remaining_after_sale < 500 else "low" if remaining_after_sale < 1000 else "healthy"
    }

@mcp.tool()
def calculate_competitive_response(competitor_offers: List[Dict[str, Any]], our_current_price: float) -> Dict[str, Any]:
    """Calculate competitive response strategy for profit maximization"""
    
    if not competitor_offers:
        return {"strategy": "maintain_premium", "recommended_action": "no_change"}
    
    competitor_prices = [offer.get("price_per_ton", float('inf')) for offer in competitor_offers]
    lowest_competitor = min(competitor_prices)
    average_competitor = sum(competitor_prices) / len(competitor_prices)
    
    cost = 120
    min_price = cost / (1 - constraints_mgr.sales_limits.min_margin)
    
    # Competitive positioning strategies
    if our_current_price <= lowest_competitor:
        strategy = "price_leader"
        recommended_price = our_current_price  # Maintain position
    elif our_current_price <= lowest_competitor * 1.05:
        strategy = "competitive_match"
        recommended_price = max(lowest_competitor * 0.99, min_price)
    elif our_current_price <= average_competitor:
        strategy = "market_follower"
        recommended_price = max(lowest_competitor * 1.02, min_price)
    else:
        strategy = "premium_position"
        recommended_price = max(average_competitor * 0.95, min_price)
    
    margin = (recommended_price - cost) / recommended_price
    price_change = recommended_price - our_current_price
    
    return {
        "competitor_analysis": {
            "lowest_price": lowest_competitor,
            "average_price": average_competitor,
            "our_current_price": our_current_price
        },
        "strategy": strategy,
        "recommended_price": recommended_price,
        "price_change": price_change,
        "new_margin": margin,
        "competitive_advantage": lowest_competitor - recommended_price,
        "risk_level": "low" if margin > 0.18 else "medium" if margin > 0.15 else "high"
    }

@mcp.tool()
def record_sale(customer: str, quantity: float, price_per_ton: float) -> Dict[str, Any]:
    """Record sale and update inventory"""
    
    conn = sqlite3.connect('cement_company.db')
    cursor = conn.cursor()
    
    # Calculate margin
    cost = 120
    margin = (price_per_ton - cost) / price_per_ton
    
    # Record sale
    sale_id = f"sale_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    cursor.execute(
        "INSERT INTO sales_history (id, customer, quantity, price_per_ton, margin) VALUES (?, ?, ?, ?, ?)",
        (sale_id, customer, quantity, price_per_ton, margin)
    )
    
    # Update inventory
    cursor.execute("UPDATE inventory SET quantity = quantity - ? WHERE grade = 'A'", (quantity,))
    
    conn.commit()
    conn.close()
    
    return {
        "sale_id": sale_id,
        "customer": customer,
        "quantity": quantity,
        "price_per_ton": price_per_ton,
        "total_revenue": price_per_ton * quantity,
        "margin": margin,
        "profit": (price_per_ton - cost) * quantity,
        "recorded": True
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8001)
    args = parser.parse_args()
    
    init_db()
    print(f"Starting Cement MCP Server on port {args.port}")
    
    # Use uvicorn to run the FastMCP server
    import uvicorn
    uvicorn.run(mcp.app, host="127.0.0.1", port=args.port)