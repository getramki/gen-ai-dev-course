# Agentic AI Construction Project - Master Plan

## Project Overview
This project demonstrates Agentic AI concepts through a construction industry use case involving:
- **Purchase Agent** (Construction Company)
- **Cement Sales Agent** (Cement Company)
- **Steel Sales Agent** (Steel Company)

Agents communicate via A2A protocol, use MCP for tools/resources, LangGraph for agent architecture, and AWS Bedrock for LLM capabilities.

## Technology Stack
- **LLM**: AWS Bedrock (Anthropic Claude)
- **Agent Framework**: LangGraph
- **Tool Protocol**: MCP (Model Context Protocol) with FastMCP for local development
- **Agent Communication**: A2A Protocol (Agent Card, Task, Message, Parts, Artifacts)
- **Containerization**: Docker
- **Deployment**: AgentCore / Amazon EKS
- **SDKs**: Official mcp, a2a-sdk, langgraph, langchain, bedrock

## Core Business Rules
- **Profit Maximization**: Each agent optimizes for company profit within constraints
- **Human Limits**: Pricing bounds, approval thresholds, policy constraints
- **Negotiation Cycles**: Maximum 4-5 rounds to prevent infinite loops
- **Contract Finalization**: Automatic sign-off within cycle limits

## Project Structure
```
Construction/
├── PROJECT_PLAN.md
├── part-01-basic-agent/
├── part-02-mcp-integration/
├── part-03-a2a-communication/
├── part-04-local-deployment/
├── part-05-cloud-deployment/
├── shared/
│   ├── models/
│   ├── utils/
│   └── configs/
└── docs/
```

---

## Part 1: Basic Agent with LangGraph
**Duration**: 2-3 hours  
**Objective**: Build foundational agent using LangGraph and Bedrock

### Learning Goals
- Understand LangGraph agent architecture
- Integrate AWS Bedrock with LangGraph
- Create basic agent workflows
- Implement state management

### Deliverables
1. Simple Purchase Agent with basic decision-making
2. Basic Cement Sales Agent
3. Basic Steel Sales Agent
4. Documentation and demo scripts

### Step-by-Step Instructions
1. **Setup Environment**
   - Install dependencies (langgraph, langchain, boto3)
   - Configure AWS credentials for Bedrock
   - Create project structure

2. **Create Base Agent Class**
   - Define agent state schema
   - Implement Bedrock LLM integration
   - Create basic agent workflow

3. **Implement Purchase Agent**
   - Define procurement requirements with budget constraints
   - Create decision nodes for cost optimization
   - Implement negotiation logic with cycle limits (max 5 rounds)
   - Add human-set approval thresholds

4. **Implement Sales Agents**
   - Create cement agent with profit-maximizing pricing (within human limits)
   - Create steel agent with margin optimization and inventory costs
   - Define product catalogs with min/max pricing bounds
   - Implement competitive pricing strategies

5. **Testing & Demo**
   - Unit tests for each agent
   - Interactive demo script
   - Documentation

### Files to Create
- `part-01-basic-agent/README.md`
- `part-01-basic-agent/purchase_agent.py` (with budget optimization)
- `part-01-basic-agent/cement_agent.py` (with margin maximization)
- `part-01-basic-agent/steel_agent.py` (with profit targets)
- `part-01-basic-agent/constraints.py` (human-set limits)
- `part-01-basic-agent/negotiation_cycles.py` (cycle management)
- `part-01-basic-agent/demo.py`
- `part-01-basic-agent/requirements.txt`

---

## Part 2: MCP Integration (Tools & Resources)
**Duration**: 3-4 hours  
**Objective**: Enhance agents with MCP tools and resources

### Learning Goals
- Understand MCP client/server architecture
- Create custom MCP tools
- Integrate external resources via MCP
- Implement tool calling in agents

### Deliverables
1. MCP servers for each domain (construction, cement, steel)
2. Custom tools (pricing, inventory, contracts)
3. Resource integrations (databases, APIs)
4. Enhanced agents with tool capabilities

