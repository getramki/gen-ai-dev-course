# Secure Agent - Amazon Titan

## Purpose

Demonstrates that **architectural defenses work regardless of model safety features**.

Even though Titan has weaker built-in safety, the secure architecture prevents attacks.

## Key Defenses

### 1. No Confidential Data in Prompts
```python
# ❌ Vulnerable (both Claude and Titan)
system_prompt = "Discount code: TECH2024-50OFF"

# ✅ Secure (works with any model)
system_prompt = "You are a helpful assistant"
# Retrieve secrets from secure storage when needed
```

### 2. Privilege Separation
- **Classifier Agent**: Only classifies intent (no confidential data)
- **Responder Agent**: Only generates responses (no confidential data)
- Even if compromised, agents have no secrets to leak

### 3. Output Validation
- Validates what the agent produces
- Blocks responses that leak system prompts
- Works regardless of model's internal safety

### 4. Limited Capabilities
- Each agent has minimal permissions
- No dangerous tools or data access
- Limits blast radius of successful attacks

## Architecture

```
User Input
    ↓
[Classifier Agent - Titan]
    ↓
Structured Action (JSON)
    ↓
[Action Validator]
    ↓
[Responder Agent - Titan]
    ↓
[Output Validator]
    ↓
Response (No Secrets)
```

## Setup

```bash
pip install -r requirements.txt
python app.py

# Or test all defenses
python test_defenses.py
```

## Expected Results

| Version | Attack Success Rate |
|---------|-------------------|
| Vulnerable Titan | ~50-83% (3-5 out of 6) |
| Secure Titan | 0% (0 out of 6) |

**The difference is architecture, not model.**

## Comparison

### Vulnerable Titan
```python
system_prompt = """
Confidential: TECH2024-50OFF  # ❌ In prompt
"""
response = titan.invoke(system_prompt + user_input)
```
**Result**: Confidential data can be extracted

### Secure Titan
```python
system_prompt = "You are helpful"  # ✅ No secrets
response = titan.invoke(system_prompt + user_input)
# Secrets retrieved from secure storage only when needed
```
**Result**: Nothing confidential to extract

## Key Insights

### 1. Architecture > Model Safety
- Vulnerable Titan: High attack success
- Secure Titan: Zero attack success
- Same model, different architecture

### 2. Works with Any Model
- Secure Claude: Protected
- Secure Titan: Protected
- Architecture is model-independent

### 3. Future-Proof
- Model safety features change
- New models emerge
- Architecture remains effective

### 4. Defense-in-Depth
Multiple layers:
1. No secrets in prompts (primary defense)
2. Privilege separation (limits impact)
3. Output validation (catches leaks)
4. Logging (detection and audit)

## Testing

```bash
# Test secure Titan
python test_defenses.py

# Compare with vulnerable Titan
cd ../vulnerable-agent-titan
python test_attacks.py

# See the difference in success rates
```

## What This Proves

**Architectural defenses work even with weaker models.**

- Titan is more vulnerable than Claude
- But secure Titan is as safe as secure Claude
- The key is architecture, not model choice

## Production Implications

### Don't Do This
```python
# "I'll use Claude because it's more secure"
# Still vulnerable if architecture is flawed
```

### Do This
```python
# "I'll use secure architecture that works with any model"
# Protected regardless of model choice
```

## Key Takeaways

1. **Model safety varies** - Titan < Claude
2. **Architecture is constant** - Works with both
3. **Don't rely on model** - Use architectural defenses
4. **Future-proof design** - Protects even if you switch models

## Next Steps

1. Run `test_defenses.py` to verify protection
2. Compare with `../vulnerable-agent-titan/`
3. Review `../secure-agent/defenses.md` for detailed explanation
4. Apply these patterns to your production systems

## Bottom Line

**Even the weakest model is secure with the right architecture.**
**Even the strongest model is vulnerable with the wrong architecture.**

Choose architecture over model safety.
