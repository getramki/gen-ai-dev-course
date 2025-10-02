"""
Topic 3.2: Basic Chat Completion with Claude (6 minutes)

Learning Goals:
- Master message handling and conversation patterns
- Implement effective prompt engineering techniques
- Process and validate responses properly
- Handle conversation context and memory
"""

from langchain_aws.chat_models import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
import json

def setup_chat_completion():
    """Initialize ChatBedrock for completion examples"""
    
    print("=== Chat Completion Setup ===\n")
    
    try:
        chat = ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            model_kwargs={
                "max_tokens": 150,
                "temperature": 0.7
            }
        )
        
        print("✅ ChatBedrock initialized for completion examples")
        return chat
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return None

def demonstrate_single_message_completion(chat):
    """Show simple single-message completion"""
    
    print("=== Single Message Completion ===\n")
    
    if not chat:
        print("❌ Chat not available")
        return
    
    # Simple completion
    message = HumanMessage(content="Explain machine learning in one paragraph.")
    
    try:
        response = chat.invoke([message])
        
        print("Input Message:")
        print(f"   {message.content}")
        print()
        
        print("Response:")
        print(f"   {response.content}")
        print()
        
        print("Response Metadata:")
        print(f"   Type: {type(response)}")
        print(f"   Length: {len(response.content)} characters")
        
    except Exception as e:
        print(f"❌ Single message completion failed: {e}")
    
    print()

def demonstrate_system_message_usage(chat):
    """Show how system messages influence responses"""
    
    print("=== System Message Usage ===\n")
    
    if not chat:
        print("❌ Chat not available")
        return
    
    # Test different system messages
    system_scenarios = [
        {
            "name": "Technical Expert",
            "system": "You are a senior software engineer with 10 years of experience.",
            "question": "What is the best way to handle errors in Python?"
        },
        {
            "name": "Beginner Teacher", 
            "system": "You are a patient teacher explaining concepts to beginners.",
            "question": "What is the best way to handle errors in Python?"
        }
    ]
    
    for scenario in system_scenarios:
        print(f"Scenario: {scenario['name']}")
        
        messages = [
            SystemMessage(content=scenario['system']),
            HumanMessage(content=scenario['question'])
        ]
        
        try:
            response = chat.invoke(messages)
            print(f"Response: {response.content[:100]}...")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        print()

def demonstrate_conversation_context(chat):
    """Show multi-turn conversation handling"""
    
    print("=== Conversation Context ===\n")
    
    if not chat:
        print("❌ Chat not available")
        return
    
    # Build conversation step by step
    conversation = [
        SystemMessage(content="You are a helpful Python tutor."),
        HumanMessage(content="What is a list in Python?")
    ]
    
    try:
        # First exchange
        response1 = chat.invoke(conversation)
        print("Turn 1:")
        print(f"Human: {conversation[1].content}")
        print(f"AI: {response1.content[:80]}...")
        print()
        
        # Add AI response and continue conversation
        conversation.append(AIMessage(content=response1.content))
        conversation.append(HumanMessage(content="Can you show me an example?"))
        
        response2 = chat.invoke(conversation)
        print("Turn 2:")
        print(f"Human: {conversation[3].content}")
        print(f"AI: {response2.content[:80]}...")
        print()
        
        print(f"Conversation length: {len(conversation)} messages")
        
    except Exception as e:
        print(f"❌ Conversation failed: {e}")

def demonstrate_prompt_templates(chat):
    """Show ChatPromptTemplate usage with ChatBedrock"""
    
    print("=== Prompt Templates ===\n")
    
    if not chat:
        print("❌ Chat not available")
        return
    
    # Create structured prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in {domain}. Provide {style} explanations."),
        ("human", "Explain {concept} with a practical example.")
    ])
    
    # Create chain
    chain = prompt | chat
    
    test_cases = [
        {
            "domain": "web development",
            "style": "concise",
            "concept": "REST APIs"
        },
        {
            "domain": "data science", 
            "style": "detailed",
            "concept": "machine learning"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"   Domain: {case['domain']}")
        print(f"   Style: {case['style']}")
        print(f"   Concept: {case['concept']}")
        
        try:
            response = chain.invoke(case)
            print(f"   Response: {response.content[:100]}...")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        print()

def demonstrate_response_processing():
    """Show response processing and validation techniques"""
    
    print("=== Response Processing ===\n")
    
    # Simulate different response types
    sample_responses = [
        AIMessage(content="Python is a high-level programming language."),
        AIMessage(content='{"language": "Python", "type": "interpreted"}'),
        AIMessage(content="Here are three key points:\n1. Easy syntax\n2. Large ecosystem\n3. Versatile applications")
    ]
    
    for i, response in enumerate(sample_responses, 1):
        print(f"Response {i} Processing:")
        
        # Basic validation
        if response.content:
            print(f"   ✅ Content present ({len(response.content)} chars)")
        else:
            print("   ❌ Empty content")
        
        # Check for JSON
        try:
            json.loads(response.content)
            print("   📄 Contains valid JSON")
        except json.JSONDecodeError:
            print("   📝 Plain text response")
        
        # Check for structured content
        if '\n' in response.content and any(char in response.content for char in ['1.', '2.', '3.']):
            print("   📋 Contains structured list")
        
        print(f"   Preview: {response.content[:50]}...")
        print()

def implement_error_handling_patterns():
    """Show error handling patterns for chat completion"""
    
    print("=== Error Handling Patterns ===\n")
    
    def safe_chat_invoke(chat, messages, max_retries=3):
        """Safe chat invocation with retry logic"""
        
        for attempt in range(max_retries):
            try:
                response = chat.invoke(messages)
                
                # Validate response
                if not response.content.strip():
                    raise ValueError("Empty response received")
                
                return response
                
            except Exception as e:
                print(f"   Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    print("   ❌ All retries exhausted")
                    return None
        
        return None
    
    print("Error Handling Features:")
    print("• Retry logic for transient failures")
    print("• Response validation")
    print("• Graceful degradation")
    print("• Detailed error logging")
    print()
    
    # Example usage
    try:
        chat = ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1"
        )
        
        message = HumanMessage(content="Test message")
        result = safe_chat_invoke(chat, [message])
        
        if result:
            print("✅ Safe invocation successful")
        else:
            print("❌ Safe invocation failed after retries")
            
    except Exception as e:
        print(f"❌ Error handling demo failed: {e}")

if __name__ == "__main__":
    print("Module 3.2: Basic Chat Completion with Claude\n")
    
    # Setup
    chat = setup_chat_completion()
    
    # Demonstrations
    demonstrate_single_message_completion(chat)
    demonstrate_system_message_usage(chat)
    demonstrate_conversation_context(chat)
    demonstrate_prompt_templates(chat)
    demonstrate_response_processing()
    implement_error_handling_patterns()
    
    # Summary
    print("="*50)
    print("✅ Topic 3.2 Complete!")
    print("Key Takeaways:")
    print("• System messages shape AI behavior and responses")
    print("• Conversation context enables multi-turn interactions")
    print("• Prompt templates provide structured, reusable patterns")
    print("• Response validation and error handling are essential")
    print("🚀 Ready for Topic 3.3: Streaming Responses!")
    print("="*50)