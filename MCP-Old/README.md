# Model Context Protocol (MCP) Hands-On Course - 3 Days (6 Hours Total)

## Course Overview
This comprehensive hands-on course teaches Model Context Protocol (MCP) fundamentals through practical exercises using Amazon Bedrock models. Learn to build MCP clients and servers with real-world examples.

## Course Structure

### Day 1 (2 hours)
- **Module 1**: MCP Architecture & Fundamentals (30 min)
- **Module 2**: Setting up MCP Environment with Amazon Bedrock (45 min)
- **Module 3**: Building Your First MCP Server (45 min)

### Day 2 (2 hours)
- **Module 4**: Creating MCP Clients (30 min)
- **Module 5**: Tools and Resources in MCP (45 min)
- **Module 6**: Prompts and Templates (45 min)

### Day 3 (2 hours)
- **Module 7**: Advanced MCP Features (30 min)
- **Module 8**: Real-world MCP Applications (45 min)
- **Module 9**: Testing and Debugging MCP (30 min)
- **Module 10**: Deployment and Best Practices (15 min)

## Prerequisites
- Python 3.8+ knowledge
- AWS account with Bedrock access
- Basic understanding of APIs and JSON
- Command line familiarity

## Learning Objectives
By the end of this course, you will be able to:
- Understand MCP architecture and core concepts
- Build MCP servers with tools and resources
- Create MCP clients that interact with Amazon Bedrock
- Implement prompts and templates
- Handle real-world MCP scenarios
- Deploy and maintain MCP applications

## What You'll Build
- File system MCP server
- Weather data MCP server
- Database query MCP server
- Multi-tool MCP client
- Bedrock-integrated chat application

## Module Structure
Each module contains:
- `README.md` - Theory and concepts
- `exercises.md` - Hands-on exercises
- `examples/` - Python code examples
- `solutions/` - Exercise solutions

## Getting Started
1. Clone this repository
2. Install Python 3.8+
3. Configure AWS credentials
4. Install dependencies: `pip install -r requirements.txt`
5. Navigate to Module 1 to begin

## Course Navigation
- [Module 1 - MCP Architecture & Fundamentals](./module-01-mcp-fundamentals/)
- [Module 2 - Environment Setup with Bedrock](./module-02-environment-setup/)
- [Module 3 - Building MCP Server](./module-03-mcp-server/)
- [Module 4 - Creating MCP Clients](./module-04-mcp-client/)
- [Module 5 - Tools and Resources](./module-05-tools-resources/)
- [Module 6 - Prompts and Templates](./module-06-prompts-templates/)
- [Module 7 - Advanced MCP Features](./module-07-advanced-features/)
- [Module 8 - Real-world Applications](./module-08-real-world-apps/)
- [Module 9 - Testing and Debugging](./module-09-testing-debugging/)
- [Module 10 - Deployment and Best Practices](./module-10-deployment/)

## Quick Start Example
```python
# Simple MCP Server
from mcp import Server
import asyncio

server = Server("my-server")

@server.tool()
async def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    asyncio.run(server.run())
```

## Support
- Check module-specific README files for detailed instructions
- Review solutions/ directories for complete implementations
- Refer to AWS Bedrock documentation for model-specific details