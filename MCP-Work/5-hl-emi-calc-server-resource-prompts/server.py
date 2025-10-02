#!/usr/bin/env python3
from fastmcp import FastMCP

mcp = FastMCP("Home Loan EMI Calculator with Resources")

@mcp.tool()
def calculate_home_loan_emi(principal: float, annual_rate: float, tenure_years: int) -> str:
    """Calculate home loan EMI, total amount, and interest.
    
    Args:
        principal: Loan amount in currency
        annual_rate: Annual interest rate as percentage
        tenure_years: Loan tenure in years
    """
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12
    
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
    
    emi = round(emi, 2)
    total_amount = emi * tenure_months
    total_interest = total_amount - principal
    
    return (f"EMI Calculation Results:\n"
            f"Monthly EMI: ₹{emi:,.2f}\n"
            f"Total Amount: ₹{total_amount:,.2f}\n"
            f"Total Interest: ₹{total_interest:,.2f}\n"
            f"Principal: ₹{principal:,.2f}\n"
            f"Interest Rate: {annual_rate}% per annum\n"
            f"Tenure: {tenure_years} years")

@mcp.resource("file://emi-formula")
def get_emi_formula() -> str:
    """EMI calculation formula and explanation."""
    return """EMI Formula: P * r * (1+r)^n / ((1+r)^n - 1)

Where:
- P = Principal loan amount
- r = Monthly interest rate (annual rate / 12 / 100)
- n = Number of monthly installments (years * 12)

Example: For ₹10,00,000 at 8.5% for 20 years
- P = 1000000
- r = 8.5/12/100 = 0.007083
- n = 20*12 = 240
- EMI = ₹8,678"""

@mcp.resource("file://interest-rates")
def get_interest_rates() -> str:
    """Current home loan interest rates in India."""
    return """Current Home Loan Interest Rates (Indicative):

SBI: 8.50% - 9.65%
HDFC: 8.60% - 9.50%
ICICI: 8.75% - 9.40%
Axis Bank: 8.80% - 9.30%
Kotak: 8.70% - 9.25%

Note: Rates vary based on loan amount, tenure, and credit profile."""

@mcp.resource("file://loan-eligibility")
def get_loan_eligibility() -> str:
    """Home loan eligibility criteria."""
    return """Home Loan Eligibility Criteria:

1. Age: 21-65 years
2. Income: Minimum ₹25,000/month
3. Employment: 2+ years experience
4. Credit Score: 750+ preferred
5. Debt-to-Income Ratio: <50%
6. Property Value: Up to 80-90% financing

Documents Required:
- Income proof, Bank statements
- Property documents, ID proof"""

@mcp.tool()
def get_emi_advice() -> str:
    """Get EMI advisory guidance."""
    return """You are a home loan EMI advisor. Help users:

1. Calculate EMI for different loan scenarios
2. Compare loan options from different banks
3. Understand the impact of interest rates and tenure
4. Optimize loan terms based on affordability
5. Explain EMI components (principal + interest)

Always ask for:
- Loan amount needed
- Preferred tenure
- Monthly income for affordability check
- Any existing loans/EMIs

Provide practical advice on loan planning."""

@mcp.tool()
def get_loan_comparison_guide() -> str:
    """Get loan comparison guidance."""
    return """Compare home loan options by analyzing:

1. Interest rates from different lenders
2. Processing fees and charges
3. Prepayment penalties
4. Loan tenure flexibility
5. Total cost of borrowing

Create a comparison table showing:
- Bank name
- Interest rate
- EMI amount
- Total interest payable
- Total amount payable

Recommend the best option based on user's financial profile."""

if __name__ == "__main__":
    mcp.run()