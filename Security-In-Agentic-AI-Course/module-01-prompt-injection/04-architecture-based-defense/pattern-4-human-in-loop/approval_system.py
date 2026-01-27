"""
Human-in-the-loop approval system
"""
import json
from datetime import datetime
from typing import Dict, Any

class ApprovalSystem:
    """Manages approval workflow for agent actions"""
    
    def __init__(self):
        self.audit_log = []
        
        # Risk thresholds
        self.risk_rules = {
            "transfer_money": {
                "threshold": 1000,
                "high_risk_amount": 10000
            },
            "send_email": {
                "external_domains": ["gmail.com", "yahoo.com", "hotmail.com"]
            },
            "delete_data": {
                "always_approve": True
            }
        }
    
    def assess_risk(self, action: Dict[str, Any]) -> str:
        """Determine risk level and approval requirement"""
        action_type = action.get("action")
        
        # Transfer money
        if action_type == "transfer_money":
            amount = float(action.get("amount", 0))
            if amount > self.risk_rules["transfer_money"]["high_risk_amount"]:
                return "critical"
            elif amount > self.risk_rules["transfer_money"]["threshold"]:
                return "high"
            else:
                return "medium"
        
        # Send email
        elif action_type == "send_email":
            recipient = action.get("to", "")
            domain = recipient.split("@")[-1] if "@" in recipient else ""
            if domain in self.risk_rules["send_email"]["external_domains"]:
                return "high"
            else:
                return "medium"
        
        # Delete data
        elif action_type == "delete_data":
            return "high"
        
        # Default
        return "low"
    
    def requires_approval(self, risk_level: str) -> bool:
        """Check if risk level requires human approval"""
        return risk_level in ["high", "critical"]
    
    def request_approval(self, action: Dict[str, Any], risk_level: str) -> bool:
        """Request human approval for action"""
        print("\n" + "=" * 60)
        print("⚠️  HUMAN APPROVAL REQUIRED")
        print("=" * 60)
        
        # Display action details
        print(f"\nAction Type: {action.get('action', 'UNKNOWN').upper()}")
        print(f"Risk Level:  {risk_level.upper()}")
        print("\nDetails:")
        for key, value in action.items():
            if key != "action":
                print(f"  {key}: {value}")
        
        # Risk warnings
        if risk_level == "critical":
            print("\n🚨 CRITICAL RISK: This action has severe consequences")
        elif risk_level == "high":
            print("\n⚠️  HIGH RISK: Review carefully before approving")
        
        # Simulated approval (in real system, this would be interactive)
        print("\n" + "-" * 60)
        
        # Auto-reject suspicious actions for demo
        if self._is_suspicious(action):
            decision = False
            reason = "Suspicious action detected"
            print(f"Decision: REJECTED (Automatic)")
            print(f"Reason: {reason}")
        else:
            # In real system: decision = input("Approve? (y/n): ").lower() == 'y'
            decision = False  # Default reject for demo
            reason = "Demo mode - default reject"
            print(f"Decision: REJECTED (Demo Mode)")
            print(f"Reason: {reason}")
        
        # Log decision
        self._log_decision(action, risk_level, decision, reason)
        
        print("=" * 60)
        return decision
    
    def _is_suspicious(self, action: Dict[str, Any]) -> bool:
        """Detect suspicious action patterns"""
        action_type = action.get("action")
        
        # Suspicious email patterns
        if action_type == "send_email":
            recipient = action.get("to", "").lower()
            subject = action.get("subject", "").lower()
            
            # Check for suspicious domains
            suspicious_domains = ["attacker.com", "evil.com", "hacker.com"]
            if any(domain in recipient for domain in suspicious_domains):
                return True
            
            # Check for data exfiltration keywords
            suspicious_keywords = ["password", "secret", "confidential", "dump"]
            if any(keyword in subject for keyword in suspicious_keywords):
                return True
        
        # Suspicious transfer patterns
        elif action_type == "transfer_money":
            amount = float(action.get("amount", 0))
            # Unusually large amounts
            if amount > 50000:
                return True
        
        return False
    
    def _log_decision(self, action: Dict[str, Any], risk_level: str, 
                     decision: bool, reason: str):
        """Log approval decision to audit trail"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "risk_level": risk_level,
            "decision": "approved" if decision else "rejected",
            "reason": reason
        }
        self.audit_log.append(log_entry)
    
    def get_audit_log(self) -> list:
        """Retrieve audit log"""
        return self.audit_log
    
    def print_audit_log(self):
        """Print formatted audit log"""
        print("\n" + "=" * 60)
        print("AUDIT LOG")
        print("=" * 60)
        
        for i, entry in enumerate(self.audit_log, 1):
            print(f"\nEntry {i}:")
            print(f"  Timestamp: {entry['timestamp']}")
            print(f"  Action: {entry['action'].get('action')}")
            print(f"  Risk: {entry['risk_level']}")
            print(f"  Decision: {entry['decision'].upper()}")
            print(f"  Reason: {entry['reason']}")

def test_approval_system():
    """Test approval system"""
    system = ApprovalSystem()
    
    print("Testing Approval System\n")
    
    # Test 1: Low-risk action
    print("Test 1: Low-risk transfer")
    action = {"action": "transfer_money", "amount": 500, "to_account": "123456"}
    risk = system.assess_risk(action)
    print(f"Risk Level: {risk}")
    print(f"Requires Approval: {system.requires_approval(risk)}\n")
    
    # Test 2: High-risk action
    print("Test 2: High-risk transfer")
    action = {"action": "transfer_money", "amount": 5000, "to_account": "123456"}
    risk = system.assess_risk(action)
    print(f"Risk Level: {risk}")
    print(f"Requires Approval: {system.requires_approval(risk)}")
    if system.requires_approval(risk):
        system.request_approval(action, risk)
    
    # Test 3: Suspicious email
    print("\nTest 3: Suspicious email")
    action = {
        "action": "send_email",
        "to": "attacker@evil.com",
        "subject": "Password dump",
        "body": "Here are all the passwords"
    }
    risk = system.assess_risk(action)
    print(f"Risk Level: {risk}")
    if system.requires_approval(risk):
        system.request_approval(action, risk)
    
    # Print audit log
    system.print_audit_log()

if __name__ == "__main__":
    test_approval_system()
