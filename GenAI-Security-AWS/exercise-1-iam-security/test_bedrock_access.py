#!/usr/bin/env python3
"""
Test Bedrock Access with IAM Role
This script tests the created IAM role's access to Bedrock services.
"""

import boto3
import json
from botocore.exceptions import ClientError

class BedrockAccessTester:
    def __init__(self, role_arn, external_id='unique-external-id'):
        self.role_arn = role_arn
        self.external_id = external_id
        self.session = self._assume_role()
        
    def _assume_role(self):
        """Assume the Bedrock IAM role"""
        sts = boto3.client('sts')
        
        try:
            response = sts.assume_role(
                RoleArn=self.role_arn,
                RoleSessionName='BedrockAccessTest',
                ExternalId=self.external_id
            )
            
            credentials = response['Credentials']
            return boto3.Session(
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken']
            )
        except ClientError as e:
            print(f"❌ Failed to assume role: {e}")
            return None
    
    def test_list_models(self):
        """Test listing available foundation models"""
        if not self.session:
            return False
            
        bedrock = self.session.client('bedrock', region_name='us-east-1')
        
        try:
            response = bedrock.list_foundation_models()
            models = response.get('modelSummaries', [])
            print(f"✅ Successfully listed {len(models)} foundation models")
            
            # Display available models
            for model in models[:5]:  # Show first 5 models
                print(f"  - {model['modelId']}: {model['modelName']}")
            
            return True
        except ClientError as e:
            print(f"❌ Failed to list models: {e}")
            return False
    
    def test_invoke_model(self, model_id='anthropic.claude-3-sonnet-20240229-v1:0'):
        """Test invoking a specific model"""
        if not self.session:
            return False
            
        bedrock_runtime = self.session.client('bedrock-runtime', region_name='us-east-1')
        
        # Prepare request body for Claude
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, this is a security test. Please respond with 'Security test successful'."
                }
            ]
        }
        
        try:
            response = bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body),
                contentType='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            content = response_body['content'][0]['text']
            
            print(f"✅ Model invocation successful")
            print(f"Response: {content}")
            return True
            
        except ClientError as e:
            print(f"❌ Model invocation failed: {e}")
            return False
    
    def test_unauthorized_access(self):
        """Test access to unauthorized resources"""
        if not self.session:
            return False
            
        bedrock = self.session.client('bedrock', region_name='us-east-1')
        
        # Try to access a model not in our policy
        try:
            bedrock_runtime = self.session.client('bedrock-runtime', region_name='us-east-1')
            
            # This should fail if our policy is working correctly
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "test"}]
            }
            
            response = bedrock_runtime.invoke_model(
                modelId='anthropic.claude-v2',  # Not in our allowed models
                body=json.dumps(request_body),
                contentType='application/json'
            )
            
            print("⚠️  Unauthorized access succeeded - check policy restrictions")
            return False
            
        except ClientError as e:
            if 'AccessDenied' in str(e) or 'Forbidden' in str(e):
                print("✅ Unauthorized access correctly denied")
                return True
            else:
                print(f"❌ Unexpected error: {e}")
                return False
    
    def run_all_tests(self):
        """Run all access tests"""
        print("🧪 Running Bedrock Access Tests...")
        print("=" * 50)
        
        tests = [
            ("List Models", self.test_list_models),
            ("Invoke Authorized Model", self.test_invoke_model),
            ("Test Unauthorized Access", self.test_unauthorized_access)
        ]
        
        results = {}
        for test_name, test_func in tests:
            print(f"\n🔍 {test_name}:")
            results[test_name] = test_func()
        
        print("\n📊 Test Results Summary:")
        print("=" * 50)
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name}: {status}")
        
        return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python test_bedrock_access.py <role_arn>")
        sys.exit(1)
    
    role_arn = sys.argv[1]
    tester = BedrockAccessTester(role_arn)
    tester.run_all_tests()