#!/usr/bin/env python3
"""
Interactive Insurance Agent Demo
Run this for a hands-on experience with the insurance agent.
"""

from strands import Agent
from insurance_agent import premium_calculator, risk_assessor, policy_lookup, claims_processor, coverage_advisor

def main():
    # Create the insurance agent
    agent = Agent(
        name="InsuranceAgent",
        description="Interactive insurance assistant for personalized help",
        tools=[premium_calculator, risk_assessor, policy_lookup, claims_processor, coverage_advisor]
    )
    
    print("🏠 Welcome to the Interactive Insurance Agent! 🏠")
    print("Ask me anything about insurance - premiums, policies, claims, or coverage advice.")
    print("Type 'quit' to exit.\n")
    
    # Sample questions to get started
    sample_questions = [
        "Calculate auto insurance premium for $60,000 coverage, age 28",
        "What's my risk level? Age 35, Texas, 0 claims, credit 720",
        "Look up policy POL002",
        "Check claim CLM001 status",
        "Recommend coverage: $75,000 income, 2 kids, $250,000 assets"
    ]
    
    print("💡 Try these sample questions:")
    for i, question in enumerate(sample_questions, 1):
        print(f"{i}. {question}")
    print()
    
    while True:
        try:
            user_input = input("🤔 Your question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Thank you for using the Insurance Agent!")
                break
            
            if not user_input:
                continue
            
            print("\n🤖 Agent Response:")
            agent(user_input)
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Thank you for using the Insurance Agent!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again.\n")

if __name__ == "__main__":
    main()