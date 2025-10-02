def calculate_emi(principal, annual_rate, tenure_years):
    """Calculate EMI using the standard formula"""
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12
    
    if monthly_rate == 0:
        return principal / tenure_months
    
    emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
    return round(emi, 2)

def main():
    print("Home Loan EMI Calculator")
    print("-" * 25)
    
    try:
        principal = float(input("Enter loan amount: "))
        annual_rate = float(input("Enter annual interest rate (%): "))
        tenure_years = int(input("Enter loan tenure (years): "))
        
        emi = calculate_emi(principal, annual_rate, tenure_years)
        total_amount = emi * tenure_years * 12
        total_interest = total_amount - principal
        
        print(f"\nEMI: ₹{emi:,.2f}")
        print(f"Total Amount: ₹{total_amount:,.2f}")
        print(f"Total Interest: ₹{total_interest:,.2f}")
        
    except ValueError:
        print("Please enter valid numbers")

if __name__ == "__main__":
    main()