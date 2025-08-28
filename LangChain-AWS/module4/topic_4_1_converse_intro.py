"""
Topic 4.1: Introduction to ChatBedrockConverse (6 minutes)

Learning Goals:
- Understand ChatBedrockConverse enhanced features
- Master initialization and configuration differences
- Learn conversation-specific optimizations
- Establish when to use ChatBedrockConverse vs ChatBedrock
"""

from langchain_aws.chat_models import ChatBedrock, ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import time

def explore_chatbedrockconverse_features():
    """Understand ChatBedrockConverse enhanced capabilities"""
    
    print("=== ChatBedrockConverse Features ===\n")
    
    print("Enhanced Conversation Features:")
    print("• Native multi-turn conversation support")
    print("• Improved context window management")
    print("• Better conversation state handling")
    print("• Enhanced system message processing")
    print("• Optimized for dialogue applications\n")
    
    print("Key Differences from ChatBedrock:")
    print("• Direct parameter specification (no model_kwargs)")
    print("• Enhanced conversation memory handling")
    print("• Better performance for multi-turn dialogues")
    print("• Simplified configuration for chat applications")
    print("• Native support for conversation patterns\n")

def demonstrate_initialization_differences():
    """Show initialization differences between ChatBedrock and ChatBedrockConverse"""
    
    print("=== Initialization Comparison ===\n")
    
    # ChatBedrock initialization
    print("1. ChatBedrock Initialization:")
    try:
        chatbedrock = ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            model_kwargs={
                "max_tokens": 200,
                "temperature": 0.7
            }
        )
        print("✅ ChatBedrock initialized")
        print(f"   Parameters in model_kwargs: {chatbedrock.model_kwargs}")
    except Exception as e:
        print(f"❌ ChatBedrock failed: {e}")
    
    print()
    
    # ChatBedrockConverse initialization
    print("2. ChatBedrockConverse Initialization:")
    try:
        chatconverse = ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=200,
            temperature=0.7
        )
        print("✅ ChatBedrockConverse initialized")
        print(f"   Direct parameters: max_tokens={chatconverse.max_tokens}, temperature={chatconverse.temperature}")
    except Exception as e:
        print(f"❌ ChatBedrockConverse failed: {e}")
    
    print()

def test_basic_conversation_capabilities():
    """Test basic conversation capabilities of ChatBedrockConverse"""
    
    print("=== Basic Conversation Test ===\n")
    
    try:
        chat = ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=150,
            temperature=0.7
        )
        
        # Simple conversation test
        messages = [
            SystemMessage(content="You are a helpful programming tutor."),
            HumanMessage(content="What is Python?")
        ]
        
        print("Testing basic conversation:")
        print(f"System: {messages[0].content}")
        print(f"Human: {messages[1].content}")
        
        response = chat.invoke(messages)
        print(f"Assistant: {response.content[:100]}...")
        
        return chat
        
    except Exception as e:
        print(f"❌ Basic conversation test failed: {e}")
        return None

def demonstrate_conversation_context_handling():
    """Show how ChatBedrockConverse handles conversation context"""
    
    print("=== Conversation Context Handling ===\n")
    
    try:
        chat = ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=100,
            temperature=0.6
        )
        
        # Build conversation step by step
        conversation = [
            SystemMessage(content="You are a helpful assistant specializing in technology."),
            HumanMessage(content="What is machine learning?")
        ]
        
        # First exchange
        response1 = chat.invoke(conversation)
        print("Turn 1:")
        print(f"Human: {conversation[1].content}")
        print(f"AI: {response1.content[:80]}...")
        
        # Add response and continue
        conversation.append(AIMessage(content=response1.content))
        conversation.append(HumanMessage(content="Can you give me a practical example?"))
        
        response2 = chat.invoke(conversation)
        print("\nTurn 2:")
        print(f"Human: {conversation[3].content}")
        print(f"AI: {response2.content[:80]}...")
        
        # Add another turn
        conversation.append(AIMessage(content=response2.content))
        conversation.append(HumanMessage(content="How do I get started learning it?"))
        
        response3 = chat.invoke(conversation)
        print("\nTurn 3:")
        print(f"Human: {conversation[5].content}")
        print(f"AI: {response3.content[:80]}...")
        
        print(f"\nConversation length: {len(conversation)} messages")
        print("✅ Context maintained across multiple turns")
        
    except Exception as e:
        print(f"❌ Context handling test failed: {e}")
    
    print()

