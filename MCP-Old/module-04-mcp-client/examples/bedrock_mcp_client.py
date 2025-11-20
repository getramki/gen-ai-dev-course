import boto3
import json
from mcp import Client
import asyncio
from typing import Dict, List, Any, Optional
import logging
import re
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BedrockMCPClient:
    """MCP Client integrated with Amazon Bedrock models"""
    
    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.getenv('AWS_REGION', 'us-east-1')
        self.bedrock = boto3.client('bedrock-runtime', region_name=self.region_name)
        self.mcp_client = None
        self.available_tools = []
        self.conversation_history = []
        self.default_model = os.getenv('BEDROCK_CLAUDE_HAIKU', 'anthropic.claude-3-haiku-20240307-v1:0')
    
    async def connect_to_server(self, server_url: str) -> bool:
        """Connect to MCP server and discover available tools"""
        try:
            self.mcp_client = Client(server_url)
            await self.mcp_client.connect()
            self.available_tools = await self.mcp_client.list_tools()
            logger.info(f"✅ Connected to MCP server with {len(self.available_tools)} tools")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to MCP server: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from MCP server"""
        if self.mcp_client:
            await self.mcp_client.disconnect()
            logger.info("Disconnected from MCP server")
    
    async def call_bedrock(
        self, 
        prompt: str, 
        model_id: str = None,
        max_tokens: int = 1000,
        include_history: bool = True
    ) -> str:
        """Call Amazon Bedrock model with optional conversation history"""
        try:
            model_id = model_id or self.default_model
            
            # Prepare messages
            messages = []
            if include_history:
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
            
            # Update conversation history if using history
            if include_history:
                self.conversation_history.append({"role": "user", "content": prompt})
                self.conversation_history.append({"role": "assistant", "content": assistant_response})
                
                # Keep history manageable (last 10 exchanges)
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]
            
            return assistant_response
            
        except Exception as e:
            logger.error(f"Bedrock call failed: {e}")
            raise Exception(f"Bedrock call failed: {str(e)}")
    
    async def execute_tool(self, tool_name: str, parameters: Dict) -> Any:
        """Execute MCP tool with error handling"""
        try:
            if not self.mcp_client:
                raise Exception("Not connected to MCP server")
            
            logger.info(f"Executing tool: {tool_name} with params: {parameters}")
            result = await self.mcp_client.call_tool(tool_name, parameters)
            logger.info(f"Tool executed successfully: {tool_name}")
            return result
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            raise Exception(f"Tool execution failed: {str(e)}")
    
    def get_tools_description(self) -> str:
        """Get formatted description of available tools for AI model"""
        if not self.available_tools:
            return "No MCP tools are currently available."
        
        descriptions = ["Available MCP tools that you can use:"]
        for tool in self.available_tools:
            desc = f"- **{tool['name']}**: {tool.get('description', 'No description available')}"
            
            # Add parameter information if available
            if 'inputSchema' in tool and 'properties' in tool['inputSchema']:
                params = []
                properties = tool['inputSchema']['properties']
                required = tool['inputSchema'].get('required', [])
                
                for param_name, param_info in properties.items():
                    param_desc = f"{param_name}"
                    if param_name in required:
                        param_desc += " (required)"
                    if 'type' in param_info:
                        param_desc += f": {param_info['type']}"
                    params.append(param_desc)
                
                if params:
                    desc += f"\n  Parameters: {', '.join(params)}"
            
            descriptions.append(desc)
        
        return "\n".join(descriptions)
    
    async def chat_with_tools(self, user_input: str, model_id: str = None) -> str:
        """Enhanced chat that can intelligently use MCP tools"""
        try:
            # Create system prompt with tool information
            tools_info = self.get_tools_description()
            system_prompt = f"""You are an AI assistant with access to MCP (Model Context Protocol) tools. 

{tools_info}

