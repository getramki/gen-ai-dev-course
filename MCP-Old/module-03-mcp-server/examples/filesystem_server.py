import os
import json
from pathlib import Path
import asyncio
import logging
from typing import Optional, List, Dict, Any
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server
server = Server("filesystem-server")

async def read_file(file_path: str) -> str:
    """Read and return the contents of a file"""
    try:
        path = Path(file_path)
        if not path.exists():
            raise ValueError(f"File not found: {file_path}")
        
        # Security check - prevent directory traversal
        if ".." in file_path:
            raise ValueError("Directory traversal not allowed")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info(f"Read file: {file_path} ({len(content)} chars)")
        return content
        
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        raise ValueError(f"Failed to read file: {str(e)}")

async def write_file(file_path: str, content: str) -> str:
    """Write content to a file"""
    try:
        path = Path(file_path)
        
        # Security check
        if ".." in file_path:
            raise ValueError("Directory traversal not allowed")
        
        # Create parent directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Wrote file: {file_path} ({len(content)} chars)")
        return f"Successfully wrote {len(content)} characters to {file_path}"
        
    except Exception as e:
        logger.error(f"Error writing {file_path}: {e}")
        raise ValueError(f"Failed to write file: {str(e)}")

async def list_directory(dir_path: str) -> List[Dict]:
    """List contents of a directory with details"""
    try:
        path = Path(dir_path)
        
        # Security check
        if ".." in dir_path:
            raise ValueError("Directory traversal not allowed")
        
        if not path.exists():
            raise ValueError(f"Directory not found: {dir_path}")
        
        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {dir_path}")
        
        items = []
        for item in sorted(path.iterdir()):
            item_info = {
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "path": str(item.relative_to(path))
            }
            
            if item.is_file():
                item_info["size"] = item.stat().st_size
                item_info["extension"] = item.suffix
            
            items.append(item_info)
        
        logger.info(f"Listed directory: {dir_path} ({len(items)} items)")
        return items
        
    except Exception as e:
        logger.error(f"Error listing {dir_path}: {e}")
        raise ValueError(f"Failed to list directory: {str(e)}")

async def file_exists(file_path: str) -> bool:
    """Check if a file or directory exists"""
    try:
        # Security check
        if ".." in file_path:
            raise ValueError("Directory traversal not allowed")
        
        exists = Path(file_path).exists()
        logger.info(f"Checked existence: {file_path} = {exists}")
        return exists
        
    except Exception as e:
        logger.error(f"Error checking {file_path}: {e}")
        raise ValueError(f"Failed to check file existence: {str(e)}")

async def get_file_info(file_path: str) -> Dict:
    """Get detailed information about a file"""
    try:
        path = Path(file_path)
        
        # Security check
        if ".." in file_path:
            raise ValueError("Directory traversal not allowed")
        
        if not path.exists():
            raise ValueError(f"File not found: {file_path}")
        
        stat = path.stat()
        info = {
            "name": path.name,
            "path": str(path),
            "type": "directory" if path.is_dir() else "file",
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "permissions": oct(stat.st_mode)[-3:]
        }
        
        if path.is_file():
            info["extension"] = path.suffix
        
        logger.info(f"Got file info: {file_path}")
        return info
        
    except Exception as e:
        logger.error(f"Error getting info for {file_path}: {e}")
        raise ValueError(f"Failed to get file info: {str(e)}")

async def search_files(directory: str, pattern: str, case_sensitive: Optional[bool] = False) -> List[Dict]:
    """Search for files matching a pattern in a directory"""
    import fnmatch
    
    try:
        path = Path(directory)
        
        # Security check
        if ".." in directory:
            raise ValueError("Directory traversal not allowed")
        
        if not path.exists():
            raise ValueError(f"Directory not found: {directory}")
        
        matches = []
        for file_path in path.rglob("*"):
            if file_path.is_file():
                filename = file_path.name
                
                # Apply pattern matching
                if case_sensitive:
                    match = fnmatch.fnmatch(filename, pattern)
                else:
                    match = fnmatch.fnmatch(filename.lower(), pattern.lower())
                
                if match:
                    matches.append({
                        "name": filename,
                        "path": str(file_path.relative_to(path)),
                        "size": file_path.stat().st_size,
                        "extension": file_path.suffix
                    })
        
        logger.info(f"Found {len(matches)} files matching '{pattern}' in {directory}")
        return matches
        
    except Exception as e:
        logger.error(f"Error searching files: {e}")
        raise ValueError(f"Failed to search files: {str(e)}")

# Register tools with the server
@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="read_file",
            description="Read and return the contents of a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the file to read"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="write_file",
            description="Write content to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the file to write"},
                    "content": {"type": "string", "description": "Content to write to the file"}
                },
                "required": ["file_path", "content"]
            }
        ),
        Tool(
            name="list_directory",
            description="List contents of a directory with details",
            inputSchema={
                "type": "object",
                "properties": {
                    "dir_path": {"type": "string", "description": "Path to the directory to list"}
                },
                "required": ["dir_path"]
            }
        ),
        Tool(
            name="file_exists",
            description="Check if a file or directory exists",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to check"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="get_file_info",
            description="Get detailed information about a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the file"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="search_files",
            description="Search for files matching a pattern in a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Directory to search in"},
                    "pattern": {"type": "string", "description": "File pattern to match"},
                    "case_sensitive": {"type": "boolean", "description": "Whether search is case sensitive", "default": False}
                },
                "required": ["directory", "pattern"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    try:
        if name == "read_file":
            result = await read_file(arguments["file_path"])
        elif name == "write_file":
            result = await write_file(arguments["file_path"], arguments["content"])
        elif name == "list_directory":
            result = await list_directory(arguments["dir_path"])
        elif name == "file_exists":
            result = await file_exists(arguments["file_path"])
        elif name == "get_file_info":
            result = await get_file_info(arguments["file_path"])
        elif name == "search_files":
            result = await search_files(
                arguments["directory"], 
                arguments["pattern"], 
                arguments.get("case_sensitive", False)
            )
        else:
            raise ValueError(f"Unknown tool: {name}")
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    except Exception as e:
        logger.error(f"Error in {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting Filesystem MCP Server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())