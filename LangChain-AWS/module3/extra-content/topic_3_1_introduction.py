"""
Topic 3.1: Introduction to ChatBedrock (6 minutes)

Learning Goals:
- Understand ChatBedrock architecture and benefits
- Master initialization patterns and configurations
- Learn supported models and their capabilities
- Establish best practices for production use
"""

from langchain_aws.chat_models import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import boto3
from botocore.exceptions import ClientError

def explore_chatbedrock_architecture():
    """Understand ChatBedrock design and benefits"""
    
    print("=== ChatBedrock Architecture ===\n")
    
    print("ChatBedrock Benefits:")
    print("• Unified LangChain interface for Bedrock models")
    print("• Automatic message formatting and parsing")
    print("• Built-in streaming and async support")
    print("• Seamless chain composition with LCEL")
    print("• Error handling and retry mechanisms\n")
    
    print("vs Direct Bedrock API:")
    print("• Direct API: Manual message formatting, custom parsing")
    print("• ChatBedrock: Automatic handling, LangChain integration")
    print("• Direct API: Custom streaming implementation")
    print("• ChatBedrock: Built-in streaming with standard interface\n")

def demonstrate_initialization_patterns():
    """Show different ChatBedrock initialization approaches"""
    
    print("=== Initialization Patterns ===\n")
    
    # Pattern 1: Basic initialization
    print("1. Basic Initialization:")
    try:
        basic_chat = ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1"
        )
        print("✅ Basic ChatBedrock initialized")
        print(f"   Model: {basic_chat.model_id}")
        print(f"   Region: {basic_chat.region_name}")
    except Exception as e:
        print(f"❌ Basic initialization failed: {e}")
    
    print()
    
    # Pattern 2: With model parameters
    print("2. With Model Parameters:")
    try:
        configured_chat = ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            model_kwargs={
                "max_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            }
        )
        print("✅ Configured ChatBedrock initialized")
        print(f"   Parameters: {configured_chat.model_kwargs}")
    except Exception as e:
        print(f"❌ Configured initialization failed: {e}")
    
    print()
    
    # Pattern 3: With custom client
    print("3. With Custom Boto3 Client:")
    try:
        custom_client = boto3.client(
            'bedrock-runtime',
            region_name='us-east-1'
        )
        
        client_chat = ChatBedrock(
            client=custom_client,
            model_id="anthropic.claude-3-haiku-20240307-v1:0"
        )
        print("✅ Custom client ChatBedrock initialized")
        print(f"   Client region: {custom_client.meta.region_name}")
    except Exception as e:
        print(f"❌ Custom client initialization failed: {e}")
    
    print()

def explore_supported_models():
    """Explore available models and their characteristics"""
    
    print("=== Supported Models ===\n")
    
    models = [
        {
            "id": "anthropic.claude-3-haiku-20240307-v1:0",
            "name": "Claude-3 Haiku",
            "strengths": "Fast, cost-effective, good for simple tasks",
            "use_cases": "Chat, basic Q&A, content generation"
        },
        {
            "id": "anthropic.claude-3-sonnet-20240229-v1:0", 
            "name": "Claude-3 Sonnet",
            "strengths": "Balanced performance and capability",
            "use_cases": "Complex reasoning, analysis, coding"
        },
        {
            "id": "amazon.titan-text-express-v1",
            "name": "Titan Text Express",
            "strengths": "AWS native, good performance",
            "use_cases": "Text generation, summarization"
        }
    ]
    
    for model in models:
        print(f"📦 {model['name']}")
        print(f"   ID: {model['id']}")
        print(f"   Strengths: {model['strengths']}")
        print(f"   Use Cases: {model['use_cases']}")
        print()

def test_basic_functionality():
    """Test basic ChatBedrock functionality"""
    
    print("=== Basic Functionality Test ===\n")
    
    try:
        # Initialize ChatBedrock
        chat = ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            model_kwargs={"max_tokens": 50}
        )
        
        # Test simple message
        message = HumanMessage(content="Say hello and introduce yourself briefly.")
        
        print("Sending test message...")
        response = chat.invoke([message])
        
        print("✅ ChatBedrock Response:")
        print(f"   Type: {type(response)}")
        print(f"   Content: {response.content}")
        print(f"   Length: {len(response.content)} characters")
        
        return chat
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"❌ AWS Error: {error_code}")
        if error_code == 'AccessDeniedException':
            print("   Solution: Request model access in AWS Console")
        return None
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return None

def demonstrate_message_types():
    """Show different message types and their usage"""
    
    print("=== Message Types ===\n")
    
    # Different message types
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="What is Python?"),
        AIMessage(content="Python is a programming language."),
        HumanMessage(content="Tell me more about its features.")
    ]
    
    print("Message Types in LangChain:")
    for i, msg in enumerate(messages, 1):
        print(f"{i}. {type(msg).__name__}: {msg.content[:50]}...")
    
    print("\nMessage Flow:")
    print("SystemMessage → Sets context and behavior")
    print("HumanMessage → User input")
    print("AIMessage → Assistant response (for conversation history)")
    print("HumanMessage → Follow-up user input")
    print()

def establish_best_practices():
    """Establish ChatBedrock best practices"""
    
    print("=== Best Practices ===\n")
    
    practices = [
        {
            "category": "Initialization",
            "practices": [
                "Always specify region explicitly",
                "Set reasonable token limits",
                "Use environment variables for sensitive config",
                "Initialize once, reuse instances"
            ]
        },
        {
            "category": "Error Handling", 
            "practices": [
                "Handle AccessDeniedException for model access",
                "Implement retry logic for transient errors",
                "Validate responses before processing",
                "Log errors for debugging"
            ]
        },
        {
            "category": "Performance",
            "practices": [
                "Choose appropriate model for task complexity",
                "Optimize token usage to control costs",
                "Use streaming for real-time applications",
                "Cache responses when appropriate"
            ]
        }
    ]
    
    for practice_group in practices:
        print(f"🎯 {practice_group['category']}:")
        for practice in practice_group['practices']:
            print(f"   • {practice}")
        print()

if __name__ == "__main__":
    print("Module 3.1: Introduction to ChatBedrock\n")
    
    explore_chatbedrock_architecture()
    demonstrate_initialization_patterns()
    explore_supported_models()
    
    # Test functionality
    chat_instance = test_basic_functionality()
    
    demonstrate_message_types()
    establish_best_practices()
    
    # Summary
    print("="*50)
    print("✅ Topic 3.1 Complete!")
    print("Key Takeaways:")
    print("• ChatBedrock provides unified LangChain interface")
    print("• Multiple initialization patterns for different needs")
    print("• Choose models based on task requirements")
    print("• Follow best practices for production deployment")
    
    if chat_instance:
        print("🚀 Ready for Topic 3.2: Chat Completion!")
    else:
        print("⚠️  Fix initialization issues before continuing")
    
    print("="*50)