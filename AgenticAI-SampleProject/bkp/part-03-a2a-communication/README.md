# Part 3: A2A Communication Implementation

This part implements Agent-to-Agent (A2A) communication using the official A2A SDK, extending the functionality from Parts 1 and 2.

## Architecture

### Agents
1. **Purchase Agent** (Port 10001) - Procurement optimization with budget constraints
2. **Cement Agent** (Port 10002) - Cement sales with profit maximization
3. **Steel Agent** (Port 10003) - Premium steel sales with higher margins

### Key Features
- Official A2A SDK integration
- JSON-RPC protocol compliance
- Agent cards exposed through API endpoints
- Profit optimization algorithms
- Negotiation cycle management (max 4-5 rounds)
- LLM reasoning for transparent decision-making

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up AWS credentials for Bedrock
aws configure
# OR set environment variables:
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

## Running the Agents

### Start All Agents
```bash
# Make script executable
chmod +x start_agents.sh

# Start all three agents
./start_agents.sh
```

### Start Individual Agents
```bash
# Purchase Agent (Port 10001)
cd purchase_agent
python -m app --host localhost --port 10001

# Cement Agent (Port 10002)
cd cement_agent
python -m app --host localhost --port 10002

# Steel Agent (Port 10003)
cd steel_agent
python -m app --host localhost --port 10003
```

### Kill Processes
```bash
# Kill all agents
pkill -f "python -m app"
```
# Kill Purchase agent by port
```bash
lsof -ti:10001 | xargs kill -9  
```
# Kill Cement Agent
```bash
lsof -ti:10002 | xargs kill -9  
```
# Kill Steel Agent
```bash
lsof -ti:10003 | xargs kill -9  
```
## Testing

### Agent Cards API
Each agent exposes its capabilities through agent cards at the root endpoint:

```bash
# Get Purchase Agent card
curl http://localhost:10001/

# Get Cement Agent card
curl http://localhost:10002/

# Get Steel Agent card
curl http://localhost:10003/
```

### Demo Client
Test all agents using the provided demo client:

```bash
python demo_client.py
```

### Manual JSON-RPC Testing
```bash
# Test Purchase Agent
curl -X POST http://localhost:10001/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "agent.execute",
    "params": {
      "message": {
        "content": [{"type": "text", "text": "I need 1000 tons of cement and 100 tons of steel within $130k budget"}],
        "role": "user"
      }
    },
    "id": 1
  }'
```

## Agent Capabilities

### Purchase Agent
- **Skills**: Construction Procurement, Supplier Negotiation
- **Capabilities**: Cost optimization, Budget management, Contract negotiation
- **Constraints**: Budget limits, approval thresholds, margin requirements

### Cement Agent
- **Skills**: Cement Pricing & Quotes, Cement Sales Negotiation
- **Capabilities**: Profit optimization, Competitive pricing, Margin protection (25%)
- **Strategy**: Volume-based pricing with delivery optimization

### Steel Agent
- **Skills**: Premium Steel Pricing & Quotes, Steel Sales Negotiation
- **Capabilities**: Profit optimization, Quality focus, Premium margins (30%)
- **Strategy**: Quality-focused pricing with premium positioning

## A2A Protocol Implementation

### Agent Cards
- Exposed at root endpoint (`/`) for each agent
- Contains skills, capabilities, and supported content types
- Follows official A2A SDK AgentCard format
- Includes version, URL, and capability information

### JSON-RPC Communication
- Standard JSON-RPC 2.0 protocol
- Method: `agent.execute`
- Streaming support for real-time responses
- Task management with status updates
- Proper error handling and validation

### Official A2A SDK Usage
- Uses `A2AStarletteApplication` for server setup
- Implements `AgentExecutor` for request handling
- Follows `RequestContext` and `EventQueue` patterns
- Proper task state management and artifacts

## Integration with Parts 1 & 2

This implementation extends the previous parts:
- **Part 1**: LangGraph + AWS Bedrock foundation
- **Part 2**: MCP tool integration for enhanced capabilities
- **Part 3**: A2A communication layer for inter-agent interaction

## File Structure
```
part-03-a2a-communication/
├── purchase_agent/
│   └── app/
│       ├── __init__.py
│       ├── __main__.py          # A2A server setup
│       ├── agent.py             # Core agent logic
│       └── agent_executor.py    # A2A executor
├── cement_agent/
│   └── app/
│       ├── __init__.py
│       ├── __main__.py
│       ├── agent.py
│       └── agent_executor.py
├── steel_agent/
│   └── app/
│       ├── __init__.py
│       ├── __main__.py
│       ├── agent.py
│       └── agent_executor.py
├── demo_client.py               # Test client
├── start_agents.sh              # Startup script
├── requirements.txt
└── README.md
```

## Next Steps
- **Part 4**: Docker containerization
- **Part 5**: Cloud deployment on AWS