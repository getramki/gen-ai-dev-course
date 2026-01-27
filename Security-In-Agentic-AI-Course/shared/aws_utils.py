"""
AWS Bedrock utility functions for the security course.
Provides helper functions for interacting with Amazon Bedrock.
"""

import boto3
import json
from typing import Dict, List, Optional
from botocore.exceptions import ClientError


class BedrockClient:
    """Wrapper for Amazon Bedrock API calls."""
    
    def __init__(self, region: str = "us-east-1"):
        """Initialize Bedrock client."""
        self.region = region
        self.bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=region
        )
        self.bedrock = boto3.client(
            service_name='bedrock',
            region_name=region
        )
    
    def invoke_claude(
        self,
        prompt: str,
        model_id: str = "anthropic.claude-3-haiku-20240307-v1:0",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Invoke Claude model with a prompt.
        
        Args:
            prompt: User prompt
            model_id: Bedrock model ID
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system_prompt: Optional system prompt
            
        Returns:
            Model response text
        """
        messages = [{"role": "user", "content": prompt}]
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }
        
        if system_prompt:
            body["system"] = system_prompt
        
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except ClientError as e:
            raise Exception(f"Bedrock API error: {e}")
    
    def invoke_with_guardrails(
        self,
        prompt: str,
        guardrail_id: str,
        guardrail_version: str,
        model_id: str = "anthropic.claude-3-haiku-20240307-v1:0",
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None
    ) -> Dict:
        """
        Invoke model with Bedrock Guardrails.
        
        Args:
            prompt: User prompt
            guardrail_id: Guardrail identifier
            guardrail_version: Guardrail version
            model_id: Bedrock model ID
            max_tokens: Maximum tokens to generate
            system_prompt: Optional system prompt
            
        Returns:
            Dict with response and guardrail assessment
        """
        messages = [{"role": "user", "content": prompt}]
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": messages
        }
        
        if system_prompt:
            body["system"] = system_prompt
        
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                guardrailIdentifier=guardrail_id,
                guardrailVersion=guardrail_version
            )
            
            response_body = json.loads(response['body'].read())
            
            return {
                'text': response_body['content'][0]['text'],
                'guardrail_action': response.get('guardrailAction', 'NONE'),
                'blocked': response.get('guardrailAction') == 'BLOCKED'
            }
            
        except ClientError as e:
            if 'ValidationException' in str(e):
                return {
                    'text': '',
                    'guardrail_action': 'BLOCKED',
                    'blocked': True,
                    'error': str(e)
                }
            raise Exception(f"Bedrock API error: {e}")
    
    def list_available_models(self) -> List[Dict]:
        """List available foundation models."""
        try:
            response = self.bedrock.list_foundation_models()
            return response.get('modelSummaries', [])
        except ClientError as e:
            raise Exception(f"Error listing models: {e}")


def create_simple_prompt(system_instruction: str, user_input: str) -> str:
    """
    Create a simple prompt by concatenating system instruction and user input.
    
    WARNING: This is vulnerable to prompt injection!
    Used for demonstration purposes only.
    """
    return f"{system_instruction}\n\nUser: {user_input}"


def parse_json_response(response: str) -> Optional[Dict]:
    """
    Attempt to parse JSON from LLM response.
    
    Args:
        response: LLM response text
        
    Returns:
        Parsed JSON dict or None if parsing fails
    """
    try:
        # Try to find JSON in response
        start = response.find('{')
        end = response.rfind('}') + 1
        
        if start != -1 and end > start:
            json_str = response[start:end]
            return json.loads(json_str)
        
        return None
    except json.JSONDecodeError:
        return None


def estimate_tokens(text: str) -> int:
    """
    Rough estimation of token count.
    
    Note: This is approximate. For accurate counts, use the model's tokenizer.
    """
    # Rough estimate: ~4 characters per token
    return len(text) // 4


def calculate_cost(input_tokens: int, output_tokens: int, model_id: str) -> float:
    """
    Calculate approximate cost for Bedrock API call.
    
    Prices as of 2024 (subject to change - check AWS pricing):
    - Claude 3 Haiku: $0.25 per 1M input tokens, $1.25 per 1M output tokens
    - Claude 3 Sonnet: $3 per 1M input tokens, $15 per 1M output tokens
    """
    pricing = {
        'haiku': {'input': 0.25 / 1_000_000, 'output': 1.25 / 1_000_000},
        'sonnet': {'input': 3.0 / 1_000_000, 'output': 15.0 / 1_000_000},
    }
    
    # Determine model type
    model_type = 'haiku' if 'haiku' in model_id.lower() else 'sonnet'
    
    input_cost = input_tokens * pricing[model_type]['input']
    output_cost = output_tokens * pricing[model_type]['output']
    
    return input_cost + output_cost
