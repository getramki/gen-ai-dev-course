"""Debug script to test purchase agent streaming response."""

import asyncio
import logging
from uuid import uuid4
import httpx

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    MessageSendParams,
    SendStreamingMessageRequest,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_purchase_agent_streaming():
    """Test purchase agent with streaming to debug response handling."""
    
    base_url = "http://localhost:10001"
    
    async with httpx.AsyncClient(timeout=120.0) as httpx_client:
        try:
            # Get agent card
            resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
            agent_card = await resolver.get_agent_card()
            
            print(f"✅ Connected to: {agent_card.name}")
            print(f"Description: {agent_card.description}")
            
            # Create client
            client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)
            
            # Test message
            test_message = """
PROCUREMENT REQUEST:
- Project: Downtown Construction Complex
- Cement: 1000 tons, Grade 42.5 OPC
- Steel: 100 tons, Grade A rebar and structural
- Budget: $130,000 total
- Delivery: Within 14 days to downtown site
- Payment: 30 days net

Please analyze this procurement request and provide cost breakdown with recommendations.
"""
            
            print(f"\n📤 Sending message:")
            print(test_message)
            
            # Send streaming message
            streaming_request = SendStreamingMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(
                    message={
                        'role': 'user',
                        'parts': [{'kind': 'text', 'text': test_message}],
                        'message_id': uuid4().hex,
                    }
                )
            )
            
            print(f"\n📥 Streaming response:")
            
            # Handle streaming response
            stream_response = client.send_message_streaming(streaming_request)
            chunk_count = 0
            
            async for chunk in stream_response:
                chunk_count += 1
                print(f"\n--- CHUNK {chunk_count} ---")
                print(f"Chunk type: {type(chunk)}")
                print(f"Raw chunk: {chunk}")
                
                # Handle different event types
                if hasattr(chunk, 'root') and chunk.root:
                    if hasattr(chunk.root, 'result'):
                        result = chunk.root.result
                        print(f"Result type: {type(result)}")
                        
                        # Handle Task object
                        if hasattr(result, 'id'):
                            print(f"Task ID: {result.id}")
                        if hasattr(result, 'status'):
                            print(f"Status: {result.status}")
                        if hasattr(result, 'message') and result.message:
                            print(f"Message: {result.message}")
                            if hasattr(result.message, 'parts') and result.message.parts:
                                for i, part in enumerate(result.message.parts):
                                    if hasattr(part.root, 'text'):
                                        print(f"Part {i} text: {part.root.text}")
                    
                    elif hasattr(chunk.root, 'event'):
                        event = chunk.root.event
                        print(f"Event type: {type(event)}")
                        print(f"Event: {event}")
                        
                        # Extract task info from event
                        if hasattr(event, 'task_id'):
                            print(f"Task ID: {event.task_id}")
                        if hasattr(event, 'status'):
                            print(f"Status: {event.status}")
                        if hasattr(event, 'message') and event.message:
                            print(f"Message: {event.message}")
                            if hasattr(event.message, 'parts') and event.message.parts:
                                for i, part in enumerate(event.message.parts):
                                    if hasattr(part.root, 'text'):
                                        print(f"Part {i} text: {part.root.text}")
                
                # Check for completion
                chunk_str = str(chunk).lower()
                if 'completed' in chunk_str or 'input-required' in chunk_str:
                    print(f"✅ Task status detected: {chunk_str[:100]}...")
                    break
            
            print(f"\n✅ Streaming completed. Total chunks: {chunk_count}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Error details: {e}", exc_info=True)

if __name__ == "__main__":
    print("Purchase Agent Streaming Debug")
    print("=" * 50)
    print("Make sure purchase agent is running on port 10001")
    print("=" * 50)
    
    asyncio.run(test_purchase_agent_streaming())