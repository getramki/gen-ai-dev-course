import pytest
import asyncio
import tempfile
import os
from filesystem_server import read_file, write_file

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
        # Print the content for debugging
        print(f"Content read: {content}")
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
        # Print the result for debugging
        print(f"Write result: {result}")

        # Verify content
        with open(temp_path, 'r') as f:
            assert f.read() == "Test content"
            # Print the content for debugging
            print(f"Content written: {f.read()}")
    finally:
        os.unlink(temp_path)