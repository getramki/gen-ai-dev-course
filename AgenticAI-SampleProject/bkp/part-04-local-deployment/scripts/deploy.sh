#!/bin/bash

# Deploy script for construction agents
set -e

echo "🚀 Deploying Construction A2A Agents"
echo "===================================="

# Check AWS credentials
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS credentials not configured. Please run 'aws configure' or ensure ~/.aws/credentials exists."
    exit 1
fi

echo "✅ AWS credentials verified"

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install Docker Compose."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Start services
echo "🚀 Starting agent services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for agents to start (using local AWS credentials)..."
sleep 30

# Check health status
echo "🏥 Checking agent health..."
echo ""

# Check Purchase Agent
if curl -f http://localhost:10001/.well-known/agent-card.json > /dev/null 2>&1; then
    echo "✅ Purchase Agent (port 10001) - HEALTHY"
else
    echo "❌ Purchase Agent (port 10001) - UNHEALTHY"
fi

# Check Cement Agent
if curl -f http://localhost:10002/.well-known/agent-card.json > /dev/null 2>&1; then
    echo "✅ Cement Agent (port 10002) - HEALTHY"
else
    echo "❌ Cement Agent (port 10002) - UNHEALTHY"
fi

# Check Steel Agent
if curl -f http://localhost:10003/.well-known/agent-card.json > /dev/null 2>&1; then
    echo "✅ Steel Agent (port 10003) - HEALTHY"
else
    echo "❌ Steel Agent (port 10003) - UNHEALTHY"
fi

echo ""
echo "📊 Container status:"
docker-compose ps

echo ""
echo "📋 Available endpoints:"
echo "  Purchase Agent: http://localhost:10001"
echo "  Cement Agent:   http://localhost:10002"
echo "  Steel Agent:    http://localhost:10003"

echo ""
echo "🧪 Run tests: ./scripts/test.sh"
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop: docker-compose down"