#!/usr/bin/env python3
"""
Test script for MCP servers
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from mcp_client import call_cement_tool, call_steel_tool, call_construction_tool

async def test_cement_server():
    """Test cement MCP server"""
    print("🧪 Testing Cement MCP Server...")
    
    # Test calculate_optimal_margin
    result = await call_cement_tool(
        "calculate_optimal_margin",
        quantity=500,
        competitor_price=170,
        grade="A"
    )
    print(f"✅ Optimal Margin: {result}")
    
    # Test analyze_pricing_strategy
    result = await call_steel_tool(
        "analyze_pricing_strategy",
        order_size=500,
        market_conditions="competitive"
    )
    print(f"✅ Pricing Strategy: {result}")

async def test_steel_server():
    """Test steel MCP server"""
    print("\n🧪 Testing Steel MCP Server...")
    
    # Test calculate_inventory_carrying_cost
    result = await call_steel_tool(
        "calculate_inventory_carrying_cost",
        grade="B",
        quantity=100,
        months_projected=3
    )
    print(f"✅ Inventory Cost: {result}")
    
    # Test optimize_grade_pricing
    result = await call_steel_tool(
        "optimize_grade_pricing",
        quantity=100,
        grade="B",
        urgency="normal"
    )
    print(f"✅ Grade Pricing: {result}")

async def test_construction_server():
    """Test construction MCP server"""
    print("\n🧪 Testing Construction MCP Server...")
    
    # Test create_project
    result = await call_construction_tool(
        "create_project",
        project_id="test_001",
        name="Test Project",
        budget=100000
    )
    print(f"✅ Create Project: {result}")
    
    # Test calculate_total_cost
    result = await call_construction_tool(
        "calculate_total_cost",
        cement_tons=100,
        cement_price=150,
        steel_tons=50,
        steel_price=600
    )
    print(f"✅ Total Cost: {result}")

async def main():
    """Run all tests"""
    print("🚀 Testing MCP Servers with Official SDK\n")
    
    try:
        await test_cement_server()
        await test_steel_server()
        await test_construction_server()
        print("\n✅ All MCP server tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())