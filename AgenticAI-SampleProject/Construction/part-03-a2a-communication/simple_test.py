"""Simple test to verify A2A agents are working with basic JSON-RPC."""

import asyncio
import httpx
import json

async def test_basic_jsonrpc(name: str, url: str, message: str):
    """Test basic JSON-RPC communication."""
    print(f"\n=== Testing {name} ===")
    
    payload = {
        "jsonrpc": "2.0",
        "method": "agent.execute",
        "params": {
            "message": {
                "content": [{"type": "text", "text": message}],
                "role": "user"
            }
        },
        "id": 1
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
                return True
            else:
                print(f"Error: {response.text}")
                return False
                
    except Exception as e:
        print(f"Error: {e}")
        return False

async def main():
    """Test all agents with simple JSON-RPC."""
    agents = [
        ("Purchase Agent", "http://localhost:10001", "Hello"),
        ("Cement Agent", "http://localhost:10002", "Hello"),
        ("Steel Agent", "http://localhost:10003", "Hello")
    ]
    
    print("Simple A2A JSON-RPC Test")
    print("=" * 40)
    
    for name, url, message in agents:
        await test_basic_jsonrpc(name, url, message)

if __name__ == "__main__":
    asyncio.run(main())