import json
from typing import List
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("test")

@mcp.tool()
def test_tool(message: str) -> str:
    """Simple test tool"""
    return f"Received: {message}"

if __name__ == "__main__":
    mcp.run(transport='stdio')