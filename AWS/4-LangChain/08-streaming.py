"""
08 - Streaming Responses

This script demonstrates:
- Streaming responses from agents
- Real-time token generation
- Handling streaming events
- Better user experience with streaming

Prerequisites:
- Completed 07-short-term-memory.py
"""

from langchain_aws import ChatBedrock
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
import sys

print("="*60)
print("Streaming Responses Examples")
print("="*60 + "\n")

# Custom callback handler for streaming
class CustomStreamingHandler(BaseCallbackHandler):
    """Custom handler to capture streaming events."""
    
    def __init__(self):
        self.tokens = []
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Called when a new token is generated."""
        self.tokens.append(token)
        sys.stdout.write(token)
        sys.stdout.flush()
    
    def on_llm_start(self, *args, **kwargs) -> None:
        """Called when LLM starts generating."""
        print("[Streaming started]")
    
    def on_llm_end(self, *args, **kwargs) -> None:
        """Called when LLM finishes generating."""
        print("\n[Streaming ended]")

# Create simple tools
def get_info(topic: str) -> str:
    """Get information about a topic."""
    info_db = {
        "python": "Python is a high-level programming language known for its simplicity and readability.",
        "docker": "Docker is a platform for developing, shipping, and running applications in containers.",
        "aws": "AWS (Amazon Web Services) is a comprehensive cloud computing platform.",
    }
    return info_db.get(topic.lower(), f"No information available for {topic}")

tools = [
    Tool(
        name="GetInfo",
        func=get_info,
        description="Get information about a topic. Input: topic name (python, docker, or aws)"
    )
]

# Example 1: Basic Streaming with ChatBedrock
print("Example 1: Basic Streaming with ChatBedrock")
print("-" * 60)
print("Streaming a simple response without agents.\n")

streaming_llm = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={"temperature": 0.7, "max_tokens": 500},
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

print("Question: What is machine learning?\n")
print("Response: ", end="")
response = streaming_llm.invoke("Explain machine learning in 2 sentences.")
print("\n")

# Example 2: Streaming with Custom Handler
print("Example 2: Streaming with Custom Handler")
print("-" * 60)
print("Using a custom callback handler to track tokens.\n")

custom_handler = CustomStreamingHandler()
streaming_llm_custom = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={"temperature": 0.7, "max_tokens": 500},
    streaming=True,
    callbacks=[custom_handler]
)

print("Question: What is cloud computing?\n")
print("Response: ", end="")
response = streaming_llm_custom.invoke("Explain cloud computing in 2 sentences.")
print(f"\nTotal tokens received: {len(custom_handler.tokens)}\n")

# Example 3: Streaming with Agent
print("Example 3: Streaming with Agent")
print("-" * 60)
print("Stream responses from an agent with tools.\n")

streaming_agent_llm = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={"temperature": 0.5, "max_tokens": 1000},
    streaming=True
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the available tools to answer questions."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
agent = create_tool_calling_agent(streaming_agent_llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True
)

print("Question: Tell me about Python\n")
response = agent_executor.invoke({"input": "Tell me about Python"})
print(f"\nFinal Answer: {response['output']}\n")

# Example 4: Streaming with astream_events (Modern Approach)
print("Example 4: Streaming Events")
print("-" * 60)
print("Using astream_events for detailed streaming control.\n")

async def stream_agent_response():
    """Async function to stream agent responses."""
    from langchain_core.messages import HumanMessage
    
    streaming_llm_async = ChatBedrock(
        model_id="us.amazon.nova-pro-v1:0",
        region_name="us-east-1",
        model_kwargs={"temperature": 0.7, "max_tokens": 500},
        streaming=True
    )
    
    print("Question: What are the benefits of Docker?\n")
    print("Response: ", end="")
    
    async for chunk in streaming_llm_async.astream("List 3 benefits of Docker in brief."):
        print(chunk.content, end="", flush=True)
    
    print("\n")

# Run async example
import asyncio
try:
    asyncio.run(stream_agent_response())
except Exception as e:
    print(f"Async streaming example skipped: {e}\n")

# Example 5: Comparing Streaming vs Non-Streaming
print("Example 5: Streaming vs Non-Streaming Comparison")
print("-" * 60)

import time

# Non-streaming
print("Non-Streaming (waits for complete response):")
non_streaming_llm = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={"temperature": 0.7, "max_tokens": 300},
    streaming=False
)

start = time.time()
response = non_streaming_llm.invoke("Explain containers in 3 sentences.")
elapsed = time.time() - start
print(f"Response: {response.content}")
print(f"Time: {elapsed:.2f}s (user waits entire time)\n")

# Streaming
print("Streaming (shows tokens as they arrive):")
streaming_llm_compare = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={"temperature": 0.7, "max_tokens": 300},
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

start = time.time()
response = streaming_llm_compare.invoke("Explain containers in 3 sentences.")
elapsed = time.time() - start
print(f"\nTime: {elapsed:.2f}s (user sees progress immediately)\n")

print("="*60)
print("\n✓ Streaming complete!")
print("\nWhat you learned:")
print("- How to enable streaming in ChatBedrock")
print("- Using StreamingStdOutCallbackHandler")
print("- Creating custom streaming handlers")
print("- Streaming with agents")
print("- Benefits of streaming for user experience")
print("- Async streaming with astream()")
