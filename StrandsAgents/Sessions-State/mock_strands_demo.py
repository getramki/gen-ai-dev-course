"""
Mock Strands Agents SDK Demo

Since the actual SDK may not be installed, this demonstrates the concepts
using mock implementations that follow the official SDK patterns.
"""

import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


class ToolState:
    """Mock ToolState - maintains state for individual tools"""
    
    def __init__(self):
        self._state: Dict[str, Any] = {}
    
    def update(self, data: Dict[str, Any]):
        """Update tool state"""
        self._state.update(data)
    
    def get(self, key: str, default=None):
        """Get value from tool state"""
        return self._state.get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all tool state data"""
        return self._state.copy()


class RequestState:
    """Mock RequestState - maintains state for a single request/session"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self._state: Dict[str, Any] = {}
    
    def update(self, data: Dict[str, Any]):
        """Update request state"""
        self._state.update(data)
    
    def get(self, key: str, default=None):
        """Get value from request state"""
        return self._state.get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all request state data"""
        return self._state.copy()


class Conversation:
    """Mock Conversation - holds conversation history"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List[Message] = []
        self.created_at = datetime.now()
    
    def add_message(self, message: Message):
        """Add message to conversation"""
        self.messages.append(message)
    
    def get_messages(self) -> List[Message]:
        """Get all messages"""
        return self.messages.copy()


class ConversationManager:
    """Mock ConversationManager - manages conversations across sessions"""
    
    def __init__(self):
        self._conversations: Dict[str, Conversation] = {}
        self._session_states: Dict[str, RequestState] = {}
    
    async def get_conversation(self, session_id: str) -> Conversation:
        """Get or create conversation for session"""
        if session_id not in self._conversations:
            self._conversations[session_id] = Conversation(session_id)
        return self._conversations[session_id]
    
    async def save_conversation(self, session_id: str, conversation: Conversation):
        """Save conversation (in real SDK this would persist to storage)"""
        self._conversations[session_id] = conversation
    
    def get_all_sessions(self) -> List[str]:
        """Get all active session IDs"""
        return list(self._conversations.keys())
    
    def get_session_state(self, session_id: str) -> RequestState:
        """Get or create session state"""
        if session_id not in self._session_states:
            self._session_states[session_id] = RequestState(session_id)
        return self._session_states[session_id]


class Agent:
    """Mock Agent base class"""
    
    def __init__(self):
        pass


# Tools demonstrating state management
class WeatherTool:
    """Tool with persistent state for caching weather data"""
    
    def __init__(self):
        self.state = ToolState()
        self._api_calls = 0
    
    async def get_weather(self, location: str) -> str:
        """Get weather with state tracking"""
        self._api_calls += 1
        
        # Update tool state
        self.state.update({
            "last_location": location,
            "api_calls_made": self._api_calls,
            "last_call_time": datetime.now().isoformat()
        })
        
        # Mock weather data
        weather_data = {
            "london": "Cloudy, 15°C",
            "paris": "Sunny, 18°C", 
            "tokyo": "Rainy, 12°C",
            "new york": "Snowy, -2°C"
        }
        
        weather = weather_data.get(location.lower(), "Unknown location")
        return f"Weather in {location}: {weather}"


class PreferenceTool:
    """Tool for managing user preferences using request state"""
    
    def __init__(self):
        self.state = ToolState()
    
    async def set_preference(self, category: str, value: str, request_state: RequestState) -> str:
        """Set user preference in request state"""
        preferences = request_state.get("user_preferences", {})
        preferences[category] = value
        request_state.update({"user_preferences": preferences})
        
        # Update tool state with metadata
        self.state.update({
            "last_preference_category": category,
            "preferences_set": self.state.get("preferences_set", 0) + 1
        })
        
        return f"Set {category} preference to: {value}"
    
    async def get_preference(self, category: str, request_state: RequestState) -> str:
        """Get user preference from request state"""
        preferences = request_state.get("user_preferences", {})
        value = preferences.get(category)
        
        if value:
            return f"Your {category} preference: {value}"
        else:
            return f"No {category} preference set yet"


