#!/usr/bin/env python3
"""
MCP Server for Steel Company Tools
Provides inventory cost optimization, grade-based pricing, and profit calculation tools
"""

import sys
import os

# Add parent directory to path for constraints_manager
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import asyncio
from typing import Dict, List, Any
from constraints_manager import ConstraintsManager
import sqlite3
import json
from datetime import datetime, timedelta

server = Server("steel-company-tools")
constraints_mgr = ConstraintsManager()

# Initialize database
def init_db():
    conn = sqlite3.connect('steel_company.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            grade TEXT PRIMARY KEY,
            quantity REAL,
            cost_per_ton REAL,
            storage_cost_per_month REAL,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_prices (
            grade TEXT,
            date DATE,
            market_price REAL,
            PRIMARY KEY (grade, date)
        )
    ''')
    
    # Insert initial inventory
    cursor.execute("INSERT OR REPLACE INTO inventory VALUES ('A', 2000, 500, 5, ?)", (datetime.now(),))
    cursor.execute("INSERT OR REPLACE INTO inventory VALUES ('B', 3000, 400, 4, ?)", (datetime.now(),))
    cursor.execute("INSERT OR REPLACE INTO inventory VALUES ('C', 5000, 300, 3, ?)", (datetime.now(),))
    
    conn.commit()
    conn.close()

def calculate_inventory_carrying_cost(grade: str, quantity: float, months_projected: int = 3) -> Dict[str, Any]:
    """Calculate inventory carrying costs for profit optimization"""
    
    conn = sqlite3.connect('steel_company.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT cost_per_ton, storage_cost_per_month FROM inventory WHERE grade = ?", (grade,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return {"error": f"Grade {grade} not found"}
    
    cost_per_ton, storage_cost_per_month = result
    
    # Calculate carrying costs
    total_storage_cost = storage_cost_per_month * months_projected * quantity
    insurance_cost = cost_per_ton * 0.002 * months_projected * quantity  # 0.2% per month
    depreciation_cost = cost_per_ton * 0.001 * months_projected * quantity  # 0.1% per month
    
    total_carrying_cost = total_storage_cost + insurance_cost + depreciation_cost
    carrying_cost_per_ton = total_carrying_cost / quantity if quantity > 0 else 0
    
    # Adjusted cost basis for pricing
    adjusted_cost_per_ton = cost_per_ton + carrying_cost_per_ton
    
    return {
        "grade": grade,
        "quantity": quantity,
        "base_cost_per_ton": cost_per_ton,
        "storage_cost": total_storage_cost,
        "insurance_cost": insurance_cost,
        "depreciation_cost": depreciation_cost,
        "total_carrying_cost": total_carrying_cost,
        "carrying_cost_per_ton": carrying_cost_per_ton,
        "adjusted_cost_per_ton": adjusted_cost_per_ton,
        "months_projected": months_projected
    }

def optimize_grade_pricing(quantity: float, grade: str, urgency: str = "normal") -> Dict[str, Any]:
    """Optimize pricing by grade considering inventory levels and urgency"""
    
    conn = sqlite3.connect('steel_company.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT quantity, cost_per_ton, storage_cost_per_month FROM inventory WHERE grade = ?", (grade,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return {"error": f"Grade {grade} not found"}
    
    available_qty, cost_per_ton, storage_cost = result
    
    # Base pricing by grade
    grade_multipliers = {"A": 1.5, "B": 1.25, "C": 1.0}
    base_price = cost_per_ton * grade_multipliers.get(grade, 1.0)
    
    # Inventory level adjustments
    inventory_ratio = available_qty / 1000  # Normalize to 1000 tons
    if inventory_ratio > 3:  # High inventory - aggressive pricing
        inventory_adjustment = 0.95
    elif inventory_ratio < 1:  # Low inventory - premium pricing
        inventory_adjustment = 1.10
    else:
        inventory_adjustment = 1.0
    
    # Urgency adjustments
    urgency_multipliers = {
        "urgent": 1.15,    # Premium for rush orders
        "normal": 1.0,
        "flexible": 0.95   # Discount for flexible delivery
    }
    urgency_adjustment = urgency_multipliers.get(urgency, 1.0)
    
    # Volume discounts
    if quantity >= 200:
        volume_discount = 0.95
    elif quantity >= 100:
        volume_discount = 0.97
    else:
        volume_discount = 1.0
    
    # Calculate final price
    adjusted_price = base_price * inventory_adjustment * urgency_adjustment * volume_discount
    
    # Ensure minimum margin
    min_price = cost_per_ton * (1 + constraints_mgr.sales_limits.min_margin)
    final_price = max(adjusted_price, min_price)
    
    margin = (final_price - cost_per_ton) / final_price
    total_profit = (final_price - cost_per_ton) * quantity
    
    return {
        "grade": grade,
        "quantity": quantity,
        "base_cost": cost_per_ton,
        "base_price": base_price,
        "inventory_adjustment": inventory_adjustment,
        "urgency_adjustment": urgency_adjustment,
        "volume_discount": volume_discount,
        "final_price": final_price,
        "margin": margin,
        "total_revenue": final_price * quantity,
        "total_profit": total_profit,
        "available_inventory": available_qty,
        "can_fulfill": available_qty >= quantity
    }

def calculate_bulk_discount_strategy(quantities: List[float], grades: List[str]) -> Dict[str, Any]:
    """Calculate optimal bulk discount strategy for multi-grade orders"""
    
    total_value = 0
    total_cost = 0
    grade_details = []
    
    conn = sqlite3.connect('steel_company.db')
    cursor = conn.cursor()
    
    for qty, grade in zip(quantities, grades):
        cursor.execute("SELECT cost_per_ton FROM inventory WHERE grade = ?", (grade,))
        result = cursor.fetchone()
        
        if result:
            cost = result[0]
            grade_multipliers = {"A": 1.5, "B": 1.25, "C": 1.0}
            base_price = cost * grade_multipliers.get(grade, 1.0)
            
            grade_value = base_price * qty
            grade_cost = cost * qty
            
            total_value += grade_value
            total_cost += grade_cost
            
            grade_details.append({
                "grade": grade,
                "quantity": qty,
                "unit_price": base_price,
                "total_value": grade_value
            })
    
    conn.close()
    
    # Bulk discount tiers
    total_quantity = sum(quantities)
    if total_quantity >= 500:
        bulk_discount = 0.08  # 8% for large orders
    elif total_quantity >= 200:
        bulk_discount = 0.05  # 5% for medium orders
    elif total_quantity >= 100:
        bulk_discount = 0.03  # 3% for small bulk
    else:
        bulk_discount = 0
    
    # Apply discount but ensure minimum margin
    discounted_value = total_value * (1 - bulk_discount)
    total_margin = (discounted_value - total_cost) / discounted_value if discounted_value > 0 else 0
    
    # Adjust if margin too low
    if total_margin < constraints_mgr.sales_limits.min_margin:
        required_value = total_cost / (1 - constraints_mgr.sales_limits.min_margin)
        actual_discount = (total_value - required_value) / total_value
        discounted_value = required_value
        bulk_discount = max(0, actual_discount)
    
    return {
        "order_summary": {
            "total_quantity": total_quantity,
            "total_grades": len(set(grades)),
            "grade_breakdown": grade_details
        },
        "pricing": {
            "original_value": total_value,
            "bulk_discount_rate": bulk_discount,
            "discounted_value": discounted_value,
            "total_savings": total_value - discounted_value,
            "final_margin": (discounted_value - total_cost) / discounted_value,
            "total_profit": discounted_value - total_cost
        },
        "recommendation": "approve" if total_margin >= 0.15 else "review"
    }

def analyze_market_positioning(grade: str, competitor_prices: List[float]) -> Dict[str, Any]:
    """Analyze market positioning for competitive pricing strategy"""
    
    conn = sqlite3.connect('steel_company.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT cost_per_ton FROM inventory WHERE grade = ?", (grade,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return {"error": f"Grade {grade} not found"}
    
    cost = result[0]
    
    if not competitor_prices:
        return {"error": "No competitor prices provided"}
    
    # Market analysis
    min_competitor = min(competitor_prices)
    max_competitor = max(competitor_prices)
    avg_competitor = sum(competitor_prices) / len(competitor_prices)
    
    # Our pricing options
    min_viable_price = cost * (1 + constraints_mgr.sales_limits.min_margin)
    
    # Positioning strategies
    strategies = {
        "price_leader": min_competitor * 0.98,
        "market_match": avg_competitor,
        "premium_position": max_competitor * 1.05,
        "value_position": avg_competitor * 0.95
    }
    
    # Evaluate each strategy
    strategy_analysis = {}
    for strategy_name, price in strategies.items():
        if price >= min_viable_price:
            margin = (price - cost) / price
            strategy_analysis[strategy_name] = {
                "price": price,
                "margin": margin,
                "viable": True,
                "competitive_advantage": min_competitor - price
            }
        else:
            strategy_analysis[strategy_name] = {
                "price": price,
                "margin": (price - cost) / price if price > 0 else 0,
                "viable": False,
                "reason": "Below minimum margin threshold"
            }
    
    # Recommend best strategy
    viable_strategies = {k: v for k, v in strategy_analysis.items() if v["viable"]}
    if viable_strategies:
        best_strategy = max(viable_strategies.keys(), 
                          key=lambda k: viable_strategies[k]["margin"])
    else:
        best_strategy = "minimum_viable"
        strategy_analysis["minimum_viable"] = {
            "price": min_viable_price,
            "margin": constraints_mgr.sales_limits.min_margin,
            "viable": True,
            "competitive_advantage": min_competitor - min_viable_price
        }
    
    return {
        "grade": grade,
        "market_analysis": {
            "competitor_min": min_competitor,
            "competitor_max": max_competitor,
            "competitor_avg": avg_competitor,
            "market_spread": max_competitor - min_competitor
        },
        "our_constraints": {
            "cost": cost,
            "min_viable_price": min_viable_price,
            "min_margin": constraints_mgr.sales_limits.min_margin
        },
        "strategies": strategy_analysis,
        "recommended_strategy": best_strategy,
        "recommended_price": strategy_analysis[best_strategy]["price"]
    }

def calculate_delivery_cost_impact(quantity: float, distance_km: float, urgency: str = "normal") -> Dict[str, Any]:
    """Calculate delivery cost impact on pricing and profit margins"""
    
    # Base delivery costs
    base_cost_per_km = 2.5  # $2.5 per km
    base_cost_per_ton = 15  # $15 per ton base handling
    
    # Urgency multipliers
    urgency_multipliers = {
        "urgent": 1.5,
        "normal": 1.0,
        "flexible": 0.8
    }
    
    multiplier = urgency_multipliers.get(urgency, 1.0)
    
    # Calculate costs
    distance_cost = base_cost_per_km * distance_km * multiplier
    handling_cost = base_cost_per_ton * quantity * multiplier
    total_delivery_cost = distance_cost + handling_cost
    
    delivery_cost_per_ton = total_delivery_cost / quantity if quantity > 0 else 0
    
    # Pricing options
    absorb_cost = True  # Company absorbs delivery cost
    pass_through = False  # Customer pays delivery separately
    
    return {
        "delivery_details": {
            "quantity": quantity,
            "distance_km": distance_km,
            "urgency": urgency,
            "urgency_multiplier": multiplier
        },
        "costs": {
            "distance_cost": distance_cost,
            "handling_cost": handling_cost,
            "total_delivery_cost": total_delivery_cost,
            "cost_per_ton": delivery_cost_per_ton
        },
        "pricing_options": {
            "absorb_cost": {
                "margin_impact": delivery_cost_per_ton,
                "recommended": distance_km <= 100
            },
            "pass_through": {
                "additional_charge": total_delivery_cost,
                "recommended": distance_km > 100
            }
        }
    }

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="calculate_inventory_carrying_cost",
            description="Calculate inventory carrying costs for profit optimization",
            inputSchema={
                "type": "object",
                "properties": {
                    "grade": {"type": "string"},
                    "quantity": {"type": "number"},
                    "months_projected": {"type": "integer", "default": 3}
                },
                "required": ["grade", "quantity"]
            }
        ),
        types.Tool(
            name="optimize_grade_pricing",
            description="Optimize pricing by grade considering inventory levels and urgency",
            inputSchema={
                "type": "object",
                "properties": {
                    "quantity": {"type": "number"},
                    "grade": {"type": "string"},
                    "urgency": {"type": "string", "default": "normal"}
                },
                "required": ["quantity", "grade"]
            }
        ),
        types.Tool(
            name="calculate_bulk_discount_strategy",
            description="Calculate optimal bulk discount strategy for multi-grade orders",
            inputSchema={
                "type": "object",
                "properties": {
                    "quantities": {"type": "array", "items": {"type": "number"}},
                    "grades": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["quantities", "grades"]
            }
        ),
        types.Tool(
            name="analyze_market_positioning",
            description="Analyze market positioning for competitive pricing strategy",
            inputSchema={
                "type": "object",
                "properties": {
                    "grade": {"type": "string"},
                    "competitor_prices": {"type": "array", "items": {"type": "number"}}
                },
                "required": ["grade", "competitor_prices"]
            }
        ),
        types.Tool(
            name="calculate_delivery_cost_impact",
            description="Calculate delivery cost impact on pricing and profit margins",
            inputSchema={
                "type": "object",
                "properties": {
                    "quantity": {"type": "number"},
                    "distance_km": {"type": "number"},
                    "urgency": {"type": "string", "default": "normal"}
                },
                "required": ["quantity", "distance_km"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "calculate_inventory_carrying_cost":
        result = calculate_inventory_carrying_cost(**arguments)
    elif name == "optimize_grade_pricing":
        result = optimize_grade_pricing(**arguments)
    elif name == "calculate_bulk_discount_strategy":
        result = calculate_bulk_discount_strategy(**arguments)
    elif name == "analyze_market_positioning":
        result = analyze_market_positioning(**arguments)
    elif name == "calculate_delivery_cost_impact":
        result = calculate_delivery_cost_impact(**arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")
    
    return [types.TextContent(type="text", text=str(result))]

async def main():
    init_db()
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="steel-company-tools",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())