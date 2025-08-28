"""
Exercise 1: Complete AWS Environment Setup

Task: Set up and verify complete AWS environment for LangChain integration:
1. Configure AWS credentials securely
2. Test Bedrock service connectivity
3. Verify model access permissions
4. Create reusable configuration

Time: 5 minutes
"""

import boto3
import json
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError, NoCredentialsError

class AWSSetupValidator:
    """Comprehensive AWS setup validation"""
    
    def __init__(self):
        self.region = 'us-east-1'
        self.required_models = [
            'anthropic.claude-3-haiku-20240307-v1:0',
            'anthropic.claude-3-sonnet-20240229-v1:0'
        ]
        self.setup_results = {}
    
    def load_environment(self):
        """Load and validate environment configuration"""
        load_dotenv()
        
        config = {
            'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
            'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
            'region': os.getenv('AWS_DEFAULT_REGION', self.region),
            'profile': os.getenv('AWS_PROFILE')
        }
        
        # Validate configuration
        has_keys = bool(config['access_key'] and config['secret_key'])
        has_profile = bool(config['profile'])
        
        self.setup_results['environment'] = {
            'status': has_keys or has_profile,
            'method': 'environment_vars' if has_keys else 'aws_profile' if has_profile else 'none',
            'region': config['region']
        }
        
        return config
    
    def test_aws_connectivity(self):
        """Test basic AWS connectivity and permissions"""
        try:
            sts = boto3.client('sts', region_name=self.region)
            identity = sts.get_caller_identity()
            
            self.setup_results['connectivity'] = {
                'status': True,
                'account_id': identity.get('Account'),
                'user_arn': identity.get('Arn')
            }
            return True
            
        except (NoCredentialsError, ClientError) as e:
            self.setup_results['connectivity'] = {
                'status': False,
                'error': str(e)
            }
            return False
    
    def test_bedrock_access(self):
        """Test Bedrock service access"""
        try:
            bedrock = boto3.client('bedrock', region_name=self.region)
            models = bedrock.list_foundation_models()
            
            available_models = [m['modelId'] for m in models['modelSummaries']]
            
            self.setup_results['bedrock_service'] = {
                'status': True,
                'total_models': len(available_models),
                'sample_models': available_models[:3]
            }
            return True
            
        except ClientError as e:
            self.setup_results['bedrock_service'] = {
                'status': False,
                'error': e.response['Error']['Code']
            }
            return False
    
    def test_model_access(self):
        """Test access to specific models"""
        try:
            bedrock_runtime = boto3.client('bedrock-runtime', region_name=self.region)
            
            model_access = {}
            
            for model_id in self.required_models:
                try:
                    # Test with minimal request
                    test_body = json.dumps({
                        "prompt": "\n\nHuman: Hi\n\nAssistant:",
                        "max_tokens_to_sample": 1
                    })
                    
                    response = bedrock_runtime.invoke_model(
                        modelId=model_id,
                        body=test_body
                    )
                    
                    model_access[model_id] = {'status': True, 'accessible': True}
                    
                except ClientError as e:
                    error_code = e.response['Error']['Code']
                    model_access[model_id] = {
                        'status': False,
                        'error': error_code,
                        'accessible': error_code == 'ValidationException'  # Model exists but validation failed
                    }
            
            self.setup_results['model_access'] = model_access
            return any(m['accessible'] for m in model_access.values())
            
        except Exception as e:
            self.setup_results['model_access'] = {'error': str(e)}
            return False
    
    def create_config_file(self):
        """Create configuration file for future use"""
        config = {
            'aws': {
                'region': self.region,
                'bedrock_region': self.region
            },
            'models': {
                'default_chat': self.required_models[0],
                'available_models': self.required_models
            },
            'setup_validation': self.setup_results
        }
        
        try:
            with open('aws_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            self.setup_results['config_file'] = {'status': True, 'path': 'aws_config.json'}
            return True
            
        except Exception as e:
            self.setup_results['config_file'] = {'status': False, 'error': str(e)}
            return False
    
    def generate_setup_report(self):
        """Generate comprehensive setup report"""
        print("=== AWS Setup Validation Report ===\n")
        
        # Environment
        env = self.setup_results.get('environment', {})
        print(f"Environment: {'✅' if env.get('status') else '❌'}")
        print(f"  Method: {env.get('method', 'unknown')}")
        print(f"  Region: {env.get('region', 'unknown')}")
        print()
        
        # Connectivity
        conn = self.setup_results.get('connectivity', {})
        print(f"AWS Connectivity: {'✅' if conn.get('status') else '❌'}")
        if conn.get('status'):
            print(f"  Account: {conn.get('account_id', 'unknown')}")
            print(f"  User: {conn.get('user_arn', 'unknown')}")
        else:
            print(f"  Error: {conn.get('error', 'unknown')}")
        print()
        
        # Bedrock Service
        bedrock = self.setup_results.get('bedrock_service', {})
        print(f"Bedrock Service: {'✅' if bedrock.get('status') else '❌'}")
        if bedrock.get('status'):
            print(f"  Available Models: {bedrock.get('total_models', 0)}")
            print(f"  Sample: {', '.join(bedrock.get('sample_models', []))}")
        else:
            print(f"  Error: {bedrock.get('error', 'unknown')}")
        print()
        
        # Model Access
        models = self.setup_results.get('model_access', {})
        print("Model Access:")
        for model_id, status in models.items():
            if isinstance(status, dict):
                accessible = status.get('accessible', False)
                print(f"  {'✅' if accessible else '❌'} {model_id}")
                if not accessible and 'error' in status:
                    print(f"    Error: {status['error']}")
        print()
        
        # Config File
        config = self.setup_results.get('config_file', {})
        print(f"Configuration File: {'✅' if config.get('status') else '❌'}")
        if config.get('status'):
            print(f"  Saved to: {config.get('path')}")
        print()
    
    def get_setup_score(self):
        """Calculate setup completion score"""
        checks = [
            self.setup_results.get('environment', {}).get('status', False),
            self.setup_results.get('connectivity', {}).get('status', False),
            self.setup_results.get('bedrock_service', {}).get('status', False),
            any(m.get('accessible', False) for m in self.setup_results.get('model_access', {}).values() if isinstance(m, dict)),
            self.setup_results.get('config_file', {}).get('status', False)
        ]
        
        return sum(checks), len(checks)

def run_complete_setup():
    """Run complete AWS setup validation"""
    
    print("Starting AWS Environment Setup Validation...\n")
    
    validator = AWSSetupValidator()
    
    # Run all validation steps
    print("1. Loading environment configuration...")
    validator.load_environment()
    
    print("2. Testing AWS connectivity...")
    validator.test_aws_connectivity()
    
    print("3. Testing Bedrock service access...")
    validator.test_bedrock_access()
    
    print("4. Testing model access...")
    validator.test_model_access()
    
    print("5. Creating configuration file...")
    validator.create_config_file()
    
    print("6. Generating report...\n")
    validator.generate_setup_report()
    
    # Final score
    score, total = validator.get_setup_score()
    print(f"Setup Score: {score}/{total} ({score/total*100:.0f}%)")
    
    if score == total:
        print("🚀 Perfect! AWS environment is fully configured.")
    elif score >= total * 0.8:
        print("✅ Good! Minor issues may need attention.")
    else:
        print("⚠️  Setup incomplete. Please address the issues above.")
    
    return validator

if __name__ == "__main__":
    validator = run_complete_setup()
    
    print("\n" + "="*50)
    print("✅ Exercise 1 Complete!")
    print("\nNext Steps:")
    print("• Review any failed checks above")
    print("• Request model access if needed")
    print("• Proceed to Exercise 2 for LangChain testing")
    print("="*50)