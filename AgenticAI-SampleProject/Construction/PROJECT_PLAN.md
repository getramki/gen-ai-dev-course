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

### Files Created ✅
- `part-01-basic-agent/README.md` - Project documentation and setup guide
- `part-01-basic-agent/purchase_agent.py` - Purchase agent with budget optimization and LangGraph
- `part-01-basic-agent/cement_agent.py` - Cement sales agent with margin maximization
- `part-01-basic-agent/steel_agent.py` - Steel sales agent with profit targets
- `part-01-basic-agent/constraints.py` - Human-set limits and approval thresholds
- `part-01-basic-agent/negotiation_cycles.py` - Cycle management (max 5 rounds)
- `part-01-basic-agent/demo.py` - Interactive demo with LLM reasoning
- `part-01-basic-agent/requirements.txt` - Dependencies (LangGraph, Bedrock, etc.)

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

### Files Created ✅
- `part-02-mcp-integration/README.md` - MCP integration documentation
- `part-02-mcp-integration/fastmcp_servers/` - FastMCP servers for each domain:
  - `construction_server.py` - Budget tracking, ROI calculation tools
  - `cement_server.py` - Margin analysis, pricing optimization tools
  - `steel_server.py` - Inventory costs, profit calculation tools
- `part-02-mcp-integration/tools/` - Custom MCP tools directory
- `part-02-mcp-integration/enhanced_agents/` - MCP-enhanced agents:
  - `enhanced_purchase_agent.py` - Purchase agent with MCP tools
  - `enhanced_cement_agent.py` - Cement agent with profit optimization
  - `enhanced_steel_agent.py` - Steel agent with margin analysis
- `part-02-mcp-integration/constraints_manager.py` - Human limits enforcement
- `part-02-mcp-integration/demo.py` - MCP integration demo
- `part-02-mcp-integration/requirements.txt` - MCP dependencies
- `part-02-mcp-integration/*.db` - SQLite databases (construction, cement, steel)

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

### Files Created ✅
- `part-03-a2a-communication/README.md` - A2A implementation documentation
- `part-03-a2a-communication/purchase_agent/` - A2A Purchase Agent:
  - `app/__main__.py` - A2A server setup with agent card
  - `app/agent.py` - Enhanced agent with procurement analysis
  - `app/agent_executor.py` - A2A protocol executor
- `part-03-a2a-communication/cement_agent/` - A2A Cement Agent:
  - `app/__main__.py` - A2A server with cement sales capabilities
  - `app/agent.py` - Cement agent with profit optimization
  - `app/agent_executor.py` - A2A protocol executor
- `part-03-a2a-communication/steel_agent/` - A2A Steel Agent:
  - `app/__main__.py` - A2A server with premium steel sales
  - `app/agent.py` - Steel agent with margin maximization
  - `app/agent_executor.py` - A2A protocol executor
- `part-03-a2a-communication/negotiation_demo.py` - Inter-agent negotiation orchestrator
- `part-03-a2a-communication/demo_client.py` - A2A SDK client for testing
- `part-03-a2a-communication/test_agent_cards.py` - Agent card verification
- `part-03-a2a-communication/debug_purchase_agent.py` - Streaming debug tool
- `part-03-a2a-communication/start_agents.sh` - Agent startup script
- `part-03-a2a-communication/requirements.txt` - A2A SDK dependencies
- `part-03-a2a-communication/logs/` - Conversation and contract logs:
  - `conversation_*.json` - Time-stamped agent interactions
  - `negotiation_*.log` - Detailed negotiation logs
  - `final_contract_*.json` - Contract artifacts
- `part-03-a2a-communication/IMPLEMENTATION_SUMMARY.md` - Implementation details
- `part-03-a2a-communication/NEGOTIATION_SUMMARY.md` - Negotiation results summary

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

### Files Created ✅
- `part-04-local-deployment/README.md` - Docker deployment documentation
- `part-04-local-deployment/Dockerfile.purchase` - Purchase agent container
- `part-04-local-deployment/Dockerfile.cement` - Cement agent container
- `part-04-local-deployment/Dockerfile.steel` - Steel agent container
- `part-04-local-deployment/docker-compose.yml` - Multi-container orchestration
- `part-04-local-deployment/.env.example` - Environment configuration template
- `part-04-local-deployment/scripts/` - Management scripts:
  - `build.sh` - Build Docker images
  - `deploy.sh` - Deploy containers with health checks
  - `test.sh` - Test deployment and agent communication
  - `cleanup.sh` - Clean up resources
- `part-04-local-deployment/DEMO_INSTRUCTIONS.md` - 65-minute step-by-step demo guide

---

## Part 5-A: AgentCore Deployment (Direct)
**Duration**: 2-3 hours  
**Objective**: Deploy Part 4 agents directly to AWS AgentCore platform

