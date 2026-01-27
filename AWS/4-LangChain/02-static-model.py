"""
02 - Static Model Configuration

This script demonstrates:
- Configuring model with fixed parameters
- Understanding temperature, max_tokens, top_p
- Using different static configurations

Prerequisites:
- Completed 01-setup-and-basic-agent.py
"""

from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage, SystemMessage

print("="*60)
print("Static Model Configuration Examples")
print("="*60 + "\n")

# Configuration 1: Creative Model (High Temperature)
print("Configuration 1: Creative Model (High Temperature)")
print("-" * 60)
creative_model = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={
        "temperature": 0.9,  # High creativity
        "max_tokens": 500,
        "top_p": 0.95
    }
)

messages = [
    SystemMessage(content="You are a creative storyteller."),
    HumanMessage(content="Tell me a one-sentence story about a robot.")
]

response = creative_model.invoke(messages)
print(f"Response: {response.content}\n")

# Configuration 2: Precise Model (Low Temperature)
print("Configuration 2: Precise Model (Low Temperature)")
print("-" * 60)
precise_model = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={
        "temperature": 0.1,  # Low creativity, more deterministic
        "max_tokens": 500,
        "top_p": 0.5
    }
)

messages = [
    SystemMessage(content="You are a precise technical assistant."),
    HumanMessage(content="What is 2+2?")
]

response = precise_model.invoke(messages)
print(f"Response: {response.content}\n")

# Configuration 3: Balanced Model
print("Configuration 3: Balanced Model")
print("-" * 60)
balanced_model = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={
        "temperature": 0.5,  # Balanced
        "max_tokens": 300,
        "top_p": 0.8
    }
)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Explain what Docker is in one sentence.")
]

response = balanced_model.invoke(messages)
print(f"Response: {response.content}\n")

# Configuration 4: Concise Model (Limited Tokens)
print("Configuration 4: Concise Model (Limited Tokens)")
print("-" * 60)
concise_model = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={
        "temperature": 0.3,
        "max_tokens": 50,  # Very limited output
        "top_p": 0.7
    }
)

messages = [
    HumanMessage(content="Describe Python programming language.")
]

response = concise_model.invoke(messages)
print(f"Response: {response.content}\n")

print("="*60)
print("\n✓ Static model configuration complete!")
print("\nKey Parameters Explained:")
print("- temperature: Controls randomness (0.0-1.0)")
print("  * Low (0.1-0.3): Deterministic, factual")
print("  * Medium (0.4-0.7): Balanced")
print("  * High (0.8-1.0): Creative, varied")
print("- max_tokens: Maximum response length")
print("- top_p: Nucleus sampling (0.0-1.0)")
print("  * Lower values: More focused responses")
print("  * Higher values: More diverse responses")
