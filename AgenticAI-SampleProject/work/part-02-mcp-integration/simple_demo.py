#!/usr/bin/env python3
"""
Simple Demo: Enhanced Agents with Official MCP SDK Integration
Demonstrates profit optimization using proper MCP servers
"""

import sys
import os
import asyncio

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from mcp_client import call_cement_tool, call_steel_tool, call_construction_tool

async def demo_mcp_tools():
    """Demonstrate MCP tools working with official SDK"""
    print("🚀 MCP Tools Demo with Official SDK")
    print("=" * 50)
    
    print("\n💰 Construction Tools Demo:")
    
    # Create project
    result = await call_construction_tool(
        "create_project",
        project_id="demo_001",
        name="Demo Construction Project",
        budget=100000
    )
    print(f"✅ Project Created: {result.get('message', 'Success')}")
    
    # Calculate total cost
    result = await call_construction_tool(
        "calculate_total_cost",
        cement_tons=100,
        cement_price=150,
        steel_tons=50,
        steel_price=600
    )
    print(f"💵 Total Cost Analysis:")
    print(f"   Total Cost: ${result.get('total_cost', 0):,.2f}")
    print(f"   Savings: ${result.get('savings', 0):,.2f}")
    print(f"   Within Constraints: {result.get('within_constraints', False)}")
    
    print("\n🏭 Cement Tools Demo:")
    
    # Calculate optimal margin
    result = await call_cement_tool(
        "calculate_optimal_margin",
        quantity=500,
        competitor_price=170,
        grade="A"
    )
    print(f"📊 Optimal Margin Analysis:")
    print(f"   Optimal Price: ${result.get('optimal_price', 0):.2f}/ton")
    print(f"   Optimal Margin: {result.get('optimal_margin', 0):.1%}")
    print(f"   Total Profit: ${result.get('total_profit', 0):,.2f}")
    
    # Check inventory
    result = await call_cement_tool(
        "check_inventory_availability",
        quantity=500,
        grade="A"
    )
    print(f"📦 Inventory Status:")
    print(f"   Available: {result.get('available_quantity', 0)} tons")
    print(f"   Can Fulfill: {result.get('can_fulfill', False)}")
    print(f"   Status: {result.get('inventory_status', 'unknown')}")
    
    print("\n🔩 Steel Tools Demo:")
    
    # Calculate inventory costs
    result = await call_steel_tool(
        "calculate_inventory_carrying_cost",
        grade="B",
        quantity=100,
        months_projected=3
    )
    print(f"💸 Inventory Carrying Costs:")
    print(f"   Base Cost: ${result.get('base_cost_per_ton', 0):.2f}/ton")
    print(f"   Carrying Cost: ${result.get('carrying_cost_per_ton', 0):.2f}/ton")
    print(f"   Adjusted Cost: ${result.get('adjusted_cost_per_ton', 0):.2f}/ton")
    
    # Optimize grade pricing
    result = await call_steel_tool(
        "optimize_grade_pricing",
        quantity=100,
        grade="B",
        urgency="normal"
    )
    print(f"⚙️ Grade Pricing Optimization:")
    print(f"   Final Price: ${result.get('final_price', 0):.2f}/ton")
    print(f"   Margin: {result.get('margin', 0):.1%}")
    print(f"   Can Fulfill: {result.get('can_fulfill', False)}")

async def demo_integration_benefits():
    """Demonstrate benefits of MCP integration"""
    print("\n🎯 MCP Integration Benefits")
    print("=" * 40)
    
    print("\n✅ Official MCP SDK Benefits:")
    print("   • Proper protocol compliance")
    print("   • Standardized tool interfaces")
    print("   • Better error handling")
    print("   • Type safety with schemas")
    print("   • Async/await support")
    
    print("\n🔧 Tool Capabilities:")
    print("   • Real-time cost calculations")
    print("   • Dynamic margin optimization")
    print("   • Inventory management")
    print("   • Constraint validation")
    print("   • ROI analysis")
    
    print("\n📊 Business Value:")
    print("   • Automated profit optimization")
    print("   • Risk mitigation through constraints")
    print("   • Data-driven decision making")
    print("   • Scalable tool architecture")
    print("   • Transparent operations")

async def main():
    """Run the demo"""
    try:
        await demo_mcp_tools()
        await demo_integration_benefits()
        
        print("\n" + "=" * 50)
        print("✅ MCP Demo Complete!")
        print("\nKey Achievements:")
        print("• Replaced mock FastMCP with official MCP SDK")
        print("• Proper MCP protocol implementation")
        print("• Async tool communication")
        print("• Type-safe tool interfaces")
        print("• Production-ready architecture")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Make sure MCP SDK is installed: pip install mcp")

if __name__ == "__main__":
    asyncio.run(main())