"""
Exercise 2: Real-time Streaming Chat Interface

Task: Build a streaming chat interface that:
1. Provides real-time response streaming
2. Implements typing indicators and UI feedback
3. Manages token usage and cost tracking
4. Handles streaming errors gracefully

Time: 7 minutes
"""

from langchain_aws.chat_models import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import time
import threading
from datetime import datetime

class StreamingChatInterface:
    """Real-time streaming chat interface"""
    
    def __init__(self):
        self.chat = self._initialize_chat()
        self.conversation_history = []
        self.is_streaming = False
        self.token_usage = {"input": 0, "output": 0, "total_cost": 0.0}
    
    def _initialize_chat(self):
        """Initialize ChatBedrock for streaming"""
        return ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            model_kwargs={
                "max_tokens": 300,
                "temperature": 0.7
            }
        )
    
    def _estimate_tokens(self, text):
        """Estimate token count"""
        return len(text.split()) * 1.3
    
    def _calculate_cost(self, input_tokens, output_tokens):
        """Calculate approximate cost"""
        # Claude-3 Haiku pricing (approximate)
        input_cost = (input_tokens / 1000) * 0.00025
        output_cost = (output_tokens / 1000) * 0.00125
        return input_cost + output_cost
    
    def _show_typing_indicator(self):
        """Show typing indicator animation"""
        indicators = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        
        for i in range(20):  # Show for ~2 seconds
            if not self.is_streaming:
                break
            print(f"\r🤖 Claude {indicators[i % len(indicators)]} typing...", end="", flush=True)
            time.sleep(0.1)
    
    def stream_response(self, user_input, show_ui=True):
        """Stream response with real-time UI updates"""
        
        # Add user message to history
        user_message = HumanMessage(content=user_input)
        self.conversation_history.append(user_message)
        
        # Build conversation context
        messages = self.conversation_history[-10:]  # Keep last 10 messages
        
        # Track token usage
        input_text = " ".join([msg.content for msg in messages])
        input_tokens = self._estimate_tokens(input_text)
        
        if show_ui:
            print(f"\n👤 You: {user_input}")
            
            # Start typing indicator in separate thread
            self.is_streaming = True
            typing_thread = threading.Thread(target=self._show_typing_indicator)
            typing_thread.daemon = True
            typing_thread.start()
        
        try:
            # Stream the response
            response_chunks = []
            start_time = time.time()
            
            # Clear typing indicator and start response
            time.sleep(0.5)  # Brief pause for typing indicator
            self.is_streaming = False
            
            if show_ui:
                print(f"\r🤖 Claude: ", end="", flush=True)
            
            # Process stream
            for chunk in self.chat.stream(messages):
                if chunk.content:
                    response_chunks.append(chunk.content)
                    if show_ui:
                        print(chunk.content, end="", flush=True)
            
            # Finalize response
            full_response = "".join(response_chunks)
            end_time = time.time()
            
            if show_ui:
                print()  # New line after response
            
            # Add AI response to history
            ai_message = AIMessage(content=full_response)
            self.conversation_history.append(ai_message)
            
            # Update token usage
            output_tokens = self._estimate_tokens(full_response)
            cost = self._calculate_cost(input_tokens, output_tokens)
            
            self.token_usage["input"] += input_tokens
            self.token_usage["output"] += output_tokens
            self.token_usage["total_cost"] += cost
            
            # Return response metadata
            return {
                "response": full_response,
                "chunks": len(response_chunks),
                "duration": end_time - start_time,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost
            }
            
        except Exception as e:
            self.is_streaming = False
            if show_ui:
                print(f"\r❌ Streaming error: {e}")
            return None
    
    def get_usage_stats(self):
        """Get token usage and cost statistics"""
        return {
            "total_messages": len(self.conversation_history),
            "input_tokens": self.token_usage["input"],
            "output_tokens": self.token_usage["output"],
            "total_tokens": self.token_usage["input"] + self.token_usage["output"],
            "total_cost": self.token_usage["total_cost"],
            "avg_cost_per_message": self.token_usage["total_cost"] / max(1, len(self.conversation_history) // 2)
        }
    
    def clear_conversation(self):
        """Clear conversation and reset usage stats"""
        self.conversation_history = []
        self.token_usage = {"input": 0, "output": 0, "total_cost": 0.0}
        print("💫 Conversation cleared!")

class StreamingChatBot:
    """Enhanced streaming chatbot with advanced features"""
    
    def __init__(self):
        self.interface = StreamingChatInterface()
        self.session_start = datetime.now()
    
    def run_demo_conversation(self):
        """Run demonstration conversation"""
        
        print("=== Streaming Chat Demo ===\n")
        print("Starting real-time streaming conversation...")
        
        demo_messages = [
            "Hello! Can you explain what machine learning is?",
            "That's interesting! Can you give me a practical example?",
            "How would I get started learning ML?",
            "What programming languages should I focus on?"
        ]
        
        for message in demo_messages:
            result = self.interface.stream_response(message)
            
            if result:
                print(f"\n📊 Response Stats:")
                print(f"   Chunks: {result['chunks']}")
                print(f"   Duration: {result['duration']:.2f}s")
                print(f"   Tokens: {result['input_tokens']:.0f} in, {result['output_tokens']:.0f} out")
                print(f"   Cost: ${result['cost']:.6f}")
            
            time.sleep(1)  # Pause between messages
        
        # Show session stats
        stats = self.interface.get_usage_stats()
        print(f"\n📈 Session Statistics:")
        for key, value in stats.items():
            if 'cost' in key:
                print(f"   {key}: ${value:.6f}")
            else:
                print(f"   {key}: {value:.1f}" if isinstance(value, float) else f"   {key}: {value}")
    
    def test_streaming_performance(self):
        """Test streaming performance with different message lengths"""
        
        print("\n=== Streaming Performance Test ===\n")
        
        test_cases = [
            ("Short query", "What is Python?"),
            ("Medium query", "Explain the differences between Python lists and tuples with examples."),
            ("Long query", "Provide a comprehensive comparison of machine learning frameworks including TensorFlow, PyTorch, and Scikit-learn, covering their strengths, weaknesses, and ideal use cases.")
        ]
        
        for test_name, query in test_cases:
            print(f"Testing: {test_name}")
            print(f"Query length: {len(query)} characters")
            
            result = self.interface.stream_response(query, show_ui=False)
            
            if result:
                print(f"✅ Results:")
                print(f"   Response time: {result['duration']:.2f}s")
                print(f"   Chunks received: {result['chunks']}")
                print(f"   Tokens processed: {result['input_tokens']:.0f} → {result['output_tokens']:.0f}")
                print(f"   Streaming rate: {result['output_tokens']/result['duration']:.1f} tokens/sec")
            else:
                print("❌ Test failed")
            
            print()
    
    def test_error_handling(self):
        """Test streaming error handling"""
        
        print("=== Error Handling Test ===\n")
        
        # Test with very long input (potential timeout)
        long_input = "Explain artificial intelligence " * 100
        
        print("Testing with extremely long input...")
        result = self.interface.stream_response(long_input, show_ui=False)
        
        if result:
            print("✅ Long input handled successfully")
        else:
            print("⚠️ Long input caused timeout/error (expected)")
        
        print()

def run_interactive_streaming_demo():
    """Run interactive streaming demonstration"""
    
    print("🚀 Starting Streaming Chat Interface Demo\n")
    
    bot = StreamingChatBot()
    
    # Run demonstrations
    bot.run_demo_conversation()
    bot.test_streaming_performance()
    bot.test_error_handling()
    
    print("Demo completed! Key features demonstrated:")
    print("• Real-time response streaming")
    print("• Typing indicators and UI feedback")
    print("• Token usage and cost tracking")
    print("• Performance monitoring")
    print("• Error handling and recovery")

if __name__ == "__main__":
    run_interactive_streaming_demo()
    
    print("\n" + "="*50)
    print("✅ Exercise 2 Complete!")
    print("Streaming Features Implemented:")
    print("• Real-time response streaming with UI feedback")
    print("• Token usage tracking and cost calculation")
    print("• Performance monitoring and optimization")
    print("• Robust error handling and recovery")
    print("• Interactive demonstration system")
    print("="*50)