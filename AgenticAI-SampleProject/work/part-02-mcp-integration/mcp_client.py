#!/usr/bin/env python3
"""
MCP Client for connecting to MCP servers
"""

import asyncio
import subprocess
import json
from typing import Dict, Any, List
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    """Client for communicating with MCP servers"""
    
    def __init__(self):
        self.sessions = {}
    
    async def connect_server(self, server_name: str, server_path: str):
        """Connect to an MCP server"""
        try:
            server_params = StdioServerParameters(
                command="python",
                args=[server_path]
            )
            
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    self.sessions[server_name] = session
                    return True
        except Exception as e:
            print(f"Failed to connect to {server_name}: {e}")
            return False
    
    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on a specific MCP server"""
        if server_name not in self.sessions:
            return {"error": f"Server {server_name} not connected"}
        
        try:
            session = self.sessions[server_name]
            result = await session.call_tool(tool_name, arguments)
            
            if result.content:
                # Extract text content from MCP response
                text_content = ""
                for content in result.content:
                    if hasattr(content, 'text'):
                        text_content += content.text
                
                # Try to parse as JSON, fallback to string
                try:
                    return json.loads(text_content)
                except json.JSONDecodeError:
                    return {"result": text_content}
            
            return {"result": "No content returned"}
            
        except Exception as e:
            return {"error": str(e)}
    
    async def list_tools(self, server_name: str) -> List[Dict[str, Any]]:
        """List available tools on a server"""
        if server_name not in self.sessions:
            return []
        
        try:
            session = self.sessions[server_name]
            tools = await session.list_tools()
            return [{"name": tool.name, "description": tool.description} for tool in tools.tools]
        except Exception as e:
            print(f"Failed to list tools for {server_name}: {e}")
            return []

class SimpleMCPClient:
    """Simplified MCP client using subprocess for direct server communication"""
    
    def __init__(self):
        self.server_processes = {}
    
    async def call_tool_subprocess(self, server_path: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call MCP tool using subprocess communication"""
        try:
            # Create MCP request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            # Start server process
            process = await asyncio.create_subprocess_exec(
                "python", server_path,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Send initialization
            init_request = {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "enhanced-agent", "version": "1.0.0"}
                }
            }
            
            init_json = json.dumps(init_request) + "\n"
            process.stdin.write(init_json.encode())
            await process.stdin.drain()
            
            # Read initialization response
            init_response = await process.stdout.readline()
            
            # Send tool call request
            request_json = json.dumps(request) + "\n"
            process.stdin.write(request_json.encode())
            await process.stdin.drain()
            
            # Read response
            response_line = await process.stdout.readline()
            process.stdin.close()
            await process.wait()
            
            if response_line:
                response = json.loads(response_line.decode().strip())
                if "result" in response:
                    # Extract content from MCP response
                    result = response["result"]
                    if "content" in result and result["content"]:
                        content_text = result["content"][0].get("text", "")
                        try:
                            return json.loads(content_text)
                        except json.JSONDecodeError:
                            return {"result": content_text}
                    return result
                elif "error" in response:
                    return {"error": response["error"]}
            
            return {"error": "No response from server"}
            
        except Exception as e:
            return {"error": str(e)}

# Global MCP client instance
mcp_client = SimpleMCPClient()

async def call_cement_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """Call cement server tool"""
    server_path = "/home/ramakrishna/Code/GenAI-for-Dev-Course/AgenticAI-SampleProject/work/part-02-mcp-integration/fastmcp_servers/cement_server.py"
    return await mcp_client.call_tool_subprocess(server_path, tool_name, kwargs)

async def call_steel_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """Call steel server tool"""
    server_path = "/home/ramakrishna/Code/GenAI-for-Dev-Course/AgenticAI-SampleProject/work/part-02-mcp-integration/fastmcp_servers/steel_server.py"
    return await mcp_client.call_tool_subprocess(server_path, tool_name, kwargs)

async def call_construction_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """Call construction server tool"""
    server_path = "/home/ramakrishna/Code/GenAI-for-Dev-Course/AgenticAI-SampleProject/work/part-02-mcp-integration/fastmcp_servers/construction_server.py"
    return await mcp_client.call_tool_subprocess(server_path, tool_name, kwargs)