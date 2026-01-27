# LangChain Agents with AWS Bedrock Nova Pro

A comprehensive, hands-on guide to building AI agents using LangChain with AWS Bedrock Nova Pro as the backend LLM. Perfect for novice programmers!

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Learning Path](#learning-path)
- [Quick Start](#quick-start)
- [Module Details](#module-details)
- [Key Concepts](#key-concepts)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)

## 🎯 Overview

This course teaches you how to build intelligent AI agents that can:
- Reason about problems and decide which actions to take
- Use tools to perform specific tasks
- Remember conversation context
- Stream responses in real-time
- Adapt their behavior dynamically

**Backend LLM**: AWS Bedrock Nova Pro (us.amazon.nova-pro-v1:0)  
**Framework**: LangChain (Latest version as of 2024)  
**Difficulty**: Beginner-friendly

## ✅ Prerequisites

### Required Knowledge
- Basic Python programming (variables, functions, loops)
- Command line basics
- Basic understanding of APIs

### Required Software
- Python 3.9 or higher
- AWS Account with Bedrock access
- AWS CLI configured

### AWS Setup
1. Create an AWS account
2. Enable Amazon Bedrock in your region (us-east-1 recommended)
3. Request access to Nova Pro model
4. Configure AWS credentials:
```bash
aws configure
```

## 📦 Installation

### Step 1: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv langchain-env

# Activate it
# On Linux/Mac:
source langchain-env/bin/activate
# On Windows:
langchain-env\Scripts\activate
```

### Step 2: Install Required Packages
```bash
pip install langchain langchain-aws langchain-community boto3
```

### Step 3: Verify Installation
```bash
python -c "import langchain; print(langchain.__version__)"
python -c "import boto3; print(boto3.__version__)"
```

### Step 4: Test AWS Connection
```bash
aws bedrock list-foundation-models --region us-east-1
```

## 🎓 Learning Path

Follow these modules in order. Each builds on the previous one:

| # | Module | Time | Key Concepts |
|---|--------|------|--------------|
| 00 | [Plan](00-plan.md) | 5 min | Course overview and roadmap |
| 01 | [Setup & Basic Agent](01-setup-and-basic-agent.py) | 20 min | Initialize Bedrock, create first agent |
| 02 | [Static Model](02-static-model.py) | 15 min | Configure temperature, tokens, top_p |
| 03 | [Dynamic Model](03-dynamic-model.py) | 20 min | Switch models at runtime |
| 04 | [Basic Tools](04-tools-basic.py) | 25 min | Create and use simple tools |
| 05 | [Advanced Tools](05-tools-advanced.py) | 30 min | Complex tools, error handling |
| 06 | [Agent Invocation](06-agent-invocation.py) | 20 min | Different invocation methods |
| 07 | [Short-Term Memory](07-short-term-memory.py) | 30 min | Add conversation memory |
| 08 | [Streaming](08-streaming.py) | 25 min | Real-time response streaming |
| 09 | [Complete Agent](09-complete-agent.py) | 30 min | Production-ready agent |

**Total Time**: ~3.5 hours

## 🚀 Quick Start

### Run Your First Agent (5 minutes)

```bash
# Navigate to the directory
cd /home/ramakrishna/Code/GenAI-for-Dev-Course/AWS/4-LangChain

# Run the first example
python 01-setup-and-basic-agent.py
```

You should see output showing the agent reasoning and using tools!

### Try the Complete Agent

```bash
# Run the full-featured agent
python 09-complete-agent.py
```

## 📚 Module Details

### Module 01: Setup and Basic Agent
**File**: `01-setup-and-basic-agent.py`

Learn to:
- Initialize AWS Bedrock with Nova Pro
- Create a simple greeting tool
- Build a basic ReAct agent
- Invoke the agent with queries

**Key Code**:
```python
llm = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1"
)
```

---

### Module 02: Static Model Configuration
**File**: `02-static-model.py`

Learn to:
- Configure temperature (creativity control)
- Set max_tokens (response length)
- Adjust top_p (nucleus sampling)
- Use different configurations for different tasks

**Key Parameters**:
- `temperature`: 0.0 (deterministic) to 1.0 (creative)
- `max_tokens`: Maximum response length
- `top_p`: 0.0 (focused) to 1.0 (diverse)

---

### Module 03: Dynamic Model Configuration
**File**: `03-dynamic-model.py`

Learn to:
- Switch model configurations at runtime
- Create a model manager class
- Adjust parameters based on task type
- Use different modes (creative, analytical, conversational)

**Use Cases**:
- Creative writing: High temperature
- Math problems: Low temperature
- Chat: Balanced settings

---

### Module 04: Basic Tools
**File**: `04-tools-basic.py`

Learn to:
- Create custom tools with specific functions
- Define tool descriptions
- Use multiple tools with one agent
- Understand how agents select tools

**Example Tools**:
- Calculator
- Current time
- Text counter

---

### Module 05: Advanced Tools
**File**: `05-tools-advanced.py`

Learn to:
- Build complex tools with error handling
- Simulate API calls
- Parse and validate inputs
- Return structured data (JSON)

**Example Tools**:
- Weather API (simulated)
- Data analyzer
- Text processor
- Unit converter

---

### Module 06: Agent Invocation
**File**: `06-agent-invocation.py`

Learn to:
- Use `invoke()` for single queries
- Use `batch()` for multiple queries
- Get intermediate reasoning steps
- Handle errors gracefully
- Control execution with max_iterations

**Methods**:
```python
# Single query
result = agent.invoke({"input": "query"})

# Batch queries
results = agent.batch([{"input": "q1"}, {"input": "q2"}])
```

---

### Module 07: Short-Term Memory
**File**: `07-short-term-memory.py`

Learn to:
- Add conversation memory to agents
- Use ConversationBufferMemory (unlimited)
- Use ConversationBufferWindowMemory (limited)
- Manage memory manually

**Memory Types**:
- **Buffer Memory**: Remembers everything
- **Window Memory**: Remembers last N interactions

---

### Module 08: Streaming
**File**: `08-streaming.py`

Learn to:
- Enable streaming in ChatBedrock
- Use StreamingStdOutCallbackHandler
- Create custom streaming handlers
- Stream with agents
- Compare streaming vs non-streaming

**Benefits**:
- Better user experience
- Immediate feedback
- Perceived faster responses

---

### Module 09: Complete Agent
**File**: `09-complete-agent.py`

A production-ready agent combining:
- ✅ Dynamic model configuration
- ✅ Multiple comprehensive tools
- ✅ Conversation memory
- ✅ Streaming responses
- ✅ Error handling
- ✅ Intelligent tool selection

**This is your template for real applications!**

---

## 🔑 Key Concepts

### What is an Agent?
An agent is an autonomous entity that:
1. Receives a query
2. Reasons about what to do
3. Decides which tools to use
4. Executes actions
5. Returns a final answer

### ReAct Pattern
Agents use the ReAct (Reasoning + Acting) pattern:
```
Question → Thought → Action → Observation → Thought → Final Answer
```

### Tools
Functions that agents can call to perform specific tasks:
- Calculations
- API calls
- Database queries
- File operations
- Web searches

### Memory
Allows agents to remember previous interactions:
- **Short-term**: Recent conversation context
- **Buffer**: All interactions
- **Window**: Last N interactions

### Streaming
Real-time token generation for better UX:
- Tokens appear as they're generated
- User sees progress immediately
- Better perceived performance

## 🔧 Troubleshooting

### Issue: "No module named 'langchain'"
**Solution**:
```bash
pip install langchain langchain-aws langchain-community
```

### Issue: "Could not connect to Bedrock"
**Solution**:
1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify region: Use `us-east-1`
3. Check Bedrock access in AWS Console

### Issue: "Model not found"
**Solution**:
1. Request access to Nova Pro in AWS Console
2. Wait for approval (usually instant)
3. Verify model ID: `us.amazon.nova-pro-v1:0`

### Issue: "Rate limit exceeded"
**Solution**:
1. Add delays between requests
2. Use batch processing
3. Request quota increase in AWS Console

### Issue: Agent not using tools correctly
**Solution**:
1. Check tool descriptions (be specific)
2. Lower temperature for more deterministic behavior
3. Add examples in tool descriptions

## 📖 Additional Resources

### Official Documentation
- [LangChain Docs](https://python.langchain.com/)
- [AWS Bedrock Docs](https://docs.aws.amazon.com/bedrock/)
- [LangChain Agents Guide](https://python.langchain.com/docs/modules/agents/)

### AWS Bedrock Models
- Nova Pro: Best for complex reasoning
- Nova Lite: Faster, cheaper
- Nova Micro: Smallest, fastest

### LangChain Concepts
- [Agents](https://python.langchain.com/docs/modules/agents/)
- [Tools](https://python.langchain.com/docs/modules/agents/tools/)
- [Memory](https://python.langchain.com/docs/modules/memory/)
- [Callbacks](https://python.langchain.com/docs/modules/callbacks/)

### Community
- [LangChain Discord](https://discord.gg/langchain)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)

## 🎯 Next Steps

After completing this course, you can:

1. **Build Custom Agents**
   - Create agents for specific domains
   - Add custom tools for your use case
   - Integrate with your applications

2. **Explore Advanced Topics**
   - Long-term memory with vector stores
   - Multi-agent systems
   - Agent planning and reflection
   - Custom agent types

3. **Production Deployment**
   - Add logging and monitoring
   - Implement rate limiting
   - Add authentication
   - Deploy to AWS Lambda or ECS

4. **Integrate with Other Services**
   - Connect to databases
   - Call external APIs
   - Process files and documents
   - Build web interfaces

## 💡 Tips for Success

1. **Run each example**: Don't just read, execute the code
2. **Experiment**: Modify parameters and see what happens
3. **Read the output**: Understand the agent's reasoning
4. **Start simple**: Master basics before advanced topics
5. **Build projects**: Apply concepts to real problems

## 📝 Practice Exercises

After completing the modules, try these:

1. **Personal Assistant Agent**
   - Tools: Calendar, reminders, notes
   - Memory: Remember user preferences

2. **Data Analysis Agent**
   - Tools: CSV reader, statistics, visualization
   - Dynamic model: Adjust based on data size

3. **Research Agent**
   - Tools: Web search, summarization
   - Streaming: Show progress during research

4. **Code Helper Agent**
   - Tools: Code execution, linting, documentation
   - Memory: Remember project context

## 🤝 Contributing

Found an issue or have suggestions? Feel free to:
- Report bugs
- Suggest improvements
- Share your agent implementations

## 📄 License

This course is provided as educational material. Use freely for learning and development.

---

**Happy Learning! 🚀**

Start with `01-setup-and-basic-agent.py` and work your way through each module. By the end, you'll be building sophisticated AI agents with confidence!
