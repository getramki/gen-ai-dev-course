#!/usr/bin/env python3
from fastmcp import FastMCP

mcp = FastMCP("Home Loan EMI Calculator")

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

if __name__ == "__main__":
    mcp.run()