### Learning Goals
- AgentCore platform concepts and architecture
- Agent registration and lifecycle management
- AgentCore-specific A2A communication
- Platform monitoring and debugging

### Deliverables
1. AgentCore deployment of containerized agents
2. Agent registration and setup
3. Platform-specific testing
4. AgentCore monitoring dashboard

### Step-by-Step Instructions
1. **AgentCore Setup**
   - Configure AgentCore environment
   - Setup agent registration
   - Configure platform permissions

2. **Direct Agent Deployment**
   - Deploy Part 4 Docker containers to AgentCore
   - Configure agent cards for platform
   - Test AgentCore-specific features with LangChain tools

3. **Platform Integration**
   - Setup AgentCore A2A communication
   - Configure platform monitoring
   - Test inter-agent communication on platform

4. **Production Readiness**
   - Performance optimization for platform
   - Security configuration
   - Monitoring and alerting setup

### Files to Create
- `part-05a-agentcore-direct/README.md`
- `part-05a-agentcore-direct/agentcore-config/`
- `part-05a-agentcore-direct/deployment-scripts/`
- `part-05a-agentcore-direct/monitoring/`

---

## Part 5-B: AgentCore with Lambda MCP Tools
**Duration**: 4-5 hours  
**Objective**: Deploy agents with Lambda-based MCP tools via AgentCore Gateway

### Learning Goals
- Lambda functions as MCP tools
- AgentCore Gateway MCP integration
- Serverless tool architecture
- MCP protocol over AgentCore Gateway

### Deliverables
1. Lambda functions for each agent's MCP tools
2. AgentCore Gateway MCP configuration
3. Enhanced agents using Lambda MCP tools
4. End-to-end MCP tool integration

### Step-by-Step Instructions
1. **Lambda MCP Tools Development**
   - Convert Part 2 FastMCP servers to Lambda functions
   - Create Lambda for Purchase Agent tools (budget tracking, ROI calculation)
   - Create Lambda for Cement Agent tools (margin analysis, pricing optimization)
   - Create Lambda for Steel Agent tools (inventory costs, profit calculation)

2. **AgentCore Gateway Integration**
   - Configure AgentCore Gateway for MCP protocol
   - Setup Lambda function endpoints
   - Configure MCP tool discovery and routing

3. **Agent Enhancement**
   - Modify agents to use AgentCore Gateway MCP tools
   - Replace LangChain tools with MCP Lambda calls
   - Test tool integration and performance

4. **Production Deployment**
   - Deploy Lambda functions with proper IAM roles
   - Configure AgentCore Gateway routing
   - Setup monitoring and logging for Lambda tools
   - Test complete agent-to-Lambda-tool workflow

### Files to Create
- `part-05b-agentcore-lambda-mcp/README.md`
- `part-05b-agentcore-lambda-mcp/lambda-functions/`
  - `purchase-agent-tools/` - Lambda MCP tools for purchase agent
  - `cement-agent-tools/` - Lambda MCP tools for cement agent
  - `steel-agent-tools/` - Lambda MCP tools for steel agent
- `part-05b-agentcore-lambda-mcp/agentcore-gateway/`
- `part-05b-agentcore-lambda-mcp/enhanced-agents/`
- `part-05b-agentcore-lambda-mcp/deployment/`
- `part-05b-agentcore-lambda-mcp/monitoring/`

---

## Part 6-A: EKS Deployment with Embedded Agents
**Duration**: 3-4 hours  
**Objective**: Deploy Part 4 agents to EKS with A2A communication across subdomains

### Learning Goals
- EKS cluster creation with eksctl
- Kubernetes namespaces and deployments
- External A2A communication across subdomains
- Horizontal Pod Autoscaling (HPA)
- Ingress controllers and load balancing

### Deliverables
1. EKS cluster with separate namespaces for each agent
2. External A2A communication across different subdomains
3. Horizontal autoscaling demonstration
4. Production monitoring and scaling

### Step-by-Step Instructions
1. **EKS Infrastructure with eksctl**
   - Create EKS cluster using eksctl
   - Setup node groups and networking
   - Configure ingress controllers

2. **Namespace-based Agent Deployment**
   - Create namespaces: `part-a-purchase-ns`, `part-a-cement-ns`, `part-a-steel-ns`
   - Deploy Part 4 agents (with embedded LangChain tools) to separate namespaces
   - Configure Kubernetes deployments and services

3. **Multi-Subdomain A2A Communication**
   - Deploy purchase agent on `purchase.construction.example.com`
   - Deploy cement agent on `cement.construction.example.com`
   - Deploy steel agent on `steel.construction.example.com`
   - Configure external A2A communication across internet-facing endpoints

4. **Horizontal Pod Autoscaling**
   - Configure HPA for each agent deployment
   - Setup CPU and memory-based scaling
   - Load testing to demonstrate autoscaling