When a user request can be fulfilled using these tools:
1. Identify the appropriate tool(s)
2. Determine the required parameters from the user's request
3. Respond with a JSON object: {{"action": "use_tool", "tool": "tool_name", "parameters": {{"param1": "value1"}}}}

If no tools are needed or the request is conversational, respond normally.

User request: {user_input}"""
            
            # Get AI response
            ai_response = await self.call_bedrock(
                system_prompt, 
                model_id=model_id,
                include_history=False  # Don't include history for tool decision
            )
            
            # Check if AI wants to use a tool
            if self._is_tool_call(ai_response):
                return await self._handle_tool_call(ai_response, user_input)
            else:
                # Regular conversation - include history
                return await self.call_bedrock(user_input, model_id=model_id)
            
        except Exception as e:
            logger.error(f"Chat with tools failed: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def _is_tool_call(self, response: str) -> bool:
        """Check if the response contains a tool call"""
        return '"action": "use_tool"' in response or '"action":"use_tool"' in response
    
    async def _handle_tool_call(self, ai_response: str, original_request: str) -> str:
        """Handle tool call from AI response"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{[^{}]*"action"[^{}]*\}', ai_response, re.DOTALL)
            if not json_match:
                return "I wanted to use a tool but couldn't format the request properly."
            
            tool_call = json.loads(json_match.group())
            
            # Validate tool call structure
            if 'tool' not in tool_call or 'parameters' not in tool_call:
                return "I wanted to use a tool but the request format was invalid."
            
            # Execute the tool
            tool_result = await self.execute_tool(
                tool_call['tool'], 
                tool_call['parameters']
            )
            
            # Get AI to interpret the result
            interpretation_prompt = f"""The user asked: "{original_request}"

I used the MCP tool '{tool_call['tool']}' with parameters {tool_call['parameters']} and got this result:

{tool_result}

Please provide a helpful, natural response to the user based on this result. Don't mention the technical details of the tool call unless relevant."""
            
            final_response = await self.call_bedrock(
                interpretation_prompt,
                include_history=False
            )
            
            # Update conversation history with the final exchange
            self.conversation_history.append({"role": "user", "content": original_request})
            self.conversation_history.append({"role": "assistant", "content": final_response})
            
            return final_response
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse tool call JSON: {e}")
            return "I wanted to help with a tool but couldn't parse the request properly."
        except Exception as e:
            logger.error(f"Tool call handling failed: {e}")
            return f"I tried to use a tool to help, but encountered an error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation history"
        
        return f"Conversation has {len(self.conversation_history)//2} exchanges"

# Interactive demo function
async def interactive_demo():
    """Run an interactive demo of the Bedrock MCP Client"""
    client = BedrockMCPClient()
    
    print("🚀 Bedrock MCP Client Demo")
    print("=" * 50)
    
    # Try to connect to a local MCP server (you'll need to start one)
    server_url = input("Enter MCP server URL (or press Enter for default): ").strip()
    if not server_url:
        server_url = "stdio://python filesystem_server.py"  # Default
    
    print(f"Connecting to: {server_url}")
    connected = await client.connect_to_server(server_url)
    
    if not connected:
        print("❌ Could not connect to MCP server. Please ensure a server is running.")
        return
    
    print("\n🤖 Connected! Available commands:")
    print("- Type your questions or requests")
    print("- 'tools' - Show available tools")
    print("- 'clear' - Clear conversation history")
    print("- 'quit' - Exit")
    print("-" * 50)
    
    try:
        while True:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'clear':
                client.clear_history()
                print("🧹 Conversation history cleared!")
                continue
            elif user_input.lower() == 'tools':
                print("\n🔧 " + client.get_tools_description())
                continue
            elif not user_input:
                continue
            
            print("🤖 Assistant: ", end="", flush=True)
            try:
                response = await client.chat_with_tools(user_input)
                print(response)
            except Exception as e:
                print(f"Error: {str(e)}")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(interactive_demo())