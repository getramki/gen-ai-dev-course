# Module 4: Creating MCP Clients

## Learning Objectives
- Build MCP clients that connect to servers
- Integrate Amazon Bedrock models with MCP
- Handle client-server communication
- Create interactive AI applications
- Implement error handling and retries

## MCP Client Fundamentals

### Client Architecture
```
┌─────────────────┐    MCP Protocol    ┌─────────────────┐
│   MCP Client    │◄──────────────────►│   MCP Server    │
│                 │                    │                 │
│ ┌─────────────┐ │                    │ ┌─────────────┐ │
│ │   Bedrock   │ │                    │ │    Tools    │ │
│ │   Models    │ │                    │ │ Resources   │ │
│ │             │ │                    │ │  Prompts    │ │
│ └─────────────┘ │                    │ └─────────────┘ │
└─────────────────┘                    └─────────────────┘
```

### Basic Client Structure
```python
from mcp import Client
import asyncio

async def main():
    # Connect to MCP server
    client = Client("server-url")
    await client.connect()
    
    # Discover available tools
    tools = await client.list_tools()
    
    # Call a tool
    result = await client.call_tool("tool_name", {"param": "value"})
    
    await client.disconnect()

asyncio.run(main())
```

## Building a Bedrock-Integrated MCP Client

### Step 1: Basic Client Setup
```python
import boto3
import json
from mcp import Client
import asyncio
from typing import Dict, List, Any

class BedrockMCPClient:
    def __init__(self, region_name: str = "us-east-1"):
        self.bedrock = boto3.client('bedrock-runtime', region_name=region_name)
        self.mcp_client = None
        self.available_tools = []
    
    async def connect_to_server(self, server_url: str):
        """Connect to MCP server"""
        self.mcp_client = Client(server_url)
        await self.mcp_client.connect()
        self.available_tools = await self.mcp_client.list_tools()
        print(f"Connected to MCP server with {len(self.available_tools)} tools")
```

### Step 2: Bedrock Integration
```python
async def call_bedrock(self, prompt: str, model_id: str = "anthropic.claude-3-haiku-20240307-v1:0") -> str:
    """Call Amazon Bedrock model"""
    try:
        body = json.dumps({
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "anthropic_version": "bedrock-2023-05-31"
        })
        
        response = self.bedrock.invoke_model(
            modelId=model_id,
            body=body
        )
        
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
        
    except Exception as e:
        raise Exception(f"Bedrock call failed: {str(e)}")
```

### Step 3: Tool Integration
```python
async def execute_tool(self, tool_name: str, parameters: Dict) -> Any:
    """Execute MCP tool"""
    try:
        if not self.mcp_client:
            raise Exception("Not connected to MCP server")
        
        result = await self.mcp_client.call_tool(tool_name, parameters)
        return result
        
    except Exception as e:
        raise Exception(f"Tool execution failed: {str(e)}")

async def get_available_tools_description(self) -> str:
    """Get formatted description of available tools"""
    if not self.available_tools:
        return "No tools available"
    
    descriptions = []
    for tool in self.available_tools:
        desc = f"- {tool['name']}: {tool.get('description', 'No description')}"
        descriptions.append(desc)
    
    return "\n".join(descriptions)
```

## Complete Bedrock MCP Client

