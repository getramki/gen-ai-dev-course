"""
06 - Agent Invocation Methods

This script demonstrates:
- Different ways to invoke agents
- Synchronous invocation
- Batch processing
- Error handling during invocation

Prerequisites:
- Completed 05-tools-advanced.py
"""

from langchain_aws import ChatBedrock
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
import time

print("="*60)
print("Agent Invocation Methods")
print("="*60 + "\n")

# Initialize the model
llm = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={"temperature": 0.5, "max_tokens": 1000}
)

# Create simple tools
def multiply(numbers: str) -> str:
    """Multiply comma-separated numbers."""
    try:
        nums = [float(x.strip()) for x in numbers.split(',')]
        result = 1
        for num in nums:
            result *= num
        return f"Result: {result}"
    except:
        return "Error: Please provide comma-separated numbers"

def reverse_text(text: str) -> str:
    """Reverse the input text."""
    return f"Reversed: {text[::-1]}"

tools = [
    Tool(name="Multiply", func=multiply, 
         description="Multiply numbers. Input: comma-separated numbers"),
    Tool(name="ReverseText", func=reverse_text,
         description="Reverse text. Input: text to reverse")
]

# Create agent
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

# Method 1: Simple Invoke
print("Method 1: Simple Invoke")
print("-" * 60)
print("This is the standard way to invoke an agent.\n")

start_time = time.time()
result = agent_executor.invoke({"input": "Multiply 5, 10, and 2"})
elapsed = time.time() - start_time

print(f"\nResult: {result['output']}")
print(f"Time taken: {elapsed:.2f} seconds\n")

# Method 2: Invoke with Return Intermediate Steps
print("Method 2: Invoke with Intermediate Steps")
print("-" * 60)
print("This returns all intermediate reasoning steps.\n")

agent_with_steps = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)

result = agent_with_steps.invoke({"input": "Reverse the word 'LangChain'"})
print(f"Final Output: {result['output']}")
print(f"\nIntermediate Steps: {len(result['intermediate_steps'])} steps")
for i, step in enumerate(result['intermediate_steps'], 1):
    print(f"  Step {i}: {step[0].tool} - {step[1]}")
print()

# Method 3: Batch Invocation
print("Method 3: Batch Invocation")
print("-" * 60)
print("Process multiple queries efficiently.\n")

queries = [
    {"input": "Multiply 3 and 7"},
    {"input": "Reverse the word 'Python'"},
    {"input": "Multiply 2, 4, and 5"}
]

start_time = time.time()
results = agent_executor.batch(queries)
elapsed = time.time() - start_time

for i, result in enumerate(results, 1):
    print(f"Query {i}: {queries[i-1]['input']}")
    print(f"Answer: {result['output']}\n")

print(f"Total time for {len(queries)} queries: {elapsed:.2f} seconds")
print(f"Average time per query: {elapsed/len(queries):.2f} seconds\n")

# Method 4: Invoke with Error Handling
print("Method 4: Invoke with Error Handling")
print("-" * 60)
print("Gracefully handle errors during invocation.\n")

def safe_invoke(agent_exec, query):
    """Safely invoke agent with error handling."""
    try:
        result = agent_exec.invoke({"input": query})
        return {"success": True, "output": result['output']}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Valid query
result1 = safe_invoke(agent_executor, "Multiply 10 and 20")
print(f"Query 1 - Success: {result1['success']}")
if result1['success']:
    print(f"Output: {result1['output']}\n")
else:
    print(f"Error: {result1['error']}\n")

# Method 5: Invoke with Timeout Control
print("Method 5: Invoke with Max Iterations")
print("-" * 60)
print("Control agent execution with iteration limits.\n")

limited_agent = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True,
    max_iterations=3,  # Limit iterations
    early_stopping_method="generate"
)

result = limited_agent.invoke({"input": "Multiply 6 and 9"})
print(f"\nResult: {result['output']}\n")

print("="*60)
print("\n✓ Agent invocation methods complete!")
print("\nWhat you learned:")
print("- invoke(): Standard synchronous invocation")
print("- return_intermediate_steps: Get reasoning steps")
print("- batch(): Process multiple queries efficiently")
print("- Error handling: Graceful failure management")
print("- max_iterations: Control execution limits")
