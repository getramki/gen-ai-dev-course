import asyncio
import logging
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AddNumbersArgs(BaseModel):
    a: float
    b: float

class GreetArgs(BaseModel):
    name: str

async def test_basic_mcp_server():
    """Test basic MCP server functionality"""
    
    # Create MCP server
    server = Server("test-server")
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="add_numbers",
                description="Add two numbers together",
                inputSchema=AddNumbersArgs.model_json_schema()
            ),
            Tool(
                name="greet",
                description="Greet someone by name",
                inputSchema=GreetArgs.model_json_schema()
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name == "add_numbers":
            args = AddNumbersArgs(**arguments)
            result = args.a + args.b
            return [TextContent(type="text", text=str(result))]
        elif name == "greet":
            args = GreetArgs(**arguments)
            result = f"Hello, {args.name}! Welcome to MCP."
            return [TextContent(type="text", text=result)]
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    # Test server setup
    print("✅ MCP Server created successfully!")
    print(f"Server name: test-server")
    
    # Test tool listing
    tools = await list_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    # Test tool execution
    try:
        result1 = await call_tool("add_numbers", {"a": 5, "b": 3})
        print(f"✅ add_numbers(5, 3) = {result1[0].text}")
        
        result2 = await call_tool("greet", {"name": "Developer"})
        print(f"✅ greet('Developer') = {result2[0].text}")
        
        return True
    except Exception as e:
        print(f"❌ Tool execution failed: {e}")
        return False

async def main():
    print("Testing Basic MCP Setup...")
    print("-" * 40)
    
    success = await test_basic_mcp_server()
    
    if success:
        print("\n✅ All MCP tests passed!")
    else:
        print("\n❌ Some MCP tests failed!")

if __name__ == "__main__":
    asyncio.run(main())