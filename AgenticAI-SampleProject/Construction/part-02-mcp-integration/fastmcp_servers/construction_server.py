#!/usr/bin/env python3
"""
FastMCP Server for Construction Company Tools
Provides profit calculation, budget tracking, and ROI analysis tools
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
mcp = MockMCP("Construction Tools Server")
from typing import Dict, List, Any
from constraints_manager import ConstraintsManager
import sqlite3
import json

# MCP server initialized above
constraints_mgr = ConstraintsManager()

# Initialize database
def init_db():
    conn = sqlite3.connect('construction.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            name TEXT,
            budget REAL,
            spent REAL DEFAULT 0,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            project_id TEXT,
            supplier TEXT,
            material TEXT,
            quantity REAL,
            unit_price REAL,
            total_cost REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

@mcp.tool()
def calculate_total_cost(cement_tons: float, cement_price: float, steel_tons: float, steel_price: float) -> Dict[str, Any]:
    """Calculate total procurement cost with profit optimization analysis"""
    
    cement_total = cement_tons * cement_price
    steel_total = steel_tons * steel_price
    total_cost = cement_total + steel_total
    
    # Analyze against constraints
    decision = {
        "cement_price_per_ton": cement_price,
        "steel_price_per_ton": steel_price,
        "total_cost": total_cost
    }
    
    validation = constraints_mgr.validate_purchase_decision(decision)
    
    # Calculate savings potential
    max_cement_budget = cement_tons * constraints_mgr.purchase_limits.max_price_per_ton_cement
    max_steel_budget = steel_tons * constraints_mgr.purchase_limits.max_price_per_ton_steel
    max_total = max_cement_budget + max_steel_budget
    
    savings = max_total - total_cost
    savings_percentage = (savings / max_total) * 100 if max_total > 0 else 0
    
    return {
        "cement_cost": cement_total,
        "steel_cost": steel_total,
        "total_cost": total_cost,
        "max_budget": max_total,
        "savings": savings,
        "savings_percentage": savings_percentage,
        "within_constraints": validation["valid"],
        "constraint_violations": validation["violations"],
        "approval_required": constraints_mgr.check_approval_required(decision, "purchase")
    }

@mcp.tool()
def track_budget_utilization(project_id: str, proposed_cost: float) -> Dict[str, Any]:
    """Track budget utilization and remaining capacity"""
    
    conn = sqlite3.connect('construction.db')
    cursor = conn.cursor()
    
    # Get project budget
    cursor.execute("SELECT budget, spent FROM projects WHERE id = ?", (project_id,))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        return {"error": "Project not found"}
    
    budget, spent = result
    remaining = budget - spent
    projected_remaining = remaining - proposed_cost
    utilization = ((spent + proposed_cost) / budget) * 100
    
    conn.close()
    
    return {
        "project_id": project_id,
        "total_budget": budget,
        "spent": spent,
        "remaining": remaining,
        "proposed_cost": proposed_cost,
        "projected_remaining": projected_remaining,
        "utilization_percentage": utilization,
        "over_budget": projected_remaining < 0,
        "budget_status": "critical" if utilization > 90 else "warning" if utilization > 75 else "healthy"
    }

@mcp.tool()
def analyze_supplier_performance(supplier_name: str) -> Dict[str, Any]:
    """Analyze supplier cost performance and reliability"""
    
    conn = sqlite3.connect('construction.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT material, AVG(unit_price) as avg_price, COUNT(*) as order_count,
               SUM(total_cost) as total_spent
        FROM transactions 
        WHERE supplier = ?
        GROUP BY material
    """, (supplier_name,))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return {"error": "No transaction history found"}
    
    performance = {}
    total_orders = 0
    total_value = 0
    
    for material, avg_price, count, spent in results:
        performance[material] = {
            "average_price": avg_price,
            "order_count": count,
            "total_spent": spent
        }
        total_orders += count
        total_value += spent
    
    return {
        "supplier": supplier_name,
        "materials": performance,
        "total_orders": total_orders,
        "total_value": total_value,
        "average_order_value": total_value / total_orders if total_orders > 0 else 0
    }

@mcp.tool()
def calculate_roi_projection(investment: float, material_savings: float, project_duration_months: int) -> Dict[str, Any]:
    """Calculate ROI projection for procurement decisions"""
    
    # Simple ROI calculation
    monthly_savings = material_savings / project_duration_months if project_duration_months > 0 else 0
    annual_savings = monthly_savings * 12
    roi_percentage = (annual_savings / investment) * 100 if investment > 0 else 0
    
    payback_months = investment / monthly_savings if monthly_savings > 0 else float('inf')
    
    return {
        "investment": investment,
        "projected_annual_savings": annual_savings,
        "roi_percentage": roi_percentage,
        "payback_period_months": payback_months,
        "break_even": payback_months <= 12,
        "recommendation": "approve" if roi_percentage > 15 else "review" if roi_percentage > 5 else "reject"
    }

@mcp.tool()
def create_project(project_id: str, name: str, budget: float) -> Dict[str, Any]:
    """Create new construction project for tracking"""
    
    conn = sqlite3.connect('construction.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO projects (id, name, budget) VALUES (?, ?, ?)",
            (project_id, name, budget)
        )
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "project_id": project_id,
            "name": name,
            "budget": budget,
            "message": "Project created successfully"
        }
    except sqlite3.IntegrityError:
        conn.close()
        return {"error": "Project ID already exists"}

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    
    init_db()
    print(f"Starting Construction MCP Server on port {args.port}")
    
    # Use uvicorn to run the FastMCP server
    import uvicorn
    uvicorn.run(mcp.app, host="127.0.0.1", port=args.port)