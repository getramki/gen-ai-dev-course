import boto3
import json
from dotenv import load_dotenv
import os

load_dotenv()

def test_bedrock_connection():
    """Test basic connection to Amazon Bedrock"""
    try:
        client = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        
        # Test with Claude 3 Haiku
        body = json.dumps({
            "messages": [{"role": "user", "content": "Hello! Can you respond with just 'Connection successful'?"}],
            "max_tokens": 50,
            "anthropic_version": "bedrock-2023-05-31"
        })
        
        response = client.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=body
        )
        
        result = json.loads(response['body'].read())
        print("✅ Bedrock Connection Successful!")
        print("Response:", result['content'][0]['text'])
        return True
        
    except Exception as e:
        print("❌ Bedrock Connection Failed!")
        print("Error:", str(e))
        return False

def test_multiple_models():
    """Test multiple Bedrock models"""
    models = [
        'anthropic.claude-3-haiku-20240307-v1:0',
        'anthropic.claude-3-5-sonnet-20241022-v2:0'
    ]
    
    client = boto3.client(
        'bedrock-runtime',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    
    for model_id in models:
        try:
            body = json.dumps({
                "messages": [{"role": "user", "content": f"Say hello from {model_id.split('.')[1]}"}],
                "max_tokens": 30,
                "anthropic_version": "bedrock-2023-05-31"
            })
            
            response = client.invoke_model(modelId=model_id, body=body)
            result = json.loads(response['body'].read())
            
            print(f"✅ {model_id}: {result['content'][0]['text']}")
            
        except Exception as e:
            print(f"❌ {model_id}: {str(e)}")

if __name__ == "__main__":
    print("Testing Amazon Bedrock Setup...")
    print("-" * 40)
    
    if test_bedrock_connection():
        print("\nTesting multiple models...")
        print("-" * 40)
        test_multiple_models()
    
    print("\nSetup test complete!")