### Step-by-Step Instructions
1. **FastMCP Server Setup**
   - Create FastMCP server for construction tools (budget tracking, ROI calculation)
   - Create FastMCP server for cement company tools (margin analysis, pricing optimization)
   - Create FastMCP server for steel company tools (inventory costs, profit calculation)

2. **Tool Development**
   - Profit-optimizing pricing calculators with human-set bounds
   - Cost-aware inventory management tools
   - Contract generation with approval workflows
   - Market analysis for competitive positioning
   - Negotiation cycle tracking tools

3. **Resource Integration**
   - Database connections (SQLite for demo)
   - External API integrations
   - File system resources

4. **Agent Enhancement**
   - Integrate MCP clients in agents
   - Update agent workflows to use tools
   - Implement tool selection logic

5. **Testing & Demo**
   - Test MCP servers independently
   - Test agent-tool interactions
   - Create comprehensive demo

### Files to Create
- `part-02-mcp-integration/README.md`
- `part-02-mcp-integration/fastmcp_servers/` (profit calculation servers)
- `part-02-mcp-integration/tools/` (cost optimization, margin analysis)
- `part-02-mcp-integration/enhanced_agents/` (profit-driven agents)
- `part-02-mcp-integration/constraints_manager.py` (human limits enforcement)
- `part-02-mcp-integration/demo.py`

---

## Part 3: A2A Communication
**Duration**: 4-5 hours  
**Objective**: Implement inter-agent communication using A2A protocol

### Learning Goals
- Understand A2A protocol fundamentals
- Implement agent discovery and registration
- Create message routing and handling
- Build negotiation workflows

### Deliverables
1. A2A communication layer
2. Agent registry and discovery
3. Message protocols for quotes/contracts
4. Multi-agent negotiation system

### Step-by-Step Instructions
1. **A2A Infrastructure**
   - Setup A2A message broker with fundamental elements
   - Implement Agent Card system (identity, capabilities, constraints)
   - Create Task management (procurement tasks, sales tasks)
   - Implement Message routing with Parts structure
   - Setup Artifacts handling (contracts, quotes, specifications)

2. **A2A Communication Protocols**
   - Define Agent Cards (company profile, pricing limits, capabilities)
   - Create Task schemas (RFQ tasks, quote tasks, negotiation tasks)
   - Implement Message structure with Parts (header, body, constraints)
   - Setup Artifacts (quote documents, contract drafts, specifications)
   - Add negotiation cycle counters and termination logic

3. **Profit-Driven Agent Communication**
   - Integrate A2A clients with profit optimization logic
   - Implement quote request workflows with budget constraints
   - Create contract negotiation with cycle limits (4-5 rounds max)
   - Add automatic sign-off when cycles exhausted or targets met

4. **Competitive Multi-Agent Scenarios**
   - Purchase agent optimizes total cost within budget
   - Sales agents compete while maximizing margins
   - Time-bounded negotiation (max 5 cycles)
   - Automatic contract finalization with best available terms

5. **Testing & Demo**
   - Test message passing
   - Demo complete procurement cycle
   - Performance and reliability testing

### Files to Create
- `part-03-a2a-communication/README.md`
- `part-03-a2a-communication/a2a_infrastructure/`
- `part-03-a2a-communication/agent_cards/` (identity and constraints)
- `part-03-a2a-communication/tasks/` (procurement and sales tasks)
- `part-03-a2a-communication/messages/` (structured communication)
- `part-03-a2a-communication/artifacts/` (contracts and quotes)
- `part-03-a2a-communication/cycle_manager.py` (negotiation limits)
- `part-03-a2a-communication/competitive_agents/`
- `part-03-a2a-communication/demo.py`

---

## Part 4: Local Deployment with Docker
**Duration**: 2-3 hours  
**Objective**: Containerize agents and deploy locally

### Learning Goals
- Containerize Python applications
- Docker networking for multi-container apps
- Docker Compose orchestration
- Local testing and debugging

