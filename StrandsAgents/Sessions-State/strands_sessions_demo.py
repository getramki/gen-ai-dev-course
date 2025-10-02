"""
Strands Agents SDK Sessions and State Demo

This demo demonstrates the official Strands Agents SDK concepts:
- Conversation History
- Conversation Manager
- Tool State
- Request State
- Session Management
"""

import asyncio
from typing import Dict, Any, Optional
from strands_agents import Agent, ConversationManager, ToolState, RequestState
from strands_agents.types import Message, MessageRole


class WeatherTool:
    """Example tool to demonstrate tool state"""
    
    def __init__(self):
        self.state = ToolState()
        self.cache = {}
    
    async def get_weather(self, location: str) -> str:
        """Simulate weather API call with state caching"""
        # Check tool state cache
        if location in self.cache:
            return f"Weather in {location}: {self.cache[location]} (from cache)"
        
        # Simulate API call
        weather = f"Sunny, 22°C"  # Mock data
        self.cache[location] = weather
        
        # Update tool state
        self.state.update({"last_location": location, "cache_size": len(self.cache)})
        
        return f"Weather in {location}: {weather}"


class PreferenceTool:
    """Tool to manage user preferences with state"""
    
    def __init__(self):
        self.state = ToolState()
    
    async def set_preference(self, key: str, value: str, request_state: RequestState) -> str:
        """Set user preference in request state"""
        preferences = request_state.get("user_preferences", {})
        preferences[key] = value
        request_state.update({"user_preferences": preferences})
        
        self.state.update({"last_preference_set": key})
        return f"Set {key} preference to {value}"
    
    async def get_preference(self, key: str, request_state: RequestState) -> str:
        """Get user preference from request state"""
        preferences = request_state.get("user_preferences", {})
        value = preferences.get(key)
        
        if value:
            return f"Your {key} preference is: {value}"
        else:
            return f"No {key} preference set"


class SessionStateAgent(Agent):
    """Agent demonstrating session and state management"""
    
    def __init__(self):
        super().__init__()
        self.weather_tool = WeatherTool()
        self.preference_tool = PreferenceTool()
        self.conversation_manager = ConversationManager()
    
    async def process_message(self, message: str, session_id: str) -> str:
        """Process message with full state management"""
        
        # Create request state for this interaction
        request_state = RequestState(session_id=session_id)
        
        # Get conversation history from manager
        conversation = await self.conversation_manager.get_conversation(session_id)
        
        # Add user message to conversation history
        user_message = Message(role=MessageRole.USER, content=message)
        conversation.add_message(user_message)
        
        # Process based on message content
        response = await self._generate_response(message, conversation, request_state)
        
        # Add agent response to conversation history
        agent_message = Message(role=MessageRole.ASSISTANT, content=response)
        conversation.add_message(agent_message)
        
        # Save conversation state
        await self.conversation_manager.save_conversation(session_id, conversation)
        
        return response
    
    async def _generate_response(self, message: str, conversation, request_state: RequestState) -> str:
        """Generate response using tools and state"""
        message_lower = message.lower()
        
        # Weather queries
        if "weather" in message_lower:
            if "in" in message_lower:
                # Extract location (simple parsing)
                parts = message_lower.split("in")
                if len(parts) > 1:
                    location = parts[1].strip().split()[0]
                    return await self.weather_tool.get_weather(location)
            return "Please specify a location for weather info"
        
        # Preference management
        elif "set preference" in message_lower or "prefer" in message_lower:
            if "coffee" in message_lower:
                return await self.preference_tool.set_preference("beverage", "coffee", request_state)
            elif "tea" in message_lower:
                return await self.preference_tool.set_preference("beverage", "tea", request_state)
            return "Please specify what you prefer"
        
        elif "my preference" in message_lower or "what do i prefer" in message_lower:
            return await self.preference_tool.get_preference("beverage", request_state)
        
        # Conversation history queries
        elif "history" in message_lower or "conversation" in message_lower:
            message_count = len(conversation.messages)
            return f"Our conversation has {message_count} messages so far"
        
        # Tool state queries
        elif "tool state" in message_lower:
            weather_state = self.weather_tool.state.get_all()
            pref_state = self.preference_tool.state.get_all()
            return f"Weather tool state: {weather_state}, Preference tool state: {pref_state}"
        
        # Request state queries
        elif "request state" in message_lower or "session state" in message_lower:
            state_data = request_state.get_all()
            return f"Current request state: {state_data}"
        
        # Default response
        else:
            return f"I received: '{message}'. Try asking about weather, setting preferences, or checking state!"


async def demo_strands_sessions_state():
    """Main demo showcasing Strands Agents SDK features"""
    print("=== Strands Agents SDK Sessions and State Demo ===\n")
    
    # Initialize agent
    agent = SessionStateAgent()
    
    # Demo with two different sessions
    session1_id = "session_alice_001"
    session2_id = "session_bob_002"
    
    print("=== Session 1: Alice's Conversation ===")
    alice_messages = [
        "Hello!",
        "What's the weather in London?",
        "I prefer coffee",
        "What's my preference?",
        "Show me our conversation history",
        "What's the weather in Paris?",
        "Show me the tool state"
    ]
    
    for msg in alice_messages:
        print(f"Alice: {msg}")
        response = await agent.process_message(msg, session1_id)
        print(f"Agent: {response}\n")
    
    print("=== Session 2: Bob's Conversation ===")
    bob_messages = [
        "Hi there!",
        "I prefer tea over coffee",
        "What do I prefer?",
        "What's the weather in Tokyo?",
        "Show me my session state",
        "Check our conversation history"
    ]
    
    for msg in bob_messages:
        print(f"Bob: {msg}")
        response = await agent.process_message(msg, session2_id)
        print(f"Agent: {response}\n")
    
    print("=== Demonstrating State Isolation ===")
    
    # Check Alice's preferences
    alice_pref_response = await agent.process_message("What's my preference?", session1_id)
    print(f"Alice's preference check: {alice_pref_response}")
    
    # Check Bob's preferences  
    bob_pref_response = await agent.process_message("What's my preference?", session2_id)
    print(f"Bob's preference check: {bob_pref_response}")
    
    print("\n=== Final State Summary ===")
    
    # Get conversation managers for both sessions
    alice_conv = await agent.conversation_manager.get_conversation(session1_id)
    bob_conv = await agent.conversation_manager.get_conversation(session2_id)
    
    print(f"Alice's session - Total messages: {len(alice_conv.messages)}")
    print(f"Bob's session - Total messages: {len(bob_conv.messages)}")
    
    # Show tool states
    print(f"Weather tool cache size: {len(agent.weather_tool.cache)}")
    print(f"Weather tool state: {agent.weather_tool.state.get_all()}")
    print(f"Preference tool state: {agent.preference_tool.state.get_all()}")


if __name__ == "__main__":
    asyncio.run(demo_strands_sessions_state())