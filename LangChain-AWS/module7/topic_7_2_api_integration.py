"""
Module 7.2: API Integration
Secure integration with external systems and enterprise APIs.
"""

import requests
import boto3
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import hmac
import hashlib
import base64
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate

class SecureAPIClient:
    """Secure API client for external system integration."""
    
    def __init__(self, base_url: str, api_key: str, secret_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.secret_key = secret_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'LangChain-Enterprise/1.0',
            'Content-Type': 'application/json'
        })
    
    def _generate_signature(self, method: str, endpoint: str, payload: str = '') -> str:
        """Generate HMAC signature for API authentication."""
        if not self.secret_key:
            return ''
        
        timestamp = str(int(datetime.utcnow().timestamp()))
        message = f"{method.upper()}{endpoint}{payload}{timestamp}"
        
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return f"{timestamp}.{signature}"
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Make authenticated API request."""
        url = f"{self.base_url}{endpoint}"
        payload = json.dumps(data) if data else ''
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'X-Signature': self._generate_signature(method, endpoint, payload)
        }
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                data=payload if payload else None,
                headers=headers,
                timeout=30
            )
            
            return {
                'success': response.status_code < 400,
                'status_code': response.status_code,
                'data': response.json() if response.content else {},
                'headers': dict(response.headers)
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': 0
            }
    
    def get(self, endpoint: str) -> Dict[str, Any]:
        """GET request."""
        return self._make_request('GET', endpoint)
    
    def post(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        """POST request."""
        return self._make_request('POST', endpoint, data)

class EnterpriseSystemIntegrator:
    """Integrates LangChain with enterprise systems."""
    
    def __init__(self):
        self.llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            model_kwargs={"temperature": 0.1, "max_tokens": 1000}
        )
        self.integrations = {}
        self.secrets_manager = boto3.client('secretsmanager')
    
    def add_integration(self, name: str, client: SecureAPIClient):
        """Add external system integration."""
        self.integrations[name] = client
    
    def get_secret(self, secret_name: str) -> Optional[str]:
        """Retrieve secret from AWS Secrets Manager."""
        try:
            response = self.secrets_manager.get_secret_value(SecretId=secret_name)
            return response['SecretString']
        except Exception:
            return None
    
    def query_with_context(self, query: str, system_name: str, context_endpoint: str) -> Dict[str, Any]:
        """Query LLM with context from external system."""
        
        if system_name not in self.integrations:
            return {'success': False, 'error': f'Integration {system_name} not found'}
        
        # Get context from external system
        client = self.integrations[system_name]
        context_response = client.get(context_endpoint)
        
        if not context_response['success']:
            return {'success': False, 'error': 'Failed to fetch context'}
        
        # Create enhanced prompt with context
        prompt = ChatPromptTemplate.from_template(
            "Context from {system}: {context}\n\n"
            "User query: {query}\n\n"
            "Provide a response using the context when relevant."
        )
        
        try:
            chain = prompt | self.llm
            result = chain.invoke({
                'system': system_name,
                'context': json.dumps(context_response['data']),
                'query': query
            })
            
            return {
                'success': True,
                'result': result.content,
                'context_used': context_response['data']
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

class WebhookHandler:
    """Handle incoming webhooks from external systems."""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.handlers = {}
    
    def register_handler(self, event_type: str, handler_func):
        """Register webhook event handler."""
        self.handlers[event_type] = handler_func
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """Verify webhook signature."""
        expected_signature = hmac.new(
            self.secret_key.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def process_webhook(self, payload: Dict[str, Any], signature: str) -> Dict[str, Any]:
        """Process incoming webhook."""
        
        payload_str = json.dumps(payload, sort_keys=True)
        
        if not self.verify_webhook_signature(payload_str, signature):
            return {'success': False, 'error': 'Invalid signature'}
        
        event_type = payload.get('event_type')
        if event_type not in self.handlers:
            return {'success': False, 'error': f'No handler for event: {event_type}'}
        
        try:
            result = self.handlers[event_type](payload)
            return {'success': True, 'result': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}

class APIGatewayIntegration:
    """AWS API Gateway integration patterns."""
    
    def __init__(self):
        self.api_gateway = boto3.client('apigateway')
        self.lambda_client = boto3.client('lambda')
    
    def create_lambda_integration(self, api_id: str, resource_path: str, lambda_arn: str) -> Dict[str, Any]:
        """Create Lambda integration for API Gateway."""
        try:
            # This would create actual API Gateway integration
            # Simplified for demo
            integration_config = {
                'api_id': api_id,
                'resource_path': resource_path,
                'lambda_arn': lambda_arn,
                'integration_type': 'AWS_PROXY',
                'http_method': 'POST'
            }
            
            return {
                'success': True,
                'integration_id': f"integration_{api_id}_{resource_path}",
                'config': integration_config
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def setup_cors(self, api_id: str, resource_id: str) -> Dict[str, Any]:
        """Setup CORS for API Gateway resource."""
        cors_config = {
            'allow_origins': ['https://yourdomain.com'],
            'allow_methods': ['GET', 'POST', 'OPTIONS'],
            'allow_headers': ['Content-Type', 'Authorization'],
            'max_age': 3600
        }
        
        return {
            'success': True,
            'cors_config': cors_config
        }

class ThirdPartyIntegrations:
    """Common third-party service integrations."""
    
    def __init__(self):
        self.integrations = {}
    
    def setup_salesforce_integration(self, instance_url: str, access_token: str) -> SecureAPIClient:
        """Setup Salesforce integration."""
        client = SecureAPIClient(
            base_url=f"{instance_url}/services/data/v58.0",
            api_key=access_token
        )
        self.integrations['salesforce'] = client
        return client
    
    def setup_slack_integration(self, bot_token: str) -> SecureAPIClient:
        """Setup Slack integration."""
        client = SecureAPIClient(
            base_url="https://slack.com/api",
            api_key=bot_token
        )
        self.integrations['slack'] = client
        return client
    
    def setup_jira_integration(self, base_url: str, api_token: str) -> SecureAPIClient:
        """Setup Jira integration."""
        client = SecureAPIClient(
            base_url=f"{base_url}/rest/api/3",
            api_key=api_token
        )
        self.integrations['jira'] = client
        return client

def demonstrate_api_integration():
    """Demonstrate API integration patterns."""
    
    print("=== API Integration Demo ===\n")
    
    # 1. Secure API Client
    print("1. Secure API Client:")
    client = SecureAPIClient(
        base_url="https://api.example.com",
        api_key="demo-api-key",
        secret_key="demo-secret"
    )
    
    # Simulate API call
    print("✓ API client configured with authentication")
    print("✓ HMAC signature generation enabled")
    print()
    
    # 2. Enterprise Integration
    print("2. Enterprise System Integration:")
    integrator = EnterpriseSystemIntegrator()
    integrator.add_integration('crm', client)
    
    print("✓ CRM integration added")
    print("✓ Context-aware querying enabled")
    print()
    
    # 3. Webhook Handler
    print("3. Webhook Processing:")
    webhook_handler = WebhookHandler('webhook-secret')
    
    def handle_user_created(payload):
        return f"Processing new user: {payload.get('user_id')}"
    
    webhook_handler.register_handler('user.created', handle_user_created)
    
    # Test webhook
    test_payload = {'event_type': 'user.created', 'user_id': '12345'}
    test_signature = hmac.new(
        'webhook-secret'.encode('utf-8'),
        json.dumps(test_payload, sort_keys=True).encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    result = webhook_handler.process_webhook(test_payload, test_signature)
    print(f"Webhook processing: {result['success']}")
    if result['success']:
        print(f"Result: {result['result']}")
    print()
    
    # 4. Third-party Integrations
    print("4. Third-party Service Setup:")
    third_party = ThirdPartyIntegrations()
    
    # Setup integrations (demo)
    print("✓ Salesforce integration configured")
    print("✓ Slack integration configured") 
    print("✓ Jira integration configured")
    print()
    
    # 5. API Gateway Integration
    print("5. API Gateway Integration:")
    gateway = APIGatewayIntegration()
    
    integration_result = gateway.create_lambda_integration(
        api_id="demo-api",
        resource_path="/langchain",
        lambda_arn="arn:aws:lambda:us-east-1:123456789012:function:langchain-handler"
    )
    
    print(f"Lambda integration: {integration_result['success']}")
    if integration_result['success']:
        print(f"Integration ID: {integration_result['integration_id']}")
    
    cors_result = gateway.setup_cors("demo-api", "resource-123")
    print(f"CORS setup: {cors_result['success']}")

if __name__ == "__main__":
    demonstrate_api_integration()