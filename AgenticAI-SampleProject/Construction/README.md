# Agentic AI for Enterprise Procurement - Complete Implementation Guide

This repository contains a complete, production-ready implementation of autonomous AI agents for enterprise procurement, demonstrating Model Context Protocol (MCP) for internal system communication and Agent-to-Agent (A2A) protocol for cross-company negotiations.

## 📚 Blog Post Series

This implementation is accompanied by a three-part blog post series that explains the concepts, architecture, and deployment in detail:

### Part 1: Enterprise Procurement Reimagined – How Agentic AI with MCP Tools Transforms B2B Negotiations

**Published:** January 6, 2026  
**Read on CaveatWisdom:** [Link to Post 1]

**What You'll Learn:**
- The challenge of integrating AI agents with diverse enterprise systems (SAP, ERP, Oracle, Workday)
- How Model Context Protocol (MCP) provides standardized tool access for agents
- Building MCP servers with FastMCP for enterprise systems (Stores, Production, Logistics, Finance, Operations)
- Deploying MCP tools as AWS Lambda functions for serverless scalability
- Real-world procurement decision flow using MCP tools

**Key Concepts:**
- **Problem:** Hard-coded integrations break with every API change, agents make suboptimal decisions without complete data
- **Solution:** MCP standardizes agent-to-system communication, enabling dynamic tool discovery and complete enterprise data access
- **Implementation:** AWS Bedrock for agents, Lambda for MCP servers, Aurora for caching, EventBridge for real-time updates

**Code Examples in This Repo:**
- `part-02-mcp-integration/` - FastMCP server implementations
- `part-02-mcp-integration/fastmcp_servers/` - Stores, Production, Logistics, Finance, Operations MCP servers
- `part-02-mcp-integration/enhanced_agents/` - Agents with MCP tool integration

---

### Part 2: Beyond APIs – How Agent-to-Agent Communication Protocols Enable Autonomous Business Networks

**Published:** January 10, 2026  
**Read on CaveatWisdom:** [Link to Post 2]

**What You'll Learn:**
- The limitations of traditional API integrations for multi-company negotiations
- How Agent-to-Agent (A2A) protocol enables autonomous cross-company communication
- A2A protocol components: Agent Cards, Tasks, Messages, Artifacts
- Multi-round autonomous negotiation between Purchase Agent and Supplier Agents
- Complete audit trails for compliance and governance

**Key Concepts:**
- **Problem:** Custom API integrations for each supplier don't scale, manual orchestration required for multi-party negotiations
- **Solution:** A2A protocol standardizes agent communication across companies, enabling autonomous business networks
- **Implementation:** EventBridge for A2A messaging, API Gateway for agent endpoints, Step Functions for orchestration, S3 for artifacts

**Code Examples in This Repo:**
- `part-03-a2a-communication/` - A2A protocol implementation
- `part-03-a2a-communication/purchase_agent/` - Purchase Agent with A2A capability
- `part-03-a2a-communication/cement_agent/` - Cement Sales Agent with A2A
- `part-03-a2a-communication/steel_agent/` - Steel Sales Agent with A2A
- `part-03-a2a-communication/logs/` - Complete negotiation logs and contracts

---

### Part 3: Deploying Agentic AI with MCP and A2A Capability on Amazon EKS

**Published:** January 14, 2026  
**Read on CaveatWisdom:** [Link to Post 3]

**What You'll Learn:**
- Production deployment challenges for MCP and A2A-enabled agents
- Amazon EKS architecture with namespace isolation for security
- IAM Roles for Service Accounts (IRSA) for secure AWS access without credentials
- Network policies for isolating MCP traffic (internal) from A2A traffic (external)
- Horizontal Pod Autoscaling for independent agent and MCP tool scaling
- Complete observability with CloudWatch Container Insights

**Key Concepts:**
- **Problem:** Ad-hoc deployments create security vulnerabilities, can't handle load spikes, no isolation between components
- **Solution:** EKS provides production-grade orchestration with security, scalability, and observability built-in
- **Implementation:** Namespace per agent domain, separate pods for agents and MCP tools, IRSA for credentials, HPA for scaling

**Code Examples in This Repo:**
- `part-04-local-deployment/` - Docker and Docker Compose setup
- `part-06a-eks-embedded-agents/` - EKS deployment with agents and MCP tools
- `part-06b1-eks-mcp-scripts/` - Kubernetes manifests for production deployment
- `part-06b2-eks-helm-charts/` - Helm charts for automated deployment

---

## 🏗️ Repository Structure

