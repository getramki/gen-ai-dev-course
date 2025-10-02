# Part 1: Basic Agents with LangGraph

## Overview
This module demonstrates foundational agentic AI concepts using LangGraph and AWS Bedrock. Each agent optimizes for company profit within human-set constraints and negotiation cycle limits.

## Key Features
- **Profit Maximization**: Each agent works toward company objectives
- **Human Constraints**: Pricing bounds, margins, and approval thresholds
- **Cycle Limits**: Maximum 5 negotiation rounds to prevent infinite loops
- **LangGraph Workflows**: State-based agent decision making
- **AWS Bedrock Integration**: Ready for LLM-powered reasoning

## Agents

### Purchase Agent
- **Objective**: Minimize total procurement cost
- **Constraints**: Budget limits, quality requirements
- **Strategy**: Aggressive cost reduction within bounds

### Cement Sales Agent  
- **Objective**: Maximize margin per sale
- **Constraints**: 15% minimum margin, 20% maximum discount
- **Strategy**: Volume-based pricing with competitive positioning

### Steel Sales Agent
- **Objective**: Optimize profit considering inventory costs
- **Constraints**: 12% minimum margin, grade-based pricing
- **Strategy**: Inventory optimization with competitive pricing

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure AWS**
   ```bash
   aws configure  # Ensure Bedrock access
   export AWS_DEFAULT_REGION=us-east-1
   ```

3. **Run Demo**
   ```bash
   python demo.py
   ```

## Demo Scenarios

### Individual Agent Testing
- Purchase agent budget optimization
- Cement agent margin maximization  
- Steel agent inventory management

### Competitive Negotiation
- Multi-cycle bidding process
- Automatic cycle advancement
- Constraint enforcement
- Auto-finalization at cycle limits

### Constraint Validation
- Minimum margin enforcement
- Maximum discount limits
- Budget boundary testing

## Business Rules Applied

- **Negotiation Cycles**: 1-5 rounds with decreasing adjustment limits
- **Auto-Finalization**: Best available terms when cycles exhausted
- **Profit Optimization**: Each agent maximizes company value
- **Human Oversight**: Approval thresholds and policy enforcement

## Next Steps
- Part 2: Add MCP tools for enhanced capabilities
- Part 3: Implement A2A communication between agents
- Part 4: Containerize for local deployment
- Part 5: Deploy to cloud environments