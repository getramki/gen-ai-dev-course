"""
Exercise 1: Multi-turn Conversation Manager

Task: Build an advanced conversation management system that:
1. Handles complex multi-turn dialogues with context preservation
2. Implements intelligent memory management strategies
3. Tracks conversation state and topics dynamically
4. Provides conversation analytics and insights

Time: 8 minutes
"""

from langchain_aws.chat_models import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from datetime import datetime
from typing import List, Dict, Optional
import json

class AdvancedConversationManager:
    """Sophisticated conversation management system"""
    
    def __init__(self, memory_strategy="adaptive", max_context_tokens=2000):
        self.chat = self._initialize_chat()
        self.memory_strategy = memory_strategy
        self.max_context_tokens = max_context_tokens
        
        # Conversation state
        self.messages = []
        self.conversation_summary = ""
        self.current_topic = None
        self.conversation_stage = "initial"
        self.user_profile = {}
        
        # Analytics
        self.conversation_stats = {
            "start_time": datetime.now(),
            "turn_count": 0,
            "topics_discussed": [],
            "total_tokens_used": 0
        }
    
    def _initialize_chat(self):
        """Initialize ChatBedrockConverse"""
        return ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=250,
            temperature=0.7
        )
    
    def _estimate_tokens(self, text):
        """Estimate token count for text"""
        return len(text.split()) * 1.3
    
    def _get_total_context_tokens(self, messages):
        """Calculate total tokens in message context"""
        return sum(self._estimate_tokens(msg.content) for msg in messages)
    
    def _detect_topic(self, message_content):
        """Detect conversation topic from message content"""
        content_lower = message_content.lower()
        
        topic_keywords = {
            "technology": ["python", "programming", "code", "software", "ai", "machine learning"],
            "travel": ["travel", "vacation", "trip", "hotel", "flight", "destination"],
            "health": ["health", "fitness", "exercise", "diet", "medical", "wellness"],
            "education": ["learn", "study", "course", "school", "university", "education"],
            "business": ["business", "work", "job", "career", "company", "startup"],
            "entertainment": ["movie", "music", "game", "book", "show", "entertainment"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return topic
        
        return "general"
    
    def _update_conversation_stage(self):
        """Update conversation stage based on turn count and content"""
        turn_count = self.conversation_stats["turn_count"]
        
        if turn_count <= 1:
            self.conversation_stage = "greeting"
        elif turn_count <= 3:
            self.conversation_stage = "topic_establishment"
        elif turn_count <= 8:
            self.conversation_stage = "deep_discussion"
        elif turn_count <= 12:
            self.conversation_stage = "problem_solving"
        else:
            self.conversation_stage = "conclusion"
    
    def _apply_memory_strategy(self):
        """Apply selected memory management strategy"""
        if self.memory_strategy == "adaptive":
            self._adaptive_memory_management()
        elif self.memory_strategy == "sliding_window":
            self._sliding_window_memory()
        elif self.memory_strategy == "summary_buffer":
            self._summary_buffer_memory()
    
    def _adaptive_memory_management(self):
        """Adaptive memory management based on context and tokens"""
        total_tokens = self._get_total_context_tokens(self.messages)
        
        if total_tokens > self.max_context_tokens:
            # Use different strategies based on conversation stage
            if self.conversation_stage in ["greeting", "topic_establishment"]:
                self._sliding_window_memory(max_messages=6)
            elif self.conversation_stage == "deep_discussion":
                self._summary_buffer_memory()
            else:
                self._token_based_trimming()
    
    def _sliding_window_memory(self, max_messages=8):
        """Keep only recent messages"""
        if len(self.messages) > max_messages:
            # Always preserve system messages
            system_msgs = [m for m in self.messages if isinstance(m, SystemMessage)]
            other_msgs = [m for m in self.messages if not isinstance(m, SystemMessage)]
            
            keep_count = max_messages - len(system_msgs)
            self.messages = system_msgs + other_msgs[-keep_count:]
    
    def _summary_buffer_memory(self):
        """Create summary of older messages"""
        if len(self.messages) > 8:
            # Summarize older half, keep recent half
            mid_point = len(self.messages) // 2
            old_messages = self.messages[:mid_point]
            
            # Create simple summary
            topics = set()
            for msg in old_messages:
                if isinstance(msg, HumanMessage):
                    topic = self._detect_topic(msg.content)
                    topics.add(topic)
            
            self.conversation_summary = f"Earlier discussion covered: {', '.join(topics)}"
            self.messages = self.messages[mid_point:]
    
    def _token_based_trimming(self):
        """Trim messages based on token count"""
        target_tokens = self.max_context_tokens * 0.8  # Leave some buffer
        
        # Keep messages from most recent backwards
        kept_messages = []
        current_tokens = 0
        
        for message in reversed(self.messages):
            msg_tokens = self._estimate_tokens(message.content)
            if current_tokens + msg_tokens <= target_tokens:
                kept_messages.insert(0, message)
                current_tokens += msg_tokens
            elif isinstance(message, SystemMessage):
                # Always keep system messages
                kept_messages.insert(0, message)
        
        self.messages = kept_messages
    
    def send_message(self, user_input, system_context=None):
        """Send message and get response with full conversation management"""
        
        # Create user message
        user_message = HumanMessage(content=user_input)
        
        # Update conversation analytics
        self.conversation_stats["turn_count"] += 1
        
        # Detect and track topic
        detected_topic = self._detect_topic(user_input)
        if detected_topic != self.current_topic:
            self.current_topic = detected_topic
            if detected_topic not in self.conversation_stats["topics_discussed"]:
                self.conversation_stats["topics_discussed"].append(detected_topic)
        
        # Update conversation stage
        self._update_conversation_stage()
        
        # Add user message to conversation
        self.messages.append(user_message)
        
        # Apply memory management
        self._apply_memory_strategy()
        
        # Prepare context for model
        context_messages = []
        
        # Add summary if available
        if self.conversation_summary:
            context_messages.append(SystemMessage(content=f"Context: {self.conversation_summary}"))
        
        # Add system context if provided
        if system_context:
            context_messages.append(SystemMessage(content=system_context))
        
        # Add conversation messages
        context_messages.extend(self.messages)
        
        try:
            # Get AI response
            response = self.chat.invoke(context_messages)
            
            # Add AI response to conversation
            ai_message = AIMessage(content=response.content)
            self.messages.append(ai_message)
            
            # Update token usage
            context_tokens = self._get_total_context_tokens(context_messages)
            response_tokens = self._estimate_tokens(response.content)
            self.conversation_stats["total_tokens_used"] += context_tokens + response_tokens
            
            return {
                "response": response.content,
                "topic": self.current_topic,
                "stage": self.conversation_stage,
                "context_tokens": context_tokens,
                "response_tokens": response_tokens
            }
            
        except Exception as e:
            return {"error": f"Conversation failed: {e}"}
    
    def get_conversation_analytics(self):
        """Get comprehensive conversation analytics"""
        duration = datetime.now() - self.conversation_stats["start_time"]
        
        return {
            "conversation_stats": self.conversation_stats,
            "current_state": {
                "topic": self.current_topic,
                "stage": self.conversation_stage,
                "message_count": len(self.messages),
                "has_summary": bool(self.conversation_summary)
            },
            "performance": {
                "duration_minutes": duration.total_seconds() / 60,
                "avg_tokens_per_turn": self.conversation_stats["total_tokens_used"] / max(1, self.conversation_stats["turn_count"]),
                "memory_strategy": self.memory_strategy
            }
        }
    
    def export_conversation(self, filename=None):
        """Export conversation to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        export_data = {
            "conversation_id": timestamp,
            "analytics": self.get_conversation_analytics(),
            "messages": [
                {
                    "type": type(msg).__name__,
                    "content": msg.content,
                    "timestamp": datetime.now().isoformat()
                }
                for msg in self.messages
            ],
            "summary": self.conversation_summary
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            return f"Conversation exported to {filename}"
        except Exception as e:
            return f"Export failed: {e}"

def run_conversation_demo():
    """Run comprehensive conversation management demo"""
    
    print("=== Advanced Conversation Manager Demo ===\n")
    
    # Initialize conversation manager
    manager = AdvancedConversationManager(memory_strategy="adaptive")
    
    # Demo conversation with various topics
    demo_messages = [
        "Hello! I'm interested in learning about artificial intelligence.",
        "What programming languages should I focus on for AI development?",
        "I've heard Python is popular. Can you explain why?",
        "What about machine learning frameworks? Which ones are best?",
        "How long does it typically take to become proficient in ML?",
        "Are there any good online courses you'd recommend?",
        "What about practical projects to build a portfolio?",
        "Should I focus on a specific domain like computer vision or NLP?",
        "What's the job market like for AI developers?",
        "Any tips for someone just starting their AI journey?"
    ]
    
    print("Starting conversation with topic transitions and memory management...\n")
    
    for i, message in enumerate(demo_messages, 1):
        print(f"👤 User (Turn {i}): {message}")
        
        result = manager.send_message(message)
        
        if "error" in result:
            print(f"❌ {result['error']}")
            continue
        
        print(f"🤖 Assistant: {result['response'][:100]}...")
        print(f"📊 Topic: {result['topic']} | Stage: {result['stage']} | Tokens: {result['context_tokens']}→{result['response_tokens']}")
        print()
    
    # Show final analytics
    analytics = manager.get_conversation_analytics()
    print("📈 Final Conversation Analytics:")
    print(f"   Duration: {analytics['performance']['duration_minutes']:.1f} minutes")
    print(f"   Total turns: {analytics['conversation_stats']['turn_count']}")
    print(f"   Topics discussed: {analytics['conversation_stats']['topics_discussed']}")
    print(f"   Final stage: {analytics['current_state']['stage']}")
    print(f"   Total tokens: {analytics['conversation_stats']['total_tokens_used']:.0f}")
    print(f"   Avg tokens/turn: {analytics['performance']['avg_tokens_per_turn']:.0f}")
    
    # Export conversation
    export_result = manager.export_conversation()
    print(f"💾 {export_result}")

def test_memory_strategies():
    """Test different memory management strategies"""
    
    print("\n=== Memory Strategy Comparison ===\n")
    
    strategies = ["adaptive", "sliding_window", "summary_buffer"]
    
    for strategy in strategies:
        print(f"Testing {strategy} strategy:")
        
        manager = AdvancedConversationManager(memory_strategy=strategy, max_context_tokens=800)
        
        # Simulate long conversation
        for i in range(12):
            message = f"This is test message number {i+1} about various topics including technology and programming."
            result = manager.send_message(message)
            
            if "error" not in result:
                analytics = manager.get_conversation_analytics()
                print(f"   Turn {i+1}: {analytics['current_state']['message_count']} messages, "
                      f"Stage: {analytics['current_state']['stage']}")
        
        final_analytics = manager.get_conversation_analytics()
        print(f"   Final: {final_analytics['conversation_stats']['total_tokens_used']:.0f} tokens used")
        print()

if __name__ == "__main__":
    run_conversation_demo()
    test_memory_strategies()
    
    print("\n" + "="*50)
    print("✅ Exercise 1 Complete!")
    print("Advanced Features Implemented:")
    print("• Intelligent multi-turn conversation management")
    print("• Adaptive memory strategies with token optimization")
    print("• Dynamic topic detection and conversation staging")
    print("• Comprehensive analytics and conversation export")
    print("• Production-ready error handling and monitoring")
    print("="*50)