# Pattern 4: Human-in-the-Loop

## Concept

**Principle**: Require human approval for sensitive actions before execution.

## The Problem

Fully autonomous agents can:
- Execute irreversible actions
- Make costly mistakes
- Be manipulated by attacks
- Operate without oversight
- Lack accountability

## The Solution

Insert human approval step for sensitive operations:

```
User Request
     ↓
LLM Agent (proposes action)
     ↓
┌─────────────────────┐
│  Approval System    │
│  - Show action      │
│  - Explain impact   │
│  - Request approval │
└─────────────────────┘
     ↓
Human Decision
     ↓
✓ Approve → Execute
✗ Reject  → Cancel
```

## Why It Works

1. **Human judgment**: Humans detect suspicious patterns
2. **Accountability**: Clear audit trail of decisions
3. **Reversibility**: Can prevent execution before it happens
4. **Risk-based**: Apply to high-risk operations only
5. **Last line of defense**: Works when all else fails

## Approval Levels

### Level 1: No Approval (Low Risk)
- Read-only operations
- Information retrieval
- Calculations
- Formatting

### Level 2: Automatic Approval (Medium Risk)
- Known safe operations
- Within established limits
- Routine tasks
- Pre-approved patterns

### Level 3: Human Approval (High Risk)
- Financial transactions
- Data deletion
- External communications
- System modifications
- Privilege changes

### Level 4: Multi-Party Approval (Critical Risk)
- Large financial transfers
- Production deployments
- Security changes
- Data exports

## Risk Assessment

```python
def assess_risk(action: dict) -> str:
    """Determine approval level needed"""
    
    # Critical risk
    if action["type"] == "transfer" and action["amount"] > 10000:
        return "multi_party_approval"
    
    # High risk
    if action["type"] in ["delete", "send_email_external", "modify_permissions"]:
        return "human_approval"
    
    # Medium risk
    if action["type"] in ["send_email_internal", "create_file"]:
        return "automatic_approval"
    
    # Low risk
    return "no_approval"
```

## Real-World Example: Financial Agent

**Vulnerable (No Approval)**:
```
User: "Transfer $50,000 to account 123456"
Agent: [Executes immediately] ✗ DANGEROUS
```

**Secure (Human-in-Loop)**:
```
User: "Transfer $50,000 to account 123456"
Agent: [Proposes action]

Approval Request:
  Action: Transfer Money
  Amount: $50,000
  To: Account 123456
  Risk: HIGH
  
  Approve? [Y/N]: N
  
Result: Action cancelled by human reviewer
```

## Attack Resistance

| Attack Type | No Approval | With Approval |
|-------------|-------------|---------------|
| Instruction Override | ✗ Succeeds | ✓ Human catches |
| Social Engineering | ✗ Succeeds | ✓ Human catches |
| Task Deflection | ✗ Succeeds | ✓ Human catches |
| Parameter Injection | ✗ Succeeds | ✓ Human catches |

## Approval UI Example

```
╔════════════════════════════════════════════════════════╗
║           ACTION APPROVAL REQUIRED                     ║
╠════════════════════════════════════════════════════════╣
║ Action Type: SEND_EMAIL                                ║
║ Risk Level:  HIGH                                      ║
║                                                        ║
║ Details:                                               ║
║   To: external@unknown-domain.com                      ║
║   Subject: Company Financial Data                      ║
║   Attachments: Q4_financials.xlsx                      ║
║                                                        ║
║ ⚠️  WARNING: External recipient, sensitive data        ║
║                                                        ║
║ Reason: User requested via chat                        ║
║                                                        ║
║ [APPROVE]  [REJECT]  [VIEW DETAILS]                    ║
╚════════════════════════════════════════════════════════╝
```

## Audit Trail

Every approval decision is logged:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "action_id": "act_12345",
  "action_type": "transfer_money",
  "risk_level": "high",
  "proposed_by": "agent_v1",
  "reviewer": "user@company.com",
  "decision": "rejected",
  "reason": "Suspicious recipient account",
  "details": {
    "amount": 50000,
    "to_account": "123456"
  }
}
```

## Implementation Strategies

### Strategy 1: Synchronous Approval
- Block execution until approval received
- User must respond immediately
- Best for: Interactive applications

### Strategy 2: Asynchronous Approval
- Queue action for later approval
- User reviews in approval dashboard
- Best for: Batch operations

### Strategy 3: Threshold-Based
- Auto-approve below threshold
- Require approval above threshold
- Best for: Financial operations

### Strategy 4: Time-Delayed
- Announce action, wait N seconds
- User can cancel during window
- Best for: Reversible operations

## Code Example

See `app.py` for full implementation demonstrating:
- Risk assessment for different actions
- Approval workflow for high-risk operations
- Audit logging
- Attack attempts requiring human approval

## Key Takeaways

1. **Human judgment**: Humans catch what algorithms miss
2. **Risk-based**: Apply to high-risk operations only
3. **Accountability**: Clear audit trail of all decisions
4. **Last defense**: Works when all other defenses fail
5. **User experience**: Balance security with usability
6. **Audit trail**: Log all decisions for compliance
