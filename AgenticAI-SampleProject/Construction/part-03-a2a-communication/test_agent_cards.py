"""Test script to verify agent cards are properly exposed through API."""

import asyncio
import httpx
import json

async def test_agent_card(name: str, url: str):
    """Test if agent card is properly exposed."""
    print(f"\n=== Testing {name} Agent Card ===")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}/")
            
            if response.status_code == 200:
                card = response.json()
                print(f"✅ Agent card retrieved successfully")
                print(f"Name: {card.get('name', 'Unknown')}")
                print(f"Description: {card.get('description', 'No description')}")
                print(f"Version: {card.get('version', 'Unknown')}")
                print(f"URL: {card.get('url', 'Unknown')}")
                
                skills = card.get('skills', [])
                if skills:
                    print(f"Skills ({len(skills)}):")
                    for skill in skills:
                        print(f"  - {skill.get('name', 'Unknown')}")
                        print(f"    {skill.get('description', 'No description')}")
                
                capabilities = card.get('capabilities', {})
                if capabilities:
                    print(f"Capabilities:")
                    print(f"  - Streaming: {capabilities.get('streaming', False)}")
                    print(f"  - Push Notifications: {capabilities.get('push_notifications', False)}")
                
                return True
            else:
                print(f"❌ Failed to get agent card: HTTP {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error connecting to {name}: {e}")
        return False

async def main():
    """Test all agent cards."""
    agents = [
        ("Purchase", "http://localhost:10001"),
        ("Cement", "http://localhost:10002"), 
        ("Steel", "http://localhost:10003")
    ]
    
    print("Testing Agent Card API Exposure")
    print("=" * 50)
    print("Note: Make sure all agents are running first!")
    print("Run: ./start_agents.sh")
    
    results = []
    for name, url in agents:
        success = await test_agent_card(name, url)
        results.append((name, success))
    
    print("\n" + "=" * 50)
    print("Summary:")
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name} Agent: {status}")

if __name__ == "__main__":
    asyncio.run(main())