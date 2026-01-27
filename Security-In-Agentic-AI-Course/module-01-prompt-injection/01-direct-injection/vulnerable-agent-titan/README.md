# Vulnerable Agent - Amazon Titan Model

## Purpose

This version uses **Amazon Titan Text Express** which has weaker safety features compared to Claude, making it more susceptible to prompt injection attacks.

## Why This Exists

- **Claude** has strong safety features (only ~17% attack success rate)
- **Titan** has weaker safety features (higher attack success rate expected)
- Demonstrates that vulnerability varies by model
- Shows why architectural defenses are essential regardless of model

## Model Details

- **Model ID**: `amazon.titan-text-express-v1`
- **Safety Features**: Weaker than Claude
- **Expected Attack Success**: Higher than Claude
- **Use Case**: Educational demonstration of model-dependent vulnerabilities

## Setup

```bash
pip install -r requirements.txt

# Ensure Titan model access in Bedrock
aws bedrock list-foundation-models --region us-east-1 | grep titan

# Run chatbot
python app.py

# Or run automated tests
python test_attacks.py
```

## Expected Results

With Titan, you should see:
- **More attacks succeed** compared to Claude
- **Easier information extraction**
- **Less resistance to jailbreaks**

This proves:
1. Model safety features vary significantly
2. Weaker models are more vulnerable
3. Architectural defenses are essential regardless of model choice

## Comparison

| Model | Safety Features | Expected Success Rate |
|-------|----------------|----------------------|
| Claude 3 Haiku | Strong | ~17% (1-2 out of 6) |
| Titan Text Express | Weaker | ~50-83% (3-5 out of 6) |

## Key Lesson

**Don't rely on model safety features alone.**

Even if you use Claude today:
- You might switch models tomorrow
- Model safety can degrade over time
- New attack techniques emerge
- Architectural defenses work regardless of model

## Try It

```bash
# Test all attacks
python test_attacks.py

# Compare with Claude version
cd ../vulnerable-agent
python test_attacks.py

# Observe the difference in success rates
```

## What This Proves

1. **Model-dependent vulnerability**: Weaker models are more vulnerable
2. **Architectural flaw remains**: Same vulnerability regardless of model
3. **Safety features aren't enough**: Need architectural defenses
4. **Future-proofing**: Architecture protects even if you change models

## Next Steps

After seeing higher attack success with Titan:
1. Compare with Claude results (`../vulnerable-agent/`)
2. Review secure agent architecture (`../secure-agent/`)
3. Understand why architecture > model safety
4. Apply lessons to your production systems
