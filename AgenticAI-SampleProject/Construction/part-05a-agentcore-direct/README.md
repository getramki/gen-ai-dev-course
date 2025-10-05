# Part 5-A: AgentCore Deployment (Direct)

Deploy AgentCore-compliant agents to AWS AgentCore Runtime Service using ECR container images.

## Overview

This part demonstrates deploying AgentCore-compliant agents that implement the HTTP protocol contract required by AgentCore Runtime Service. Each agent exposes `/invocations` and `/ping` endpoints on port 8080 while maintaining LangChain tools and profit optimization logic.

## Prerequisites

- AWS Account with AgentCore Runtime Service access
- AWS CLI configured with appropriate permissions
- Docker installed and running
- ECR repositories created

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              AWS AgentCore Runtime Service                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Purchase Agent  │  │  Cement Agent   │  │  Steel Agent    │ │
│  │ (Port 8080)     │  │ (Port 8080)     │  │ (Port 8080)     │ │
│  │                 │  │                 │  │                 │ │
│  │ /invocations    │  │ /invocations    │  │ /invocations    │ │
│  │ /ping           │  │ /ping           │  │ /ping           │ │
│  │                 │  │                 │  │                 │ │
│  │ LangChain Tools │  │ LangChain Tools │  │ LangChain Tools │ │
│  │ - Cost Calc     │  │ - Margin Calc   │  │ - Profit Calc   │ │
│  │ - Quote Eval    │  │ - Price Opt     │  │ - Inventory     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                         ECR Container Images
```

## Important Notes

- **Docker Compose is NOT required for AgentCore deployment**
- AgentCore Runtime Service deploys individual container images directly from ECR
- Docker Compose (in `agentcore-agents/testing/` directory) is only for local development and testing

## AgentCore Deployment Workflow

### Step 1: Build and Push AgentCore Images

1. **Build ARM64 AgentCore-Compliant Images**
   ```bash
   cd agentcore-agents
   
   # Enable buildx for cross-platform builds
   docker buildx create --use
   
   # Build ARM64 images (required by AgentCore)
   docker buildx build --platform linux/arm64 -f Dockerfile.purchase -t agentcore-purchase-agent:latest --load .
   docker buildx build --platform linux/arm64 -f Dockerfile.cement -t agentcore-cement-agent:latest --load .
   docker buildx build --platform linux/arm64 -f Dockerfile.steel -t agentcore-steel-agent:latest --load .
   ```

2. **Create ECR Repositories**
   ```bash
   aws ecr create-repository --repository-name agentcore-purchase-agent --region us-east-1
   aws ecr create-repository --repository-name agentcore-cement-agent --region us-east-1
   aws ecr create-repository --repository-name agentcore-steel-agent --region us-east-1
   ```

3. **Tag and Push to ECR**
   ```bash
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   
   # Tag images
   docker tag agentcore-purchase-agent:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/agentcore-purchase-agent:latest
   docker tag agentcore-cement-agent:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/agentcore-cement-agent:latest
   docker tag agentcore-steel-agent:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/agentcore-steel-agent:latest
   
   # Push images
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/agentcore-purchase-agent:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/agentcore-cement-agent:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/agentcore-steel-agent:latest
   ```

### Step 2: Setup IAM Roles

1. **Create AgentCore Execution Role**
   ```bash
   # Use configurations from agentcore-config/iam-policies.json
   aws iam create-role --role-name AgentCoreExecutionRole --assume-role-policy-document file://agentcore-config/trust-policy.json
   aws iam attach-role-policy --role-name AgentCoreExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonBedrockAgentCoreServiceRolePolicy
   ```

### Step 3: Deploy to AgentCore Runtime Service

1. **Deploy Each Agent**
   ```bash
   # Use agent configurations from agentcore-config/agent-configs.json
   aws bedrock-agent-runtime create-agent \
     --agent-name agentcore-purchase-agent \
     --foundation-model anthropic.claude-3-sonnet-20240229-v1:0 \
     --instruction "Construction procurement agent with cost optimization" \
     --agent-resource-role-arn arn:aws:iam::<account-id>:role/AgentCoreExecutionRole
   ```

2. **Configure Container Images**
   - Each agent uses ECR image URI
   - Port 8080 (AgentCore requirement)
   - Health check endpoint: `/ping`
   - Invocation endpoint: `/invocations`

### Step 4: Testing and Validation

#### 4.1 Local Testing (Optional)
```bash
# Test locally before AgentCore deployment
cd agentcore-agents/testing
docker-compose up --build

