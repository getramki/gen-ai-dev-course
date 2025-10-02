# StrandsAgents QuickStart Guide

## Overview
StrandsAgents is a framework for building AI agents that can interact with various tools and services. This guide will help you get started quickly.

## Installation

### Prerequisites
- Python 3.8+
- pip or uv package manager

### Install StrandsAgents
```bash
pip install strands-agents
```

### Install those development packages:
```bash
pip install strands-agents-tools strands-agents-builder
```
## Project Setup

## Basic Usage

### 1. Create Your First Agent

```python
from strandsagents import Agent, Tool

# Define a simple tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"

# Create a tool
calc_tool = Tool(
    name="calculator",
    description="Perform mathematical calculations",
    function=calculator
)

# Create an agent
agent = Agent(
    name="MathAgent",
    description="An agent that can perform calculations",
    tools=[calc_tool]
)

# Use the agent
response = agent.run("What is 15 + 27?")
print(response)
```

### 2. Agent with Multiple Tools

```python
from strandsagents import Agent, Tool
import requests

def web_search(query: str) -> str:
    """Search the web for information"""
    # Simplified example - replace with actual search API
    return f"Search results for: {query}"

def weather_check(city: str) -> str:
    """Get weather information for a city"""
    # Simplified example - replace with actual weather API
    return f"Weather in {city}: Sunny, 25°C"

# Create tools
search_tool = Tool(name="web_search", description="Search the web", function=web_search)
weather_tool = Tool(name="weather", description="Get weather info", function=weather_check)

# Create multi-tool agent
agent = Agent(
    name="AssistantAgent",
    description="A helpful assistant with web search and weather capabilities",
    tools=[search_tool, weather_tool]
)

# Use the agent
response = agent.run("What's the weather like in New York?")
print(response)
```

### 3. Configuration Options

```python
from strandsagents import Agent, Config

# Configure agent behavior
config = Config(
    max_iterations=10,
    temperature=0.7,
    model="gpt-4",
    timeout=30
)

agent = Agent(
    name="ConfiguredAgent",
    description="An agent with custom configuration",
    config=config
)
```

## Key Concepts

### Tools
- **Function-based**: Wrap Python functions as tools
- **Class-based**: Create tool classes for complex functionality
- **Built-in tools**: Use pre-built tools for common tasks

### Agents
- **Single-purpose**: Agents focused on specific tasks
- **Multi-tool**: Agents that can use multiple tools
- **Conversational**: Agents that maintain conversation context

### Workflows
- **Sequential**: Execute tools in order
- **Conditional**: Branch based on results
- **Parallel**: Execute multiple tools simultaneously

## Common Patterns

### Error Handling
```python
try:
    response = agent.run("Your query here")
    print(response)
except Exception as e:
    print(f"Agent error: {e}")
```

### Async Operations
```python
import asyncio
from strandsagents import AsyncAgent

async def main():
    agent = AsyncAgent(name="AsyncAgent")
    response = await agent.run_async("Your query here")
    print(response)

asyncio.run(main())
```

### Tool Chaining
```python
# Tools can call other tools automatically
agent = Agent(
    name="ChainAgent",
    tools=[tool1, tool2, tool3],
    allow_tool_chaining=True
)
```

## Next Steps

1. **Explore Examples**: Check the `examples/` directory for more complex use cases
2. **Read Documentation**: Visit the full documentation for advanced features
3. **Build Custom Tools**: Create tools specific to your use case
4. **Deploy Agents**: Learn about deployment options and scaling

## Resources

- [Full Documentation](https://strandsagents.com/0.1.x/documentation/)
- [API Reference](https://strandsagents.com/0.1.x/api/)
- [Examples Repository](https://github.com/strandsagents/examples)
- [Community Forum](https://community.strandsagents.com)

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure StrandsAgents is properly installed
2. **Tool Not Found**: Check tool registration and naming
3. **Timeout Issues**: Adjust timeout settings in configuration
4. **Memory Issues**: Monitor agent memory usage for long conversations

### Getting Help

- Check the documentation first
- Search existing issues on GitHub
- Join the community forum
- Contact support for enterprise users