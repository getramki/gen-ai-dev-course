#!/bin/bash

# Start all A2A agents for construction procurement demo
# Building on Part 1 (LangGraph + Bedrock) + Part 2 (MCP) + Part 3 (A2A SDK)

echo "🚀 Starting Construction A2A Agents"
echo "=================================="
echo "Part 1: LangGraph + Bedrock (Basic Agents)"
echo "Part 2: + MCP Integration (Enhanced Tools)"  
echo "Part 3: + A2A SDK (Inter-Agent Communication)"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Start agents in background
echo "🏗️  Starting Purchase Agent (Port 10001)..."
cd purchase_agent && python -m app --host localhost --port 10001 &
PURCHASE_PID=$!
cd ..

echo "🏭 Starting Cement Sales Agent (Port 10002)..."
cd cement_agent && python -m app --host localhost --port 10002 &
CEMENT_PID=$!
cd ..

echo "🔩 Starting Steel Sales Agent (Port 10003)..."
cd steel_agent && python -m app --host localhost --port 10003 &
STEEL_PID=$!
cd ..

# Wait for agents to start
echo "⏳ Waiting for agents to initialize..."
sleep 5

echo "✅ All agents started successfully!"
echo ""
echo "🌐 Agent Endpoints:"
echo "   Purchase Agent: http://localhost:10001"
echo "   Cement Agent:   http://localhost:10002"
echo "   Steel Agent:    http://localhost:10003"
echo ""
echo "🧪 Run demo client:"
echo "   python demo_client.py"
echo ""
echo "🛑 Stop agents:"
echo "   kill $PURCHASE_PID $CEMENT_PID $STEEL_PID"

# Keep script running
echo "Press Ctrl+C to stop all agents..."
trap "echo '🛑 Stopping agents...'; kill $PURCHASE_PID $CEMENT_PID $STEEL_PID; exit" INT
wait