# Part 4: Docker Deployment Demo Instructions

## Complete Step-by-Step Demonstration

### Prerequisites Check
- [ ] Docker installed and running
- [ ] Docker Compose available
- [ ] AWS credentials configured locally (`aws configure` or `~/.aws/credentials`)
- [ ] Part 3 agents tested locally

### Demo Flow

## Phase 1: Environment Setup (5 minutes)

### Step 1: Navigate to Part 4
```bash
cd part-04-local-deployment
```

### Step 2: Verify AWS Configuration
```bash
# Check AWS credentials are configured
aws sts get-caller-identity

# Optional: Copy environment template for region
cp .env.example .env
```

**Expected Output:**
```json
{
    "UserId": "AIDACKCEVSQ6C2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-user"
}
```

### Step 3: Verify Docker
```bash
# Check Docker is running
docker info

# Check Docker Compose
docker-compose --version
```

**Expected Output:**
- Docker info displays without errors
- Docker Compose version 1.29+ or 2.x

## Phase 2: Build Container Images (10 minutes)

### Step 4: Build All Images
```bash
./scripts/build.sh
```

**Expected Output:**
```
🏗️  Building Construction A2A Agents Docker Images
==================================================
📦 Building Purchase Agent image...
📦 Building Cement Agent image...
📦 Building Steel Agent image...
✅ All images built successfully!
```

### Step 5: Verify Images
```bash
docker images | grep construction
```

**Expected Output:**
```
construction-purchase-agent   latest   abc123   2 minutes ago   500MB
construction-cement-agent     latest   def456   1 minute ago    500MB
construction-steel-agent      latest   ghi789   30 seconds ago  500MB
```

## Phase 3: Deploy Containers (10 minutes)

### Step 6: Deploy All Agents
```bash
./scripts/deploy.sh
```

**Expected Output:**
```
🚀 Deploying Construction A2A Agents
====================================
✅ AWS credentials verified
🛑 Stopping existing containers...
🚀 Starting agent services...
⏳ Waiting for agents to start (using local AWS credentials)...
🏥 Checking agent health...

✅ Purchase Agent (port 10001) - HEALTHY
✅ Cement Agent (port 10002) - HEALTHY
✅ Steel Agent (port 10003) - HEALTHY
```

### Step 7: Verify Container Status
```bash
docker-compose ps
```

**Expected Output:**
```
Name                          State    Ports
construction-purchase-agent   Up       0.0.0.0:10001->10001/tcp
construction-cement-agent     Up       0.0.0.0:10002->10002/tcp
construction-steel-agent      Up       0.0.0.0:10003->10003/tcp
```

## Phase 4: Test Deployment (10 minutes)

### Step 8: Run Comprehensive Tests
```bash
./scripts/test.sh
```

**Expected Output:**
```
🧪 Testing Containerized Construction Agents
===========================================
📋 Testing Agent Cards...
  Testing Purchase Agent...
    ✅ Agent card retrieved
    📝 Name: Construction Purchase Agent
  Testing Cement Agent...
    ✅ Agent card retrieved
    📝 Name: Cement Sales Agent
  Testing Steel Agent...
    ✅ Agent card retrieved
    📝 Name: Steel Sales Agent

🔗 Testing A2A Communication...
  Testing Purchase Agent JSON-RPC...
    ✅ JSON-RPC endpoint responding
```

### Step 9: Manual Agent Card Verification
```bash
# Test each agent card
curl http://localhost:10001/.well-known/agent-card.json | jq '.name'
curl http://localhost:10002/.well-known/agent-card.json | jq '.name'  
curl http://localhost:10003/.well-known/agent-card.json | jq '.name'
```

**Expected Output:**
```
"Construction Purchase Agent"
"Cement Sales Agent"
"Steel Sales Agent"
```

## Phase 5: Full Negotiation Demo (15 minutes)

### Step 10: Run Part 3 Negotiation with Containers
```bash
# Navigate to Part 3
cd ../part-03-a2a-communication

# Run negotiation demo (agents now in containers)
python negotiation_demo.py
```

