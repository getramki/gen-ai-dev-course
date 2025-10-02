"""
Topic 4.2: Multi-turn Conversations and Context Management (6 minutes)

Learning Goals:
- Master advanced multi-turn conversation patterns
- Implement efficient context window management
- Optimize conversation memory strategies
- Handle long conversations and context limits
"""

from langchain_aws.chat_models import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import List, Dict
import json

def setup_conversation_manager():
    """Initialize ChatBedrockConverse for conversation management"""
    
    print("=== Conversation Manager Setup ===\n")
    
    try:
        chat = ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=200,
            temperature=0.7
        )
        
        print("✅ ChatBedrockConverse initialized for conversation management")
        return chat
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return None

def demonstrate_multi_turn_patterns(chat):
    """Show different multi-turn conversation patterns"""
    
    print("=== Multi-turn Conversation Patterns ===\n")
    
    if not chat:
        print("❌ Chat not available")
        return
    
    # Pattern 1: Information Gathering
    print("Pattern 1: Information Gathering Conversation")
    
    info_conversation = [
        SystemMessage(content="You are a helpful travel assistant. Ask follow-up questions to provide better recommendations."),
        HumanMessage(content="I want to plan a vacation.")
    ]
    
    try:
        # Turn 1
        response1 = chat.invoke(info_conversation)
        print(f"Assistant: {response1.content[:80]}...")
        
        # Turn 2 - User provides more info
        info_conversation.extend([
            AIMessage(content=response1.content),
            HumanMessage(content="I'm thinking about Europe, maybe for 2 weeks.")
        ])
        
        response2 = chat.invoke(info_conversation)
        print(f"Assistant: {response2.content[:80]}...")
        
        # Turn 3 - More specific
        info_conversation.extend([
            AIMessage(content=response2.content),
            HumanMessage(content="I love history and museums, budget around $3000.")
        ])
        
        response3 = chat.invoke(info_conversation)
        print(f"Assistant: {response3.content[:80]}...")
        
        print(f"✅ Information gathering: {len(info_conversation)} messages")
        
    except Exception as e:
        print(f"❌ Information gathering failed: {e}")
    
    print()

def implement_context_window_management():
    """Implement strategies for managing context window limits"""
    
    print("=== Context Window Management ===\n")
    
    class ConversationContextManager:
        """Manage conversation context within token limits"""
        
        def __init__(self, max_context_messages=10):
            self.max_context_messages = max_context_messages
            self.conversation_summary = ""
        
        def estimate_message_tokens(self, message):
            """Rough token estimation for messages"""
            return len(message.content.split()) * 1.3
        
        def get_total_tokens(self, messages):
            """Get total estimated tokens for message list"""
            return sum(self.estimate_message_tokens(msg) for msg in messages)
        
        def manage_context(self, messages, max_tokens=3000):
            """Manage context to stay within token limits"""
            
            # Always keep system message
            system_messages = [msg for msg in messages if isinstance(msg, SystemMessage)]
            other_messages = [msg for msg in messages if not isinstance(msg, SystemMessage)]
            
            # Keep recent messages within limit
            managed_messages = system_messages.copy()
            current_tokens = sum(self.estimate_message_tokens(msg) for msg in system_messages)
            
            # Add messages from most recent backwards
            for message in reversed(other_messages):
                msg_tokens = self.estimate_message_tokens(message)
                if current_tokens + msg_tokens <= max_tokens:
                    managed_messages.insert(-len(system_messages) or len(managed_messages), message)
                    current_tokens += msg_tokens
                else:
                    break
            
            # Ensure proper order
            managed_messages.sort(key=lambda x: messages.index(x))
            
            return managed_messages
        
        def create_conversation_summary(self, messages):
            """Create summary of older conversation parts"""
            # Simple summarization (in production, use LLM)
            topics = []
            for msg in messages:
                if isinstance(msg, HumanMessage) and len(msg.content) > 20:
                    topics.append(msg.content[:30] + "...")
            
            return f"Previous conversation topics: {', '.join(topics[:3])}"
    
    # Test context management
    manager = ConversationContextManager()
    
    # Simulate long conversation
    long_conversation = [
        SystemMessage(content="You are a helpful coding assistant."),
        HumanMessage(content="What is Python?"),
        AIMessage(content="Python is a high-level programming language..."),
        HumanMessage(content="How do I install Python?"),
        AIMessage(content="You can install Python by downloading..."),
        HumanMessage(content="What are Python libraries?"),
        AIMessage(content="Python libraries are collections of modules..."),
        HumanMessage(content="Can you explain object-oriented programming?"),
        AIMessage(content="Object-oriented programming is a paradigm..."),
        HumanMessage(content="What is the difference between lists and tuples?")
    ]
    
    print("Context Management Test:")
    print(f"Original conversation: {len(long_conversation)} messages")
    
    total_tokens = manager.get_total_tokens(long_conversation)
    print(f"Estimated tokens: {total_tokens:.0f}")
    
    managed = manager.manage_context(long_conversation, max_tokens=500)
    managed_tokens = manager.get_total_tokens(managed)
    
    print(f"Managed conversation: {len(managed)} messages")
    print(f"Managed tokens: {managed_tokens:.0f}")
    print("✅ Context successfully managed within limits")
    
    print()

