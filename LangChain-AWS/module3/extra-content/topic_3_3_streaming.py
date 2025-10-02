"""
Topic 3.3: Streaming Responses and Token Management (6 minutes)

Learning Goals:
- Implement real-time streaming responses
- Optimize token usage and cost management
- Handle streaming errors and edge cases
- Build responsive user interfaces with streaming
"""

from langchain_aws.chat_models import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
import time
import asyncio

def setup_streaming_chat():
    """Initialize ChatBedrock for streaming examples"""
    
    print("=== Streaming Setup ===\n")
    
    try:
        chat = ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            model_kwargs={
                "max_tokens": 300,
                "temperature": 0.7
            }
        )
        
        print("✅ ChatBedrock initialized for streaming")
        return chat
        
    except Exception as e:
        print(f"❌ Streaming setup failed: {e}")
        return None

def demonstrate_basic_streaming(chat):
    """Show basic streaming implementation"""
    
    print("=== Basic Streaming ===\n")
    
    if not chat:
        print("❌ Chat not available")
        return
    
    message = HumanMessage(content="Explain the concept of machine learning step by step.")
    
    try:
        print("Streaming response:")
        print("🤖 Claude: ", end="", flush=True)
        
        full_response = ""
        chunk_count = 0
        start_time = time.time()
        
        # Stream the response
        for chunk in chat.stream([message]):
            if chunk.content:
                print(chunk.content, end="", flush=True)
                full_response += chunk.content
                chunk_count += 1
        
        end_time = time.time()
        
        print("\n")
        print(f"Streaming Stats:")
        print(f"   Total chunks: {chunk_count}")
        print(f"   Total time: {end_time - start_time:.2f}s")
        print(f"   Response length: {len(full_response)} characters")
        print(f"   Avg chunk size: {len(full_response) / chunk_count:.1f} chars")
        
    except Exception as e:
        print(f"❌ Basic streaming failed: {e}")
    
    print()

def demonstrate_streaming_with_processing(chat):
    """Show streaming with real-time processing"""
    
    print("=== Streaming with Processing ===\n")
    
    if not chat:
        print("❌ Chat not available")
        return
    
    message = HumanMessage(content="List 5 benefits of using Python for data science.")
    
    try:
        print("Processing stream in real-time:")
        
        buffer = ""
        sentences = []
        
        for chunk in chat.stream([message]):
            if chunk.content:
                buffer += chunk.content
                
                # Process complete sentences as they arrive
                while '.' in buffer:
                    sentence_end = buffer.find('.') + 1
                    sentence = buffer[:sentence_end].strip()
                    buffer = buffer[sentence_end:]
                    
                    if sentence:
                        sentences.append(sentence)
                        print(f"📝 Sentence {len(sentences)}: {sentence}")
        
        # Process remaining buffer
        if buffer.strip():
            sentences.append(buffer.strip())
            print(f"📝 Final: {buffer.strip()}")
        
        print(f"\nProcessed {len(sentences)} sentences in real-time")
        
    except Exception as e:
        print(f"❌ Streaming with processing failed: {e}")
    
    print()

def demonstrate_token_management():
    """Show token counting and cost estimation"""
    
    print("=== Token Management ===\n")
    
    def estimate_tokens(text):
        """Simple token estimation (rough approximation)"""
        return len(text.split()) * 1.3  # Approximate tokens per word
    
    def calculate_cost(input_tokens, output_tokens, model="claude-3-haiku"):
        """Calculate approximate cost"""
        # Approximate pricing (as of 2024)
        pricing = {
            "claude-3-haiku": {"input": 0.00025, "output": 0.00125}  # per 1K tokens
        }
        
        rates = pricing.get(model, pricing["claude-3-haiku"])
        input_cost = (input_tokens / 1000) * rates["input"]
        output_cost = (output_tokens / 1000) * rates["output"]
        
        return input_cost + output_cost
    
    # Example usage
    sample_inputs = [
        "What is Python?",
        "Explain machine learning algorithms in detail with examples and use cases.",
        "Write a comprehensive guide to web development including frontend, backend, databases, and deployment strategies."
    ]
    
    print("Token and Cost Estimation:")
    for i, input_text in enumerate(sample_inputs, 1):
        input_tokens = estimate_tokens(input_text)
        estimated_output = 150  # Assume average response length
        
        cost = calculate_cost(input_tokens, estimated_output)
        
        print(f"Query {i}:")
        print(f"   Input: '{input_text[:50]}...'")
        print(f"   Est. input tokens: {input_tokens:.0f}")
        print(f"   Est. output tokens: {estimated_output}")
        print(f"   Est. cost: ${cost:.6f}")
        print()

