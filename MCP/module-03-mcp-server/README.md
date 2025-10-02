# Module 3: Building Your First MCP Server

## Learning Objectives
- Create a functional MCP server from scratch
- Implement tools with proper schemas
- Handle different data types and validation
- Add error handling and logging
- Test server functionality

## MCP Server Fundamentals

### Server Structure
```python
from mcp import Server
import asyncio

# Create server instance
server = Server("my-server")

# Define tools using decorators
@server.tool()
async def my_tool(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"

# Run server
if __name__ == "__main__":
    asyncio.run(server.run())
```

### Key Components
1. **Server Instance**: Main server object
2. **Tools**: Functions exposed to clients
3. **Schemas**: Input/output validation
4. **Error Handling**: Graceful error management

## Building a File System MCP Server

Let's build a practical server that provides file system operations.

### Step 1: Basic Server Setup
```python
from mcp import Server
import os
import json
from pathlib import Path
import asyncio

server = Server("filesystem-server")
```

### Step 2: Implement File Operations

#### Read File Tool
```python
@server.tool()
async def read_file(file_path: str) -> str:
    """Read contents of a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")
```

#### List Directory Tool
```python
@server.tool()
async def list_directory(dir_path: str) -> list:
    """List contents of a directory"""
    try:
        path = Path(dir_path)
        if not path.exists():
            raise ValueError(f"Directory not found: {dir_path}")
        
        items = []
        for item in path.iterdir():
            items.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None
            })
        return items
    except Exception as e:
        raise ValueError(f"Error listing directory: {str(e)}")
```

#### Write File Tool
```python
@server.tool()
async def write_file(file_path: str, content: str) -> str:
    """Write content to a file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {file_path}"
    except Exception as e:
        raise ValueError(f"Error writing file: {str(e)}")
```

## Advanced Tool Features

### Type Validation
```python
from typing import Optional, List, Dict

@server.tool()
async def search_files(
    directory: str,
    pattern: str,
    case_sensitive: Optional[bool] = False
) -> List[Dict[str, str]]:
    """Search for files matching a pattern"""
    import glob
    import fnmatch
    
    try:
        path = Path(directory)
        if not path.exists():
            raise ValueError(f"Directory not found: {directory}")
        
        matches = []
        for file_path in path.rglob("*"):
            if file_path.is_file():
                filename = file_path.name
                if case_sensitive:
                    match = fnmatch.fnmatch(filename, pattern)
                else:
                    match = fnmatch.fnmatch(filename.lower(), pattern.lower())
                
                if match:
                    matches.append({
                        "path": str(file_path),
                        "name": filename,
                        "size": file_path.stat().st_size
                    })
        
        return matches
    except Exception as e:
        raise ValueError(f"Error searching files: {str(e)}")
```

### Error Handling Best Practices
```python
import logging

logger = logging.getLogger(__name__)

@server.tool()
async def safe_operation(input_data: str) -> str:
    """Example of proper error handling"""
    try:
        # Validate input
        if not input_data or not isinstance(input_data, str):
            raise ValueError("Input must be a non-empty string")
        
        # Log operation
        logger.info(f"Processing: {input_data[:50]}...")
        
        # Perform operation
        result = input_data.upper()
        
        # Log success
        logger.info("Operation completed successfully")
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise ValueError(f"Operation failed: {str(e)}")
```

## Complete File System Server Example

```python
from mcp import Server
import os
import json
from pathlib import Path
import asyncio
import logging
from typing import Optional, List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server
server = Server("filesystem-server")

@server.tool()
async def read_file(file_path: str) -> str:
    """Read and return the contents of a file"""
    try:
        path = Path(file_path)
        if not path.exists():
            raise ValueError(f"File not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info(f"Read file: {file_path} ({len(content)} chars)")
        return content
        
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        raise ValueError(f"Failed to read file: {str(e)}")

@server.tool()
async def write_file(file_path: str, content: str) -> str:
    """Write content to a file"""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Wrote file: {file_path} ({len(content)} chars)")
        return f"Successfully wrote {len(content)} characters to {file_path}"
        
    except Exception as e:
        logger.error(f"Error writing {file_path}: {e}")
        raise ValueError(f"Failed to write file: {str(e)}")

@server.tool()
async def list_directory(dir_path: str) -> List[Dict]:
    """List contents of a directory with details"""
    try:
        path = Path(dir_path)
        if not path.exists():
            raise ValueError(f"Directory not found: {dir_path}")
        
        items = []
        for item in sorted(path.iterdir()):
            item_info = {
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "path": str(item)
            }
            
            if item.is_file():
                item_info["size"] = item.stat().st_size
            
            items.append(item_info)
        
        logger.info(f"Listed directory: {dir_path} ({len(items)} items)")
        return items
        
    except Exception as e:
        logger.error(f"Error listing {dir_path}: {e}")
        raise ValueError(f"Failed to list directory: {str(e)}")

@server.tool()
async def file_exists(file_path: str) -> bool:
    """Check if a file or directory exists"""
    try:
        exists = Path(file_path).exists()
        logger.info(f"Checked existence: {file_path} = {exists}")
        return exists
    except Exception as e:
        logger.error(f"Error checking {file_path}: {e}")
        raise ValueError(f"Failed to check file existence: {str(e)}")

async def main():
    """Run the MCP server"""
    logger.info("Starting Filesystem MCP Server...")
    logger.info(f"Available tools: {[tool.name for tool in server.tools]}")
    
    # In a real implementation, this would start the server
    # For testing, we'll just show it's ready
    print("🚀 Filesystem MCP Server is ready!")
    print("Available tools:")
    for tool in server.tools:
        print(f"  - {tool.name}: {tool.description}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Testing Your Server

### Unit Tests
```python
import pytest
import asyncio
import tempfile
import os

@pytest.mark.asyncio
async def test_read_file():
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("Hello, World!")
        temp_path = f.name
    
    try:
        # Test reading
        content = await read_file(temp_path)
        assert content == "Hello, World!"
    finally:
        os.unlink(temp_path)

@pytest.mark.asyncio
async def test_write_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_path = f.name
    
    try:
        # Test writing
        result = await write_file(temp_path, "Test content")
        assert "Successfully wrote" in result
        
        # Verify content
        with open(temp_path, 'r') as f:
            assert f.read() == "Test content"
    finally:
        os.unlink(temp_path)
```

## Best Practices

### 1. Input Validation
- Always validate input parameters
- Use type hints for clarity
- Provide meaningful error messages

### 2. Error Handling
- Catch specific exceptions
- Log errors appropriately
- Return user-friendly error messages

### 3. Documentation
- Write clear tool descriptions
- Document parameters and return values
- Include usage examples

### 4. Security
- Validate file paths to prevent directory traversal
- Limit file operations to safe directories
- Sanitize user input

### 5. Performance
- Use async/await for I/O operations
- Implement timeouts for long operations
- Consider memory usage for large files

## Next Steps

In Module 4, we'll create MCP clients that can interact with our server and integrate with Amazon Bedrock models.

## Quick Reference

```python
# Basic server structure
server = Server("name")

@server.tool()
async def tool_name(param: type) -> return_type:
    """Description"""
    # Implementation
    return result

# Run server
asyncio.run(server.run())
```