def explore_configuration_options():
    """Explore ChatBedrockConverse configuration options"""
    
    print("=== Configuration Options ===\n")
    
    configurations = [
        {
            "name": "Conservative Chat",
            "params": {
                "max_tokens": 100,
                "temperature": 0.2,
                "top_p": 0.9
            },
            "use_case": "Factual Q&A, customer support"
        },
        {
            "name": "Balanced Conversation",
            "params": {
                "max_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            },
            "use_case": "General chat, tutoring"
        },
        {
            "name": "Creative Dialogue",
            "params": {
                "max_tokens": 300,
                "temperature": 0.8,
                "top_p": 0.95
            },
            "use_case": "Creative writing, brainstorming"
        }
    ]
    
    for config in configurations:
        print(f"Configuration: {config['name']}")
        print(f"   Parameters: {config['params']}")
        print(f"   Use Case: {config['use_case']}")
        
        try:
            chat = ChatBedrockConverse(
                model_id="anthropic.claude-3-haiku-20240307-v1:0",
                region_name="us-east-1",
                **config['params']
            )
            print("   ✅ Configuration valid")
            
        except Exception as e:
            print(f"   ❌ Configuration failed: {e}")
        
        print()

def demonstrate_streaming_with_converse():
    """Show streaming capabilities with ChatBedrockConverse"""
    
    print("=== Streaming with ChatBedrockConverse ===\n")
    
    try:
        chat = ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=200,
            temperature=0.7
        )
        
        message = HumanMessage(content="Explain the benefits of using ChatBedrockConverse for conversation applications.")
        
        print("Streaming response:")
        print("🤖 Assistant: ", end="", flush=True)
        
        chunk_count = 0
        start_time = time.time()
        
        for chunk in chat.stream([message]):
            if chunk.content:
                print(chunk.content, end="", flush=True)
                chunk_count += 1
        
        end_time = time.time()
        
        print(f"\n\nStreaming stats:")
        print(f"   Chunks: {chunk_count}")
        print(f"   Duration: {end_time - start_time:.2f}s")
        print("   ✅ Streaming works seamlessly")
        
    except Exception as e:
        print(f"❌ Streaming test failed: {e}")
    
    print()

def establish_usage_guidelines():
    """Establish when to use ChatBedrockConverse"""
    
    print("=== Usage Guidelines ===\n")
    
    guidelines = {
        "Use ChatBedrockConverse When": [
            "Building conversational applications",
            "Need enhanced multi-turn dialogue support",
            "Require simplified parameter configuration",
            "Focus on chat-specific optimizations",
            "Want better conversation state management"
        ],
        "Use ChatBedrock When": [
            "Need maximum control over API parameters",
            "Building non-conversational applications",
            "Require custom model configurations",
            "Working with streaming-heavy applications",
            "Need compatibility with older LangChain versions"
        ],
        "Best Practices": [
            "Choose based on application type, not performance",
            "Test both for your specific use case",
            "Consider team familiarity and preferences",
            "Evaluate configuration complexity needs",
            "Plan for future feature requirements"
        ]
    }
    
    for category, items in guidelines.items():
        print(f"🎯 {category}:")
        for item in items:
            print(f"   • {item}")
        print()

if __name__ == "__main__":
    print("Module 4.1: Introduction to ChatBedrockConverse\n")
    
    # Demonstrations
    explore_chatbedrockconverse_features()
    demonstrate_initialization_differences()
    
    # Test functionality
    chat_instance = test_basic_conversation_capabilities()
    
    demonstrate_conversation_context_handling()
    explore_configuration_options()
    demonstrate_streaming_with_converse()
    establish_usage_guidelines()
    
    # Summary
    print("="*50)
    print("✅ Topic 4.1 Complete!")
    print("Key Takeaways:")
    print("• ChatBedrockConverse optimized for conversations")
    print("• Direct parameter specification (no model_kwargs)")
    print("• Enhanced context and state management")
    print("• Choose based on application requirements")
    
    if chat_instance:
        print("🚀 Ready for Topic 4.2: Multi-turn Conversations!")
    else:
        print("⚠️  Fix initialization issues before continuing")
    
    print("="*50)