#!/bin/bash
# Quick start script for Agent Loop Demo

echo "🤖 Strands Agents - Agent Loop Demo"
echo "=================================="
echo ""
echo "Choose an option:"
echo "1. Run automated demo"
echo "2. Run interactive demo"
echo "3. Run automated scenarios only"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "Running automated demo..."
        python3 agent_loop_demo.py
        ;;
    2)
        echo "Starting interactive demo..."
        echo "Type 'demo' for scenarios, 'memory' to see memory, 'quit' to exit"
        python3 interactive_demo.py
        ;;
    3)
        echo "Running automated scenarios..."
        python3 interactive_demo.py --auto
        ;;
    *)
        echo "Invalid choice. Running default automated demo..."
        python3 agent_loop_demo.py
        ;;
esac