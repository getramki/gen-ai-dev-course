"""
Exercise 2: Build a Conversation Memory System

Task: Create a conversation memory system that:
1. Stores conversation history
2. Manages context window limits
3. Provides conversation summaries
4. Supports different memory strategies

Time: 5 minutes
"""

from typing import List, Dict
import json

class ConversationMemory:
    """Advanced conversation memory with multiple strategies"""
    
    def __init__(self, strategy="buffer", max_size=10):
        self.strategy = strategy
        self.max_size = max_size
        self.messages = []
        self.summary = ""
    
    def add_message(self, role: str, content: str):
        """Add a message to memory"""
        message = {
            "role": role,
            "content": content,
            "timestamp": self._get_timestamp()
        }
        
        self.messages.append(message)
        self._apply_strategy()
    
    def _get_timestamp(self):
        """Get current timestamp"""
        import time
        return int(time.time())
    
    def _apply_strategy(self):
        """Apply memory management strategy"""
        if self.strategy == "buffer":
            self._buffer_strategy()
        elif self.strategy == "summary":
            self._summary_strategy()
        elif self.strategy == "sliding":
            self._sliding_strategy()
    
    def _buffer_strategy(self):
        """Keep all messages up to max_size"""
        if len(self.messages) > self.max_size:
            self.messages = self.messages[-self.max_size:]
    
    def _summary_strategy(self):
        """Summarize old messages when limit reached"""
        if len(self.messages) > self.max_size:
            # Simple summarization (in real app, use LLM)
            old_messages = self.messages[:-self.max_size//2]
            self.summary = self._create_summary(old_messages)
            self.messages = self.messages[-self.max_size//2:]
    
    def _sliding_strategy(self):
        """Keep only recent messages"""
        if len(self.messages) > self.max_size:
            self.messages = self.messages[-self.max_size:]
    
    def _create_summary(self, messages: List[Dict]) -> str:
        """Create summary of messages"""
        topics = []
        for msg in messages:
            if len(msg["content"]) > 20:
                topics.append(msg["content"][:20] + "...")
        
        return f"Previous conversation covered: {', '.join(topics[:3])}"
    
    def get_context(self) -> str:
        """Get full conversation context"""
        context_parts = []
        
        if self.summary:
            context_parts.append(f"Summary: {self.summary}")
        
        for msg in self.messages:
            context_parts.append(f"{msg['role']}: {msg['content']}")
        
        return "\n".join(context_parts)
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        return {
            "total_messages": len(self.messages),
            "strategy": self.strategy,
            "max_size": self.max_size,
            "has_summary": bool(self.summary),
            "memory_usage": len(self.get_context())
        }

def test_memory_strategies():
    """Test different memory strategies"""
    
    print("=== Memory Strategy Comparison ===\n")
    
    # Test data
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
    
    strategies = ["buffer", "summary", "sliding"]
    
    for strategy in strategies:
        print(f"Testing {strategy.upper()} strategy:")
        memory = ConversationMemory(strategy=strategy, max_size=6)
        
        # Add all messages
        for role, content in conversation:
            memory.add_message(role, content)
        
        stats = memory.get_stats()
        print(f"  Messages kept: {stats['total_messages']}")
        print(f"  Memory usage: {stats['memory_usage']} characters")
        print(f"  Has summary: {stats['has_summary']}")
        print(f"  Context preview: {memory.get_context()[:100]}...\n")

def create_smart_memory():
    """Create a smart memory system with adaptive strategies"""
    
    class SmartMemory(ConversationMemory):
        def __init__(self):
            super().__init__(strategy="buffer", max_size=8)
            self.token_limit = 500  # Simulated token limit
        
        def _estimate_tokens(self, text: str) -> int:
            """Estimate token count (rough approximation)"""
            return len(text.split())
        
        def _get_total_tokens(self) -> int:
            """Get total tokens in current context"""
            return self._estimate_tokens(self.get_context())
        
        def _apply_strategy(self):
            """Smart strategy selection based on token usage"""
            total_tokens = self._get_total_tokens()
            
            if total_tokens > self.token_limit:
                if len(self.messages) > 10:
                    self.strategy = "summary"
                    self._summary_strategy()
                else:
                    self.strategy = "sliding"
                    self._sliding_strategy()
            else:
                self.strategy = "buffer"
                self._buffer_strategy()
    
    return SmartMemory()

def test_smart_memory():
    """Test the smart memory system"""
    
    print("=== Smart Memory System ===\n")
    
    smart_memory = create_smart_memory()
    
    # Add progressively longer messages
    messages = [
        ("user", "Hi"),
        ("assistant", "Hello! How can I help you today?"),
        ("user", "I'm working on a complex machine learning project with multiple datasets"),
        ("assistant", "That sounds interesting! Machine learning projects often involve data preprocessing, model selection, training, and evaluation phases"),
        ("user", "I need help with feature engineering and model optimization techniques"),
        ("assistant", "Feature engineering is crucial for ML success. You should consider normalization, encoding categorical variables, creating polynomial features, and using techniques like PCA for dimensionality reduction")
    ]
    
    print("Adding messages and observing strategy changes:")
    for role, content in messages:
        smart_memory.add_message(role, content)
        stats = smart_memory.get_stats()
        tokens = smart_memory._get_total_tokens()
        
        print(f"Added {role} message (tokens: {tokens})")
        print(f"  Strategy: {stats['strategy']}")
        print(f"  Messages: {stats['total_messages']}")
        print()

if __name__ == "__main__":
    test_memory_strategies()
    test_smart_memory()
    
    print("✅ Exercise 2 Complete!")
    print("\nChallenge: Enhance the memory system with:")
    print("• Semantic similarity filtering")
    print("• Importance scoring")
    print("• Persistent storage")