**Expected Output:**
```
A2A Inter-Agent Procurement Negotiation
========================================================

Connecting to agents...
✅ Connected to purchase agent
✅ Connected to cement agent
✅ Connected to steel agent

================================================================================
PHASE 1: CLIENT REQUEST TO PURCHASE AGENT
================================================================================
[Detailed negotiation flow...]

================================================================================
NEGOTIATION COMPLETE
================================================================================
✅ Cement negotiations: 4 cycles
✅ Steel negotiations: 4 cycles
✅ Final contract saved: logs/final_contract_*.json
```

### Step 11: Monitor Container Logs During Negotiation
```bash
# In another terminal, monitor logs
cd ../part-04-local-deployment
docker-compose logs -f
```

**Expected Output:**
Real-time logs showing agent processing, Bedrock calls, and A2A communication

## Phase 6: Monitoring and Management (10 minutes)

### Step 12: Check Resource Usage
```bash
docker stats --no-stream
```

**Expected Output:**
```
CONTAINER                     CPU %   MEM USAGE / LIMIT   MEM %
construction-purchase-agent   2.5%    150MiB / 2GiB      7.5%
construction-cement-agent     1.8%    140MiB / 2GiB      7.0%
construction-steel-agent      2.1%    145MiB / 2GiB      7.25%
```

### Step 13: View Individual Agent Logs
```bash
# Purchase agent logs
docker-compose logs purchase-agent | tail -20

# Cement agent logs  
docker-compose logs cement-agent | tail -20

# Steel agent logs
docker-compose logs steel-agent | tail -20
```

### Step 14: Test Container Recovery
```bash
# Stop one container
docker-compose stop cement-agent

# Verify it's down
curl http://localhost:10002/.well-known/agent-card.json
# Should fail with connection refused

# Restart container
docker-compose start cement-agent

# Wait and verify recovery
sleep 30
curl http://localhost:10002/.well-known/agent-card.json
# Should succeed
```

## Phase 7: Cleanup (5 minutes)

### Step 15: Clean Shutdown
```bash
# Stop all containers
docker-compose down

# Verify containers stopped
docker-compose ps
```

**Expected Output:**
No running containers

### Step 16: Optional Full Cleanup
```bash
# Run cleanup script (optional)
./scripts/cleanup.sh

# Follow prompts to remove images and volumes
```

## Troubleshooting Guide

### Issue: Container Won't Start
**Symptoms:** Container exits immediately or health check fails
**Solutions:**
1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify Bedrock access: `aws bedrock list-foundation-models --region us-east-1`
3. Check logs: `docker-compose logs [service-name]`

### Issue: Agent Card Not Accessible
**Symptoms:** 404 or connection refused on agent card endpoint
**Solutions:**
1. Wait longer for startup (30-40 seconds)
2. Check container status: `docker-compose ps`
3. Verify port mapping in docker-compose.yml

### Issue: Negotiation Demo Fails
**Symptoms:** Connection errors during negotiation
**Solutions:**
1. Ensure all containers are healthy
2. Check network connectivity between host and containers
3. Verify no port conflicts with local agents

## Success Criteria

✅ **All containers start successfully**
✅ **Health checks pass for all agents**
✅ **Agent cards accessible via HTTP**
✅ **JSON-RPC endpoints responding**
✅ **Full negotiation demo completes**
✅ **Container logs show proper A2A communication**
✅ **Resource usage within reasonable limits**
✅ **Container recovery works after restart**

## Demo Timing

- **Setup**: 5 minutes
- **Build**: 10 minutes  
- **Deploy**: 10 minutes
- **Test**: 10 minutes
- **Negotiation**: 15 minutes
- **Monitoring**: 10 minutes
- **Cleanup**: 5 minutes
- **Total**: ~65 minutes

## Key Demonstration Points

1. **Containerization**: Show how Part 3 agents run in isolated containers
2. **Orchestration**: Demonstrate Docker Compose multi-container management
3. **Health Monitoring**: Show health checks and container status
4. **A2A Communication**: Prove containers maintain full A2A capabilities
5. **Scalability**: Show how containers can be stopped/started independently
6. **Logging**: Demonstrate centralized logging and monitoring
7. **Recovery**: Show container restart and health recovery

This completes the Part 4 Docker deployment demonstration!