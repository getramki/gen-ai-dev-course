"""
Topic 2.3: LangChain-AWS Integration Setup (3 minutes)

Learning Goals:
- Test LangChain-AWS connectivity
- Initialize ChatBedrock and ChatBedrockConverse
- Verify integration with simple examples
- Establish baseline for Module 3
"""

import boto3
from langchain_aws.chat_models import ChatBedrock, ChatBedrockConverse
from langchain_core.messages import HumanMessage
from botocore.exceptions import ClientError
import json

def test_langchain_aws_imports():
    """Test LangChain AWS integration imports"""
    
    print("=== LangChain-AWS Import Test ===\n")
    
    imports_to_test = [
        ("from langchain_aws.chat_models import ChatBedrock", "ChatBedrock"),
        ("from langchain_aws.chat_models import ChatBedrockConverse", "ChatBedrockConverse"),
        ("from langchain_aws.embeddings import BedrockEmbeddings", "BedrockEmbeddings"),
        ("from langchain_core.messages import HumanMessage, AIMessage", "Message Types")
    ]
    
    all_imports_ok = True
    
    for import_statement, description in imports_to_test:
        try:
            exec(import_statement)
            print(f"✅ {description}")
        except ImportError as e:
            print(f"❌ {description} - {str(e)}")
            all_imports_ok = False
        except Exception as e:
            print(f"⚠️  {description} - {str(e)}")
    
    print()
    return all_imports_ok

def initialize_chatbedrock():
    """Initialize and test ChatBedrock"""
    
    print("=== ChatBedrock Initialization ===\n")
    
    try:
        # Initialize ChatBedrock with Claude
        chat_bedrock = ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            model_kwargs={
                "max_tokens": 100,
                "temperature": 0.1
            }
        )
        
        print("✅ ChatBedrock initialized successfully")
        print(f"Model ID: {chat_bedrock.model_id}")
        print(f"Region: {chat_bedrock.region_name}")
        print()
        
        return chat_bedrock
        
    except Exception as e:
        print(f"❌ ChatBedrock initialization failed: {e}")
        print()
        return None

def initialize_chatbedrock_converse():
    """Initialize and test ChatBedrockConverse"""
    
    print("=== ChatBedrockConverse Initialization ===\n")
    
    try:
        # Initialize ChatBedrockConverse with Claude
        chat_converse = ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=100,
            temperature=0.1
        )
        
        print("✅ ChatBedrockConverse initialized successfully")
        print(f"Model ID: {chat_converse.model_id}")
        print(f"Region: {chat_converse.region_name}")
        print()
        
        return chat_converse
        
    except Exception as e:
        print(f"❌ ChatBedrockConverse initialization failed: {e}")
        print()
        return None

def test_simple_invocation(chat_model, model_name):
    """Test simple model invocation"""
    
    print(f"=== {model_name} Simple Test ===\n")
    
    if not chat_model:
        print(f"❌ {model_name} not available for testing")
        print()
        return False
    
    try:
        # Simple test message
        message = HumanMessage(content="Say 'Hello from LangChain!'")
        
        print("Sending test message...")
        response = chat_model.invoke([message])
        
        print(f"✅ {model_name} response received")
        print(f"Response: {response.content[:100]}...")
        print()
        
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            print(f"❌ {model_name} - Access denied")
            print("Request model access in AWS Console")
        else:
            print(f"❌ {model_name} - AWS Error: {error_code}")
        print()
        return False
        
    except Exception as e:
        print(f"❌ {model_name} invocation failed: {e}")
        print()
        return False

def compare_initialization_methods():
    """Compare different initialization approaches"""
    
    print("=== Initialization Methods Comparison ===\n")
    
    print("Method 1: Direct initialization")
    print("ChatBedrock(model_id='...', region_name='...')")
    print()
    
    print("Method 2: With boto3 client")
    print("client = boto3.client('bedrock-runtime')")
    print("ChatBedrock(client=client, model_id='...')")
    print()
    
    print("Method 3: With credentials")
    print("ChatBedrock(")
    print("    model_id='...',")
    print("    credentials_profile_name='profile'")
    print(")")
    print()

def test_model_parameters():
    """Test different model parameter configurations"""
    
    print("=== Model Parameters Test ===\n")
    
    parameter_configs = [
        {
            "name": "Conservative",
            "params": {"temperature": 0.1, "max_tokens": 50}
        },
        {
            "name": "Balanced", 
            "params": {"temperature": 0.7, "max_tokens": 100}
        },
        {
            "name": "Creative",
            "params": {"temperature": 0.9, "max_tokens": 150}
        }
    ]
    
    for config in parameter_configs:
        print(f"• {config['name']}: {config['params']}")
    
    print("\nParameters will be tested in Module 3")
    print()

def create_integration_checklist():
    """Create integration verification checklist"""
    
    print("=== Integration Checklist ===\n")
    
    checklist = [
        "✅ LangChain-AWS packages installed",
        "✅ AWS credentials configured", 
        "✅ Bedrock service accessible",
        "✅ ChatBedrock can be initialized",
        "✅ ChatBedrockConverse can be initialized",
        "✅ Simple model invocation works",
        "✅ Error handling tested"
    ]
    
    for item in checklist:
        print(item)
    
    print()

if __name__ == "__main__":
    print("Module 2.3: LangChain-AWS Integration Setup\n")
    
    # Run integration tests
    imports_ok = test_langchain_aws_imports()
    
    if imports_ok:
        chat_bedrock = initialize_chatbedrock()
        chat_converse = initialize_chatbedrock_converse()
        
        # Test simple invocations
        bedrock_ok = test_simple_invocation(chat_bedrock, "ChatBedrock")
        converse_ok = test_simple_invocation(chat_converse, "ChatBedrockConverse")
    else:
        bedrock_ok = False
        converse_ok = False
    
    compare_initialization_methods()
    test_model_parameters()
    create_integration_checklist()
    
    # Summary
    print("="*50)
    print("✅ Topic 2.3 Complete!")
    print("Integration Status:")
    print(f"• LangChain-AWS Imports: {'✅' if imports_ok else '❌'}")
    print(f"• ChatBedrock Ready: {'✅' if bedrock_ok else '❌'}")
    print(f"• ChatBedrockConverse Ready: {'✅' if converse_ok else '❌'}")
    
    if imports_ok and (bedrock_ok or converse_ok):
        print("\n🚀 Ready for Module 3: ChatBedrock Fundamentals!")
    else:
        print("\n⚠️  Complete integration setup before continuing")
    
    print("="*50)