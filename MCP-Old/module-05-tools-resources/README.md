# Module 5: Tools and Resources in MCP

## Learning Objectives
- Understand MCP tools vs resources
- Implement complex tools with validation
- Create and manage MCP resources
- Handle different data types and formats
- Build a multi-tool MCP server

## MCP Tools Deep Dive

### Tool Characteristics
- **Executable**: Tools perform actions or computations
- **Parameterized**: Accept input parameters
- **Stateless**: Each call is independent
- **Typed**: Strong input/output typing

### Advanced Tool Implementation

```python
from mcp import Server
from typing import List, Dict, Optional, Union
from pydantic import BaseModel, validator
import asyncio

server = Server("advanced-tools-server")

class CalculationRequest(BaseModel):
    operation: str
    numbers: List[float]
    precision: Optional[int] = 2
    
    @validator('operation')
    def validate_operation(cls, v):
        allowed = ['add', 'subtract', 'multiply', 'divide', 'average']
        if v not in allowed:
            raise ValueError(f'Operation must be one of: {allowed}')
        return v

@server.tool()
async def advanced_calculator(request: CalculationRequest) -> Dict:
    """Advanced calculator with multiple operations"""
    try:
        numbers = request.numbers
        operation = request.operation
        
        if not numbers:
            raise ValueError("At least one number is required")
        
        if operation == 'add':
            result = sum(numbers)
        elif operation == 'subtract':
            result = numbers[0] - sum(numbers[1:])
        elif operation == 'multiply':
            result = 1
            for num in numbers:
                result *= num
        elif operation == 'divide':
            result = numbers[0]
            for num in numbers[1:]:
                if num == 0:
                    raise ValueError("Division by zero")
                result /= num
        elif operation == 'average':
            result = sum(numbers) / len(numbers)
        
        return {
            "operation": operation,
            "input": numbers,
            "result": round(result, request.precision),
            "count": len(numbers)
        }
        
    except Exception as e:
        raise ValueError(f"Calculation failed: {str(e)}")
```

## MCP Resources Deep Dive

### Resource Characteristics
- **Readable**: Provide data or content
- **Addressable**: Have unique URIs
- **Typed**: Specify MIME types
- **Cacheable**: Can be cached by clients

### Resource Implementation

```python
@server.resource("file://data/users.json")
async def users_database() -> Dict:
    """User database resource"""
    return {
        "uri": "file://data/users.json",
        "mimeType": "application/json",
        "content": {
            "users": [
                {"id": 1, "name": "Alice", "role": "admin"},
                {"id": 2, "name": "Bob", "role": "user"}
            ]
        }
    }

@server.resource("config://app-settings")
async def app_configuration() -> Dict:
    """Application configuration resource"""
    return {
        "uri": "config://app-settings",
        "mimeType": "application/json",
        "content": {
            "database_url": "postgresql://localhost:5432/app",
            "cache_ttl": 3600,
            "debug_mode": False,
            "api_version": "v1"
        }
    }
```

## Complete Multi-Tool Server Example

