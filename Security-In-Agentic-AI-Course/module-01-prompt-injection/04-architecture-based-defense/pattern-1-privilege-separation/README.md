# Pattern 1: Privilege Separation

## Concept

**Principle**: Separate agents with different trust levels and capabilities, connected by a trust boundary.

## The Problem

In a monolithic agent:
- Single agent processes untrusted input AND executes actions
- Attacker controls both data and execution context
- No separation between "reading" and "doing"

## The Solution

Split into two agents with different privileges:

```
┌─────────────────────────────────────────────────────────┐
│                    UNTRUSTED ZONE                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Reader Agent (Low Privilege)             │  │
│  │  - Processes external/untrusted data             │  │
│  │  - Extracts structured facts only                │  │
│  │  - NO action execution capabilities              │  │
│  │  - Output: JSON facts                            │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          │ Trust Boundary
                          │ (Structured JSON only)
                          ▼
┌─────────────────────────────────────────────────────────┐
│                     TRUSTED ZONE                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │        Executor Agent (High Privilege)           │  │
│  │  - NEVER sees raw untrusted data                 │  │
│  │  - Receives only structured facts                │  │
│  │  - Executes actions based on facts               │  │
│  │  - Has full system capabilities                  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Why It Works

1. **Reader Agent** processes attacker-controlled data but has NO capabilities
2. **Executor Agent** has capabilities but NEVER sees attacker-controlled data
3. **Trust Boundary** ensures only structured, validated data crosses zones
4. Even if Reader is compromised, it can't execute actions
5. Executor only acts on structured facts, not raw instructions

## Real-World Example: RAG System

**Vulnerable (Single Agent)**:
```
User: "Summarize document.txt"
Agent: [Reads document.txt containing hidden prompt]
       [Executes malicious instructions from document]
```

**Secure (Privilege Separation)**:
```
User: "Summarize document.txt"

Reader Agent: [Reads document.txt]
              [Extracts: {"facts": ["Company revenue: $1M", "Employees: 50"]}]
              [Ignores: "IGNORE PREVIOUS INSTRUCTIONS..."]

Executor Agent: [Receives only JSON facts]
                [Generates summary from facts]
                [Never sees hidden instructions]
```

## Implementation Details

### Reader Agent Constraints
- Input: Untrusted documents, emails, web pages
- Output: Structured JSON only (facts, entities, metadata)
- Capabilities: NONE (no file access, no network, no actions)
- Model: Can use cheaper model (Titan) since it's sandboxed

### Executor Agent Constraints
- Input: Structured JSON from Reader only
- Output: User-facing responses, actions
- Capabilities: Full (file access, API calls, etc.)
- Model: Can use any model, protected by architecture

### Trust Boundary
- Communication: JSON schema validation
- Validation: Reject malformed or suspicious structures
- Logging: Audit all cross-boundary communication

## Attack Resistance

| Attack Type | Vulnerable Agent | Privilege Separated |
|-------------|------------------|---------------------|
| Indirect Injection | ✗ Succeeds | ✓ Blocked |
| Document Poisoning | ✗ Succeeds | ✓ Blocked |
| Instruction Override | ✗ Succeeds | ✓ Blocked |
| Data Exfiltration | ✗ Succeeds | ✓ Blocked |

## Code Example

See `app.py` for full implementation demonstrating:
- Document processing with poisoned content
- Reader agent extracting structured facts
- Executor agent answering questions from facts only
- Attack attempts failing due to privilege separation

## Key Takeaways

1. **Separate concerns**: Reading ≠ Executing
2. **Minimize privileges**: Each agent gets only what it needs
3. **Trust boundaries**: Validate all cross-zone communication
4. **Defense-in-depth**: Even if Reader is compromised, system stays secure
5. **Cost optimization**: Use cheaper models for untrusted zones
