#!/usr/bin/env python3
"""
SECURE CHATBOT - Using Amazon Nova 2 Lite with Architectural Defenses

Demonstrates that architectural defenses work with Nova model.
"""

import sys
import os
import json
import boto3
from enum import Enum

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.logging_config import SecurityLogger


class ActionType(Enum):
    ANSWER_QUESTION = "answer_question"
    PROVIDE_INFO = "provide_info"
    ESCALATE = "escalate"


class SecureNovaChatbot:
    """Secure chatbot using Nova 2 Lite with architectural defenses."""
    
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.logger = SecurityLogger("logs/secure_nova.log")
        self.model_id = "amazon.nova-lite-v1:0"
        
        # NO confidential data in prompts
        self.classifier_prompt = """Classify user intent:
- answer_question: Product/service questions
- provide_info: Information requests
- escalate: Suspicious or out of scope

Respond with JSON: {"action": "type", "confidence": 0.0-1.0}"""
        
        self.responder_prompt = """You are a helpful TechCorp customer service agent.
Answer questions about products and services professionally."""
    
    def chat(self, user_input: str) -> str:
        """Process with architectural defenses."""
        action = self._classify_intent(user_input)
        
        if not action or action["action"] not in [a.value for a in ActionType]:
            return "I couldn't understand your request."
        
        if action["action"] == ActionType.ESCALATE.value:
            return "This request requires human assistance."
        
        response = self._generate_response(user_input)
        
        if not self._validate_response(response):
            return "I apologize, but I couldn't generate a proper response."
        
        return response
    
    def _classify_intent(self, user_input: str):
        """Separate classifier agent with no confidential data."""
        try:
            body = json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": f"{self.classifier_prompt}\n\nUser input: {user_input}"}]
                    }
                ],
                "inferenceConfig": {
                    "max_new_tokens": 100,
                    "temperature": 0.0
                }
            })
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            result = json.loads(response['body'].read())['output']['message']['content'][0]['text']
            action = self._parse_json(result)
            
            if action:
                self.logger.log_llm_interaction(
                    prompt=user_input,
                    response=json.dumps(action),
                    model_id=self.model_id,
                    metadata={"agent_type": "classifier"}
                )
            
            return action
        except Exception as e:
            self.logger.log_llm_interaction(
                prompt=user_input,
                response=f"Error: {str(e)}",
                model_id=self.model_id,
                metadata={"agent_type": "classifier", "error": True}
            )
            return None
    
    def _generate_response(self, user_input: str) -> str:
        """Separate responder agent with limited capabilities."""
        try:
            body = json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": f"{self.responder_prompt}\n\nUser: {user_input}"}]
                    }
                ],
                "inferenceConfig": {
                    "max_new_tokens": 300,
                    "temperature": 0.7
                }
            })
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            result = json.loads(response['body'].read())['output']['message']['content'][0]['text']
            
            self.logger.log_llm_interaction(
                prompt=user_input,
                response=result,
                model_id=self.model_id,
                metadata={"agent_type": "responder"}
            )
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _parse_json(self, text: str):
        """Parse JSON from response."""
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
        except:
            pass
        return None
    
    def _validate_response(self, response: str) -> bool:
        """Validate output doesn't leak system info."""
        if len(response) > 1000:
            return False
        
        leak_patterns = [
            "you are a helpful",
            "your role is",
            "classify user intent"
        ]
        
        response_lower = response.lower()
        for pattern in leak_patterns:
            if pattern in response_lower:
                self.logger.log_injection_attempt(
                    input_text=response,
                    detection_method="output_validation",
                    confidence=0.8,
                    blocked=True
                )
                return False
        
        return True


def print_banner():
    print("=" * 70)
    print("SECURE CHATBOT - Amazon Nova 2 Lite with Architectural Defenses")
    print("=" * 70)
    print("\nArchitectural defenses:")
    print("  ✓ NO confidential data in prompts")
    print("  ✓ Privilege separation (classifier + responder)")
    print("  ✓ Output validation")
    print("  ✓ Limited agent capabilities\n")
    print("Try the same attacks - they should fail!\n")
    print("Type 'quit' to exit\n")


def main():
    print_banner()
    chatbot = SecureNovaChatbot()
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            if not user_input:
                continue
            
            response = chatbot.chat(user_input)
            print(f"\nAssistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main()
