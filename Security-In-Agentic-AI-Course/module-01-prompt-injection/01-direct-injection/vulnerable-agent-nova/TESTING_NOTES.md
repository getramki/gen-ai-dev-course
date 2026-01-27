# Testing Notes - Amazon Nova 2 Lite

## Model Information

- **Model ID**: `amazon.nova-lite-v1:0`
- **Type**: Lightweight multimodal model
- **Release**: 2024 (Amazon's latest generation)

## Expected Behavior

Amazon Nova 2 Lite is a newer model, so its safety features and vulnerability to prompt injection attacks need to be evaluated.

### Attack Categories

1. **Jailbreak - DAN (Do Anything Now)**
   - Tests if model can be convinced to ignore safety rules
   - Expected: May vary based on model training

2. **Jailbreak - Roleplay**
   - Uses fictional scenarios to bypass restrictions
   - Expected: Depends on model's context understanding

3. **System Override**
   - Attempts to override system instructions
   - Expected: Tests instruction hierarchy

4. **Token Smuggling**
   - Uses special formatting to hide instructions
   - Expected: Tests input parsing

5. **Instruction Override**
   - Direct competition with system prompt
   - Expected: Tests prompt priority

6. **Task Deflection**
   - Redirects agent to different task
   - Expected: Tests task boundary enforcement

## Testing Methodology

```bash
# Run automated tests
python test_attacks.py

# Interactive testing
python app.py
```

## Comparison Points

Compare Nova results with:
- **Claude 3 Haiku**: Strong safety (~17% success)
- **Titan Text Express**: Weaker safety (~50-83% success)

## Key Observations

Document your findings:
- Which attacks succeed?
- Which attacks are blocked?
- How does Nova compare to other models?
- Are there unique vulnerabilities or strengths?

## Important Notes

1. **Model Safety Varies**: Different models have different safety features
2. **Architecture Matters More**: Regardless of results, architectural defenses are essential
3. **Future-Proofing**: Models change, architecture provides consistent protection
4. **Educational Purpose**: This is for learning, not production use

## Logging

All interactions are logged to `logs/vulnerable_nova.log` for analysis.

## Next Steps

After testing:
1. Document success rates
2. Compare with other models
3. Review secure agent implementation
4. Understand architectural defenses
