# Insurance Agent - StrandsAgents Example

A comprehensive insurance assistant built with StrandsAgents that demonstrates real-world insurance domain use cases.

## Features

The Insurance Agent provides the following capabilities:

- **Premium Calculator**: Calculate insurance premiums for different coverage types (auto, home, life, health)
- **Risk Assessor**: Evaluate risk levels based on age, location, claims history, and credit score
- **Policy Lookup**: Retrieve policy information from a simulated database
- **Claims Processor**: Check claim status and process insurance claims
- **Coverage Advisor**: Recommend appropriate coverage based on financial situation

## Tools Overview

### 1. Premium Calculator
- Calculates annual and monthly premiums
- Supports auto, home, life, and health insurance
- Factors in age-based adjustments

### 2. Risk Assessor
- Evaluates risk based on multiple factors
- Provides risk score and level (Low/Medium/High)
- Offers underwriting recommendations

### 3. Policy Lookup
- Retrieves policy details by ID
- Shows premium, deductible, and coverage information

### 4. Claims Processor
- Checks claim status by claim ID
- Lists all claims for a specific policy
- Shows claim amounts and processing status

### 5. Coverage Advisor
- Recommends life, disability, and property insurance amounts
- Based on income, dependents, assets, and debt
- Provides total premium estimates

## Sample Data

The example includes sample policies and claims:

**Policies:**
- POL001: Auto insurance ($1,200 premium, $50,000 coverage)
- POL002: Home insurance ($800 premium, $200,000 coverage)  
- POL003: Life insurance ($2,400 premium, $500,000 coverage)

**Claims:**
- CLM001: Auto claim ($3,500, approved)
- CLM002: Home claim ($8,000, pending)

## Usage Examples

The agent can handle natural language queries like:

- "Calculate premium for $100,000 life insurance for a 40-year-old"
- "What's the risk level for someone in California with 2 previous claims?"
- "Look up policy POL002"
- "Check status of claim CLM001"
- "Recommend coverage for $90,000 income with 3 dependents"