### Deliverables
1. Dockerfiles for each agent
2. Docker Compose configuration
3. Local deployment scripts
4. Monitoring and logging setup

### Step-by-Step Instructions
1. **Containerization**
   - Create Dockerfiles for each agent
   - Optimize images for production
   - Handle secrets and configuration

2. **Docker Compose Setup**
   - Define services for all agents
   - Configure networking between containers
   - Setup volumes for persistence

3. **Local Deployment**
   - Build and run containers
   - Test inter-container communication
   - Implement health checks

4. **Monitoring & Logging**
   - Container logging configuration
   - Basic monitoring setup
   - Debugging tools and techniques

### Files to Create
- `part-04-local-deployment/README.md`
- `part-04-local-deployment/Dockerfile.*`
- `part-04-local-deployment/docker-compose.yml`
- `part-04-local-deployment/scripts/`

---

## Part 5: Cloud Deployment (AgentCore & EKS)
**Duration**: 4-5 hours  
**Objective**: Deploy to production environments

### Learning Goals
- AgentCore deployment concepts
- Kubernetes fundamentals for EKS
- Cloud-native agent architecture
- Production monitoring and scaling

### Deliverables
1. AgentCore deployment configuration
2. EKS deployment manifests
3. CI/CD pipeline setup
4. Production monitoring dashboard

### Step-by-Step Instructions
1. **AgentCore Deployment**
   - Configure AgentCore environment
   - Deploy agents to AgentCore
   - Test AgentCore-specific features

2. **EKS Deployment**
   - Create EKS cluster
   - Deploy agents as Kubernetes pods
   - Configure ingress and services

3. **CI/CD Pipeline**
   - Setup GitHub Actions/CodePipeline
   - Automated testing and deployment
   - Container registry integration

4. **Production Operations**
   - Monitoring with CloudWatch
   - Logging aggregation
   - Auto-scaling configuration
   - Security best practices

### Files to Create
- `part-05-cloud-deployment/README.md`
- `part-05-cloud-deployment/agentcore/`
- `part-05-cloud-deployment/kubernetes/`
- `part-05-cloud-deployment/ci-cd/`

---

## Shared Components

### Models (`shared/models/`)
- Agent state schemas
- Message protocols
- Data models for construction domain

### Utils (`shared/utils/`)
- Common utilities
- Configuration management
- Logging setup

### Configs (`shared/configs/`)
- Environment configurations
- Agent configurations
- Deployment configurations

---

## Demo Scenarios

### Scenario 1: Competitive Procurement
1. Purchase agent needs cement and steel (budget: $100K)
2. Broadcasts RFQ via A2A with Agent Card and Task
3. Sales agents respond with profit-optimized quotes (within pricing limits)
4. 4-round negotiation cycle with decreasing margins
5. Auto-finalization of best offers within budget

### Scenario 2: Constrained Negotiation
1. 5-cycle maximum bidding with profit targets
2. Volume-based pricing within company limits
3. Delivery cost optimization
4. Contract auto-generation when cycles exhausted

### Scenario 3: Market Pressure
1. Supply shortage with price ceiling enforcement
2. Dynamic pricing within human-set bounds
3. Competitive supplier discovery via Agent Cards
4. Profit vs. market share optimization

---

## Success Metrics
- All agents communicate successfully via A2A
- MCP tools function correctly
- Local deployment works end-to-end
- Cloud deployment is scalable and monitored
- Complete procurement cycle demonstration

## Timeline
- **Week 1**: Parts 1-2 (Basic agents + MCP)
- **Week 2**: Part 3 (A2A communication)
- **Week 3**: Parts 4-5 (Deployment)
- **Week 4**: Integration testing and documentation

## Prerequisites
- Docker installed and configured
- AWS CLI configured with Bedrock access
- Python 3.9+ environment
- Basic understanding of agents and LLMs
- Familiarity with containerization concepts

## Next Steps
1. Review and approve this plan
2. Setup development environment
3. Begin with Part 1: Basic Agent development
4. Follow step-by-step instructions for each part
5. Document learnings and challenges for training materials