5. **Production Operations**
   - Basic monitoring with CloudWatch
   - Logging configuration
   - Security best practices

### Files to Create
- `part-06a-eks-embedded-agents/README.md`
- `part-06a-eks-embedded-agents/eksctl/`
  - `cluster-config.yaml` - EKS cluster configuration
- `part-06a-eks-embedded-agents/kubernetes/`
  - `namespaces/` - Namespace definitions
  - `deployments/` - Agent deployment manifests
  - `services/` - Service definitions
  - `ingress/` - Ingress configurations
  - `hpa/` - Horizontal Pod Autoscaler configs
- `part-06a-eks-embedded-agents/scripts/`
  - `deploy.sh` - Deployment automation
  - `test-autoscaling.sh` - HPA testing
- `part-06a-eks-embedded-agents/negotiation_demo.py` - EKS-based negotiation demo

---

## Part 6-B: EKS Deployment with Separated MCP Tools
**Duration**: 4-5 hours  
**Objective**: Deploy agents and MCP tools as separate containers with internal MCP communication

### Learning Goals
- MCP tools as separate containers
- Internal communication (Agent ↔ MCP Tools)
- Advanced Kubernetes orchestration
- Helm charts for deployment automation

### Deliverables
1. Agents and MCP tools in separate pods within same namespaces
2. Internal MCP communication between agent and tool pods
3. Kubernetes deployment scripts and Helm charts
4. Advanced monitoring and scaling

### Part 6-B-1: Kubernetes Deployment Scripts
**Duration**: 2-3 hours

#### Step-by-Step Instructions
1. **Namespace-based MCP Deployment**
   - Create namespaces: `part-b-purchase-ns`, `part-b-cement-ns`, `part-b-steel-ns`
   - Deploy agents (from Part 2) and MCP tools (from Part 2) as separate pods
   - Configure internal MCP communication within namespaces

2. **MCP Tools Containerization**
   - Create Dockerfiles for MCP servers (construction, cement, steel)
   - Deploy MCP tools as separate pods in same namespace as agents
   - Configure Kubernetes services for internal MCP communication

3. **Internal Communication Architecture**
   - Agent pods communicate with their MCP tool pods via Kubernetes services
   - MCP protocol over internal cluster networking
   - Service discovery and DNS resolution

4. **Horizontal Pod Autoscaling**
   - Configure HPA for both agents and MCP tools
   - Independent scaling of agents and tools
   - Load testing for MCP communication

#### Files to Create
- `part-06b1-eks-mcp-scripts/README.md`
- `part-06b1-eks-mcp-scripts/kubernetes/`
  - `namespaces/` - Namespace definitions
  - `agents/` - Agent deployment manifests
  - `mcp-tools/` - MCP tool deployment manifests
  - `services/` - Internal service definitions
  - `hpa/` - Autoscaling configurations
- `part-06b1-eks-mcp-scripts/dockerfiles/`
  - `mcp-construction-server/`
  - `mcp-cement-server/`
  - `mcp-steel-server/`
- `part-06b1-eks-mcp-scripts/negotiation_demo.py` - Kubernetes-based negotiation demo

### Part 6-B-2: Helm Chart Deployment
**Duration**: 2-3 hours

#### Step-by-Step Instructions
1. **Helm Chart Development**
   - Create Helm charts for agent and MCP tool deployments
   - Parameterize configurations for different environments
   - Template-based deployment automation

2. **Advanced Deployment Features**
   - Rolling updates and rollback strategies
   - ConfigMaps and Secrets management
   - Advanced networking policies

3. **Production-Grade Operations**
   - Monitoring with Prometheus and Grafana
   - Logging aggregation with Fluentd/CloudWatch
   - Advanced security configurations
   - Network policies and RBAC

#### Files to Create
- `part-06b2-eks-helm-charts/README.md`
- `part-06b2-eks-helm-charts/helm-charts/`
  - `construction-agents/` - Main Helm chart
    - `templates/` - Kubernetes templates
    - `values.yaml` - Default values
    - `Chart.yaml` - Chart metadata
  - `mcp-tools/` - MCP tools subchart
- `part-06b2-eks-helm-charts/monitoring/`
  - `prometheus/` - Monitoring configuration
  - `grafana/` - Dashboard definitions
- `part-06b2-eks-helm-charts/scripts/`
  - `helm-deploy.sh` - Helm deployment automation
- `part-06b2-eks-helm-charts/negotiation_demo.py` - Helm-based negotiation demo

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
- **Week 3**: Part 4 (Local Docker deployment)
- **Week 4**: Part 5-A (AgentCore direct deployment)
- **Week 5**: Part 5-B (AgentCore with Lambda MCP tools)
- **Week 6**: Part 6-A (EKS with embedded agents)
- **Week 7**: Part 6-B (EKS with separated MCP tools)
- **Week 8**: Integration testing and documentation

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