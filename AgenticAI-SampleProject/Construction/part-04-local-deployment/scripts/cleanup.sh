#!/bin/bash

# Cleanup script for construction agents
set -e

echo "🧹 Cleaning up Construction Agent Containers"
echo "==========================================="

# Stop and remove containers
echo "🛑 Stopping containers..."
docker-compose down

# Remove containers
echo "🗑️  Removing containers..."
docker-compose rm -f

# Remove images (optional)
read -p "🤔 Remove Docker images? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing images..."
    docker rmi construction-purchase-agent:latest || true
    docker rmi construction-cement-agent:latest || true
    docker rmi construction-steel-agent:latest || true
fi

# Remove volumes (optional)
read -p "🤔 Remove volumes (logs will be lost)? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing volumes..."
    docker-compose down -v
fi

# Clean up unused Docker resources
echo "🧹 Cleaning up unused Docker resources..."
docker system prune -f

echo "✅ Cleanup completed!"