def demonstrate_conversation_memory_patterns():
    """Show different conversation memory patterns"""
    
    print("=== Conversation Memory Patterns ===\n")
    
    class ConversationMemory:
        """Different memory strategies for conversations"""
        
        def __init__(self, strategy="sliding_window"):
            self.strategy = strategy
            self.messages = []
            self.summary = ""
        
        def add_message(self, message):
            """Add message with memory management"""
            self.messages.append(message)
            self._apply_memory_strategy()
        
        def _apply_memory_strategy(self):
            """Apply selected memory strategy"""
            if self.strategy == "sliding_window":
                self._sliding_window_memory()
            elif self.strategy == "summary_buffer":
                self._summary_buffer_memory()
            elif self.strategy == "token_buffer":
                self._token_buffer_memory()
        
        def _sliding_window_memory(self, max_messages=8):
            """Keep only recent messages"""
            if len(self.messages) > max_messages:
                # Keep system message + recent messages
                system_msgs = [m for m in self.messages if isinstance(m, SystemMessage)]
                other_msgs = [m for m in self.messages if not isinstance(m, SystemMessage)]
                
                self.messages = system_msgs + other_msgs[-(max_messages-len(system_msgs)):]
        
        def _summary_buffer_memory(self, max_messages=6):
            """Summarize old messages, keep recent ones"""
            if len(self.messages) > max_messages:
                # Create summary of older messages
                old_messages = self.messages[:-max_messages//2]
                self.summary = f"Earlier conversation covered: {len(old_messages)} exchanges"
                self.messages = self.messages[-max_messages//2:]
        
        def _token_buffer_memory(self, max_tokens=1000):
            """Keep messages within token limit"""
            total_tokens = 0
            kept_messages = []
            
            # Count from most recent backwards
            for message in reversed(self.messages):
                msg_tokens = len(message.content.split()) * 1.3
                if total_tokens + msg_tokens <= max_tokens:
                    kept_messages.insert(0, message)
                    total_tokens += msg_tokens
                else:
                    break
            
            self.messages = kept_messages
        
        def get_context(self):
            """Get conversation context for model"""
            context = []
            if self.summary:
                context.append(SystemMessage(content=f"Context: {self.summary}"))
            context.extend(self.messages)
            return context
    
    # Test different memory strategies
    strategies = ["sliding_window", "summary_buffer", "token_buffer"]
    
    for strategy in strategies:
        print(f"Testing {strategy} memory:")
        
        memory = ConversationMemory(strategy=strategy)
        
        # Add multiple messages
        test_messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="What is machine learning?"),
            AIMessage(content="Machine learning is a subset of AI..."),
            HumanMessage(content="How does it work?"),
            AIMessage(content="It works by training algorithms on data..."),
            HumanMessage(content="What are the types?"),
            AIMessage(content="There are supervised, unsupervised..."),
            HumanMessage(content="Can you give examples?"),
            AIMessage(content="Examples include classification...")
        ]
        
        for msg in test_messages:
            memory.add_message(msg)
        
        context = memory.get_context()
        print(f"   Final context: {len(context)} messages")
        print(f"   Has summary: {bool(memory.summary)}")
        print()

def implement_conversation_state_tracking():
    """Implement conversation state and topic tracking"""
    
    print("=== Conversation State Tracking ===\n")
    
    class ConversationStateTracker:
        """Track conversation state and topics"""
        
        def __init__(self):
            self.current_topic = None
            self.conversation_stage = "greeting"
            self.user_preferences = {}
            self.conversation_history = []
        
        def analyze_message(self, message):
            """Analyze message for state updates"""
            content = message.content.lower()
            
            # Simple topic detection
            topics = {
                "python": ["python", "programming", "code"],
                "travel": ["travel", "vacation", "trip", "hotel"],
                "food": ["food", "restaurant", "recipe", "cooking"],
                "weather": ["weather", "temperature", "rain", "sunny"]
            }
            
            for topic, keywords in topics.items():
                if any(keyword in content for keyword in keywords):
                    if self.current_topic != topic:
                        self.current_topic = topic
                        return f"Topic changed to: {topic}"
            
            return "Topic unchanged"
        
        def update_conversation_stage(self, message_count):
            """Update conversation stage based on progress"""
            if message_count <= 2:
                self.conversation_stage = "greeting"
            elif message_count <= 6:
                self.conversation_stage = "information_gathering"
            elif message_count <= 10:
                self.conversation_stage = "detailed_discussion"
            else:
                self.conversation_stage = "conclusion"
        
        def get_state_summary(self):
            """Get current conversation state"""
            return {
                "topic": self.current_topic,
                "stage": self.conversation_stage,
                "message_count": len(self.conversation_history),
                "preferences": self.user_preferences
            }
    
    # Test state tracking
    tracker = ConversationStateTracker()
    
    test_conversation = [
        "Hello, I need help with something.",
        "I'm learning Python programming.",
        "Can you explain functions?",
        "How do I handle errors in Python?",
        "What about object-oriented programming?"
    ]
    
    print("State Tracking Demo:")
    for i, message in enumerate(test_conversation, 1):
        topic_change = tracker.analyze_message(HumanMessage(content=message))
        tracker.update_conversation_stage(i)
        tracker.conversation_history.append(message)
        
        state = tracker.get_state_summary()
        print(f"Turn {i}: {message[:30]}...")
        print(f"   State: {state}")
        print()

if __name__ == "__main__":
    print("Module 4.2: Multi-turn Conversations and Context Management\n")
    
    # Setup
    chat = setup_conversation_manager()
    
    # Demonstrations
    demonstrate_multi_turn_patterns(chat)
    implement_context_window_management()
    demonstrate_conversation_memory_patterns()
    implement_conversation_state_tracking()
    
    # Summary
    print("="*50)
    print("✅ Topic 4.2 Complete!")
    print("Key Takeaways:")
    print("• Multi-turn patterns enable rich conversations")
    print("• Context management prevents token limit issues")
    print("• Memory strategies optimize conversation flow")
    print("• State tracking enhances conversation quality")
    print("🚀 Ready for Topic 4.3: System Messages!")
    print("="*50)