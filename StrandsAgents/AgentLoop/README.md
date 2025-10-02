# Agent Loop Demo - Strands Agents Framework

## Overview

This demo illustrates the core **Agent Loop** concept from the Strands Agents framework. The Agent Loop is the fundamental execution pattern where an agent continuously cycles through three phases:

1. **Think** - Process input and decide on actions
2. **Act** - Execute the decided actions  
3. **Observe** - Evaluate results and update internal state

## Agent Loop Concept

Based on the [Strands Agents documentation](https://strandsagents.com/0.1.x/documentation/docs/user-guide/concepts/agents/agent-loop/), the Agent Loop provides:

- **Autonomous Decision Making**: Agents can reason about their environment
- **Iterative Improvement**: Each cycle refines the agent's understanding
- **State Management**: Maintains context across iterations
- **Error Recovery**: Handles failures gracefully

## Demo Architecture

```
┌─────────────────┐
│   User Input    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   THINK Phase   │ ◄─┐
│ (Process Input) │   │
└─────────┬───────┘   │
          │           │
          ▼           │
┌─────────────────┐   │
│   ACT Phase     │   │ Agent Loop
│ (Execute Action)│   │ Iteration
└─────────┬───────┘   │
          │           │
          ▼           │
┌─────────────────┐   │
│ OBSERVE Phase   │   │
│ (Evaluate &     │ ──┘
│  Update State)  │
└─────────────────┘
```

## Files Structure

```
AgentLoop/
├── agent_loop_demo.py    # Core Agent Loop implementation
├── interactive_demo.py   # Interactive demo with user input
├── config.py            # Configuration and scenarios
├── run_demo.sh          # Quick start script
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Step-by-Step Instructions

### Prerequisites

- Python 3.8 or higher
- Basic understanding of async/await in Python

### Step 1: Setup Environment

```bash
# Navigate to the demo directory
cd /home/ramakrishna/Code/GenAI-for-Dev-Course/StrandsAgents/AgentLoop

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (currently none required)
pip install -r requirements.txt
```

### Step 2: Run the Demo

**Quick Start (Recommended)**
```bash
# Use the interactive menu
./run_demo.sh
```

**Option A: Automated Demo**
```bash
# Run the basic automated demo
python3 agent_loop_demo.py

# Or run automated scenarios
python3 interactive_demo.py --auto
```

**Option B: Interactive Demo**
```bash
# Run interactive session
python3 interactive_demo.py

# Then type commands like:
# - "Hello there!" (for greeting)
# - "demo" (to run all scenarios)
# - "memory" (to see agent memory)
# - "quit" (to exit)
```

### Step 3: Understanding the Output

The demo will show:

1. **Agent Loop Initialization** - Starting the cycle
2. **Think Phase** - Agent processing input and deciding actions
3. **Act Phase** - Executing the chosen action
4. **Observe Phase** - Evaluating results and updating state
5. **Iteration Control** - Continuing or completing the loop

### Step 4: Explore Different Scenarios

The demo includes test cases for:
- Greeting interactions
- Weather queries
- Time requests
- Complex/unknown requests

### Step 5: Examine the Code

Key components to understand:

#### AgentState Enum
```python
class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    OBSERVING = "observing"
    COMPLETED = "completed"
```

#### Core Loop Method
```python
async def run_loop(self, user_input: str) -> str:
    # Think -> Act -> Observe cycle
    action = await self.think(current_input)
    result = await self.act(action)
    observation = await self.observe(result)
```

## Expected Output

```
🤖 Strands Agents - Agent Loop Demo
========================================

🔄 Demo Scenario 1

🚀 Starting Agent Loop for: 'Hello there!'
==================================================

--- Iteration 1 ---
🤔 DemoAgent is thinking about: 'Hello there!'
🎯 DemoAgent is executing action: greet_user
👁️ DemoAgent is observing result: 'Hello! Nice to meet you!'

✅ DemoAgent completed successfully!
📤 Final Response: Hello! Nice to meet you!
```

## Key Learning Points

1. **Autonomous Cycles**: The agent runs independently through Think-Act-Observe
2. **State Management**: Agent maintains state across iterations
3. **Decision Making**: Each phase contributes to the overall intelligence
4. **Memory System**: Agent stores and recalls previous interactions
5. **Error Handling**: Graceful handling of unexpected situations

## Extending the Demo

To enhance this demo:

1. **Add Real Tools**: Integrate actual APIs (weather, time, etc.)
2. **Improve Memory**: Implement persistent storage
3. **Add Learning**: Use ML models for better decision making
4. **Multi-Agent**: Create multiple agents that interact
5. **Real Framework**: Integrate with actual Strands Agents library

## Next Steps

1. Explore the full Strands Agents framework
2. Implement more sophisticated reasoning
3. Add external tool integrations
4. Build multi-agent systems
5. Deploy in production environments

## Resources

- [Strands Agents Documentation](https://strandsagents.com/0.1.x/documentation/)
- [Agent Loop Concepts](https://strandsagents.com/0.1.x/documentation/docs/user-guide/concepts/agents/agent-loop/)
- [Python Asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

## Troubleshooting

**Issue**: Import errors
**Solution**: Ensure Python 3.8+ and check virtual environment

**Issue**: Async errors  
**Solution**: Verify asyncio compatibility and Python version

**Issue**: Demo not running
**Solution**: Check file permissions and Python path