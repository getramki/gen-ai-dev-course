# Exercise 1: Build Basic Chatbot with Claude

## 🎯 **Objective**
Create a functional chatbot using ChatBedrock with personality modes, conversation management, and error handling.

**Time**: 8 minutes  
**Difficulty**: Intermediate  
**File**: `exercise_1_chatbot.py`

## 📋 **Step-by-Step Instructions**

### Step 1: Chatbot Class Structure (2 minutes)
Create `ClaudeChatbot` class with:
```python
class ClaudeChatbot:
    def __init__(self, personality="helpful"):
        self.personality = personality
        self.conversation_history = []
        self.chat = self._initialize_chat()
        self.system_message = self._get_system_message()
```

**Key Components**:
- `personality` - Current chatbot personality mode
- `conversation_history` - List of messages for context
- `chat` - ChatBedrock instance
- `system_message` - Personality-based system prompt

### Step 2: ChatBedrock Initialization (1 minute)
Implement `_initialize_chat()` method:
```python
def _initialize_chat(self):
    return ChatBedrock(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        region_name="us-east-1",
        model_kwargs={
            "max_tokens": 200,
            "temperature": 0.7
        }
    )
```

### Step 3: Personality System (2 minutes)
Create `_get_system_message()` with personality options:
- **Helpful**: "You are a helpful and friendly assistant..."
- **Technical**: "You are a technical expert..."
- **Creative**: "You are a creative assistant..."
- **Teacher**: "You are a patient teacher..."

Return appropriate `SystemMessage` based on `self.personality`

### Step 4: Message Handling (2 minutes)
Implement `send_message(user_input)` method:
1. Create `HumanMessage` from user input
2. Build message list: `[system_message] + history + [user_message]`
3. Call `self.chat.invoke(messages)`
4. Add both user and AI messages to history
5. Manage history length (keep last 10 messages)
6. Return AI response content

### Step 5: Additional Features (1 minute)
Add utility methods:
- `change_personality(new_personality)` - Switch personality modes
- `get_conversation_stats()` - Return conversation statistics
- `clear_history()` - Reset conversation history

**Statistics to track**:
- Total messages, user messages, AI messages, current personality

## ✅ **Expected Output**
```
=== Claude Chatbot Demo ===

Demo Conversation:

👤 User: Hello! What can you help me with?
🤖 Claude: Hello! I'm Claude, your AI assistant. I can help you with a wide variety of tasks...

👤 User: Explain Python decorators in simple terms.
🤖 Claude: Python decorators are like gift wrappers for functions. They add extra functionality...

Conversation Stats: {'total_messages': 8, 'user_messages': 4, 'ai_messages': 4, 'personality': 'helpful'}

=== Personality Mode Testing ===

Testing HELPFUL personality:
Response: Artificial intelligence (AI) is technology that enables computers to perform tasks...

Testing TECHNICAL personality:
Response: Artificial Intelligence is a branch of computer science focused on creating systems...
```

## 🔧 **Common Issues**

**Issue**: ChatBedrock initialization fails
**Solution**: Verify AWS credentials and model access permissions

**Issue**: Conversation history grows too large
**Solution**: Implement history trimming (keep last 10 messages)

**Issue**: Empty or invalid responses
**Solution**: Add response validation and error handling

**Issue**: Personality changes don't take effect
**Solution**: Ensure `system_message` is updated when personality changes

## 🚀 **Challenge Extensions**
1. **Conversation Persistence**: Save/load conversation history to/from files
2. **Advanced Personalities**: Add more specialized personality modes
3. **Response Filtering**: Implement content filtering and safety checks
4. **Conversation Analytics**: Track response times, token usage, user satisfaction
5. **Multi-language Support**: Handle conversations in different languages

### Conversation Persistence Extension:
```python
def save_conversation(self, filename):
    conversation_data = {
        'personality': self.personality,
        'history': [{'type': type(msg).__name__, 'content': msg.content} 
                   for msg in self.conversation_history],
        'timestamp': datetime.now().isoformat()
    }
    with open(filename, 'w') as f:
        json.dump(conversation_data, f, indent=2)
```

## 📋 **Completion Checklist**
- [ ] ClaudeChatbot class with all required methods
- [ ] ChatBedrock properly initialized with error handling
- [ ] Four personality modes implemented and working
- [ ] Conversation history management (add, trim, clear)
- [ ] Message handling with proper context building
- [ ] Statistics tracking and reporting
- [ ] Demo conversation runs successfully
- [ ] Personality switching works correctly

## 🎓 **Learning Outcomes**
After completing this exercise, you will understand:
- ChatBedrock integration in object-oriented applications
- Conversation context management strategies
- System message usage for AI personality control
- Error handling patterns for production chatbots
- Memory management for long conversations
- Statistics collection and monitoring for AI applications