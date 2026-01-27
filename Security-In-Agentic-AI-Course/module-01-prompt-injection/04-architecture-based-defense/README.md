# Architecture-Based Defense Patterns

## Overview
This module demonstrates 4 core architectural patterns that defend against prompt injection attacks. These patterns work by **changing the system design** rather than trying to detect attacks.

## Why Architecture Over Detection?

**Detection-based defenses FAIL because:**
- Attackers can rephrase prompts infinitely
- Natural language has no formal syntax to validate
- Context matters more than keywords
- Semantic attacks bypass pattern matching

**Architecture-based defenses SUCCEED because:**
- They limit what's possible, not what's detectable
- They work regardless of attack creativity
- They provide defense-in-depth
- They follow proven security principles

## The 4 Core Patterns

### Pattern 1: Privilege Separation
**Principle**: Separate agents with different trust levels and capabilities

**How it works**:
- Reader Agent (untrusted): Processes external data, extracts structured facts
- Executor Agent (trusted): Takes actions based only on structured facts
- Trust boundary: JSON communication between agents

**Defends against**: Indirect injection through poisoned documents

**Example**: RAG system where document processor can't execute actions

---

### Pattern 2: Output Validation
**Principle**: Validate agent outputs before execution, not just inputs

**How it works**:
- Agent generates structured output (JSON)
- Validator checks output against allowed schema
- Only valid, safe actions are executed
- Invalid outputs are rejected

**Defends against**: Instruction override, task deflection

**Example**: Email agent that validates recipient addresses before sending

---

### Pattern 3: Sandboxing
**Principle**: Isolate agent execution in restricted environment

**How it works**:
- Agent runs in sandbox with limited capabilities
- File system, network, and system access restricted
- Resource limits (CPU, memory, time)
- Violations terminate execution

**Defends against**: System access, data exfiltration

**Example**: Code execution agent with no network access

---

### Pattern 4: Human-in-the-Loop
**Principle**: Require human approval for sensitive actions

**How it works**:
- Agent proposes actions, doesn't execute directly
- Human reviews and approves/rejects
- Audit trail of all decisions
- Risk-based approval thresholds

**Defends against**: All attacks on high-risk operations

**Example**: Financial transaction agent requiring approval for transfers

---

## Pattern Comparison

| Pattern | Complexity | Performance Impact | Security Level | Best For |
|---------|------------|-------------------|----------------|----------|
| Privilege Separation | Medium | Low | High | Multi-agent systems |
| Output Validation | Low | Very Low | Medium | Structured actions |
| Sandboxing | High | Medium | Very High | Code execution |
| Human-in-Loop | Low | High (latency) | Highest | Critical operations |

## Combining Patterns

**Defense-in-Depth**: Use multiple patterns together for maximum security

**Example: Secure Email Agent**
1. **Privilege Separation**: Separate email reader and sender agents
2. **Output Validation**: Validate email addresses and content structure
3. **Sandboxing**: Limit network access to approved email servers only
4. **Human-in-Loop**: Require approval for emails to external domains

## Implementation Guide

Each pattern folder contains:
- `README.md` - Pattern explanation and theory
- `app.py` - Working implementation with Amazon Bedrock
- Supporting files - Architecture diagrams, validators, etc.

## Quick Start

```bash
# Pattern 1: Privilege Separation
cd pattern-1-privilege-separation
python app.py

# Pattern 2: Output Validation
cd pattern-2-output-validation
python app.py

# Pattern 3: Sandboxing
cd pattern-3-sandboxing
python app.py

# Pattern 4: Human-in-Loop
cd pattern-4-human-in-loop
python app.py
```

## Key Takeaways

1. **Architecture > Detection**: Change the system, don't try to detect attacks
2. **Least Privilege**: Give each component minimal necessary capabilities
3. **Trust Boundaries**: Clearly separate trusted and untrusted components
4. **Validation**: Validate outputs (what agent wants to do), not inputs (what user says)
5. **Defense-in-Depth**: Layer multiple patterns for maximum security
