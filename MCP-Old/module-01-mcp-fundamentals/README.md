# Module 1: MCP Architecture & Fundamentals

## Learning Objectives
- Understand what Model Context Protocol (MCP) is
- Learn MCP architecture components
- Explore client-server communication patterns
- Understand MCP message types and flow

## What is Model Context Protocol (MCP)?

Model Context Protocol (MCP) is an open standard that enables AI applications to securely connect to external data sources and tools. It provides a standardized way for AI models to access and interact with various resources.

### Key Benefits
- **Standardized Integration**: Consistent way to connect AI models with external systems
- **Security**: Controlled access to resources with proper authentication
- **Extensibility**: Easy to add new tools and data sources
- **Interoperability**: Works across different AI platforms and models

## MCP Architecture

```
┌─────────────────┐    MCP Protocol    ┌─────────────────┐
│   MCP Client    │◄──────────────────►│   MCP Server    │
│  (AI App/Tool)  │                    │ (Data/Tools)    │
└─────────────────┘                    └─────────────────┘
```

### Core Components

1. **MCP Client**: The AI application that needs access to external resources
2. **MCP Server**: Provides access to specific tools, data sources, or capabilities
3. **MCP Protocol**: Standardized communication protocol between client and server

### Communication Flow

1. **Initialization**: Client connects to server and exchanges capabilities
2. **Discovery**: Client discovers available tools and resources
3. **Execution**: Client requests tool execution or resource access
4. **Response**: Server processes request and returns results

## MCP Message Types

### 1. Tools
Functions that the server can execute on behalf of the client.

```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": {"type": "string"}
    }
  }
}
```

### 2. Resources
Data or content that the server can provide to the client.

```json
{
  "uri": "file://data/users.json",
  "name": "User Database",
  "mimeType": "application/json"
}
```

### 3. Prompts
Pre-defined prompt templates that can be used by the client.

```json
{
  "name": "summarize_document",
  "description": "Summarize a document",
  "arguments": [
    {"name": "document", "description": "Document to summarize"}
  ]
}
```

## MCP with Amazon Bedrock

Amazon Bedrock provides foundation models that can be integrated with MCP:

- **Claude 3.5 Sonnet**: Advanced reasoning and code generation
- **Claude 3 Haiku**: Fast, lightweight responses
- **Titan Text**: AWS native text generation
- **Llama 2**: Open-source alternative

### Integration Benefits
- Managed infrastructure
- Multiple model options
- Built-in security
- Pay-per-use pricing

## Hands-On Example

Let's look at a simple MCP server structure:

```python
from mcp import Server
import asyncio

# Create MCP server
server = Server("example-server")

# Define a tool
@server.tool()
async def calculate(operation: str, a: float, b: float) -> float:
    """Perform basic calculations"""
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b
    else:
        raise ValueError("Unsupported operation")

# Run server
if __name__ == "__main__":
    asyncio.run(server.run())
```

## Key Concepts Summary

- **MCP** enables secure AI-to-external-system communication
- **Client-Server** architecture with standardized protocol
- **Tools, Resources, Prompts** are the main interaction types
- **Amazon Bedrock** provides powerful foundation models for MCP clients
- **Async/Await** patterns are used for non-blocking operations

## Next Steps

In Module 2, we'll set up the development environment and configure Amazon Bedrock integration for our MCP applications.

## Quick Quiz
1. What are the three main components of MCP architecture?
2. Name the three types of MCP interactions.
3. What are the benefits of using MCP with Amazon Bedrock?

**Answers**: 1) Client, Server, Protocol 2) Tools, Resources, Prompts 3) Managed infrastructure, multiple models, security, pay-per-use