```
Construction/
├── part-01-basic-agent/          # Basic agents with LangGraph and Bedrock
├── part-02-mcp-integration/      # MCP tools and enhanced agents
│   ├── fastmcp_servers/          # FastMCP server implementations
│   ├── enhanced_agents/          # Agents with MCP integration
│   └── *.db                      # SQLite databases for demo
├── part-03-a2a-communication/    # A2A protocol implementation
│   ├── purchase_agent/           # Purchase Agent with A2A
│   ├── cement_agent/             # Cement Sales Agent with A2A
│   ├── steel_agent/              # Steel Sales Agent with A2A
│   └── logs/                     # Negotiation logs and contracts
├── part-04-local-deployment/     # Docker and Docker Compose
│   ├── Dockerfile.*              # Container images
│   ├── docker-compose.yml        # Multi-container orchestration
│   └── scripts/                  # Deployment scripts
├── part-06a-eks-embedded-agents/ # EKS with embedded agents
│   ├── eksctl/                   # EKS cluster configuration
│   └── kubernetes/               # Kubernetes manifests
├── part-06b1-eks-mcp-scripts/    # EKS with separated MCP tools
│   ├── kubernetes/               # Deployment manifests
│   └── dockerfiles/              # MCP tool containers
└── part-06b2-eks-helm-charts/    # Helm charts for production
    ├── helm-charts/              # Chart templates
    └── monitoring/               # Prometheus and Grafana
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- AWS CLI configured with Bedrock access
- kubectl and eksctl (for EKS deployment)
- AWS account with appropriate permissions

### Part 1: Basic Agents

```bash
cd part-01-basic-agent
pip install -r requirements.txt
python demo.py
```

### Part 2: MCP Integration

```bash
cd part-02-mcp-integration

# Start FastMCP servers
python fastmcp_servers/construction_server.py &
python fastmcp_servers/cement_server.py &
python fastmcp_servers/steel_server.py &

# Run enhanced agents
python demo.py
```

### Part 3: A2A Communication

```bash
cd part-03-a2a-communication

# Start all agents
./start_agents.sh

# Run negotiation demo
python negotiation_demo.py
```

### Part 4: Local Docker Deployment

```bash
cd part-04-local-deployment

# Build and deploy
./scripts/build.sh
./scripts/deploy.sh

# Test deployment
./scripts/test.sh
```

### Part 6: EKS Production Deployment

```bash
cd part-06b1-eks-mcp-scripts

# Create EKS cluster
eksctl create cluster -f eksctl/cluster-config.yaml

# Deploy agents and MCP tools
kubectl apply -f kubernetes/namespaces/
kubectl apply -f kubernetes/agents/
kubectl apply -f kubernetes/mcp-tools/
kubectl apply -f kubernetes/hpa/

# Monitor deployment
kubectl get pods -n purchase-agent-ns --watch
```

---

## 🔑 Key Features

### Model Context Protocol (MCP)
- ✅ Standardized tool interface for enterprise systems
- ✅ Dynamic tool discovery without hard-coded integrations
- ✅ FastMCP server implementations for SAP, ERP, Oracle, Workday
- ✅ AWS Lambda deployment for serverless scalability
- ✅ Aurora PostgreSQL caching for performance

### Agent-to-Agent (A2A) Protocol
- ✅ Standardized cross-company agent communication
- ✅ Agent Cards for digital identity and capabilities
- ✅ Tasks for structured negotiation workflows
- ✅ Messages with Parts architecture (header, body, constraints)
- ✅ Artifacts for versioned, auditable contracts
- ✅ Complete audit trails in CloudWatch

### Production Deployment on EKS
- ✅ Namespace isolation for security boundaries
- ✅ IAM Roles for Service Accounts (IRSA) for secure AWS access
- ✅ Network policies for traffic control
- ✅ Secrets management with AWS Secrets Manager
- ✅ Horizontal Pod Autoscaling for dynamic load handling
- ✅ Independent scaling for agents and MCP tools
- ✅ CloudWatch Container Insights for observability

---

## 📊 Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Company A (Buyer)                         │
│  ┌──────────────┐         ┌──────────────────────────┐     │
│  │   Purchase   │◄───────►│      MCP Tools           │     │
│  │    Agent     │         │  (Stores, Production,    │     │
│  │  (Bedrock)   │         │   Logistics, Finance,    │     │
│  └──────┬───────┘         │   Operations)            │     │
│         │                 └──────────────────────────┘     │
│         │ A2A Protocol                                      │
└─────────┼───────────────────────────────────────────────────┘
          │
          ↓
┌─────────────────────────────────────────────────────────────┐
│           Amazon EventBridge (A2A Message Bus)               │
│           AWS Step Functions (Orchestration)                 │
│           Amazon S3 (Artifacts)                              │
│           CloudWatch (Audit Logs)                            │
└─────────┬───────────────────────────────┬───────────────────┘
          │                               │
          ↓                               ↓
┌─────────────────────────┐    ┌─────────────────────────┐
│      Company B          │    │      Company C          │
│  ┌──────────────┐       │    │  ┌──────────────┐       │
│  │   Cement     │       │    │  │    Steel     │       │
│  │   Sales      │       │    │  │    Sales     │       │
│  │   Agent      │       │    │  │    Agent     │       │
│  └──────┬───────┘       │    │  └──────┬───────┘       │
│         │               │    │         │               │
│  ┌──────▼───────┐       │    │  ┌──────▼───────┐       │
│  │  MCP Tools   │       │    │  │  MCP Tools   │       │
│  └──────────────┘       │    │  └──────────────┘       │
└─────────────────────────┘    └─────────────────────────┘
```

