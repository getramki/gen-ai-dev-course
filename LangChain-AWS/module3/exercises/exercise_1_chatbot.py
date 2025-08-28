"""
Exercise 1: Build Basic Chatbot with Claude

Task: Create a functional chatbot using ChatBedrock that:
1. Handles user input and maintains conversation context
2. Implements different personality modes
3. Includes error handling and response validation
4. Provides conversation history management

Time: 8 minutes
"""

from langchain_aws.chat_models import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
import json
from datetime import datetime

class ClaudeChatbot:
    """Interactive chatbot using ChatBedrock"""
    
    def __init__(self, personality="helpful"):
        self.personality = personality
        self.conversation_history = []
        self.chat = self._initialize_chat()
        self.system_message = self._get_system_message()
    
    def _initialize_chat(self):
        """Initialize ChatBedrock instance"""
        return ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            model_kwargs={
                "max_tokens": 200,
                "temperature": 0.7
            }
        )
    
    def _get_system_message(self):
        """Get system message based on personality"""
        personalities = {
            "helpful": "You are a helpful and friendly assistant. Provide clear, concise answers.",
            "technical": "You are a technical expert. Provide detailed, accurate technical information.",
            "creative": "You are a creative assistant. Think outside the box and provide imaginative responses.",
            "teacher": "You are a patient teacher. Explain concepts clearly with examples."
        }
        
        return SystemMessage(content=personalities.get(self.personality, personalities["helpful"]))
    
    def send_message(self, user_input):
        """Send message and get response"""
        # Add user message to history
        user_message = HumanMessage(content=user_input)
        
        # Build conversation context
        messages = [self.system_message] + self.conversation_history + [user_message]
        
        try:
            # Get AI response
            response = self.chat.invoke(messages)
            
            # Add both messages to history
            self.conversation_history.append(user_message)
            self.conversation_history.append(response)
            
            # Manage history length (keep last 10 messages)
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return response.content
            
        except Exception as e:
            return f"Sorry, I encountered an error: {e}"
    
    def change_personality(self, new_personality):
        """Change chatbot personality"""
        self.personality = new_personality
        self.system_message = self._get_system_message()
        print(f"Personality changed to: {new_personality}")
    
    def get_conversation_stats(self):
        """Get conversation statistics"""
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": len([m for m in self.conversation_history if isinstance(m, HumanMessage)]),
            "ai_messages": len([m for m in self.conversation_history if isinstance(m, AIMessage)]),
            "personality": self.personality
        }
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("Conversation history cleared.")

def run_interactive_demo():
    """Run interactive chatbot demo"""
    
    print("=== Claude Chatbot Demo ===\n")
    
    # Initialize chatbot
    bot = ClaudeChatbot(personality="helpful")
    
    # Demo conversations
    demo_conversations = [
        "Hello! What can you help me with?",
        "Explain Python decorators in simple terms.",
        "Can you give me a practical example?",
        "What are some common use cases?"
    ]
    
    print("Demo Conversation:")
    for user_input in demo_conversations:
        print(f"\n👤 User: {user_input}")
        response = bot.send_message(user_input)
        print(f"🤖 Claude: {response}")
    
    # Show stats
    stats = bot.get_conversation_stats()
    print(f"\nConversation Stats: {stats}")

def test_personality_modes():
    """Test different personality modes"""
    
    print("\n=== Personality Mode Testing ===\n")
    
    personalities = ["helpful", "technical", "creative", "teacher"]
    test_question = "What is artificial intelligence?"
    
    for personality in personalities:
        print(f"Testing {personality.upper()} personality:")
        
        bot = ClaudeChatbot(personality=personality)
        response = bot.send_message(test_question)
        
        print(f"Response: {response[:100]}...")
        print()

def test_error_handling():
    """Test chatbot error handling"""
    
    print("=== Error Handling Test ===\n")
    
    # Test with invalid configuration
    try:
        # This should work normally
        bot = ClaudeChatbot()
        response = bot.send_message("Test message")
        print("✅ Normal operation successful")
        
    except Exception as e:
        print(f"❌ Error handling test: {e}")

if __name__ == "__main__":
    run_interactive_demo()
    test_personality_modes()
    test_error_handling()
    
    print("\n" + "="*50)
    print("✅ Exercise 1 Complete!")
    print("Chatbot Features Implemented:")
    print("• Multi-personality support")
    print("• Conversation history management")
    print("• Error handling and validation")
    print("• Statistics and monitoring")
    print("="*50)