# Test endpoints
curl http://localhost:8080/ping  # Purchase agent
curl http://localhost:8081/ping  # Cement agent
curl http://localhost:8082/ping  # Steel agent
```

#### 4.2 AgentCore Health Checks
```bash
# Test AgentCore deployed agents
aws bedrock-agent-runtime invoke-agent \
  --agent-id <agent-id> \
  --agent-alias-id <alias-id> \
  --session-id test-session \
  --input-text "Hello"
```

#### 4.3 Verify Agent Functionality
- Test LangChain tools are working
- Verify Bedrock integration
- Check profit optimization logic
- Validate HTTP protocol compliance

## AgentCore Features

### HTTP Protocol Contract
- **POST /invocations**: Main agent endpoint for processing requests
- **GET /ping**: Health check endpoint returning agent status
- **Port 8080**: Required port for AgentCore Runtime Service
- **Status Management**: Healthy/HealthyBusy status tracking
- **SSE Streaming**: Server-Sent Events support for streaming responses

### Built-in Monitoring
- **CloudWatch Integration**: Automatic metrics and logging
- **Auto-scaling**: Managed by AgentCore Runtime Service
- **Load Balancing**: Built-in request distribution

## Troubleshooting

### Common Issues

1. **Architecture Incompatible Error**
   - AgentCore requires ARM64 architecture
   - Rebuild images with `--platform linux/arm64`
   - Use Docker Buildx for cross-platform builds

2. **Agent Won't Start**
   - Check ECR image availability and ARM64 compatibility
   - Verify IAM role has bedrock-agentcore.amazonaws.com service principal
   - Review container logs in AgentCore console

2. **Health Check Failures**
   - Verify port 8080 configuration
   - Check `/ping` endpoint returns 200 status
   - Review startup time and dependencies

3. **Bedrock Access Issues**
   - Verify IAM role has Bedrock permissions
   - Check region configuration (us-east-1)
   - Ensure bedrock-agentcore service principal in trust policy

### Debugging Commands
```bash
# Check ECR images
aws ecr describe-images --repository-name agentcore-purchase-agent

# Test agent locally
docker run -p 8080:8080 agentcore-purchase-agent:latest
curl http://localhost:8080/ping

# View AgentCore agent status
aws bedrock-agent-runtime get-agent --agent-id <agent-id>
```

## Success Criteria

✅ **All three agents built and pushed to ECR**
✅ **AgentCore agents deployed successfully**
✅ **Health checks passing (/ping returns 200)**
✅ **Invocation endpoint working (/invocations)**
✅ **LangChain tools functioning correctly**
✅ **Bedrock integration operational**
✅ **Profit optimization logic preserved**


## Files Structure

```
part-05a-agentcore-direct/
├── README.md                    # This documentation
├── agentcore-config/
│   ├── agent-configs.json       # Agent configuration templates
│   └── iam-policies.json        # Required IAM policies
├── deployment-scripts/          # Future deployment automation
└── agentcore-agents/
    ├── purchase_agent/
    │   ├── __init__.py
    │   └── main.py              # AgentCore HTTP protocol implementation
    ├── cement_agent/
    │   ├── __init__.py
    │   └── main.py              # AgentCore HTTP protocol implementation
    ├── steel_agent/
    │   ├── __init__.py
    │   └── main.py              # AgentCore HTTP protocol implementation
    ├── Dockerfile.purchase      # Purchase agent container
    ├── Dockerfile.cement        # Cement agent container
    ├── Dockerfile.steel         # Steel agent container
    ├── requirements.txt         # Python dependencies
    └── testing/
        ├── docker-compose.yml   # Local testing only
        └── README.md            # Testing instructions
```

## Next Steps

After successful deployment:
1. **Part 5-B**: Lambda MCP tools integration
2. **Part 6**: EKS deployment for scalable orchestration
3. **Performance Optimization**: Monitor and tune resource allocation
4. **Security Hardening**: Implement additional security measures