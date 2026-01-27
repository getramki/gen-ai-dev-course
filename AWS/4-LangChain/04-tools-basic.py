"""
04 - Basic Tools for Agents

This script demonstrates:
- Creating custom tools
- Defining tool schemas
- Using tools with agents

Prerequisites:
- Completed 03-dynamic-model.py
"""

from langchain_aws import ChatBedrock
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
import datetime

print("="*60)
print("Basic Tools Examples")
print("="*60 + "\n")

# Initialize the model
llm = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={"temperature": 0.3, "max_tokens": 1000}
)

# Tool 1: Calculator
print("Creating Tool 1: Calculator")
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"

calculator_tool = Tool(
    name="Calculator",
    func=calculator,
    description="Useful for mathematical calculations. Input should be a valid Python expression like '2+2' or '10*5'."
)
print("✓ Calculator tool created\n")

# Tool 2: Current Time
print("Creating Tool 2: Current Time")
def get_current_time(dummy: str = "") -> str:
    """Get the current date and time."""
    now = datetime.datetime.now()
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

time_tool = Tool(
    name="CurrentTime",
    func=get_current_time,
    description="Get the current date and time. No input needed."
)
print("✓ Time tool created\n")

# Tool 3: Text Length Counter
print("Creating Tool 3: Text Length Counter")
def count_text_length(text: str) -> str:
    """Count characters and words in text."""
    char_count = len(text)
    word_count = len(text.split())
    return f"Characters: {char_count}, Words: {word_count}"

text_counter_tool = Tool(
    name="TextCounter",
    func=count_text_length,
    description="Count the number of characters and words in a text. Input should be the text to analyze."
)
print("✓ Text counter tool created\n")

# Create agent with tools
print("Creating agent with tools...")
tools = [calculator_tool, time_tool, text_counter_tool]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the available tools to answer questions."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True
)
print("✓ Agent created\n")

# Test the tools
print("="*60)
print("Testing Tools")
print("="*60 + "\n")

# Test 1: Calculator
print("Test 1: Using Calculator")
print("-" * 60)
response = agent_executor.invoke({"input": "What is 25 multiplied by 4?"})
print(f"\nFinal Answer: {response['output']}\n")

# Test 2: Current Time
print("Test 2: Getting Current Time")
print("-" * 60)
response = agent_executor.invoke({"input": "What is the current date and time?"})
print(f"\nFinal Answer: {response['output']}\n")

# Test 3: Text Counter
print("Test 3: Counting Text")
print("-" * 60)
response = agent_executor.invoke({
    "input": "How many words are in this sentence: 'LangChain makes building AI agents easy'"
})
print(f"\nFinal Answer: {response['output']}\n")

print("="*60)
print("\n✓ Basic tools complete!")
print("\nWhat you learned:")
print("- How to create custom tools with specific functions")
print("- How to define tool descriptions for the agent")
print("- How to use multiple tools with one agent")
print("- How agents decide which tool to use")