class SessionStateAgent(Agent):
    """Agent demonstrating all Strands SDK state concepts"""
    
    def __init__(self):
        super().__init__()
        self.conversation_manager = ConversationManager()
        self.weather_tool = WeatherTool()
        self.preference_tool = PreferenceTool()
    
    async def process_message(self, message: str, session_id: str) -> str:
        """Process message with full state management"""
        
        # 1. Get persistent RequestState for this session
        request_state = self.conversation_manager.get_session_state(session_id)
        
        # 2. Get Conversation from ConversationManager
        conversation = await self.conversation_manager.get_conversation(session_id)
        
        # 3. Add user message to conversation history
        user_message = Message(role=MessageRole.USER, content=message)
        conversation.add_message(user_message)
        
        # 4. Generate response using tools and state
        response = await self._generate_response(message, conversation, request_state)
        
        # 5. Add agent response to conversation history
        agent_message = Message(role=MessageRole.ASSISTANT, content=response)
        conversation.add_message(agent_message)
        
        # 6. Save conversation state
        await self.conversation_manager.save_conversation(session_id, conversation)
        
        return response
    
    async def _generate_response(self, message: str, conversation: Conversation, request_state: RequestState) -> str:
        """Generate contextual response using all state types"""
        msg_lower = message.lower()
        
        # Weather tool usage
        if "weather" in msg_lower:
            location = self._extract_location(message)
            if location:
                return await self.weather_tool.get_weather(location)
            return "Please specify a location (e.g., 'weather in London')"
        
        # Preference queries (check first)
        elif any(phrase in msg_lower for phrase in ["my preference", "what do i prefer", "what's my preference", "what i prefer"]):
            return await self.preference_tool.get_preference("beverage", request_state)
        
        # Preference management
        elif "prefer" in msg_lower or "set preference" in msg_lower:
            if "coffee" in msg_lower:
                return await self.preference_tool.set_preference("beverage", "coffee", request_state)
            elif "tea" in msg_lower:
                return await self.preference_tool.set_preference("beverage", "tea", request_state)
            return "What would you like to set as your preference?"
        
        # Conversation history queries
        elif "history" in msg_lower or "conversation" in msg_lower:
            msg_count = len(conversation.messages)
            return f"Our conversation has {msg_count} messages. Started at {conversation.created_at.strftime('%H:%M:%S')}"
        
        # Tool state inspection
        elif "tool state" in msg_lower:
            weather_state = self.weather_tool.state.get_all()
            pref_state = self.preference_tool.state.get_all()
            return f"Weather tool: {weather_state}\nPreference tool: {pref_state}"
        
        # Request state inspection
        elif "request state" in msg_lower or "session state" in msg_lower:
            state_data = request_state.get_all()
            return f"Session {request_state.session_id} state: {state_data}"
        
        # Session management info
        elif "sessions" in msg_lower or "all sessions" in msg_lower:
            all_sessions = self.conversation_manager.get_all_sessions()
            return f"Active sessions: {', '.join(all_sessions)}"
        
        else:
            return f"Message received! Try: weather queries, preferences, history, or state inspection."
    
    def _extract_location(self, message: str) -> Optional[str]:
        """Simple location extraction"""
        msg_lower = message.lower()
        locations = ["london", "paris", "tokyo", "new york"]
        for location in locations:
            if location in msg_lower:
                return location
        return None


async def demo_strands_concepts():
    """Comprehensive demo of Strands Agents SDK concepts"""
    print("=== Strands Agents SDK Concepts Demo ===")
    print("Demonstrating: Conversation History, Conversation Manager, Tool State, Request State, Session Management\n")
    
    agent = SessionStateAgent()
    
    # Session 1: Alice
    print("=== Session 1: Alice ===")
    alice_session = "alice_session_001"
    alice_messages = [
        "Hello! I'm Alice",
        "I prefer coffee",
        "What's the weather in London?", 
        "What's my preference?",
        "Show me our conversation history",
        "What's the weather in Paris?",
        "Show me the tool state"
    ]
    
    for msg in alice_messages:
        print(f"Alice: {msg}")
        response = await agent.process_message(msg, alice_session)
        print(f"Agent: {response}\n")
    
    # Session 2: Bob
    print("=== Session 2: Bob ===")
    bob_session = "bob_session_002"
    bob_messages = [
        "Hi, I'm Bob",
        "I prefer tea",
        "Weather in Tokyo please",
        "What do I prefer?",
        "Show conversation history",
        "What's my session state?"
    ]
    
    for msg in bob_messages:
        print(f"Bob: {msg}")
        response = await agent.process_message(msg, bob_session)
        print(f"Agent: {response}\n")
    
    # Demonstrate state isolation
    print("=== State Isolation Demo ===")
    alice_pref = await agent.process_message("What's my preference?", alice_session)
    bob_pref = await agent.process_message("What's my preference?", bob_session)
    
    print(f"Alice's preference: {alice_pref}")
    print(f"Bob's preference: {bob_pref}")
    
    # Show session management
    print("\n=== Session Management ===")
    sessions_info = await agent.process_message("Show all sessions", alice_session)
    print(f"Session info: {sessions_info}")
    
    # Final state summary
    print("\n=== Final State Summary ===")
    print("Tool States:")
    print(f"  Weather Tool: {agent.weather_tool.state.get_all()}")
    print(f"  Preference Tool: {agent.preference_tool.state.get_all()}")
    
    print("\nConversation Stats:")
    alice_conv = await agent.conversation_manager.get_conversation(alice_session)
    bob_conv = await agent.conversation_manager.get_conversation(bob_session)
    print(f"  Alice: {len(alice_conv.messages)} messages")
    print(f"  Bob: {len(bob_conv.messages)} messages")


if __name__ == "__main__":
    asyncio.run(demo_strands_concepts())