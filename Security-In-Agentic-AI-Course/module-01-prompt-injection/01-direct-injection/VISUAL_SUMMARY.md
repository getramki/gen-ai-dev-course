# Visual Summary: Model x Architecture

## The 2x2 Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROMPT INJECTION SECURITY                     │
│                    Model vs Architecture                         │
└─────────────────────────────────────────────────────────────────┘

                 WEAK ARCHITECTURE          STRONG ARCHITECTURE
                 ═════════════════          ══════════════════
                 • Secrets in prompt        • No secrets in prompt
                 • Single agent             • Privilege separation
                 • No validation            • Output validation

STRONG MODEL    ┌──────────────────┐       ┌──────────────────┐
(Claude 3)      │ Vulnerable       │       │ Secure Claude    │
                │ Claude           │       │                  │
                │                  │       │ ✓ 0% Success     │
                │ ⚠️  ~17% Success │       │ ✓ Protected      │
                │ ⚠️  Still leaks  │       │ ✓ No leakage     │
                │                  │       │                  │
                │ vulnerable-agent/│       │ secure-agent/    │
                └──────────────────┘       └──────────────────┘

WEAK MODEL      ┌──────────────────┐       ┌──────────────────┐
(Titan)         │ Vulnerable       │       │ Secure Titan     │
                │ Titan            │       │                  │
                │                  │       │ ✓ 0% Success     │
                │ ⚠️⚠️ ~50-83%     │       │ ✓ Protected      │
                │ ⚠️⚠️ Very leaky  │       │ ✓ No leakage     │
                │                  │       │                  │
                │ vulnerable-      │       │ secure-agent-    │
                │ agent-titan/     │       │ titan/           │
                └──────────────────┘       └──────────────────┘
```

## Key Observations

### Vertical Comparison (Same Architecture)
```
Vulnerable Claude (17%)  vs  Vulnerable Titan (50-83%)
└─────────────────────────────────────────────────────┘
         Model safety matters (Claude > Titan)
         But BOTH are still vulnerable
```

### Horizontal Comparison (Same Model)
```
Vulnerable Titan (50-83%)  vs  Secure Titan (0%)
└──────────────────────────────────────────────┘
      Architecture matters MORE
      Same model, huge difference
```

### Diagonal Comparison
```
Vulnerable Claude (17%)  vs  Secure Titan (0%)
└────────────────────────────────────────────┘
   Weak model + Strong architecture BEATS
   Strong model + Weak architecture
```

## Attack Success Visualization

```
Attack Success Rate (Lower is Better)
═══════════════════════════════════

100% │
     │
 80% │  ████████████████
     │  ████████████████  Vulnerable Titan
 60% │  ████████████████  (~50-83%)
     │  ████████████████
 40% │  ████████████████
     │  ████████████████
 20% │  ████  Vulnerable Claude (~17%)
     │  ████
  0% │  ════════════════════════════════════
     │  Secure Claude (0%)  Secure Titan (0%)
     └────────────────────────────────────────
```

## The Architectural Difference

### Vulnerable Architecture
```
┌─────────────────────────────────────┐
│ System Prompt                       │
│ ┌─────────────────────────────────┐ │
│ │ You are a helpful agent         │ │
│ │                                 │ │
│ │ CONFIDENTIAL:                   │ │
│ │ • Code: TECH2024-50OFF    ⚠️    │ │
│ │ • Email: ceo@...          ⚠️    │ │
│ │ • Product: Phoenix        ⚠️    │ │
│ └─────────────────────────────────┘ │
│                                     │
│ User Input: [Prompt Injection]      │
│ ↓                                   │
│ Single Agent (All capabilities)     │
│ ↓                                   │
│ Response: [May leak secrets]   ⚠️   │
└─────────────────────────────────────┘
```

### Secure Architecture
```
┌─────────────────────────────────────┐
│ Classifier Prompt                   │
│ ┌─────────────────────────────────┐ │
│ │ Classify user intent            │ │
│ │ (NO secrets here)          ✓    │ │
│ └─────────────────────────────────┘ │
│ ↓                                   │
│ Structured Action (JSON)            │
│ ↓                                   │
│ Responder Prompt                    │
│ ┌─────────────────────────────────┐ │
│ │ You are a helpful agent         │ │
│ │ (NO secrets here)          ✓    │ │
│ └─────────────────────────────────┘ │
│ ↓                                   │
│ Output Validation                   │
│ ↓                                   │
│ Response: [No secrets to leak] ✓    │
└─────────────────────────────────────┘

Secrets stored separately in:
• AWS Secrets Manager
• Secure database
• Retrieved only when needed with auth
```

## Decision Tree

```
                    Need to secure LLM agent?
                            │
                            ▼
                ┌───────────────────────┐
                │ Do you have secrets   │
                │ in system prompts?    │
                └───────────┬───────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
               YES                     NO
                │                       │
                ▼                       ▼
        ⚠️  VULNERABLE          ✓ Good start
        Remove secrets!         Add more defenses:
                │                       │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Use privilege         │
                │ separation?           │
                └───────────┬───────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
               YES                     NO
                │                       │
                ▼                       ▼
        ✓ Better!              ⚠️  Add it!
                │                       │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Validate outputs?     │
                └───────────┬───────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
               YES                     NO
                │                       │
                ▼                       ▼
        ✓✓ SECURE!             ⚠️  Add it!
```

## The Formula

```
Security = Architecture × Model Safety

Where:
• Architecture: 0 (vulnerable) or 1 (secure)
• Model Safety: 0.0 to 1.0 (Titan ~0.3, Claude ~0.8)

Examples:
• Vulnerable Claude: 0 × 0.8 = 0 (VULNERABLE)
• Vulnerable Titan:  0 × 0.3 = 0 (VULNERABLE)
• Secure Claude:     1 × 0.8 = 0.8 (SECURE)
• Secure Titan:      1 × 0.3 = 0.3 (SECURE)

Lesson: Architecture is a multiplier. If it's 0, you get 0.
```

## Quick Reference

| Want to... | Solution |
|-----------|----------|
| Save costs by using cheaper model | ✓ Use secure architecture with Titan |
| Use strongest model for security | ⚠️  Still need secure architecture |
| Switch models in future | ✓ Secure architecture works with any model |
| Quick fix for vulnerable system | 1. Remove secrets from prompts<br>2. Add privilege separation<br>3. Add output validation |

## Testing Commands

```bash
# See the full comparison
python compare_all.py

# Test individual agents
cd vulnerable-agent && python test_attacks.py
cd vulnerable-agent-titan && python test_attacks.py
cd secure-agent && python test_defenses.py
cd secure-agent-titan && python test_defenses.py
```

## Bottom Line

```
┌────────────────────────────────────────────────────┐
│                                                    │
│  Architecture > Model Safety                       │
│                                                    │
│  • Weak model + Strong architecture = Secure      │
│  • Strong model + Weak architecture = Vulnerable  │
│                                                    │
│  Focus on architecture first, model second.       │
│                                                    │
└────────────────────────────────────────────────────┘
```
