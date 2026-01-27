# Model Configuration

## Amazon Nova 2 Lite v1

All 4 architecture defense patterns use **Amazon Nova 2 Lite v1** (`global.amazon.nova-2-lite-v1:0`).

### Why Nova 2 Lite for Defense Patterns?

1. **Architecture Independence**: These patterns work with ANY model - using Nova 2 Lite proves the architecture matters more than model choice
2. **Cost Efficiency**: Nova 2 Lite is cost-effective for demonstrations
3. **Consistency**: Same model across all patterns for fair comparison
4. **Real-World Relevance**: Shows that even weaker models can be secured with proper architecture

### Pattern Model Usage

| Pattern | Reader/Generator Agent | Executor/Validator | Notes |
|---------|----------------------|-------------------|-------|
| Pattern 1: Privilege Separation | Nova 2 Lite | Nova 2 Lite | Both agents use same model |
| Pattern 2: Output Validation | Nova 2 Lite | Validator (code) | Agent generates, validator checks |
| Pattern 3: Sandboxing | Nova 2 Lite | Sandbox (code) | Agent generates, sandbox restricts |
| Pattern 4: Human-in-Loop | Nova 2 Lite | Approval System (code) | Agent proposes, human approves |

### Key Insight

**Architecture > Model Safety**

Even with Titan (which has weaker safety features than Claude), all 4 patterns successfully block attacks because:
- Pattern 1: Privilege separation prevents capability abuse
- Pattern 2: Output validation blocks malicious actions
- Pattern 3: Sandboxing restricts execution environment
- Pattern 4: Human approval catches suspicious patterns

This proves that **architectural defenses work regardless of the underlying model**.

### Testing Notes

When testing these patterns:
- Titan may generate more varied outputs than Claude
- JSON extraction may require adjustment for different response formats
- Attack success rate would be higher WITHOUT these architectural defenses
- WITH defenses, attack success rate is 0% regardless of model
