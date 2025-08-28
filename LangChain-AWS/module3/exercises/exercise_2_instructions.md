# Exercise 2: Real-time Streaming Chat Interface

## 🎯 **Objective**
Build a production-ready streaming chat interface with real-time responses, UI feedback, token tracking, and error handling.

**Time**: 7 minutes  
**Difficulty**: Advanced  
**File**: `exercise_2_streaming_chat.py`

## 📋 **Step-by-Step Instructions**

### Step 1: StreamingChatInterface Class Setup (2 minutes)
Create the main interface class:
```python
class StreamingChatInterface:
    def __init__(self):
        self.chat = self._initialize_chat()
        self.conversation_history = []
        self.is_streaming = False
        self.token_usage = {"input": 0, "output": 0, "total_cost": 0.0}
```

**Key Components**:
- `chat` - ChatBedrock instance configured for streaming
- `conversation_history` - Message history for context
- `is_streaming` - Flag for UI state management
- `token_usage` - Cost tracking dictionary

### Step 2: Token Management System (1.5 minutes)
Implement token estimation and cost calculation:

**Token Estimation**:
```python
def _estimate_tokens(self, text):
    return len(text.split()) * 1.3  # Rough approximation
```

**Cost Calculation**:
```python
def _calculate_cost(self, input_tokens, output_tokens):
    # Claude-3 Haiku pricing
    input_cost = (input_tokens / 1000) * 0.00025
    output_cost = (output_tokens / 1000) * 0.00125
    return input_cost + output_cost
```

### Step 3: Typing Indicator Implementation (1 minute)
Create animated typing indicator:
```python
def _show_typing_indicator(self):
    indicators = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    for i in range(20):  # ~2 seconds
        if not self.is_streaming:
            break
        print(f"\r🤖 Claude {indicators[i % len(indicators)]} typing...", end="", flush=True)
        time.sleep(0.1)
```

**Run in separate thread** to avoid blocking main execution.

### Step 4: Core Streaming Implementation (2 minutes)
Implement `stream_response()` method:

1. **Add user message** to conversation history
2. **Start typing indicator** in background thread
3. **Stream response** using `chat.stream(messages)`
4. **Print chunks** in real-time with `print(chunk.content, end="", flush=True)`
5. **Track performance** (duration, chunks, tokens)
6. **Update token usage** and cost tracking
7. **Return metadata** dictionary

**Error Handling**: Wrap streaming in try-catch block

### Step 5: Statistics and Monitoring (30 seconds)
Implement usage tracking:
```python
def get_usage_stats(self):
    return {
        "total_messages": len(self.conversation_history),
        "input_tokens": self.token_usage["input"],
        "output_tokens": self.token_usage["output"],
        "total_cost": self.token_usage["total_cost"],
        "avg_cost_per_message": self.token_usage["total_cost"] / max(1, len(self.conversation_history) // 2)
    }
```

## ✅ **Expected Output**
```
=== Streaming Chat Demo ===

👤 You: Hello! Can you explain what machine learning is?
🤖 Claude ⠋ typing...
🤖 Claude: Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed...

📊 Response Stats:
   Chunks: 15
   Duration: 2.34s
   Tokens: 12 in, 87 out
   Cost: $0.000112

📈 Session Statistics:
   total_messages: 8
   input_tokens: 45.2
   output_tokens: 312.8
   total_cost: $0.000423
```

## 🔧 **Common Issues**

**Issue**: Typing indicator doesn't stop
**Solution**: Ensure `self.is_streaming = False` is set before streaming starts

**Issue**: Chunks not displaying in real-time
**Solution**: Use `flush=True` in print statements and `end=""` parameter

**Issue**: Threading errors with typing indicator
**Solution**: Set `daemon=True` on typing thread and handle thread cleanup

**Issue**: Token estimation inaccurate
**Solution**: Implement more sophisticated tokenization or use actual token counting

## 🚀 **Challenge Extensions**
1. **Advanced UI**: Add colors, progress bars, and better formatting
2. **Conversation Export**: Save conversations to files with timestamps
3. **Multiple Models**: Support switching between different Claude models
4. **Real Token Counting**: Integrate actual tokenization libraries
5. **WebSocket Integration**: Convert to web-based streaming interface

### Advanced UI Extension:
```python
from rich.console import Console
from rich.live import Live
from rich.text import Text

def enhanced_streaming_display(self, response_stream):
    console = Console()
    
    with Live(console=console, refresh_per_second=10) as live:
        response_text = Text()
        
        for chunk in response_stream:
            response_text.append(chunk.content)
            live.update(response_text)
```

### WebSocket Extension:
```python
import asyncio
import websockets

async def websocket_streaming_handler(websocket, path):
    async for message in websocket:
        # Stream response back through websocket
        async for chunk in self.chat.astream([HumanMessage(content=message)]):
            await websocket.send(chunk.content)
```

## 📋 **Completion Checklist**
- [ ] StreamingChatInterface class with all required methods
- [ ] Token estimation and cost calculation working
- [ ] Typing indicator animation implemented
- [ ] Real-time streaming with proper UI feedback
- [ ] Conversation history management (last 10 messages)
- [ ] Performance tracking (duration, chunks, tokens)
- [ ] Usage statistics and cost monitoring
- [ ] Error handling for streaming failures
- [ ] Demo conversation runs successfully
- [ ] Performance tests show realistic metrics

## 🎓 **Learning Outcomes**
After completing this exercise, you will understand:
- Real-time streaming implementation with ChatBedrock
- UI/UX patterns for streaming AI applications
- Token usage tracking and cost optimization
- Threading for non-blocking UI operations
- Performance monitoring and optimization techniques
- Production-ready error handling for streaming applications