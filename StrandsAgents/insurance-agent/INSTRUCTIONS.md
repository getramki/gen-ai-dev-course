# Step-by-Step Instructions: Insurance Agent

## Prerequisites

1. **Python 3.8+** installed on your system
2. **AWS CLI** configured with appropriate credentials
3. **StrandsAgents SDK** access

## Setup Instructions

### Step 1: Navigate to the Project Directory
```bash
cd /home/ramakrishna/Code/GenAI-for-Dev-Course/StrandsAgents/insurance-agent
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python -c "from strands import Agent, tool; print('StrandsAgents installed successfully')"
```

## Running the Example

### Step 4: Run the Demo
```bash
python insurance_agent.py
```

This will execute a comprehensive demo showing all insurance agent capabilities.

### Step 5: Interactive Usage
You can also use the agent interactively by modifying the main function or creating a simple interactive script:

```python
from insurance_agent import *

# Create the agent
agent = Agent(
    name="InsuranceAgent",
    description="Insurance assistant",
    tools=[premium_calculator, risk_assessor, policy_lookup, claims_processor, coverage_advisor]
)

# Ask questions
agent("What's the premium for $200,000 home insurance for a 45-year-old?")
```

## Understanding the Code

### Step 6: Explore the Tools

1. **Premium Calculator** (`premium_calculator`)
   - Input: coverage_type, coverage_amount, age
   - Calculates premiums using base rates and age factors

2. **Risk Assessor** (`risk_assessor`)
   - Input: age, location, previous_claims, credit_score
   - Returns risk level and recommendations

3. **Policy Lookup** (`policy_lookup`)
   - Input: policy_id
   - Retrieves policy details from database

4. **Claims Processor** (`claims_processor`)
   - Input: claim_id or policy_id
   - Shows claim status and details

5. **Coverage Advisor** (`coverage_advisor`)
   - Input: income, dependents, assets_value, debt
   - Recommends appropriate coverage amounts

### Step 7: Customize the Example

To adapt this for your use case:

1. **Modify Sample Data**: Update `POLICY_DATABASE` and `CLAIMS_DATABASE`
2. **Adjust Calculations**: Modify premium rates and risk factors
3. **Add New Tools**: Create additional `@tool` decorated functions
4. **Extend Database**: Add real database connections

## Testing Different Scenarios

### Step 8: Try These Queries

```python
# Premium calculations
agent("Calculate life insurance premium for $500,000 coverage, age 50")

# Risk assessment
agent("Assess risk for 22-year-old in New York, no claims, 750 credit score")

# Policy management
agent("Show me details for policy POL003")

# Claims handling
agent("What claims exist for policy POL001?")

# Coverage recommendations
agent("Recommend insurance for $120,000 income, 1 dependent, $400,000 assets")
```

## Troubleshooting

### Common Issues:

1. **Import Error**: Ensure strands-agents is installed correctly
2. **AWS Credentials**: Verify AWS CLI configuration
3. **Tool Registration**: Check that all tools use `@tool` decorator properly

### Step 9: Verify Tool Registration
```python
# Check if tools are properly registered
from insurance_agent import premium_calculator
print(hasattr(premium_calculator, '__tool__'))  # Should return True
```

## Next Steps

1. **Integrate Real Data**: Connect to actual insurance databases
2. **Add Authentication**: Implement user authentication for policy access
3. **Enhance Calculations**: Use more sophisticated actuarial models
4. **Add Validation**: Implement input validation and error handling
5. **Create Web Interface**: Build a web UI for the insurance agent