```python
from mcp import Server
import asyncio
import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = Server("multi-tool-server")

# Database setup
DB_PATH = "example.db"

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on server start
init_database()

# Task Management Tools
@server.tool()
async def create_task(title: str, description: Optional[str] = None) -> Dict:
    """Create a new task"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (title, description)
        )
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Created task: {title}")
        return {
            "id": task_id,
            "title": title,
            "description": description,
            "status": "pending",
            "message": "Task created successfully"
        }
        
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise ValueError(f"Failed to create task: {str(e)}")

@server.tool()
async def list_tasks(status: Optional[str] = None) -> List[Dict]:
    """List all tasks, optionally filtered by status"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if status:
            cursor.execute(
                "SELECT id, title, description, status, created_at FROM tasks WHERE status = ?",
                (status,)
            )
        else:
            cursor.execute(
                "SELECT id, title, description, status, created_at FROM tasks"
            )
        
        tasks = []
        for row in cursor.fetchall():
            tasks.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "status": row[3],
                "created_at": row[4]
            })
        
        conn.close()
        logger.info(f"Listed {len(tasks)} tasks")
        return tasks
        
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        raise ValueError(f"Failed to list tasks: {str(e)}")

@server.tool()
async def update_task_status(task_id: int, status: str) -> Dict:
    """Update task status"""
    try:
        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE tasks SET status = ? WHERE id = ?",
            (status, task_id)
        )
        
        if cursor.rowcount == 0:
            raise ValueError(f"Task with ID {task_id} not found")
        
        conn.commit()
        conn.close()
        
        logger.info(f"Updated task {task_id} status to {status}")
        return {
            "task_id": task_id,
            "new_status": status,
            "message": "Task status updated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        raise ValueError(f"Failed to update task: {str(e)}")

# Note Management Tools
@server.tool()
async def create_note(title: str, content: str, tags: Optional[str] = None) -> Dict:
    """Create a new note"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO notes (title, content, tags) VALUES (?, ?, ?)",
            (title, content, tags)
        )
        
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Created note: {title}")
        return {
            "id": note_id,
            "title": title,
            "content": content,
            "tags": tags,
            "message": "Note created successfully"
        }
        
    except Exception as e:
        logger.error(f"Error creating note: {e}")
        raise ValueError(f"Failed to create note: {str(e)}")

@server.tool()
async def search_notes(query: str) -> List[Dict]:
    """Search notes by title or content"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT id, title, content, tags, created_at FROM notes 
               WHERE title LIKE ? OR content LIKE ?""",
            (f"%{query}%", f"%{query}%")
        )
        
        notes = []
        for row in cursor.fetchall():
            notes.append({
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "tags": row[3],
                "created_at": row[4]
            })
        
        conn.close()
        logger.info(f"Found {len(notes)} notes matching '{query}'")
        return notes
        
    except Exception as e:
        logger.error(f"Error searching notes: {e}")
        raise ValueError(f"Failed to search notes: {str(e)}")

# Utility Tools
@server.tool()
async def get_statistics() -> Dict:
    """Get database statistics"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Count tasks by status
        cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
        task_stats = dict(cursor.fetchall())
        
        # Count total notes
        cursor.execute("SELECT COUNT(*) FROM notes")
        note_count = cursor.fetchone()[0]
        
        # Recent activity
        cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE created_at > datetime('now', '-7 days')"
        )
        recent_tasks = cursor.fetchone()[0]
        
        cursor.execute(
            "SELECT COUNT(*) FROM notes WHERE created_at > datetime('now', '-7 days')"
        )
        recent_notes = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "tasks": {
                "by_status": task_stats,
                "total": sum(task_stats.values()),
                "recent_week": recent_tasks
            },
            "notes": {
                "total": note_count,
                "recent_week": recent_notes
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise ValueError(f"Failed to get statistics: {str(e)}")

# Resources
@server.resource("database://tasks")
async def tasks_resource() -> Dict:
    """Tasks database resource"""
    tasks = await list_tasks()
    return {
        "uri": "database://tasks",
        "mimeType": "application/json",
        "content": {"tasks": tasks}
    }

@server.resource("database://notes")
async def notes_resource() -> Dict:
    """Notes database resource"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, tags, created_at FROM notes")
    
    notes = []
    for row in cursor.fetchall():
        notes.append({
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "tags": row[3],
            "created_at": row[4]
        })
    
    conn.close()
    
    return {
        "uri": "database://notes",
        "mimeType": "application/json",
        "content": {"notes": notes}
    }

async def main():
    """Run the multi-tool server"""
    logger.info("Starting Multi-Tool MCP Server...")
    
    print("🚀 Multi-Tool MCP Server is ready!")
    print(f"\nAvailable tools ({len(server.tools)}):")
    for tool in server.tools:
        print(f"  - {tool.name}: {tool.description}")
    
    print(f"\nAvailable resources ({len(server.resources)}):")
    for resource in server.resources:
        print(f"  - {resource.uri}")
    
    print("\nExample usage:")
    print("  await create_task('Learn MCP', 'Complete the MCP course')")
    print("  await create_note('MCP Notes', 'Key concepts and examples')")
    print("  await get_statistics()")
    
    # Keep server running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Multi-tool server stopped!")

if __name__ == "__main__":
    asyncio.run(main())
```

## Best Practices

### Tool Design
1. **Single Responsibility**: Each tool should do one thing well
2. **Clear Naming**: Use descriptive, action-oriented names
3. **Input Validation**: Always validate and sanitize inputs
4. **Error Handling**: Provide meaningful error messages
5. **Documentation**: Write clear descriptions and examples

### Resource Design
1. **Unique URIs**: Use clear, hierarchical URI schemes
2. **Appropriate MIME Types**: Specify correct content types
3. **Efficient Loading**: Avoid loading large resources unnecessarily
4. **Caching Strategy**: Consider how resources will be cached
5. **Access Control**: Implement appropriate security measures

### Performance Considerations
1. **Async Operations**: Use async/await for I/O operations
2. **Connection Pooling**: Reuse database connections
3. **Lazy Loading**: Load resources only when needed
4. **Timeout Handling**: Implement appropriate timeouts
5. **Memory Management**: Be mindful of memory usage

## Next Steps

In Module 6, we'll explore MCP prompts and templates for creating reusable AI interactions.

## Quick Reference

```python
# Tool with validation
@server.tool()
async def my_tool(param: Type) -> ReturnType:
    # Validate input
    # Perform operation
    # Return result

# Resource
@server.resource("scheme://path")
async def my_resource() -> Dict:
    return {
        "uri": "scheme://path",
        "mimeType": "content/type",
        "content": data
    }
```