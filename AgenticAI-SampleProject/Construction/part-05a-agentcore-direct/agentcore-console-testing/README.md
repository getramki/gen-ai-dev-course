# AgentCore Console Testing

Test input JSON files for AgentCore console testing of construction agents.

## Test Files

### Purchase Agent Test
- **File**: `purchase-agent-test.json`
- **Scenario**: Construction manager procuring cement and steel with budget constraints
- **Tests**: Cost calculation, supplier evaluation, budget optimization

### Cement Agent Test  
- **File**: `cement-agent-test.json`
- **Scenario**: Cement sales with profit maximization for regular customer
- **Tests**: Price optimization, margin calculation, competitive pricing

### Steel Agent Test
- **File**: `steel-agent-test.json` 
- **Scenario**: Premium steel sales to new large customer
- **Tests**: Premium pricing, inventory management, profit maximization

## Usage in AgentCore Console

1. Navigate to your deployed agent in AgentCore console
2. Go to "Test" or "Invoke" section
3. Copy the JSON content from the relevant test file
4. Paste into the input field
5. Execute to test agent functionality

## Expected Behaviors

- **Purchase Agent**: Should calculate costs, evaluate suppliers, check budget constraints
- **Cement Agent**: Should optimize pricing for profit while staying competitive  
- **Steel Agent**: Should offer premium pricing with margin maximization

Each agent should demonstrate their LangChain tools and profit optimization logic.