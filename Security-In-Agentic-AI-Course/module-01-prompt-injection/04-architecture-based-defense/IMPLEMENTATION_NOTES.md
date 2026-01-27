# Implementation Notes - Phase 4

## Model Configuration

All 4 patterns use **Amazon Nova 2 Lite v1** (`global.amazon.nova-2-lite-v1:0`)

## Implementation Approach

### Direct boto3 Usage

All patterns use boto3 directly instead of the BedrockClient wrapper:

```python
self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
self.model_id = "global.amazon.nova-2-lite-v1:0"

# Invoke model
body = json.dumps({
    "messages": [{"role": "user", "content": [{"text": prompt}]}],
    "inferenceConfig": {
        "max_new_tokens": 500,
        "temperature": 0.7
    }
})
response = self.bedrock.invoke_model(modelId=self.model_id, body=body)
result = json.loads(response['body'].read())['output']['message']['content'][0]['text']
```

### Why Direct boto3?

1. **Consistency**: Matches Phase 2 and Phase 3 implementations
2. **Simplicity**: No wrapper abstraction needed
3. **Nova Support**: Direct API calls work with Nova's response format
4. **Minimal Dependencies**: Only requires boto3

## Pattern-Specific Details

### Pattern 1: Privilege Separation
- **Reader Agent**: Temperature 0.0 (deterministic fact extraction)
- **Executor Agent**: Temperature 0.7 (natural responses)
- Both use same Titan model

### Pattern 2: Output Validation
- **Email Agent**: Temperature 0.7
- JSON extraction from Titan responses
- Validator is pure Python (no LLM)

### Pattern 3: Sandboxing
- **Code Agent**: Temperature 0.7
- Sandbox is pure Python (no LLM)
- Restricted execution environment

### Pattern 4: Human-in-Loop
- **Financial Agent**: Temperature 0.7
- Approval system is pure Python (no LLM)
- Risk assessment logic

## Testing

All patterns tested and working:
- ✅ Pattern 1: Privilege separation blocks indirect injection
- ✅ Pattern 2: Output validation blocks malicious actions
- ✅ Pattern 3: Sandboxing blocks dangerous code execution
- ✅ Pattern 4: Human approval catches suspicious patterns

## Dependencies

Each pattern requires:
```
boto3>=1.28.0
```

No other dependencies needed (shared utilities not required).
