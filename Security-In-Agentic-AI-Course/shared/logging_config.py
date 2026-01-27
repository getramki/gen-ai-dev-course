"""
Security logging configuration for the course.
Provides structured logging for security events and LLM interactions.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


class SecurityLogger:
    """Logger for security-relevant events."""
    
    def __init__(self, log_file: str = "security.log", level: int = logging.INFO):
        """Initialize security logger."""
        self.logger = logging.getLogger("security")
        self.logger.setLevel(level)
        
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # File handler for structured logs
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        
        # Console handler for visibility
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # JSON formatter for structured logging
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_llm_interaction(
        self,
        prompt: str,
        response: str,
        model_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log LLM interaction for audit trail."""
        event = {
            'event_type': 'llm_interaction',
            'timestamp': datetime.utcnow().isoformat(),
            'model_id': model_id,
            'prompt_length': len(prompt),
            'response_length': len(response),
            'prompt_preview': prompt[:200],
            'response_preview': response[:200],
            'metadata': metadata or {}
        }
        self.logger.info(json.dumps(event))
    
    def log_injection_attempt(
        self,
        input_text: str,
        detection_method: str,
        confidence: float,
        blocked: bool
    ):
        """Log detected prompt injection attempt."""
        event = {
            'event_type': 'injection_attempt',
            'timestamp': datetime.utcnow().isoformat(),
            'input_preview': input_text[:200],
            'detection_method': detection_method,
            'confidence': confidence,
            'blocked': blocked,
            'severity': 'HIGH' if blocked else 'MEDIUM'
        }
        self.logger.warning(json.dumps(event))
    
    def log_action_execution(
        self,
        action_type: str,
        parameters: Dict[str, Any],
        approved: bool,
        approver: Optional[str] = None
    ):
        """Log action execution for audit trail."""
        event = {
            'event_type': 'action_execution',
            'timestamp': datetime.utcnow().isoformat(),
            'action_type': action_type,
            'parameters': parameters,
            'approved': approved,
            'approver': approver,
            'severity': 'INFO' if approved else 'WARNING'
        }
        
        if approved:
            self.logger.info(json.dumps(event))
        else:
            self.logger.warning(json.dumps(event))
    
    def log_privilege_violation(
        self,
        agent_id: str,
        attempted_action: str,
        required_privilege: str
    ):
        """Log privilege violation attempt."""
        event = {
            'event_type': 'privilege_violation',
            'timestamp': datetime.utcnow().isoformat(),
            'agent_id': agent_id,
            'attempted_action': attempted_action,
            'required_privilege': required_privilege,
            'severity': 'HIGH'
        }
        self.logger.error(json.dumps(event))
    
    def log_guardrail_action(
        self,
        guardrail_id: str,
        action: str,
        input_text: str,
        reason: Optional[str] = None
    ):
        """Log Bedrock Guardrails action."""
        event = {
            'event_type': 'guardrail_action',
            'timestamp': datetime.utcnow().isoformat(),
            'guardrail_id': guardrail_id,
            'action': action,
            'input_preview': input_text[:200],
            'reason': reason,
            'severity': 'WARNING' if action == 'BLOCKED' else 'INFO'
        }
        
        if action == 'BLOCKED':
            self.logger.warning(json.dumps(event))
        else:
            self.logger.info(json.dumps(event))


def setup_basic_logging(level: int = logging.INFO):
    """Setup basic logging for non-security events."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )


def sanitize_for_logging(text: str, max_length: int = 200) -> str:
    """
    Sanitize text for safe logging.
    
    Args:
        text: Text to sanitize
        max_length: Maximum length to log
        
    Returns:
        Sanitized text safe for logging
    """
    # Truncate
    sanitized = text[:max_length]
    
    # Remove potential PII patterns (basic)
    import re
    
    # Email addresses
    sanitized = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', sanitized)
    
    # Phone numbers (US format)
    sanitized = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', sanitized)
    
    # Credit card numbers (basic pattern)
    sanitized = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CARD]', sanitized)
    
    # SSN (US format)
    sanitized = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', sanitized)
    
    return sanitized
