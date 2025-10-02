# Part 4: Local Deployment with Docker

This part containerizes the A2A agents from Part 3 using Docker and Docker Compose for local deployment.

## Overview

Containerizes the three A2A agents:
- **Purchase Agent** (Port 10001) - Procurement optimization
- **Cement Agent** (Port 10002) - Cement sales with profit maximization  
- **Steel Agent** (Port 10003) - Premium steel sales

## Prerequisites

- Docker and Docker Compose installed
- AWS credentials configured locally (`~/.aws/credentials` or `aws configure`)
- Part 3 agents working locally

## Quick Start

### 1. Verify AWS Configuration
```bash
# Ensure AWS credentials are configured locally
aws sts get-caller-identity

# Copy environment template (optional)
cp .env.example .env
```

### 2. Build and Deploy
```bash
# Build Docker images
./scripts/build.sh

# Deploy containers
./scripts/deploy.sh
```

### 3. Test Deployment
```bash
# Test all agents
./scripts/test.sh
```

## Step-by-Step Instructions

### Step 1: Verify AWS Configuration

Ensure AWS credentials are configured locally:
```bash
# Check current AWS configuration
aws sts get-caller-identity

# If not configured, run:
aws configure
```

Optionally create `.env` file for region:
```bash
cp .env.example .env
```

### Step 2: Build Docker Images

Build all agent images:
```bash
./scripts/build.sh
```

This creates three Docker images:
- `construction-purchase-agent:latest`
- `construction-cement-agent:latest`
- `construction-steel-agent:latest`

### Step 3: Deploy Containers

Start all agent containers:
```bash
./scripts/deploy.sh
```

This will:
- Stop any existing containers
- Start all three agents
- Wait for health checks
- Display status and endpoints

### Step 4: Verify Deployment

Test agent health and connectivity:
```bash
./scripts/test.sh
```

Check individual agent cards:
```bash
# Purchase Agent
curl http://localhost:10001/.well-known/agent-card.json

# Cement Agent  
curl http://localhost:10002/.well-known/agent-card.json

# Steel Agent
curl http://localhost:10003/.well-known/agent-card.json
```

### Step 5: Run Negotiation Demo

With containers running, test the full negotiation:
```bash
cd ../part-03-a2a-communication
python negotiation_demo.py
```

## Container Architecture

### Network Configuration
- **Network**: `agent-network` (bridge)
- **Ports**: 10001-10003 exposed to host
- **Inter-container**: Agents can communicate via container names

### Volume Management
- **Logs**: Shared volume `agent-logs` for persistent logging
- **Data**: Stateless containers (no persistent data)

### Health Checks
- **Endpoint**: `/.well-known/agent-card.json`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3 attempts

## Management Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f purchase-agent
```

### Container Status
```bash
# Service status
docker-compose ps

# Resource usage
docker stats
```

### Stop Services
```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart purchase-agent
```

## Troubleshooting

### Container Won't Start
1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify Docker daemon is running
3. Check logs: `docker-compose logs [service-name]`

### Health Check Failures
1. Wait longer for startup (agents need ~30-40 seconds)
2. Check Bedrock access: `aws bedrock list-foundation-models --region us-east-1`
3. Verify port availability (10001-10003)

### Agent Communication Issues
1. Ensure all containers are healthy
2. Check network connectivity between containers
3. Verify agent card endpoints are responding

### Performance Issues
1. Monitor resource usage: `docker stats`
2. Check container logs for errors
3. Increase container memory limits if needed

## File Structure

```
part-04-local-deployment/
├── README.md                    # This documentation
├── docker-compose.yml           # Multi-container orchestration
├── Dockerfile.purchase          # Purchase agent container
├── Dockerfile.cement            # Cement agent container  
├── Dockerfile.steel             # Steel agent container
├── .env.example                 # Environment template
└── scripts/
    ├── build.sh                 # Build Docker images
    ├── deploy.sh                # Deploy containers
    ├── test.sh                  # Test deployment
    └── cleanup.sh               # Clean up resources
```

## Integration with Part 3

This deployment:
- ✅ Uses exact same agent code from Part 3
- ✅ Maintains all A2A communication capabilities
- ✅ Preserves agent cards and negotiation logic
- ✅ Supports client running locally (outside containers)
- ✅ Provides same endpoints (ports 10001-10003)

## Next Steps

- **Part 5**: Cloud deployment with Kubernetes/EKS
- **Monitoring**: Add Prometheus/Grafana for production monitoring
- **Scaling**: Implement horizontal scaling for high load
- **Security**: Add authentication and TLS encryption

## Demo Scenarios

### Scenario 1: Basic Container Health
1. Deploy containers: `./scripts/deploy.sh`
2. Verify health: `./scripts/test.sh`
3. Check agent cards via curl commands

### Scenario 2: Full Negotiation
1. Ensure containers are running
2. Run negotiation demo from Part 3
3. Monitor container logs during negotiation

### Scenario 3: Container Recovery
1. Stop one container: `docker-compose stop cement-agent`
2. Observe health check failures
3. Restart: `docker-compose start cement-agent`
4. Verify recovery and health restoration