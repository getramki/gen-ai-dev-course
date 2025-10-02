# Agentic AI Home Loan EMI Client

An AI-powered assistant that uses AWS Bedrock Claude Haiku to help users with home loan EMI calculations via MCP.

## Prerequisites

1. AWS credentials configured (via AWS CLI, environment variables, or IAM role)
2. Access to Bedrock Claude Haiku model in us-east-1 region

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python agent.py
```

## Features

- Natural language interaction with Claude Haiku
- Automatic parameter extraction from user queries
- Integration with MCP EMI calculator server
- Conversational interface for EMI calculations

## Example Queries

- "Calculate EMI for a loan of 5000000 at 8.5% for 20 years"
- "What's the EMI for 50 lakh loan at 9% interest for 15 years?"
- "Help me understand home loan EMI calculation"