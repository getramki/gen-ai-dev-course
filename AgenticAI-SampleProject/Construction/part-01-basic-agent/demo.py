#!/usr/bin/env python3
"""
Part 1 Demo: Basic Agents with LangGraph and Profit Optimization
Demonstrates competitive negotiation with cycle limits and human constraints
"""

import os
from purchase_agent import PurchaseAgent
from cement_agent import CementAgent
from steel_agent import SteelAgent
from negotiation_cycles import CycleManager

def setup_environment():
    """Setup AWS credentials for Bedrock"""
    # Ensure AWS credentials are configured
    if not os.getenv('AWS_DEFAULT_REGION'):
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    
    print("✅ Environment configured for AWS Bedrock")

def demo_individual_agents():
    """Demonstrate each agent's profit optimization logic"""
    print("\n=== Individual Agent Demonstrations ===")
    
    # Purchase Agent Demo
    print("\n1. Purchase Agent (Cost Minimization)")
    purchase_agent = PurchaseAgent()
    
    requirements = {
        "cement_tons": 500,
        "steel_tons": 200,
        "quality_grade": "A",
        "delivery_deadline": "2026-03-15"
    }
    
    result = purchase_agent.process_procurement(requirements, 150000)
    print(f"   Budget: ${result['budget']:,}")
    print(f"   Target cement price: ${result['requirements']['target_cement_price']:.2f}/ton")
    print(f"   Target steel price: ${result['requirements']['target_steel_price']:.2f}/ton")
    
    # Cement Agent Demo
    print("\n2. Cement Sales Agent (Margin Maximization)")
    cement_agent = CementAgent()
    
    rfq = {"id": "RFQ_001", "cement_tons": 500}
    quote = cement_agent.generate_quote(rfq)
    print(f"   Price: ${quote['price_per_ton']:.2f}/ton")
    print(f"   Total: ${quote['total_price']:,.2f}")
    print(f"   Margin: {quote['margin']:.1%}")
    print(f"   Discount: {quote['discount']:.1%}")
    
    # Steel Agent Demo
    print("\n3. Steel Sales Agent (Inventory Optimization)")
    steel_agent = SteelAgent()
    
    rfq = {"id": "RFQ_002", "steel_tons": 200, "steel_grade": "A"}
    quote = steel_agent.generate_quote(rfq)
    print(f"   Grade A Price: ${quote['price_per_ton']:.2f}/ton")
    print(f"   Total: ${quote['total_price']:,.2f}")
    print(f"   Margin: {quote['margin']:.1%}")
    print(f"   Delivery: {quote['delivery_days']} days")

def demo_agreement_scenario():
    """Demonstrate successful agreement within budget"""
    print("\n=== Agreement Scenario (Success) ===")
    
    cement_agent = CementAgent()
    steel_agent = SteelAgent()
    purchase_agent = PurchaseAgent()
    
    print(f"\n🏗️  Construction Company RFQ (Reasonable Budget):")
    print(f"   - Cement: 300 tons")
    print(f"   - Steel Grade B: 100 tons")
    print(f"   - Budget: $120,000")
    
    # Generate quotes
    rfq_cement = {"id": "agreement_001", "cement_tons": 300}
    rfq_steel = {"id": "agreement_001", "steel_tons": 100, "steel_grade": "B"}
    
    cement_quote = cement_agent.generate_quote(rfq_cement)
    steel_quote = steel_agent.generate_quote(rfq_steel)
    
    total_cost = cement_quote["total_price"] + steel_quote["total_price"]
    
    print(f"\n📋 Quotes Received:")
    print(f"   Cement: ${cement_quote['price_per_ton']:.2f}/ton = ${cement_quote['total_price']:,.2f}")
    print(f"   Steel:  ${steel_quote['price_per_ton']:.2f}/ton = ${steel_quote['total_price']:,.2f}")
    print(f"   Total:  ${total_cost:,.2f}")
    
    # Purchase agent evaluation
    requirements = {"cement_tons": 300, "steel_tons": 100}
    purchase_result = purchase_agent.process_procurement(requirements, 120000)
    
    if total_cost <= 120000:
        print(f"\n✅ AGREEMENT REACHED!")
        print(f"   Within budget by: ${120000 - total_cost:,.2f}")
        print(f"   Contract terms accepted")
    else:
        print(f"\n❌ Budget exceeded by: ${total_cost - 120000:,.2f}")

