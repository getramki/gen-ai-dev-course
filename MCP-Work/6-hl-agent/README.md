# Enhanced Home Loan Advisory Agent

An AI-powered home loan advisor that uses the enhanced MCP server with resources and prompts for comprehensive loan guidance.

## Features

- **EMI Calculations**: Calculate EMI with detailed breakdown
- **Interest Rate Information**: Current rates from major banks
- **Eligibility Guidance**: Loan eligibility criteria and requirements
- **Formula Explanations**: Detailed EMI calculation methodology
- **Advisory Prompts**: AI-powered loan advice and comparisons

## Prerequisites

1. AWS credentials configured
2. Access to Bedrock Claude Haiku model in us-east-1 region
3. Enhanced MCP server running

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python agent.py
```

## Example Queries

- "Calculate EMI for 50 lakh loan at 8.5% for 20 years"
- "What are current home loan interest rates?"
- "Am I eligible for a home loan with 40k monthly income?"
- "Explain how EMI is calculated"
- "Compare loan options for my profile"

The agent automatically loads resources and prompts from the MCP server to provide comprehensive home loan advisory services.