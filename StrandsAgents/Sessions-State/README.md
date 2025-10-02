# Strands Agents SDK Sessions and State Demo

This demo demonstrates the core concepts of **Sessions and State** management in the Strands Agents SDK, following the official documentation at: https://strandsagents.com/0.1.x/documentation/docs/user-guide/concepts/agents/sessions-state/

## Key Strands SDK Concepts Demonstrated

### 1. Conversation History
- **Message Storage**: All user and agent messages are stored in conversation objects
- **Temporal Context**: Messages include timestamps and maintain chronological order
- **Session Persistence**: Conversation history persists across multiple interactions within a session

### 2. Conversation Manager
- **Session Management**: Creates and manages conversations for different sessions
- **Persistence**: Handles saving and retrieving conversation data
- **Isolation**: Ensures conversations are isolated between different sessions

### 3. Tool State
- **Tool-Specific State**: Each tool maintains its own persistent state
- **Cross-Request Persistence**: Tool state persists across multiple requests
- **Metadata Tracking**: Tools can track usage statistics, cache data, etc.

### 4. Request State
- **Per-Request Context**: State that exists for the duration of a single request
- **Session-Scoped Data**: User preferences and session-specific information
- **Temporary Storage**: Data that doesn't need to persist beyond the current session

### 5. Session Management
- **Multi-User Support**: Handle multiple concurrent user sessions
- **State Isolation**: Each session maintains independent state
- **Lifecycle Management**: Create, manage, and clean up sessions

## Demo Files

### 1. `strands_sessions_demo.py` (Requires SDK)
Real Strands Agents SDK implementation - requires `pip install strands-agents`

### 2. `mock_strands_demo.py` (Standalone)
Mock implementation demonstrating all concepts without SDK dependency

## Step-by-Step Instructions

### Option A: Using Mock Implementation (Recommended for Learning)

#### Step 1: Navigate to Demo Directory
```bash
cd /home/ramakrishna/Code/GenAI-for-Dev-Course/StrandsAgents/Sessions-State
```

#### Step 2: Run Mock Demo
```bash
python3 mock_strands_demo.py
```

### Option B: Using Real Strands SDK

#### Step 1: Install Strands Agents SDK
```bash
pip install strands-agents
```

#### Step 2: Run SDK Demo
```bash
python3 strands_sessions_demo.py
```

### Option C: Interactive Demo
```bash
python3 interactive_demo.py
```

## Expected Output

```
=== Strands Agents SDK Concepts Demo ===
Demonstrating: Conversation History, Conversation Manager, Tool State, Request State, Session Management

=== Session 1: Alice ===
Alice: Hello! I'm Alice
Agent: Message received! Try: weather queries, preferences, history, or state inspection.

Alice: I prefer coffee
Agent: Set beverage preference to: coffee

Alice: What's the weather in London?
Agent: Weather in London: Cloudy, 15°C

Alice: What's my preference?
Agent: Your beverage preference: coffee

Alice: Show me our conversation history
Agent: Our conversation has 8 messages. Started at 14:23:15

[... more interactions ...]

=== State Isolation Demo ===
Alice's preference: Your beverage preference: coffee
Bob's preference: Your beverage preference: tea

=== Final State Summary ===
Tool States:
  Weather Tool: {'last_location': 'tokyo', 'api_calls_made': 3, 'last_call_time': '2024-01-15T14:23:45'}
  Preference Tool: {'last_preference_category': 'beverage', 'preferences_set': 2}
```

## Code Architecture

### Core Components

1. **Message & MessageRole**: Represent individual messages with roles (user/assistant/system)
2. **ToolState**: Manages persistent state for individual tools
3. **RequestState**: Manages session-scoped state for requests
4. **Conversation**: Holds conversation history for a session
5. **ConversationManager**: Manages multiple conversations across sessions
6. **Agent**: Orchestrates all components to process messages

### State Flow

```
User Message → RequestState → Agent → Tools (with ToolState) → Response
     ↓                                                            ↑
Conversation History ← ConversationManager ← Agent Response ←────┘
```

## Key Features Demonstrated

### 1. Conversation History Management
```python
# Messages are automatically stored with timestamps
user_message = Message(role=MessageRole.USER, content=message)
conversation.add_message(user_message)
```

### 2. Tool State Persistence
```python
# Tools maintain state across requests
self.state.update({
    "last_location": location,
    "api_calls_made": self._api_calls
})
```

### 3. Request State for Session Data
```python
# User preferences stored in request state
preferences = request_state.get("user_preferences", {})
request_state.update({"user_preferences": preferences})
```

### 4. Session Isolation
- Each session has independent conversation history
- Request state is session-scoped
- Tool state is shared but tracks per-session usage

## Interactive Commands

When running the interactive demo, try these commands:
- `"weather in [location]"` - Get weather with tool state tracking
- `"I prefer [coffee/tea]"` - Set preferences in request state
- `"what's my preference?"` - Retrieve from request state
- `"show conversation history"` - Display conversation messages
- `"show tool state"` - View tool state data
- `"show session state"` - View request state data

## Learning Objectives

After running this demo, you'll understand:

1. **How conversation history is maintained** across multiple interactions
2. **How tools maintain persistent state** for caching and metadata
3. **How request state manages session-specific data** like user preferences
4. **How the conversation manager handles multiple sessions** simultaneously
5. **How state isolation works** between different user sessions

## Next Steps

1. **Extend Tools**: Add more tools with different state requirements
2. **Add Persistence**: Implement database storage for conversation history
3. **Session Expiry**: Add session timeout and cleanup mechanisms
4. **Advanced State**: Implement hierarchical state management
5. **Real Integration**: Connect to actual Strands Agents SDK

## Troubleshooting

### Common Issues
1. **Import Errors**: Use mock demo if SDK not installed
2. **Python Version**: Requires Python 3.7+
3. **Async Issues**: Ensure proper async/await usage

### SDK Installation Issues
If `strands-agents` package is not available:
1. Use the mock implementation (`mock_strands_demo.py`)
2. Check official documentation for installation instructions
3. Verify package availability in your Python environment