def demonstrate_streaming_error_handling(chat):
    """Show error handling for streaming responses"""
    
    print("=== Streaming Error Handling ===\n")
    
    def safe_stream(chat, messages, timeout=30):
        """Safe streaming with timeout and error handling"""
        
        try:
            start_time = time.time()
            chunks = []
            
            for chunk in chat.stream(messages):
                # Check timeout
                if time.time() - start_time > timeout:
                    print("⚠️ Streaming timeout reached")
                    break
                
                if chunk.content:
                    chunks.append(chunk.content)
                    print(".", end="", flush=True)
            
            print()
            return "".join(chunks)
            
        except Exception as e:
            print(f"❌ Streaming error: {e}")
            return None
    
    if chat:
        message = HumanMessage(content="Explain quantum computing briefly.")
        
        print("Testing safe streaming:")
        result = safe_stream(chat, [message])
        
        if result:
            print(f"✅ Safe streaming completed ({len(result)} chars)")
        else:
            print("❌ Safe streaming failed")
    else:
        print("❌ Chat not available for error handling test")
    
    print()

def demonstrate_streaming_ui_patterns():
    """Show UI patterns for streaming responses"""
    
    print("=== Streaming UI Patterns ===\n")
    
    class StreamingUI:
        """Simple streaming UI simulator"""
        
        def __init__(self):
            self.buffer = ""
            self.typing_indicator = True
        
        def add_chunk(self, chunk):
            """Add chunk to UI buffer"""
            self.buffer += chunk
            self.show_typing_indicator()
        
        def show_typing_indicator(self):
            """Simulate typing indicator"""
            if self.typing_indicator:
                print("💭 Claude is typing...", end="\r")
        
        def finalize_response(self):
            """Finalize the response display"""
            self.typing_indicator = False
            print(" " * 20, end="\r")  # Clear typing indicator
            print(f"🤖 Claude: {self.buffer}")
    
    # Simulate streaming UI
    ui = StreamingUI()
    
    # Simulate chunks arriving
    sample_chunks = [
        "Python is a ",
        "high-level programming ",
        "language known for ",
        "its simplicity and ",
        "readability."
    ]
    
    print("Simulating streaming UI:")
    for chunk in sample_chunks:
        ui.add_chunk(chunk)
        time.sleep(0.5)  # Simulate network delay
    
    ui.finalize_response()
    print()

def implement_streaming_best_practices():
    """Demonstrate streaming best practices"""
    
    print("=== Streaming Best Practices ===\n")
    
    practices = [
        {
            "category": "Performance",
            "tips": [
                "Use streaming for responses >100 tokens",
                "Implement client-side buffering",
                "Show typing indicators for better UX",
                "Handle network interruptions gracefully"
            ]
        },
        {
            "category": "Error Handling",
            "tips": [
                "Set reasonable timeouts (30-60 seconds)",
                "Implement retry logic for failed streams",
                "Validate chunks before processing",
                "Provide fallback to non-streaming mode"
            ]
        },
        {
            "category": "Cost Optimization",
            "tips": [
                "Monitor token usage in real-time",
                "Set max_tokens limits appropriately",
                "Cache responses when possible",
                "Use cheaper models for simple tasks"
            ]
        }
    ]
    
    for practice_group in practices:
        print(f"🎯 {practice_group['category']}:")
        for tip in practice_group['tips']:
            print(f"   • {tip}")
        print()

if __name__ == "__main__":
    print("Module 3.3: Streaming Responses and Token Management\n")
    
    # Setup
    chat = setup_streaming_chat()
    
    # Demonstrations
    demonstrate_basic_streaming(chat)
    demonstrate_streaming_with_processing(chat)
    demonstrate_token_management()
    demonstrate_streaming_error_handling(chat)
    demonstrate_streaming_ui_patterns()
    implement_streaming_best_practices()
    
    # Summary
    print("="*50)
    print("✅ Topic 3.3 Complete!")
    print("Key Takeaways:")
    print("• Streaming provides real-time user experience")
    print("• Token management is crucial for cost control")
    print("• Error handling ensures robust applications")
    print("• UI patterns enhance user engagement")
    print("🚀 Ready for Topic 3.4: Model Parameters!")
    print("="*50)