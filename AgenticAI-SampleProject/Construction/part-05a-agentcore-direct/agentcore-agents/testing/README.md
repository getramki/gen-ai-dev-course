# Local Testing with Docker Compose

This directory contains Docker Compose configuration for local testing of AgentCore agents.

## Important Note
**Docker Compose is NOT required for AgentCore deployment.** AgentCore Runtime Service deploys individual container images directly from ECR.

## Usage
This docker-compose.yml is only for:
- Local development and testing
- Running all agents together on a single machine
- Validating agent functionality before ECR deployment

## Running Tests
```bash
# Build and start all agents
docker-compose up --build

# Test endpoints
curl http://localhost:8080/ping  # Purchase agent
curl http://localhost:8081/ping  # Cement agent  
curl http://localhost:8082/ping  # Steel agent

# Stop all agents
docker-compose down
```

## Port Mapping
- Purchase Agent: localhost:8080 → container:8080
- Cement Agent: localhost:8081 → container:8080
- Steel Agent: localhost:8082 → container:8080

All containers run on port 8080 internally (AgentCore requirement).