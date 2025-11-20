#!/bin/bash

# Test script for containerized agents
set -e

echo "🧪 Testing Containerized Construction Agents"
echo "==========================================="

# Test agent cards
echo "📋 Testing Agent Cards..."

echo "  Testing Purchase Agent..."
if response=$(curl -s http://localhost:10001/.well-known/agent-card.json); then
    echo "    ✅ Agent card retrieved"
    echo "    📝 Name: $(echo $response | python3 -c "import sys, json; print(json.load(sys.stdin)['name'])")"
else
    echo "    ❌ Failed to retrieve agent card"
fi

echo "  Testing Cement Agent..."
if response=$(curl -s http://localhost:10002/.well-known/agent-card.json); then
    echo "    ✅ Agent card retrieved"
    echo "    📝 Name: $(echo $response | python3 -c "import sys, json; print(json.load(sys.stdin)['name'])")"
else
    echo "    ❌ Failed to retrieve agent card"
fi

echo "  Testing Steel Agent..."
if response=$(curl -s http://localhost:10003/.well-known/agent-card.json); then
    echo "    ✅ Agent card retrieved"
    echo "    📝 Name: $(echo $response | python3 -c "import sys, json; print(json.load(sys.stdin)['name'])")"
else
    echo "    ❌ Failed to retrieve agent card"
fi

echo ""
echo "🔗 Testing A2A Communication..."

# Test basic JSON-RPC communication
echo "  Testing Purchase Agent JSON-RPC..."
if curl -s -X POST http://localhost:10001/ \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"agent.execute","params":{"message":{"content":[{"type":"text","text":"Hello"}],"role":"user"}},"id":1}' \
    | grep -q "jsonrpc"; then
    echo "    ✅ JSON-RPC endpoint responding"
else
    echo "    ❌ JSON-RPC endpoint not responding"
fi

echo ""
echo "📊 Container Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "📋 Container Logs (last 10 lines):"
echo "--- Purchase Agent ---"
docker-compose logs --tail=5 purchase-agent

echo "--- Cement Agent ---"
docker-compose logs --tail=5 cement-agent

echo "--- Steel Agent ---"
docker-compose logs --tail=5 steel-agent

echo ""
echo "✅ Testing completed!"
echo ""
echo "🚀 To run full negotiation demo:"
echo "   cd ../part-03-a2a-communication"
echo "   python negotiation_demo.py"