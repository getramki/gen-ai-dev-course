#!/usr/bin/env python3
"""
Insurance Agent - StrandsAgents Example
A comprehensive insurance assistant that can calculate premiums, assess risks, and process claims.
"""

from strands import Agent, tool
from datetime import datetime, date
import json

# Sample insurance data
POLICY_DATABASE = {
    "POL001": {"type": "auto", "premium": 1200, "deductible": 500, "coverage": 50000},
    "POL002": {"type": "home", "premium": 800, "deductible": 1000, "coverage": 200000},
    "POL003": {"type": "life", "premium": 2400, "deductible": 0, "coverage": 500000}
}

CLAIMS_DATABASE = {
    "CLM001": {"policy_id": "POL001", "amount": 3500, "status": "approved", "date": "2024-01-15"},
    "CLM002": {"policy_id": "POL002", "amount": 8000, "status": "pending", "date": "2024-02-10"}
}

@tool(name="premium_calculator", description="Calculate insurance premium based on coverage type and amount")
def premium_calculator(coverage_type: str, coverage_amount: int, age: int = 30) -> str:
    """Calculate insurance premium based on coverage type, amount, and age"""
    base_rates = {
        "auto": 0.024,
        "home": 0.004,
        "life": 0.048,
        "health": 0.036
    }
    
    if coverage_type.lower() not in base_rates:
        return f"Error: Unsupported coverage type '{coverage_type}'. Supported: auto, home, life, health"
    
    base_rate = base_rates[coverage_type.lower()]
    age_factor = 1.0 + (age - 30) * 0.01 if age > 30 else 1.0
    annual_premium = coverage_amount * base_rate * age_factor
    
    return f"""Premium Calculation:
- Coverage Type: {coverage_type.title()}
- Coverage Amount: ${coverage_amount:,}
- Age Factor: {age_factor:.2f}
- Annual Premium: ${annual_premium:,.2f}
- Monthly Premium: ${annual_premium/12:,.2f}"""

@tool(name="risk_assessor", description="Assess risk level based on various factors")
def risk_assessor(age: int, location: str, previous_claims: int = 0, credit_score: int = 700) -> str:
    """Assess insurance risk based on age, location, claims history, and credit score"""
    risk_score = 0
    
    # Age factor
    if age < 25: risk_score += 20
    elif age > 65: risk_score += 15
    else: risk_score += 5
    
    # Location factor (simplified)
    high_risk_locations = ["florida", "california", "texas", "new york"]
    if location.lower() in high_risk_locations:
        risk_score += 15
    else:
        risk_score += 5
    
    # Claims history
    risk_score += previous_claims * 10
    
    # Credit score factor
    if credit_score < 600: risk_score += 20
    elif credit_score < 700: risk_score += 10
    else: risk_score += 0
    
    # Determine risk level
    if risk_score <= 20: risk_level = "Low"
    elif risk_score <= 40: risk_level = "Medium"
    else: risk_level = "High"
    
    return f"""Risk Assessment:
- Age: {age} years
- Location: {location.title()}
- Previous Claims: {previous_claims}
- Credit Score: {credit_score}
- Risk Score: {risk_score}/100
- Risk Level: {risk_level}
- Recommendation: {'Standard rates' if risk_level == 'Low' else 'Premium adjustment recommended' if risk_level == 'Medium' else 'Detailed underwriting required'}"""

@tool(name="policy_lookup", description="Look up policy information by policy ID")
def policy_lookup(policy_id: str) -> str:
    """Look up policy details from the database"""
    policy = POLICY_DATABASE.get(policy_id.upper())
    if not policy:
        return f"Policy {policy_id} not found in database"
    
    return f"""Policy Information:
- Policy ID: {policy_id.upper()}
- Type: {policy['type'].title()}
- Annual Premium: ${policy['premium']:,}
- Deductible: ${policy['deductible']:,}
- Coverage Amount: ${policy['coverage']:,}"""

@tool(name="claims_processor", description="Process and check status of insurance claims")
def claims_processor(claim_id: str = None, policy_id: str = None) -> str:
    """Process claims or check claim status"""
    if claim_id:
        claim = CLAIMS_DATABASE.get(claim_id.upper())
        if not claim:
            return f"Claim {claim_id} not found"
        
        return f"""Claim Details:
- Claim ID: {claim_id.upper()}
- Policy ID: {claim['policy_id']}
- Claim Amount: ${claim['amount']:,}
- Status: {claim['status'].title()}
- Date Filed: {claim['date']}"""
    
    elif policy_id:
        policy_claims = [cid for cid, claim in CLAIMS_DATABASE.items() if claim['policy_id'] == policy_id.upper()]
        if not policy_claims:
            return f"No claims found for policy {policy_id}"
        
        result = f"Claims for Policy {policy_id.upper()}:\n"
        for cid in policy_claims:
            claim = CLAIMS_DATABASE[cid]
            result += f"- {cid}: ${claim['amount']:,} ({claim['status']})\n"
        return result
    
    else:
        return "Please provide either claim_id or policy_id"

@tool(name="coverage_advisor", description="Recommend appropriate coverage based on personal situation")
def coverage_advisor(income: int, dependents: int, assets_value: int, debt: int = 0) -> str:
    """Recommend insurance coverage based on financial situation"""
    # Life insurance recommendation (10x annual income + debt)
    life_coverage = (income * 10) + debt
    
    # Disability insurance (60-70% of income)
    disability_coverage = income * 0.65
    
    # Property insurance (full replacement value)
    property_coverage = assets_value
    
    # Health insurance deductible recommendation
    emergency_fund = income * 0.1  # 10% of income
    health_deductible = min(emergency_fund, 5000)
    
    return f"""Coverage Recommendations:
- Annual Income: ${income:,}
- Dependents: {dependents}
- Assets Value: ${assets_value:,}
- Outstanding Debt: ${debt:,}

Recommended Coverage:
- Life Insurance: ${life_coverage:,}
- Disability Insurance: ${disability_coverage:,.0f}/year
- Property Insurance: ${property_coverage:,}
- Health Insurance Deductible: ${health_deductible:,.0f}

Total Estimated Annual Premium: ${(life_coverage * 0.048 + disability_coverage * 0.02 + property_coverage * 0.004):,.0f}"""

def main():
    # Create insurance agent
    agent = Agent(
        name="InsuranceAgent",
        description="A comprehensive insurance assistant that helps with premiums, risk assessment, policy lookup, claims processing, and coverage recommendations",
        tools=[premium_calculator, risk_assessor, policy_lookup, claims_processor, coverage_advisor]
    )
    
    print("=== Insurance Agent Demo ===\n")
    
    # Demo 1: Premium calculation
    print("1. Premium Calculation:")
    agent("Calculate the premium for auto insurance with $75,000 coverage for a 35-year-old")
    print()
    
    # Demo 2: Risk assessment
    print("2. Risk Assessment:")
    agent("Assess the risk for a 28-year-old in Florida with 1 previous claim and credit score of 650")
    print()
    
    # Demo 3: Policy lookup
    print("3. Policy Lookup:")
    agent("Look up policy POL001")
    print()
    
    # Demo 4: Claims processing
    print("4. Claims Processing:")
    agent("Check the status of claim CLM001")
    print()
    
    # Demo 5: Coverage recommendation
    print("5. Coverage Recommendation:")
    agent("Recommend coverage for someone with $80,000 income, 2 dependents, $300,000 in assets, and $50,000 debt")
    print()
    
    print("=== Demo Complete ===")

if __name__ == "__main__":
    main()