### EKS Deployment Architecture

```
EKS Cluster: agentic-ai-production
├── Namespace: purchase-agent-ns
│   ├── Purchase Agent Pods (2-20 replicas, HPA)
│   │   └── IRSA: Bedrock, EventBridge, Secrets Manager
│   └── MCP Tool Pods (1-10 replicas each, HPA)
│       ├── Stores MCP → SAP
│       ├── Production MCP → ERP
│       ├── Logistics MCP → Oracle
│       ├── Finance MCP → Workday
│       └── Operations MCP → QMS
├── Namespace: cement-sales-ns
│   ├── Cement Sales Agent Pods
│   └── MCP Tool Pods
└── Namespace: steel-sales-ns
    ├── Steel Sales Agent Pods
    └── MCP Tool Pods
```

---

## 🔒 Security Best Practices

### IAM Roles for Service Accounts (IRSA)
- No hardcoded AWS credentials in containers
- Temporary credentials from AWS STS
- Least privilege access per agent and MCP tool
- Separate roles for agents (Bedrock, EventBridge) and MCP tools (RDS, Secrets Manager)

### Network Policies
- Isolate MCP traffic (internal, within namespace)
- Isolate A2A traffic (external, across namespaces)
- Explicit ingress and egress rules
- Deny-by-default security posture

### Secrets Management
- AWS Secrets Manager for enterprise system credentials
- Kubernetes Secrets Store CSI Driver for mounting secrets
- KMS encryption for secrets at rest
- Automatic secret rotation

### Pod Security
- Run as non-root user
- Read-only root filesystem
- Drop all capabilities
- Seccomp profiles for syscall filtering

---

## 📈 Scalability Patterns

### Horizontal Pod Autoscaling (HPA)

**Agent Pods (A2A Load):**
- Min: 2 replicas
- Max: 20 replicas
- Target: 70% CPU, 80% memory
- Scale up: 100% every 60 seconds
- Scale down: 50% every 300 seconds

**MCP Tool Pods (Tool Call Frequency):**
- Min: 1 replica
- Max: 10 replicas
- Target: 60% CPU
- Independent scaling from agents

### Cluster Autoscaling
- Min nodes: 3
- Max nodes: 20
- Scale based on pod resource requests
- Automatic node provisioning and termination

---

## 📊 Monitoring and Observability

### CloudWatch Container Insights
- CPU and memory utilization per pod
- Network traffic and disk I/O
- Custom metrics for A2A and MCP

### Centralized Logging
- Fluent Bit for log aggregation
- CloudWatch Logs for storage
- CloudWatch Logs Insights for querying

### Alerting
- High CPU/memory utilization
- Pod failures and restarts
- A2A message latency
- MCP tool errors

---

## 🧪 Testing

### Unit Tests
```bash
cd part-02-mcp-integration
pytest tests/
```

### Integration Tests
```bash
cd part-03-a2a-communication
python test_agent_cards.py
python demo_client.py
```

### Load Testing
```bash
cd part-04-local-deployment
./scripts/test.sh
```

---

## 📖 Documentation

- **Blog Post Series:** Detailed explanations of concepts and implementation
- **PROJECT_PLAN.md:** Complete project structure and roadmap
- **BUSINESS_RULES.md:** Profit optimization and negotiation constraints
- **LEADERSHIP_USE_CASE.md:** Business value and ROI analysis
- **Part READMEs:** Specific instructions for each implementation phase

---

## 🤝 Contributing

This is a reference implementation for educational purposes. Feel free to:
- Fork and adapt for your use case
- Submit issues for bugs or questions
- Share improvements and optimizations

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👤 Author

**RamaKrishna Ponnaluri**
- Blog: [CaveatWisdom](https://caveatwisdom.com)
- GitHub: [@getramki](https://github.com/getramki)

---

## 🙏 Acknowledgments

- AWS Bedrock team for Anthropic Claude integration
- FastMCP community for MCP server framework
- LangGraph team for agent orchestration framework
- A2A protocol contributors for standardized agent communication

---

## 📚 Additional Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Agent-to-Agent Protocol](https://github.com/a2a-protocol)
- [Amazon EKS Best Practices](https://aws.github.io/aws-eks-best-practices/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

---

**Ready to build autonomous business networks? Start with Part 1 and work your way through the complete implementation!**
