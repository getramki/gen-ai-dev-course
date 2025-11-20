#!/bin/bash

# Build script for construction agents
set -e

echo "🏗️  Building Construction A2A Agents Docker Images"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build images using docker-compose (respects context configuration)
echo "📦 Building all agent images..."
docker-compose build

echo "✅ All images built successfully!"
echo ""
echo "📋 Built images:"
docker images | grep construction-.*-agent

echo ""
echo "🚀 Next steps:"
echo "1. Copy .env.example to .env and configure AWS credentials"
echo "2. Run: docker-compose up -d"
echo "3. Test agents: ./scripts/test.sh"