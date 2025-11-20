"""Working demo client using A2A SDK with proper response handling."""

import asyncio
import logging
from uuid import uuid4
import httpx

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    MessageSendParams,
    SendMessageRequest,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_agent(name: str, base_url: str, test_message: str):
    """Test agent with A2A SDK."""
    print(f"\n{'='*60}")
    print(f"Testing {name} Agent")
    print(f"{'='*60}")
    
    async with httpx.AsyncClient(timeout=120.0) as httpx_client:
        try:
            # Get agent card
            resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
            agent_card = await resolver.get_agent_card()
            
            print(f"✅ Agent: {agent_card.name}")
            print(f"   Description: {agent_card.description}")
            
            # Create client
            client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)
            
            # Send message
            print(f"\n📤 Sending: {test_message}")
            
            request = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(
                    message={
                        'role': 'user',
                        'parts': [{'kind': 'text', 'text': test_message}],
                        'message_id': uuid4().hex,
                    }
                )
            )
            
            response = await client.send_message(request)
            
            print(f"📥 Response:")
            if response.root and response.root.result:
                result = response.root.result
                print(f"   Task ID: {result.id}")
                
                # Extract message from status string
                status_str = str(result.status)
                if "text='" in status_str:
                    start = status_str.find("text='") + 6
                    end = status_str.find("')", start)
                    if end > start:
                        content = status_str[start:end]
                        print(f"   Content: {content}")
                else:
                    print(f"   Status: {status_str[:100]}...")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

async def main():
    """Test construction agents with detailed messages."""
    agents = [
        {
            "name": "Purchase Agent",
            "url": "http://localhost:10001",
            "message": "I need 1000 tons of cement and 100 tons of steel within $130k budget for a construction project"
        },
        {
            "name": "Cement Agent", 
            "url": "http://localhost:10002",
            "message": "Quote 1000 tons of cement for construction project with delivery to downtown site"
        },
        {
            "name": "Steel Agent",
            "url": "http://localhost:10003", 
            "message": "Quote 100 tons of Grade A premium steel for construction project with quality specifications"
        }
    ]
    
    print("A2A Construction Agents Demo")
    print("Using Official A2A SDK Client")
    print("=" * 60)
    
    results = []
    for agent in agents:
        success = await test_agent(agent["name"], agent["url"], agent["message"])
        results.append((agent["name"], success))
    
    print(f"\n{'='*60}")
    print("Summary:")
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name}: {status}")

if __name__ == "__main__":
    asyncio.run(main())