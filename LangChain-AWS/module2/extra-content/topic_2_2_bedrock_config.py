"""
Topic 2.2: AWS Bedrock Configuration and Model Access (4 minutes)

Learning Goals:
- Configure AWS credentials and regions
- Understand Bedrock service permissions
- Test model availability and access
- Learn about model endpoints and regions
"""

import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
import os

def load_aws_config():
    """Load AWS configuration from environment"""
    
    print("=== AWS Configuration Loading ===\n")
    
    # Load environment variables
    load_dotenv()
    
    # Check for AWS credentials
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    profile = os.getenv('AWS_PROFILE')
    
    print("Configuration Sources:")
    print(f"• Environment Variables: {'✅' if access_key else '❌'}")
    print(f"• AWS Profile: {profile if profile else 'Not set'}")
    print(f"• Default Region: {region}")
    print()
    
    return region

def test_aws_credentials():
    """Test AWS credentials and basic connectivity"""
    
    print("=== AWS Credentials Test ===\n")
    
    try:
        # Test basic AWS connectivity
        sts_client = boto3.client('sts')
        identity = sts_client.get_caller_identity()
        
        print("✅ AWS Credentials Valid")
        print(f"Account ID: {identity.get('Account', 'Unknown')}")
        print(f"User ARN: {identity.get('Arn', 'Unknown')}")
        print()
        return True
        
    except NoCredentialsError:
        print("❌ No AWS credentials found")
        print("Configure using: aws configure")
        print("Or set environment variables:")
        print("  AWS_ACCESS_KEY_ID")
        print("  AWS_SECRET_ACCESS_KEY")
        print()
        return False
        
    except ClientError as e:
        print(f"❌ AWS Error: {e}")
        print()
        return False

def check_bedrock_availability():
    """Check Bedrock service availability in regions"""
    
    print("=== Bedrock Service Availability ===\n")
    
    bedrock_regions = [
        'us-east-1',
        'us-west-2', 
        'eu-west-1',
        'ap-southeast-1',
        'ap-northeast-1'
    ]
    
    available_regions = []
    
    for region in bedrock_regions:
        try:
            bedrock = boto3.client('bedrock', region_name=region)
            # Test service availability
            bedrock.list_foundation_models()
            print(f"✅ {region} - Bedrock available")
            available_regions.append(region)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UnauthorizedOperation':
                print(f"⚠️  {region} - Access denied (check permissions)")
            else:
                print(f"❌ {region} - {error_code}")
        except Exception as e:
            print(f"❌ {region} - Service unavailable")
    
    print(f"\nAvailable regions: {len(available_regions)}")
    print()
    return available_regions

def list_available_models():
    """List available foundation models in Bedrock"""
    
    print("=== Available Foundation Models ===\n")
    
    try:
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        response = bedrock.list_foundation_models()
        
        models_by_provider = {}
        
        for model in response['modelSummaries']:
            provider = model['providerName']
            if provider not in models_by_provider:
                models_by_provider[provider] = []
            
            models_by_provider[provider].append({
                'id': model['modelId'],
                'name': model['modelName'],
                'input_modalities': model.get('inputModalities', []),
                'output_modalities': model.get('outputModalities', [])
            })
        
        for provider, models in models_by_provider.items():
            print(f"📦 {provider}:")
            for model in models[:3]:  # Show first 3 models per provider
                modalities = f"({', '.join(model['input_modalities'])} → {', '.join(model['output_modalities'])})"
                print(f"  • {model['name']} - {model['id']}")
                print(f"    {modalities}")
            
            if len(models) > 3:
                print(f"  ... and {len(models) - 3} more models")
            print()
        
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            print("❌ Access denied to Bedrock service")
            print("Required permissions:")
            print("  • bedrock:ListFoundationModels")
            print("  • bedrock:InvokeModel")
        else:
            print(f"❌ Error: {error_code}")
        print()
        return False

def check_model_access():
    """Check access to specific models we'll use in the course"""
    
    print("=== Course Model Access Check ===\n")
    
    course_models = [
        'anthropic.claude-3-sonnet-20240229-v1:0',
        'anthropic.claude-3-haiku-20240307-v1:0',
        'amazon.titan-text-express-v1'
    ]
    
    try:
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        for model_id in course_models:
            try:
                # Test with minimal input
                response = bedrock_runtime.invoke_model(
                    modelId=model_id,
                    body=json.dumps({
                        "prompt": "Test",
                        "max_tokens_to_sample": 1
                    }) if 'claude' in model_id else json.dumps({
                        "inputText": "Test",
                        "textGenerationConfig": {"maxTokenCount": 1}
                    })
                )
                print(f"✅ {model_id} - Access confirmed")
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'AccessDeniedException':
                    print(f"❌ {model_id} - Access denied")
                    print("   Request model access in AWS Console")
                elif error_code == 'ValidationException':
                    print(f"✅ {model_id} - Available (validation error expected)")
                else:
                    print(f"⚠️  {model_id} - {error_code}")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Could not test model access: {e}")
        print()
        return False

def setup_bedrock_permissions():
    """Display required IAM permissions for Bedrock"""
    
    print("=== Required IAM Permissions ===\n")
    
    permissions = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "bedrock:ListFoundationModels",
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream"
                ],
                "Resource": "*"
            }
        ]
    }
    
    print("Minimum IAM policy for Bedrock access:")
    print(json.dumps(permissions, indent=2))
    print()
    
    print("To request model access:")
    print("1. Go to AWS Console → Bedrock")
    print("2. Navigate to 'Model access'")
    print("3. Request access for required models")
    print("4. Wait for approval (usually immediate)")
    print()

if __name__ == "__main__":
    print("Module 2.2: AWS Bedrock Configuration and Model Access\n")
    
    # Run configuration checks
    region = load_aws_config()
    creds_ok = test_aws_credentials()
    
    if creds_ok:
        available_regions = check_bedrock_availability()
        models_ok = list_available_models()
        access_ok = check_model_access()
    else:
        available_regions = []
        models_ok = False
        access_ok = False
    
    setup_bedrock_permissions()
    
    # Summary
    print("="*50)
    print("✅ Topic 2.2 Complete!")
    print("Bedrock Status:")
    print(f"• AWS Credentials: {'✅' if creds_ok else '❌'}")
    print(f"• Service Access: {'✅' if available_regions else '❌'}")
    print(f"• Model Listing: {'✅' if models_ok else '❌'}")
    print(f"• Model Access: {'✅' if access_ok else '⚠️'}")
    
    if creds_ok and available_regions:
        print(f"\n🚀 Bedrock ready in {len(available_regions)} regions!")
    else:
        print("\n⚠️  Complete AWS setup before continuing")
    
    print("="*50)