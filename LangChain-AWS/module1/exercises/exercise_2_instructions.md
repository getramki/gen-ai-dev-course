# Exercise 2: Build a Conversation Memory System

## 🎯 **Objective**
Create an advanced conversation memory system with multiple management strategies and context limits.

**Time**: 5 minutes  
**Difficulty**: Intermediate  
**File**: `exercise_2_memory_system.py`

## 📋 **Step-by-Step Instructions**

### Step 1: Basic Memory Class Structure (1 minute)
Create `ConversationMemory` class with:
```python
class ConversationMemory:
    def __init__(self, strategy="buffer", max_size=10):
        self.strategy = strategy
        self.max_size = max_size
        self.messages = []
        self.summary = ""
```

### Step 2: Message Management (1 minute)
Implement `add_message(role, content)` method:
- Create message dictionary: `{"role": role, "content": content, "timestamp": timestamp}`
- Add to `self.messages` list
- Call `self._apply_strategy()` to manage size
- Use `int(time.time())` for timestamp

### Step 3: Implement Memory Strategies (2 minutes)

**Buffer Strategy** (`_buffer_strategy`):
```python
def _buffer_strategy(self):
    if len(self.messages) > self.max_size:
        self.messages = self.messages[-self.max_size:]
```

**Summary Strategy** (`_summary_strategy`):
- When limit reached, create summary of old messages
- Keep recent `max_size//2` messages
- Store summary in `self.summary`

**Sliding Strategy** (`_sliding_strategy`):
- Always keep only most recent `max_size` messages
- Simple truncation approach

**Strategy Dispatcher** (`_apply_strategy`):
```python
def _apply_strategy(self):
    if self.strategy == "buffer":
        self._buffer_strategy()
    elif self.strategy == "summary":
        self._summary_strategy()
    elif self.strategy == "sliding":
        self._sliding_strategy()
```

### Step 4: Context Retrieval (30 seconds)
Implement `get_context()` method:
- Combine summary (if exists) and current messages
- Format: `"role: content"` per line
- Return single string with newline separators

### Step 5: Statistics and Monitoring (30 seconds)
Create `get_stats()` method returning dictionary:
```python
return {
    "total_messages": len(self.messages),
    "strategy": self.strategy,
    "max_size": self.max_size,
    "has_summary": bool(self.summary),
    "memory_usage": len(self.get_context())
}
```

### Step 6: Test All Strategies (30 seconds)
Test with sample conversation:
```python
conversation = [
    ("user", "Hello, I want to learn about Python"),
    ("assistant", "Great! Python is a versatile programming language"),
    ("user", "What are the main features?"),
    ("assistant", "Python has simple syntax, dynamic typing, and rich libraries"),
    ("user", "Tell me about data structures"),
    ("assistant", "Python has lists, dictionaries, sets, and tuples"),
    ("user", "How about object-oriented programming?"),
    ("assistant", "Python supports classes, inheritance, and polymorphism"),
    ("user", "What about web development?"),
    ("assistant", "You can use Django, Flask, or FastAPI for web development")
]
```

## ✅ **Expected Output**
```
Testing BUFFER strategy:
  Messages kept: 6
  Memory usage: 245 characters
  Has summary: False
  Context preview: user: Hello, I want to learn about Python...

Testing SUMMARY strategy:
  Messages kept: 3
  Memory usage: 180 characters
  Has summary: True
  Context preview: Summary: Previous conversation covered...

Testing SLIDING strategy:
  Messages kept: 6
  Memory usage: 220 characters
  Has summary: False
  Context preview: assistant: Python has simple syntax...
```

## 🔧 **Common Issues**

**Issue**: Strategy not applied after adding messages
**Solution**: Ensure `_apply_strategy()` is called in `add_message()`

**Issue**: Summary strategy not creating summaries
**Solution**: Check message count logic and summary creation function

**Issue**: Memory usage calculation incorrect
**Solution**: Verify `get_context()` includes all relevant text

**Issue**: Timestamp import error
**Solution**: Add `import time` at top of file

## 🚀 **Challenge Extensions**
1. **Smart Memory**: Create adaptive strategy based on token usage
2. **Semantic Filtering**: Keep only relevant messages using similarity
3. **Persistent Storage**: Save/load memory from JSON files
4. **Importance Scoring**: Weight messages by importance
5. **Token-based Limiting**: Use actual token counting instead of character count

### Smart Memory Implementation Hint:
```python
class SmartMemory(ConversationMemory):
    def __init__(self):
        super().__init__(strategy="buffer", max_size=8)
        self.token_limit = 500
    
    def _get_total_tokens(self):
        return len(self.get_context().split())  # Simple token estimation
```

## 📋 **Completion Checklist**
- [ ] ConversationMemory class with all required methods
- [ ] Three memory strategies implemented correctly
- [ ] Message addition with timestamp functionality
- [ ] Context retrieval working properly
- [ ] Statistics method returns correct data structure
- [ ] All strategies tested with sample conversation
- [ ] Output matches expected format

## 🎓 **Learning Outcomes**
After completing this exercise, you will understand:
- Memory management strategies for conversational AI
- Context window optimization techniques
- Object-oriented design for AI applications
- State management and persistence patterns
- Performance monitoring and statistics collection