```python
import boto3
import json
from mcp import Client
import asyncio
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BedrockMCPClient:
    def __init__(self, region_name: str = "us-east-1"):
        self.bedrock = boto3.client('bedrock-runtime', region_name=region_name)
        self.mcp_client = None
        self.available_tools = []
        self.conversation_history = []
    
    async def connect_to_server(self, server_url: str):
        """Connect to MCP server and discover tools"""
        try:
            self.mcp_client = Client(server_url)
            await self.mcp_client.connect()
            self.available_tools = await self.mcp_client.list_tools()
            logger.info(f"Connected to MCP server with {len(self.available_tools)} tools")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from MCP server"""
        if self.mcp_client:
            await self.mcp_client.disconnect()
            logger.info("Disconnected from MCP server")
    
    async def call_bedrock(
        self, 
        prompt: str, 
        model_id: str = "anthropic.claude-3-haiku-20240307-v1:0",
        max_tokens: int = 1000
    ) -> str:
        """Call Amazon Bedrock model"""
        try:
            # Prepare messages with conversation history
            messages = self.conversation_history.copy()
            messages.append({"role": "user", "content": prompt})
            
            body = json.dumps({
                "messages": messages,
                "max_tokens": max_tokens,
                "anthropic_version": "bedrock-2023-05-31"
            })
            
            response = self.bedrock.invoke_model(
                modelId=model_id,
                body=body
            )
            
            result = json.loads(response['body'].read())
            assistant_response = result['content'][0]['text']
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return assistant_response
            
        except Exception as e:
            logger.error(f"Bedrock call failed: {e}")
            raise Exception(f"Bedrock call failed: {str(e)}")
    
    async def execute_tool(self, tool_name: str, parameters: Dict) -> Any:
        """Execute MCP tool"""
        try:
            if not self.mcp_client:
                raise Exception("Not connected to MCP server")
            
            logger.info(f"Executing tool: {tool_name} with params: {parameters}")
            result = await self.mcp_client.call_tool(tool_name, parameters)
            logger.info(f"Tool result: {str(result)[:100]}...")
            return result
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            raise Exception(f"Tool execution failed: {str(e)}")
    
    def get_tools_description(self) -> str:
        """Get formatted description of available tools for AI model"""
        if not self.available_tools:
            return "No tools available"
        
        descriptions = ["Available MCP tools:"]
        for tool in self.available_tools:
            desc = f"- {tool['name']}: {tool.get('description', 'No description')}"
            if 'inputSchema' in tool:
                schema = tool['inputSchema']
                if 'properties' in schema:
                    params = list(schema['properties'].keys())
                    desc += f" (Parameters: {', '.join(params)})"
            descriptions.append(desc)
        
        return "\n".join(descriptions)
    
    async def chat_with_tools(self, user_input: str) -> str:
        """Enhanced chat that can use MCP tools"""
        try:
            # Create enhanced prompt with tool information
            tools_info = self.get_tools_description()
            enhanced_prompt = f"""
{tools_info}

User request: {user_input}

If the user's request can be fulfilled using any of the available MCP tools, please:
1. Identify which tool(s) to use
2. Determine the required parameters
3. Respond with a JSON object in this format:
{{"action": "use_tool", "tool": "tool_name", "parameters": {{"param1": "value1"}}}}

If no tools are needed, respond normally with helpful information.
"""
            
            # Get AI response
            ai_response = await self.call_bedrock(enhanced_prompt)
            
            # Check if AI wants to use a tool
            if '"action": "use_tool"' in ai_response:
                try:
                    # Extract tool call from response
                    import re
                    json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
                    if json_match:
                        tool_call = json.loads(json_match.group())
                        
                        # Execute the tool
                        tool_result = await self.execute_tool(
                            tool_call['tool'], 
                            tool_call['parameters']
                        )
                        
                        # Get AI to interpret the result
                        interpretation_prompt = f"""
The user asked: {user_input}

I used the tool '{tool_call['tool']}' and got this result:
{tool_result}

Please provide a helpful response to the user based on this result.
"""
                        final_response = await self.call_bedrock(interpretation_prompt)
                        return final_response
                        
                except (json.JSONDecodeError, KeyError) as e:
                    logger.error(f"Failed to parse tool call: {e}")
                    return ai_response
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Chat with tools failed: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

# Example usage
async def main():
    client = BedrockMCPClient()
    
    # Connect to MCP server (replace with actual server URL)
    server_connected = await client.connect_to_server("stdio://filesystem-server")
    
    if not server_connected:
        print("Failed to connect to MCP server")
        return
    
    try:
        # Interactive chat loop
        print("🤖 Bedrock MCP Client Ready!")
        print("Type 'quit' to exit, 'clear' to clear history")
        print("-" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'clear':
                client.clear_history()
                print("History cleared!")
                continue
            elif not user_input:
                continue
            
            print("🤖 Assistant: ", end="")
            response = await client.chat_with_tools(user_input)
            print(response)
    
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## Simple Interactive Client

For testing and learning, here's a simpler client:

```python
import asyncio
from mcp import Client

class SimpleMCPClient:
    def __init__(self):
        self.client = None
        self.tools = []
    
    async def connect(self, server_url: str):
        """Connect to MCP server"""
        self.client = Client(server_url)
        await self.client.connect()
        self.tools = await self.client.list_tools()
        print(f"Connected! Available tools: {[t['name'] for t in self.tools]}")
    
    async def call_tool(self, tool_name: str, **kwargs):
        """Call a tool with parameters"""
        try:
            result = await self.client.call_tool(tool_name, kwargs)
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def interactive_session(self):
        """Run interactive session"""
        print("Available tools:")
        for tool in self.tools:
            print(f"  - {tool['name']}: {tool.get('description', 'No description')}")
        
        while True:
            print("\nEnter command (tool_name param1=value1 param2=value2) or 'quit':")
            command = input("> ").strip()
            
            if command.lower() == 'quit':
                break
            
            # Parse command
            parts = command.split()
            if not parts:
                continue
            
            tool_name = parts[0]
            params = {}
            
            for part in parts[1:]:
                if '=' in part:
                    key, value = part.split('=', 1)
                    params[key] = value
            
            # Execute tool
            result = await self.call_tool(tool_name, **params)
            print(f"Result: {result}")
    
    async def disconnect(self):
        """Disconnect from server"""
        if self.client:
            await self.client.disconnect()

# Usage example
async def demo():
    client = SimpleMCPClient()
    await client.connect("stdio://filesystem-server")
    await client.interactive_session()
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(demo())
```

## Best Practices

### 1. Connection Management
- Always handle connection failures gracefully
- Implement reconnection logic for production use
- Clean up connections properly

### 2. Error Handling
- Wrap tool calls in try-catch blocks
- Provide meaningful error messages to users
- Log errors for debugging

### 3. Performance
- Use connection pooling for multiple servers
- Implement caching for frequently used data
- Handle timeouts appropriately

### 4. Security
- Validate all inputs before sending to tools
- Implement authentication if required
- Use secure connection protocols

## Next Steps

In Module 5, we'll explore advanced MCP features including tools, resources, and prompts in detail.

## Quick Reference

```python
# Basic client pattern
client = BedrockMCPClient()
await client.connect_to_server("server-url")
response = await client.chat_with_tools("user input")
await client.disconnect()
```