"""
07 - Short-Term Memory for Agents

This script demonstrates:
- Adding conversation memory to agents
- Context retention across multiple turns
- Different memory types
- Memory management

Prerequisites:
- Completed 06-agent-invocation.py
"""

from langchain_aws import ChatBedrock
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.schema import HumanMessage, AIMessage

print("="*60)
print("Short-Term Memory Examples")
print("="*60 + "\n")

# Initialize the model
llm = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={"temperature": 0.7, "max_tokens": 1000}
)

# Create simple tools
def add_numbers(numbers: str) -> str:
    """Add comma-separated numbers."""
    try:
        nums = [float(x.strip()) for x in numbers.split(',')]
        return f"Sum: {sum(nums)}"
    except:
        return "Error: Please provide comma-separated numbers"

def save_note(note: str) -> str:
    """Save a note (simulated)."""
    return f"Note saved: '{note}'"

tools = [
    Tool(name="Add", func=add_numbers,
         description="Add numbers. Input: comma-separated numbers"),
    Tool(name="SaveNote", func=save_note,
         description="Save a note. Input: the note text")
]

# Example 1: Agent WITHOUT Memory
print("Example 1: Agent WITHOUT Memory")
print("-" * 60)
print("The agent won't remember previous interactions.\n")

prompt_no_memory = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the available tools to answer questions."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
agent_no_memory = create_tool_calling_agent(llm, tools, prompt_no_memory)
executor_no_memory = AgentExecutor(
    agent=agent_no_memory,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True
)

# First interaction
response1 = executor_no_memory.invoke({"input": "My name is Alice"})
print(f"User: My name is Alice")
print(f"Agent: {response1['output']}\n")

# Second interaction - agent won't remember
response2 = executor_no_memory.invoke({"input": "What is my name?"})
print(f"User: What is my name?")
print(f"Agent: {response2['output']}\n")

# Example 2: Agent WITH Buffer Memory
print("Example 2: Agent WITH Buffer Memory")
print("-" * 60)
print("The agent remembers all previous interactions.\n")

# Create memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

prompt_with_memory = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the available tools to answer questions."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent_with_memory = create_tool_calling_agent(llm, tools, prompt_with_memory)
executor_with_memory = AgentExecutor(
    agent=agent_with_memory,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True,
    memory=memory
)

# First interaction
response1 = executor_with_memory.invoke({"input": "My name is Bob and I like Python"})
print(f"User: My name is Bob and I like Python")
print(f"Agent: {response1['output']}\n")

# Second interaction - agent remembers
response2 = executor_with_memory.invoke({"input": "What is my name?"})
print(f"User: What is my name?")
print(f"Agent: {response2['output']}\n")

# Third interaction - agent remembers both
response3 = executor_with_memory.invoke({"input": "What programming language do I like?"})
print(f"User: What programming language do I like?")
print(f"Agent: {response3['output']}\n")

# View memory contents
print("Memory Contents:")
print(memory.load_memory_variables({}))
print()

# Example 3: Window Memory (Limited History)
print("Example 3: Window Memory (Last 2 Interactions)")
print("-" * 60)
print("The agent only remembers the last N interactions.\n")

window_memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
    k=2  # Remember only last 2 interactions
)

executor_window = AgentExecutor(
    agent=agent_with_memory,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True,
    memory=window_memory
)

# Multiple interactions
interactions = [
    "My favorite color is blue",
    "I live in New York",
    "I work as a developer",
    "What is my favorite color?"  # This should be forgotten
]

for interaction in interactions:
    response = executor_window.invoke({"input": interaction})
    print(f"User: {interaction}")
    print(f"Agent: {response['output']}\n")

# Example 4: Manual Memory Management
print("Example 4: Manual Memory Management")
print("-" * 60)
print("Manually add, view, and clear memory.\n")

manual_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Manually add to memory
manual_memory.chat_memory.add_user_message("I have a meeting at 3 PM")
manual_memory.chat_memory.add_ai_message("I'll remember that you have a meeting at 3 PM")
manual_memory.chat_memory.add_user_message("Add 10 and 20")
manual_memory.chat_memory.add_ai_message("The sum is 30")

# View memory
print("Current memory:")
messages = manual_memory.chat_memory.messages
for msg in messages:
    msg_type = "User" if isinstance(msg, HumanMessage) else "AI"
    print(f"  {msg_type}: {msg.content}")

# Clear memory
print("\nClearing memory...")
manual_memory.clear()
print(f"Memory after clearing: {len(manual_memory.chat_memory.messages)} messages\n")

print("="*60)
print("\n✓ Short-term memory complete!")
print("\nWhat you learned:")
print("- ConversationBufferMemory: Remembers all interactions")
print("- ConversationBufferWindowMemory: Remembers last N interactions")
print("- How to integrate memory with agents")
print("- Manual memory management (add, view, clear)")
print("- When to use different memory types")
