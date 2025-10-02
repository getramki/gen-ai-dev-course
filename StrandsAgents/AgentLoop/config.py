"""
Configuration for Agent Loop Demo
"""

# Agent Configuration
AGENT_CONFIG = {
    "name": "DemoAgent",
    "max_iterations": 5,
    "timeout_seconds": 30,
    "debug_mode": True
}

# Demo Scenarios
DEMO_SCENARIOS = [
    {
        "name": "Greeting Test",
        "input": "Hello there!",
        "expected_action": "greet_user"
    },
    {
        "name": "Weather Query",
        "input": "What's the weather like?",
        "expected_action": "check_weather"
    },
    {
        "name": "Time Request",
        "input": "What time is it?",
        "expected_action": "get_time"
    },
    {
        "name": "Complex Query",
        "input": "Can you help me with something complex?",
        "expected_action": "general_response"
    }
]

# Action Responses
ACTION_RESPONSES = {
    "greet_user": "Hello! Nice to meet you!",
    "check_weather": "I'd check the weather, but I don't have access to weather APIs yet.",
    "get_time": "I'd tell you the time, but I need a time service connection.",
    "general_response": "I understand your message. How can I help you further?"
}