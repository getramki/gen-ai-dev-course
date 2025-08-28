# Exercise 1: Multi-turn Conversation Manager

## 🎯 **Objective**
Build an advanced conversation management system with intelligent memory strategies, topic tracking, and comprehensive analytics.

**Time**: 8 minutes  
**Difficulty**: Advanced  
**File**: `exercise_1_conversation_system.py`

## 📋 **Step-by-Step Instructions**

### Step 1: Core Class Structure (2 minutes)
Create `AdvancedConversationManager` class:
```python
class AdvancedConversationManager:
    def __init__(self, memory_strategy="adaptive", max_context_tokens=2000):
        self.chat = self._initialize_chat()
        self.memory_strategy = memory_strategy
        self.max_context_tokens = max_context_tokens
        
        # State tracking
        self.messages = []
        self.conversation_summary = ""
        self.current_topic = None
        self.conversation_stage = "initial"
        
        # Analytics
        self.conversation_stats = {
            "start_time": datetime.now(),
            "turn_count": 0,
            "topics_discussed": [],
            "total_tokens_used": 0
        }
```

### Step 2: Topic Detection System (1.5 minutes)
Implement `_detect_topic()` method:
- Create keyword dictionary for different topics:
  - **Technology**: ["python", "programming", "code", "ai"]
  - **Travel**: ["travel", "vacation", "trip", "hotel"]
  - **Health**: ["health", "fitness", "exercise", "diet"]
  - **Education**: ["learn", "study", "course", "school"]
- Return topic based on keyword matches in message content
- Default to "general" if no matches found

### Step 3: Memory Management Strategies (2 minutes)
Implement three memory strategies:

**Adaptive Memory** (`_adaptive_memory_management`):
- Choose strategy based on conversation stage and token count
- Use sliding window for early stages
- Use summary buffer for deep discussions
- Use token-based trimming for long conversations

**Sliding Window** (`_sliding_window_memory`):
- Keep only recent N messages (default 8)
- Always preserve SystemMessage instances
- Trim older HumanMessage and AIMessage pairs

**Summary Buffer** (`_summary_buffer_memory`):
- When conversation exceeds limit, summarize older half
- Create topic-based summary from old messages
- Keep recent half of conversation intact

### Step 4: Conversation State Management (1.5 minutes)
Implement state tracking:

**Stage Detection** (`_update_conversation_stage`):
- **greeting**: turns 1-1
- **topic_establishment**: turns 2-3
- **deep_discussion**: turns 4-8
- **problem_solving**: turns 9-12
- **conclusion**: turns 13+

**Analytics Tracking**:
- Update turn count, topics discussed, token usage
- Track conversation duration and performance metrics

### Step 5: Core Message Handling (1 minute)
Implement `send_message()` method:
1. Create HumanMessage from user input
2. Update analytics (turn count, topic detection)
3. Update conversation stage
4. Apply memory management strategy
5. Build context with summary + system + messages
6. Get ChatBedrockConverse response
7. Update token usage and return structured result

## ✅ **Expected Output**
```
=== Advanced Conversation Manager Demo ===

👤 User (Turn 1): Hello! I'm interested in learning about artificial intelligence.
🤖 Assistant: Hello! It's great to hear about your interest in artificial intelligence...
📊 Topic: technology | Stage: greeting | Tokens: 45→87

👤 User (Turn 5): How long does it typically take to become proficient in ML?
🤖 Assistant: The timeline for becoming proficient in machine learning varies...
📊 Topic: technology | Stage: deep_discussion | Tokens: 234→92

📈 Final Conversation Analytics:
   Duration: 2.3 minutes
   Total turns: 10
   Topics discussed: ['technology', 'education']
   Final stage: problem_solving
   Total tokens: 1847
   Avg tokens/turn: 184
💾 Conversation exported to conversation_20241201_143022.json
```

## 🔧 **Common Issues**

**Issue**: Memory management not working properly
**Solution**: Ensure `_apply_memory_strategy()` is called after adding each message

**Issue**: Topic detection too broad/narrow
**Solution**: Adjust keyword lists and matching logic for better accuracy

**Issue**: Token estimation inaccurate
**Solution**: Calibrate estimation factor (1.3) based on actual usage patterns

**Issue**: Conversation export fails
**Solution**: Handle file permissions and ensure valid JSON serialization

## 🚀 **Challenge Extensions**
1. **Sentiment Analysis**: Track conversation sentiment over time
2. **User Profiling**: Build persistent user preference profiles
3. **Multi-language Support**: Handle conversations in different languages
4. **Advanced Summarization**: Use LLM-based summarization for better context compression
5. **Real-time Analytics Dashboard**: Create live conversation monitoring

### Sentiment Analysis Extension:
```python
def _analyze_sentiment(self, message_content):
    positive_words = ["good", "great", "excellent", "happy", "satisfied"]
    negative_words = ["bad", "terrible", "frustrated", "angry", "disappointed"]
    
    pos_count = sum(1 for word in positive_words if word in message_content.lower())
    neg_count = sum(1 for word in negative_words if word in message_content.lower())
    
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"
```

### User Profiling Extension:
```python
def _update_user_profile(self, message_content):
    # Extract preferences, interests, and behavioral patterns
    if "prefer" in message_content.lower():
        # Extract and store user preferences
        pass
    
    if "interested in" in message_content.lower():
        # Track user interests
        pass
```

## 📋 **Completion Checklist**
- [ ] AdvancedConversationManager class with all core methods
- [ ] Topic detection working with multiple categories
- [ ] Three memory strategies implemented and functional
- [ ] Conversation stage tracking updating correctly
- [ ] Analytics collection comprehensive and accurate
- [ ] Token estimation and management working
- [ ] Conversation export functionality operational
- [ ] Demo conversation runs successfully with transitions
- [ ] Memory strategy comparison shows different behaviors
- [ ] Error handling prevents crashes

## 🎓 **Learning Outcomes**
After completing this exercise, you will understand:
- Advanced conversation state management techniques
- Intelligent memory strategies for long conversations
- Topic detection and conversation flow optimization
- Analytics collection and performance monitoring
- Production-ready conversation system architecture
- Token optimization and cost management strategies