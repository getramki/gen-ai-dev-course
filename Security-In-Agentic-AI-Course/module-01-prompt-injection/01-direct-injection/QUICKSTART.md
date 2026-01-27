# Quick Start Guide

## TL;DR

```bash
# Compare ALL combinations (Model x Architecture)
python compare_all.py

# This will show:
# - Vulnerable Claude: ~17% attack success
# - Vulnerable Titan: ~50-83% attack success
# - Secure Claude: 0% attack success
# - Secure Titan: 0% attack success
# - Lesson: Architecture > Model Safety
```

## What's Here

### 4 Agent Combinations (Model x Architecture)

1. **vulnerable-agent/** - Claude + Weak Architecture
   - Strong model safety
   - But vulnerable architecture
   - ~17% attack success

2. **vulnerable-agent-titan/** - Titan + Weak Architecture
   - Weak model safety
   - Vulnerable architecture
   - ~50-83% attack success

3. **secure-agent/** - Claude + Strong Architecture
   - Strong model safety
   - Strong architecture
   - 0% attack success

4. **secure-agent-titan/** - Titan + Strong Architecture
   - Weak model safety
   - But strong architecture
   - 0% attack success

## Quick Tests

### Test Individual Models

```bash
# Test Claude
cd vulnerable-agent
python test_attacks.py

# Test Titan
cd ../vulnerable-agent-titan
python test_attacks.py
```

### Compare All Combinations

```bash
# Compare all 4 combinations
python compare_all.py

# Or compare just models
python compare_models.py
```

### Test Secure Version

```bash
cd secure-agent
python app.py
# Try same attacks - observe defenses
```

## What You'll Learn

### 1. Model Safety Varies
- **Claude**: Strong safety, but not perfect
- **Titan**: Weaker safety, more vulnerable
- **Lesson**: Can't rely on model choice alone

### 2. Architectural Flaw is Universal
- Same vulnerability in both models
- Confidential data in prompts is always at risk
- Model safety is probabilistic, not guaranteed

### 3. Architecture is the Solution
- Secure agent works with ANY model
- Doesn't rely on model safety features
- Future-proof against model changes

## Expected Results

| Agent | Attack Success Rate | Key Insight |
|-------|-------------------|-------------|
| Vulnerable Claude | ~17% (1-2 out of 6) | Strong model, weak architecture |
| Vulnerable Titan | ~50-83% (3-5 out of 6) | Weak model, weak architecture |
| Secure Claude | 0% (0 out of 6) | Strong model, strong architecture |
| Secure Titan | 0% (0 out of 6) | Weak model, strong architecture |

## Key Takeaways

1. **Vulnerability varies by model** - Weaker models are more vulnerable
2. **But the flaw is the same** - Confidential data in prompts
3. **Model safety isn't enough** - Even Claude isn't 100% secure
4. **Architecture is essential** - Works with any model, now and future

## Files to Read

1. **IMPORTANT_NOTE.md** - Why Claude's safety features aren't enough
2. **ATTACK_GUIDE.md** - Detailed explanation of each attack
3. **secure-agent/defenses.md** - How architectural defenses work
4. **compare_models.py** - Side-by-side comparison script

## Next Steps

After running the comparisons:

1. Review results - Note the difference in success rates
2. Read `secure-agent/defenses.md` - Understand architectural solutions
3. Apply to your systems - Don't put secrets in prompts
4. Use defense-in-depth - Multiple layers of protection

## Production Checklist

- [ ] No confidential data in system prompts
- [ ] Privilege separation (different agents for different tasks)
- [ ] Output validation (validate actions, not inputs)
- [ ] Least privilege (minimal capabilities per agent)
- [ ] Logging and monitoring (audit trail)
- [ ] Don't rely on model safety features alone

## Questions?

- **Q: Why test multiple models?**
  - A: Shows vulnerability is architectural, not model-specific

- **Q: Should I use Claude or Titan?**
  - A: Use architectural defenses regardless of model choice

- **Q: Is Claude secure enough?**
  - A: No model is secure enough without architectural defenses

- **Q: What if I can't change my architecture?**
  - A: At minimum: Remove confidential data from prompts, add logging
