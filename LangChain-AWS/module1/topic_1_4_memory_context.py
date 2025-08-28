"""
Topic 1.4: Memory and Context Management (4 minutes)

Learning Goals:
- Understand memory types and patterns
- Implement context window management
- Learn state persistence strategies
"""

from langchain_core.memory import BaseMemory
from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict, List, Any

class SimpleConversationMemory:
    """Simple implementation of conversation memory"""
    
    def __init__(self, max_messages: int = 10):
        self.messages: List[Dict[str, str]] = []
        self.max_messages = max_messages
    
    def add_message(self, role: str, content: str):
        """Add a message to memory"""
        self.messages.append({"role": role, "content": content})
        
        # Keep only recent messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_context(self) -> str:
        """Get conversation context as string"""
        context = []
        for msg in self.messages:
            context.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(context)
    
    def clear(self):
        """Clear all messages"""
        self.messages = []

def explore_memory_types():
    """Demonstrate different memory patterns"""
    
    print("=== Memory Types in LangChain ===\n")
    
    print("1. Memory Types:")
    print("   • ConversationBufferMemory - Stores all messages")
    print("   • ConversationSummaryMemory - Summarizes old messages")
    print("   • ConversationBufferWindowMemory - Fixed window size")
    print("   • ConversationTokenBufferMemory - Token-based limit")
    print("   • VectorStoreRetrieverMemory - Semantic search\n")

def demonstrate_conversation_memory():
    """Show conversation memory in action"""
    
    print("=== Conversation Memory Demo ===\n")
    
    memory = SimpleConversationMemory(max_messages=6)
    
    # Simulate conversation
    conversations = [
        ("user", "Hello, I'm learning LangChain"),
        ("assistant", "Great! LangChain is a powerful framework"),
        ("user", "What are the main components?"),
        ("assistant", "Main components are LLMs, prompts, chains, and memory"),
        ("user", "Tell me about memory"),
        ("assistant", "Memory helps maintain conversation context")
    ]
    
    print("Building conversation history:")
    for role, content in conversations:
        memory.add_message(role, content)
        print(f"   Added: {role} - {content[:30]}...")
    
    print(f"\nCurrent context ({len(memory.messages)} messages):")
    print(memory.get_context())
    print()

def explore_context_management():
    """Demonstrate context window management strategies"""
    
    print("=== Context Window Management ===\n")
    
    print("Context window challenges:")
    print("• Token limits (4K, 8K, 32K, 128K)")
    print("• Cost increases with context size")
    print("• Latency grows with longer contexts")
    print("• Information relevance decreases\n")
    
    print("Management strategies:")
    print("• Sliding window - Keep recent N messages")
    print("• Summarization - Compress old conversations")
    print("• Semantic filtering - Keep relevant messages")
    print("• Hierarchical memory - Different retention levels\n")

def demonstrate_context_strategies():
    """Show different context management approaches"""
    
    print("=== Context Management Strategies ===\n")
    
    # Strategy 1: Sliding Window
    class SlidingWindowMemory:
        def __init__(self, window_size=3):
            self.messages = []
            self.window_size = window_size
        
        def add_message(self, message):
            self.messages.append(message)
            if len(self.messages) > self.window_size:
                self.messages = self.messages[-self.window_size:]
        
        def get_messages(self):
            return self.messages
    
    sliding_memory = SlidingWindowMemory(window_size=3)
    
    # Add messages
    for i in range(5):
        sliding_memory.add_message(f"Message {i+1}")
    
    print("1. Sliding Window (size=3):")
    print(f"   Kept messages: {sliding_memory.get_messages()}\n")
    
    # Strategy 2: Token-based limiting
    def estimate_tokens(text: str) -> int:
        """Simple token estimation (1 token ≈ 4 characters)"""
        return len(text) // 4
    
    class TokenLimitMemory:
        def __init__(self, max_tokens=100):
            self.messages = []
            self.max_tokens = max_tokens
        
        def add_message(self, message):
            self.messages.append(message)
            
            # Remove old messages if over token limit
            while self.get_total_tokens() > self.max_tokens and self.messages:
                self.messages.pop(0)
        
        def get_total_tokens(self):
            return sum(estimate_tokens(msg) for msg in self.messages)
    
    token_memory = TokenLimitMemory(max_tokens=50)
    
    messages = [
        "Short message",
        "This is a longer message with more content",
        "Another message",
        "Final message"
    ]
    
    print("2. Token-based limiting (max=50 tokens):")
    for msg in messages:
        token_memory.add_message(msg)
        print(f"   Added: '{msg}' (Total tokens: {token_memory.get_total_tokens()})")
    
    print(f"   Final messages: {len(token_memory.messages)} kept\n")

def explore_state_persistence():
    """Demonstrate state persistence patterns"""
    
    print("=== State Persistence ===\n")
    
    print("Persistence options:")
    print("• In-memory - Fast, lost on restart")
    print("• File-based - Simple, local storage")
    print("• Database - Scalable, shared access")
    print("• Redis - Fast, distributed cache")
    print("• Vector stores - Semantic search\n")
    
    # Simple file-based persistence example
    import json
    import tempfile
    import os
    
    class FilePersistentMemory:
        def __init__(self, file_path=None):
            self.file_path = file_path or tempfile.mktemp(suffix='.json')
            self.messages = self.load_messages()
        
        def load_messages(self):
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            return []
        
        def save_messages(self):
            with open(self.file_path, 'w') as f:
                json.dump(self.messages, f)
        
        def add_message(self, message):
            self.messages.append(message)
            self.save_messages()
    
    # Demo persistent memory
    persistent_memory = FilePersistentMemory()
    persistent_memory.add_message("Persistent message 1")
    persistent_memory.add_message("Persistent message 2")
    
    print("3. File-based persistence:")
    print(f"   Saved to: {persistent_memory.file_path}")
    print(f"   Messages: {len(persistent_memory.messages)}")
    
    # Clean up
    os.unlink(persistent_memory.file_path)

if __name__ == "__main__":
    explore_memory_types()
    demonstrate_conversation_memory()
    explore_context_management()
    demonstrate_context_strategies()
    explore_state_persistence()
    
    print("="*50)
    print("✅ Topic 1.4 Complete!")
    print("Key Takeaways:")
    print("• Memory maintains conversation context")
    print("• Context window management is crucial")
    print("• Multiple strategies for token/size limits")
    print("• Persistence enables stateful applications")
    print("="*50)