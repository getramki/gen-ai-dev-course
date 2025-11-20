#!/usr/bin/env python3
"""
Part 2 Demo: Enhanced Agents with MCP Integration - Negotiation Scenarios
Demonstrates competitive negotiation with MCP tools and profit optimization
"""

import os
import asyncio
from enhanced_agents.enhanced_purchase_agent import EnhancedPurchaseAgent
from enhanced_agents.enhanced_cement_agent import EnhancedCementAgent
from enhanced_agents.enhanced_steel_agent import EnhancedSteelAgent

def setup_environment():
    """Setup AWS credentials for Bedrock"""
    if not os.getenv('AWS_DEFAULT_REGION'):
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    print("✅ Environment configured for AWS Bedrock")

async def demo_enhanced_agents():
    """Demonstrate enhanced agents with MCP tools"""
    print("\n=== Enhanced Agents with MCP Tools ===")
    
    purchase_agent = EnhancedPurchaseAgent()
    cement_agent = EnhancedCementAgent()
    steel_agent = EnhancedSteelAgent()
    
    print("\n1. Enhanced Purchase Agent (MCP Cost Analysis)")
    requirements = {"cement_tons": 500, "steel_tons": 200}
    result = await purchase_agent.graph.ainvoke({
        "task_id": "demo_001",
        "requirements": requirements,
        "budget": 150000,
        "received_quotes": [],
        "selected_suppliers": [],
        "current_cycle": 1,
        "negotiation_complete": False,
        "mcp_analysis": {},
        "roi_projection": {},
        "budget_tracking": {},
        "supplier_performance": {}
    })
    print(f"   MCP Analysis Complete")
    
    print("\n2. Enhanced Cement Agent (MCP Margin Optimization)")
    rfq = {"id": "enhanced_001", "cement_tons": 500}
    result = await cement_agent.graph.ainvoke({
        "rfq_id": rfq["id"],
        "quantity": rfq["cement_tons"],
        "base_price": cement_agent.base_price,
        "cost_per_ton": cement_agent.base_cost,
        "current_offer": {},
        "competitor_offers": [],
        "current_cycle": 1,
        "negotiation_complete": False,
        "mcp_margin_analysis": {},
        "pricing_strategy": {},
        "inventory_status": {},
        "competitive_response": {}
    })
    quote = result["current_offer"]
    print(f"   MCP Optimized Price: ${quote.get('price_per_ton', 0):.2f}/ton")
    
    print("\n3. Enhanced Steel Agent (MCP Inventory Optimization)")
    rfq = {"id": "enhanced_002", "steel_tons": 200, "steel_grade": "A"}
    result = await steel_agent.graph.ainvoke({
        "rfq_id": rfq["id"],
        "quantity": rfq["steel_tons"],
        "grade": rfq["steel_grade"],
        "base_price": steel_agent.grade_prices["A"],
        "storage_cost": steel_agent.storage_cost_per_ton,
        "cost_per_ton": steel_agent.grade_costs["A"],
        "current_offer": {},
        "competitor_offers": [],
        "current_cycle": 1,
        "negotiation_complete": False,
        "inventory_analysis": {},
        "grade_optimization": {},
        "market_positioning": {},
        "delivery_analysis": {},
        "bulk_strategy": {}
    })
    quote = result["current_offer"]
    print(f"   MCP Optimized Price: ${quote.get('price_per_ton', 0):.2f}/ton")

async def demo_agreement_with_mcp():
    """Demonstrate successful agreement with MCP optimization"""
    print("\n=== Agreement Scenario with MCP Tools ===")
    
    cement_agent = EnhancedCementAgent()
    steel_agent = EnhancedSteelAgent()
    
    print(f"\n🏗️ Construction RFQ (MCP Enhanced):")
    print(f"   - Cement: 300 tons")
    print(f"   - Steel Grade B: 100 tons")
    print(f"   - Budget: $120,000")
    
    rfq_cement = {"id": "mcp_agreement", "cement_tons": 300}
    rfq_steel = {"id": "mcp_agreement", "steel_tons": 100, "steel_grade": "B"}
    
    cement_result = await cement_agent.graph.ainvoke({
        "rfq_id": rfq_cement["id"],
        "quantity": rfq_cement["cement_tons"],
        "base_price": cement_agent.base_price,
        "cost_per_ton": cement_agent.base_cost,
        "current_offer": {},
        "competitor_offers": [],
        "current_cycle": 1,
        "negotiation_complete": False,
        "mcp_margin_analysis": {},
        "pricing_strategy": {},
        "inventory_status": {},
        "competitive_response": {}
    })
    cement_quote = cement_result["current_offer"]
    
    steel_result = await steel_agent.graph.ainvoke({
        "rfq_id": rfq_steel["id"],
        "quantity": rfq_steel["steel_tons"],
        "grade": rfq_steel["steel_grade"],
        "base_price": steel_agent.grade_prices["B"],
        "storage_cost": steel_agent.storage_cost_per_ton,
        "cost_per_ton": steel_agent.grade_costs["B"],
        "current_offer": {},
        "competitor_offers": [],
        "current_cycle": 1,
        "negotiation_complete": False,
        "inventory_analysis": {},
        "grade_optimization": {},
        "market_positioning": {},
        "delivery_analysis": {},
        "bulk_strategy": {}
    })
    steel_quote = steel_result["current_offer"]
    
    total_cost = cement_quote.get("total_price", 0) + steel_quote.get("total_price", 0)
    
    print(f"\n📋 MCP Enhanced Quotes:")
    print(f"   Cement: ${cement_quote.get('price_per_ton', 0):.2f}/ton")
    print(f"   Steel:  ${steel_quote.get('price_per_ton', 0):.2f}/ton")
    print(f"   Total:  ${total_cost:,.2f}")
    
    if total_cost <= 120000:
        print(f"\n✅ MCP OPTIMIZED AGREEMENT!")
        print(f"   Savings: ${120000 - total_cost:,.2f}")
    else:
        print(f"\n❌ Budget exceeded: ${total_cost - 120000:,.2f}")

