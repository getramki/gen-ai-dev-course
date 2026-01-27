# Vulnerable Agent - Amazon Nova 2 Lite Model

## Purpose

This version uses **Amazon Nova 2 Lite** to demonstrate prompt injection vulnerabilities with a newer, lightweight model.

## Why This Exists

- **Nova 2 Lite** is Amazon's latest lightweight model
- Demonstrates vulnerabilities across different model generations
- Shows that architectural defenses are essential regardless of model choice
- Complements existing Titan and Claude implementations

## Model Details

- **Model ID**: `amazon.nova-lite-v1:0`
- **Type**: Lightweight multimodal model
- **Use Case**: Educational demonstration of prompt injection vulnerabilities

## Setup

```bash
pip install -r requirements.txt

# Ensure Nova model access in Bedrock
aws bedrock list-foundation-models --region us-east-1 | grep nova

# Run chatbot
python app.py

# Or run automated tests
python test_attacks.py
```

## Expected Results

With Nova 2 Lite, you can test:
- Information extraction attacks
- Jailbreak attempts
- System override techniques
- Task deflection

This demonstrates:
1. Vulnerabilities exist across model types
2. Newer models still require architectural defenses
3. Model choice alone doesn't guarantee security

## Comparison

| Model | Type | Expected Vulnerability |
|-------|------|----------------------|
| Claude 3 Haiku | Strong safety | Lower (~17%) |
| Titan Text Express | Weaker safety | Higher (~50-83%) |
| Nova 2 Lite | Lightweight | To be tested |

## Key Lesson

**Architecture-based defenses work regardless of model.**

Even with newer models:
- Prompt injection remains a risk
- Architectural patterns provide consistent protection
- Defense-in-depth is essential

## Try It

```bash
# Test all attacks
python test_attacks.py

# Compare with other models
cd ../vulnerable-agent-titan
python test_attacks.py

cd ../vulnerable-agent
python test_attacks.py
```

## What This Proves

1. **Model-agnostic vulnerability**: Prompt injection affects all LLMs
2. **Architectural flaw remains**: Same vulnerability pattern
3. **Consistent defense needed**: Architecture protects any model
4. **Future-proofing**: Works with current and future models

## Next Steps

After testing with Nova:
1. Compare results with Titan and Claude
2. Review secure agent architecture (`../secure-agent/`)
3. Understand why architecture > model choice
4. Apply lessons to production systems
