# LangChain Agents with AWS Bedrock Nova Pro - Learning Plan

## Overview
This guide teaches you how to build AI agents using LangChain with AWS Bedrock Nova Pro as the backend LLM.

## Learning Sequence

### 1. Setup and Basic Agent (01-setup-and-basic-agent.py)
- Install required packages
- Configure AWS Bedrock connection
- Create your first simple agent
- Understand agent basics

### 2. Static Model (02-static-model.py)
- Configure model with fixed parameters
- Set temperature, max tokens, etc.
- Understand model configuration options

### 3. Dynamic Model (03-dynamic-model.py)
- Switch between different models at runtime
- Adjust parameters dynamically
- Use different models for different tasks

### 4. Basic Tools (04-tools-basic.py)
- Create custom tools for agents
- Define tool schemas
- Single tool usage

### 5. Advanced Tools (05-tools-advanced.py)
- Multiple tools in one agent
- Tool selection logic
- Complex tool interactions

### 6. Agent Invocation (06-agent-invocation.py)
- Different ways to invoke agents
- Synchronous vs asynchronous
- Batch processing

### 7. Short-Term Memory (07-short-term-memory.py)
- Add conversation memory
- Context retention
- Multi-turn conversations

### 8. Streaming (08-streaming.py)
- Stream responses in real-time
- Handle streaming events
- Better user experience

### 9. Complete Agent (09-complete-agent.py)
- Combine all concepts
- Production-ready agent
- Best practices

## Prerequisites

### AWS Setup
```bash
# Configure AWS credentials
aws configure
```

### Python Packages
```bash
pip install langchain langchain-aws langchain-community boto3
```

### Environment Variables (Optional)
```bash
export AWS_REGION=us-east-1
export AWS_PROFILE=default
```

## Key Concepts

### Agent
An autonomous entity that uses an LLM to decide which actions to take and in what order.

### Model
The underlying LLM (Nova Pro) that powers the agent's reasoning.

### Tools
Functions that agents can call to perform specific tasks (calculations, API calls, etc.).

### Memory
Allows agents to remember previous interactions in a conversation.

### Streaming
Real-time response generation for better user experience.

## Progress Tracking

- [ ] 01 - Setup and Basic Agent
- [ ] 02 - Static Model
- [ ] 03 - Dynamic Model
- [ ] 04 - Basic Tools
- [ ] 05 - Advanced Tools
- [ ] 06 - Agent Invocation
- [ ] 07 - Short-Term Memory
- [ ] 08 - Streaming
- [ ] 09 - Complete Agent

## Next Steps
Start with `01-setup-and-basic-agent.py` and work through each file sequentially.