def demo_disagreement_scenario():
    """Demonstrate failed negotiation due to constraints"""
    print("\n=== Disagreement Scenario (Failure) ===")
    
    cement_agent = CementAgent()
    steel_agent = SteelAgent()
    purchase_agent = PurchaseAgent()
    cycle_manager = CycleManager()
    
    print(f"\n🏗️  Construction Company RFQ (Tight Budget):")
    print(f"   - Cement: 800 tons")
    print(f"   - Steel Grade A: 300 tons")
    print(f"   - Budget: $180,000 (Unrealistic)")
    
    # Start negotiation
    task_id = "disagreement_001"
    negotiation = cycle_manager.start_negotiation(task_id, ["cement_agent", "steel_agent"])
    
    rfq_cement = {"id": task_id, "cement_tons": 800}
    rfq_steel = {"id": task_id, "steel_tons": 300, "steel_grade": "A"}
    
    # Purchase agent sets unrealistic targets
    requirements = {"cement_tons": 800, "steel_tons": 300}
    purchase_result = purchase_agent.process_procurement(requirements, 180000)
    
    print(f"\n💭 Purchase Agent Targets:")
    print(f"   Target cement: ${purchase_result['requirements']['target_cement_price']:.2f}/ton")
    print(f"   Target steel: ${purchase_result['requirements']['target_steel_price']:.2f}/ton")
    
    # Multi-cycle failed negotiation
    for cycle in range(1, 6):
        print(f"\n--- Cycle {cycle} ---")
        
        # Agents maintain minimum margins
        cement_quote = cement_agent.generate_quote(rfq_cement)
        steel_quote = steel_agent.generate_quote(rfq_steel)
        
        total_cost = cement_quote["total_price"] + steel_quote["total_price"]
        
        print(f"   Cement: ${cement_quote['price_per_ton']:.2f}/ton (margin: {cement_quote['margin']:.1%})")
        print(f"   Steel:  ${steel_quote['price_per_ton']:.2f}/ton (margin: {steel_quote['margin']:.1%})")
        print(f"   Total:  ${total_cost:,.2f}")
        print(f"   Over budget: ${total_cost - 180000:,.2f}")
        
        # Check if agents can meet budget
        cement_min_price = cement_agent.base_cost * (1 + cement_agent.constraints.min_margin)
        steel_min_price = steel_agent.grade_costs["A"] * (1 + steel_agent.constraints.min_margin)
        
        min_possible = (cement_min_price * 800) + (steel_min_price * 300)
        
        if min_possible > 180000:
            print(f"   🚫 Impossible to meet budget even at minimum margins")
            print(f"   Minimum possible: ${min_possible:,.2f}")
            break
        
        if not cycle_manager.advance_cycle(task_id):
            break
    
    print(f"\n❌ NEGOTIATION FAILED!")
    print(f"   Reason: Budget constraints incompatible with minimum margins")
    print(f"   Agents protected company profitability")

def demo_constraint_enforcement():
    """Demonstrate human-set constraint enforcement"""
    print("\n=== Constraint Enforcement Demo ===")
    
    cement_agent = CementAgent()
    
    # Test minimum margin constraint
    print("\n1. Minimum Margin Enforcement:")
    rfq = {"id": "constraint_test", "cement_tons": 1000}  # Large order
    quote = cement_agent.generate_quote(rfq)
    
    print(f"   Large order (1000 tons)")
    print(f"   Price: ${quote['price_per_ton']:.2f}/ton")
    print(f"   Margin: {quote['margin']:.1%} (min: 15%)")
    print(f"   ✅ Constraint respected: {quote['margin'] >= 0.15}")
    
    # Test maximum discount constraint
    print(f"   Discount: {quote['discount']:.1%} (max: 20%)")
    print(f"   ✅ Constraint respected: {quote['discount'] <= 0.20}")

def main():
    """Run complete Part 1 demonstration"""
    print("🚀 Part 1: Basic Agents with LangGraph Demo")
    print("=" * 50)
    
    try:
        setup_environment()
        demo_individual_agents()
        demo_agreement_scenario()
        demo_disagreement_scenario()
        demo_constraint_enforcement()
        
        print("\n" + "=" * 50)
        print("✅ Part 1 Demo Complete!")
        print("\nKey Achievements:")
        print("• Agents optimize for company profit within constraints")
        print("• Negotiation cycles limited to 5 rounds maximum")
        print("• Human-set limits enforced (margins, discounts, budgets)")
        print("• LangGraph workflows handle complex decision logic")
        print("• AWS Bedrock LLM reasoning displayed for debugging")
        print("• Both agreement and disagreement scenarios demonstrated")
        print("• Agents protect company interests even when deals fail")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Ensure AWS credentials are configured for Bedrock access")

if __name__ == "__main__":
    main()