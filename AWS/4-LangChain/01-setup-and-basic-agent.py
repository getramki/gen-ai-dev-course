"""
01 - Setup and Basic Agent with AWS Bedrock Nova Pro

This script demonstrates:
- Setting up AWS Bedrock with LangChain
- Creating a basic agent
- Making simple queries

Prerequisites:
- AWS credentials configured
- pip install langchain langchain-aws boto3
"""

from langchain_aws import ChatBedrock
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool

# Step 1: Initialize AWS Bedrock with Nova Pro model
print("Step 1: Initializing AWS Bedrock Nova Pro...")
llm = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={
        "temperature": 0.7,
        "max_tokens": 1000
    }
)
print("✓ Model initialized successfully\n")

# Step 2: Create a simple tool for the agent
print("Step 2: Creating a simple greeting tool...")
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}! Nice to meet you."

greeting_tool = Tool(
    name="Greeter",
    func=greet,
    description="Use this tool to greet someone. Input should be a person's name."
)
print("✓ Tool created\n")

# Step 3: Create agent prompt template
print("Step 3: Setting up agent prompt...")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the available tools to help answer questions."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
print("✓ Prompt configured\n")

# Step 4: Create the agent
print("Step 4: Creating the agent...")
agent = create_tool_calling_agent(llm, [greeting_tool], prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=[greeting_tool],
    verbose=False,
    handle_parsing_errors=True
)
print("✓ Agent created successfully\n")

# Step 5: Test the agent
print("Step 5: Testing the agent...")
print("="*60)
print("Query: Please greet Alice\n")

# Test 1: Simple greeting
response = agent_executor.invoke({"input": "Please greet Alice"})
print(f"Final Answer: {response['output']}\n")

print("="*60)
print("\n✓ Basic agent setup complete!")
print("\nWhat you learned:")
print("- How to initialize AWS Bedrock Nova Pro")
print("- How to create a simple tool")
print("- How to create a basic ReAct agent")
print("- How to invoke an agent with a query")
