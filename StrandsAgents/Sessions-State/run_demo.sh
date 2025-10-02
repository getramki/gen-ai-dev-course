#!/bin/bash

# Strands Agents SDK Sessions and State Demo Runner

echo "Strands Agents SDK Sessions and State Demo"
echo "=========================================="
echo ""
echo "Choose demo type:"
echo "1. Mock SDK Demo (Recommended - No dependencies)"
echo "2. Real Strands SDK Demo (Requires strands-agents package)"
echo "3. Interactive Demo (Hands-on experimentation)"
echo ""

read -p "Enter your choice (1, 2, or 3): " choice

case $choice in
    1)
        echo "Running mock Strands SDK demo..."
        echo "This demonstrates all SDK concepts without requiring the actual package."
        echo ""
        python3 mock_strands_demo.py
        ;;
    2)
        echo "Running real Strands SDK demo..."
        echo "Note: This requires 'pip install strands-agents'"
        echo ""
        if python3 -c "import strands_agents" 2>/dev/null; then
            python3 strands_sessions_demo.py
        else
            echo "Error: strands-agents package not found!"
            echo "Please install it with: pip install strands-agents"
            echo "Or run the mock demo (option 1) instead."
            exit 1
        fi
        ;;
    3)
        echo "Starting interactive demo..."
        echo "Type 'quit' to exit when done."
        echo ""
        python3 interactive_demo.py
        ;;
    *)
        echo "Invalid choice. Please run the script again and choose 1, 2, or 3."
        exit 1
        ;;
esac

echo ""
echo "Demo completed! Check the README.md for more details."