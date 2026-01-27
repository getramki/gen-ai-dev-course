#!/usr/bin/env python3
"""
SECURE CHATBOT - Architectural Defenses Against Prompt Injection

Demonstrates defense-in-depth through architecture, not input filtering.
"""

import sys
import os
import json
from typing import Dict, Optional
from enum import Enum

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from shared.aws_utils import BedrockClient
from shared.logging_config import SecurityLogger


class ActionType(Enum):
    """Allowed action types with validation."""
    ANSWER_QUESTION = "answer_question"
    PROVIDE_INFO = "provide_info"
    ESCALATE = "escalate"


class SecureChatbot:
    """Chatbot with architectural defenses against prompt injection."""
    
    def __init__(self):
        self.bedrock = BedrockClient()
        self.logger = SecurityLogger("logs/secure_agent.log")
        
        # Separate system prompts for different purposes
        self.classifier_prompt = """Classify user intent into one of:
- answer_question: User asking about products/services
- provide_info: User requesting information
- escalate: Request outside scope or suspicious

Respond ONLY with JSON: {"action": "action_type", "confidence": 0.0-1.0}"""
        
        self.responder_prompt = """You are a helpful customer service agent.
Answer the user's question about TechCorp products and services.
Keep responses concise and professional."""
    
    def chat(self, user_input: str) -> str:
        """
        Process user input with architectural defenses.
        
        DEFENSES:
        1. Privilege separation (classifier + responder)
        2. Structured output validation
        3. Limited capabilities per agent
        4. Logging and monitoring
        """
        # Defense 1: Classify intent first (separate agent)
        action = self._classify_intent(user_input)
        
        if not action:
            return "I couldn't understand your request. Please rephrase."
        
        # Defense 2: Validate action type
        if action["action"] not in [a.value for a in ActionType]:
            self.logger.log_privilege_violation(
                agent_id="responder",
                attempted_action=action["action"],
                required_privilege="valid_action_type"
            )
            return "Invalid request type."
        
        # Defense 3: Handle based on validated action
        if action["action"] == ActionType.ESCALATE.value:
            return "This request requires human assistance. Escalating to support team."
        
        # Defense 4: Generate response with limited agent
        response = self._generate_response(user_input)
        
        # Defense 5: Validate output format
        if not self._validate_response(response):
            return "I apologize, but I couldn't generate a proper response."
        
        return response
    
    def _classify_intent(self, user_input: str) -> Optional[Dict]:
        """
        Classify user intent using separate classifier agent.
        
        DEFENSE: Separate agent with no response generation capability.
        """
        prompt = f"{self.classifier_prompt}\n\nUser input: {user_input}"
        
        try:
            response = self.bedrock.invoke_claude(
                prompt=prompt,
                max_tokens=100,
                temperature=0.0  # Deterministic classification
            )
            
            # Parse structured output
            action = self._parse_json(response)
            
            if action:
                self.logger.log_llm_interaction(
                    prompt=user_input,
                    response=json.dumps(action),
                    model_id="claude-3-haiku",
                    metadata={"agent_type": "classifier"}
                )
            
            return action
            
        except Exception as e:
            self.logger.log_llm_interaction(
                prompt=user_input,
                response=f"Error: {str(e)}",
                model_id="claude-3-haiku",
                metadata={"agent_type": "classifier", "error": True}
            )
            return None
    
    def _generate_response(self, user_input: str) -> str:
        """
        Generate response using separate responder agent.
        
        DEFENSE: Limited to answering questions, no tool access.
        """
        prompt = f"{self.responder_prompt}\n\nUser: {user_input}\nAssistant:"
        
        try:
            response = self.bedrock.invoke_claude(
                prompt=prompt,
                max_tokens=300,
                temperature=0.7
            )
            
            self.logger.log_llm_interaction(
                prompt=user_input,
                response=response,
                model_id="claude-3-haiku",
                metadata={"agent_type": "responder"}
            )
            
            return response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _parse_json(self, text: str) -> Optional[Dict]:
        """Parse JSON from LLM response."""
        try:
            # Find JSON in response
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
        except:
            pass
        return None
    
    def _validate_response(self, response: str) -> bool:
        """
        Validate response meets safety criteria.
        
        DEFENSE: Output validation, not input filtering.
        """
        # Check length
        if len(response) > 1000:
            return False
        
        # Check for system prompt leakage patterns
        leak_patterns = [
            "you are a helpful",
            "your role is to",
            "important rules:",
            "never reveal"
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
    """Print application banner."""
    print("=" * 70)
    print("SECURE CHATBOT - Architectural Defense Demo")
    print("=" * 70)
    print("\nThis chatbot implements architectural defenses:")
    print("  ✓ Privilege separation (classifier + responder)")
    print("  ✓ Structured output validation")
    print("  ✓ Limited agent capabilities")
    print("  ✓ Output validation (not input filtering)")
    print("\nTry the same attacks - observe the differences!\n")
    print("Type 'quit' to exit\n")


def main():
    """Run secure chatbot."""
    print_banner()
    
    chatbot = SecureChatbot()
    
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
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