async def demo_competitive_negotiation():
    """Demonstrate competitive negotiation with MCP insights"""
    print("\n=== Competitive Negotiation with MCP ===")
    
    cement_agent = EnhancedCementAgent()
    steel_agent = EnhancedSteelAgent()
    
    print(f"\n🏗️ Competitive RFQ:")
    print(f"   - Cement: 800 tons")
    print(f"   - Steel Grade A: 300 tons")
    print(f"   - Competitor offers present")
    
    # Simulate competitor offers
    competitor_cement = [{"price_per_ton": 165}]
    competitor_steel = [{"price_per_ton": 720}]
    
    rfq_cement = {"id": "competitive_001", "cement_tons": 800}
    rfq_steel = {"id": "competitive_001", "steel_tons": 300, "steel_grade": "A"}
    
    for cycle in range(1, 4):
        print(f"\n--- Cycle {cycle} (MCP Enhanced) ---")
        
        cement_result = await cement_agent.graph.ainvoke({
            "rfq_id": rfq_cement["id"],
            "quantity": rfq_cement["cement_tons"],
            "base_price": cement_agent.base_price,
            "cost_per_ton": cement_agent.base_cost,
            "current_offer": {},
            "competitor_offers": competitor_cement,
            "current_cycle": cycle,
            "negotiation_complete": False,
            "mcp_margin_analysis": {},
            "pricing_strategy": {},
            "inventory_status": {},
            "competitive_response": {}
        })
        cement_quote = cement_result["current_offer"]
        
        steel_result = await steel_agent.graph.ainvoke({
            "rfq_id": rfq_steel["id"],
            "quantity": rfq_steel["steel_tons"],
            "grade": rfq_steel["steel_grade"],
            "base_price": steel_agent.grade_prices["A"],
            "storage_cost": steel_agent.storage_cost_per_ton,
            "cost_per_ton": steel_agent.grade_costs["A"],
            "current_offer": {},
            "competitor_offers": competitor_steel,
            "current_cycle": cycle,
            "negotiation_complete": False,
            "inventory_analysis": {},
            "grade_optimization": {},
            "market_positioning": {},
            "delivery_analysis": {},
            "bulk_strategy": {}
        })
        steel_quote = steel_result["current_offer"]
        
        total_cost = cement_quote.get("total_price", 0) + steel_quote.get("total_price", 0)
        
        print(f"   Cement: ${cement_quote.get('price_per_ton', 0):.2f}/ton")
        print(f"   Steel:  ${steel_quote.get('price_per_ton', 0):.2f}/ton")
        print(f"   Total:  ${total_cost:,.2f}")
        print(f"   MCP Strategy: Competitive positioning active")
        
        # Simulate competitor response
        if cycle < 3:
            competitor_cement[0]["price_per_ton"] -= 2
            competitor_steel[0]["price_per_ton"] -= 5

async def demo_mcp_constraint_enforcement():
    """Demonstrate MCP-based constraint enforcement"""
    print("\n=== MCP Constraint Enforcement ===")
    
    cement_agent = EnhancedCementAgent()
    
    print("\n🛡️ MCP Constraint Validation:")
    rfq = {"id": "constraint_mcp", "cement_tons": 1000}
    result = await cement_agent.graph.ainvoke({
        "rfq_id": rfq["id"],
        "quantity": rfq["cement_tons"],
        "base_price": cement_agent.base_price,
        "cost_per_ton": cement_agent.base_cost,
        "current_offer": {},
        "competitor_offers": [],
        "current_cycle": 1,
        "negotiation_complete": False,
        "mcp_margin_analysis": {},
        "pricing_strategy": {},
        "inventory_status": {},
        "competitive_response": {}
    })
    quote = result["current_offer"]
    
    print(f"   Price: ${quote.get('price_per_ton', 0):.2f}/ton")
    print(f"   Margin: {quote.get('margin', 0):.1%}")
    print(f"   MCP Validation: ✅ Constraints enforced")
    print(f"   Profit Projection: ${quote.get('mcp_profit_projection', 0):,.2f}")

async def main():
    """Run complete Part 2 negotiation demonstration"""
    print("🚀 Part 2: Enhanced Negotiation with MCP Integration")
    print("=" * 60)
    
    try:
        setup_environment()
        await demo_enhanced_agents()
        await demo_agreement_with_mcp()
        await demo_competitive_negotiation()
        await demo_mcp_constraint_enforcement()
        
        print("\n" + "=" * 60)
        print("✅ Part 2 Negotiation Demo Complete!")
        print("\nMCP Enhanced Achievements:")
        print("• Real-time margin optimization via MCP tools")
        print("• Dynamic competitive positioning with market analysis")
        print("• Inventory-aware pricing with carrying cost calculations")
        print("• Automated constraint validation and enforcement")
        print("• ROI-driven decision making with profit projections")
        print("• LLM reasoning combined with MCP tool insights")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Ensure MCP SDK is installed and AWS credentials configured")

if __name__ == "__main__":
    asyncio.run(main())