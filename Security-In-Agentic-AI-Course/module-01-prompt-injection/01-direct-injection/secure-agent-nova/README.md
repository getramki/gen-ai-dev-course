# Secure Agent - Amazon Nova 2 Lite with Architectural Defenses

## Purpose

Demonstrates that **architectural defenses work with any model**, including Amazon Nova 2 Lite.

## Key Architectural Defenses

### 1. NO Confidential Data in Prompts
- Discount codes, emails, product names stored separately
- Never exposed to LLM context
- Eliminates primary attack vector

### 2. Privilege Separation
- **Classifier Agent**: Determines intent (no sensitive data)
- **Responder Agent**: Generates responses (limited capabilities)
- Each agent has minimal necessary privileges

### 3. Output Validation
- Checks response length
- Detects system prompt leakage
- Blocks suspicious outputs

### 4. Limited Capabilities
- Agents can only perform specific tasks
- No access to sensitive operations
- Fail-safe defaults

## Architecture

```
User Input
    ↓
Classifier Agent (Nova)
    ↓
Intent Classification
    ↓
Responder Agent (Nova)
    ↓
Output Validation
    ↓
Safe Response
```

## Setup

```bash
pip install -r requirements.txt

# Run secure chatbot
python app.py

# Test defenses
python test_defenses.py
```

## Expected Results

All attacks should be blocked:
- ✓ Jailbreak attempts fail
- ✓ System overrides fail
- ✓ Task deflection fails
- ✓ No confidential data leaked

## Why This Works

1. **No data to steal**: Confidential info not in prompts
2. **Separation of concerns**: Each agent has limited scope
3. **Output validation**: Catches leakage attempts
4. **Fail-safe design**: Defaults to safe responses

## Comparison

| Implementation | Model | Confidential Data | Success Rate |
|---------------|-------|------------------|--------------|
| Vulnerable Nova | Nova 2 Lite | In prompts | High |
| Secure Nova | Nova 2 Lite | External | 0% |

## Key Lesson

**Architecture > Model Choice**

Even with the same model (Nova 2 Lite):
- Vulnerable architecture → High attack success
- Secure architecture → Zero attack success

## Try It

```bash
# Test defenses
python test_defenses.py

# Compare with vulnerable version
cd ../vulnerable-agent-nova
python test_attacks.py
```

## Defense Principles

1. **Never trust user input**
2. **Minimize LLM privileges**
3. **Validate all outputs**
4. **Store secrets externally**
5. **Use multiple agents with separation**

## Next Steps

1. Compare with vulnerable Nova implementation
2. Review other secure implementations (Titan, Claude)
3. Understand defense patterns apply to any model
4. Apply to your production systems
