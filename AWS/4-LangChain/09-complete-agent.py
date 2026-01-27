"""
09 - Complete Agent (All Concepts Combined)

This script demonstrates:
- A production-ready agent combining all concepts
- Dynamic model configuration
- Multiple tools
- Memory
- Streaming
- Error handling

Prerequisites:
- Completed all previous modules (01-08)
"""

from langchain_aws import ChatBedrock
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from langchain.memory import ConversationBufferWindowMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import datetime
import json

print("="*60)
print("Complete Agent - All Concepts Combined")
print("="*60 + "\n")

# ============================================================================
# 1. DYNAMIC MODEL CONFIGURATION
# ============================================================================
class AgentModelConfig:
    """Manages dynamic model configuration."""
    
    @staticmethod
    def get_model(mode="balanced", streaming=True):
        """Get configured model based on mode."""
        configs = {
            "creative": {"temperature": 0.9, "max_tokens": 1500},
            "precise": {"temperature": 0.2, "max_tokens": 1000},
            "balanced": {"temperature": 0.6, "max_tokens": 1200},
        }
        
        config = configs.get(mode, configs["balanced"])
        
        callbacks = [StreamingStdOutCallbackHandler()] if streaming else []
        
        return ChatBedrock(
            model_id="us.amazon.nova-pro-v1:0",
            region_name="us-east-1",
            model_kwargs=config,
            streaming=streaming,
            callbacks=callbacks
        )

# ============================================================================
# 2. COMPREHENSIVE TOOLS
# ============================================================================

def calculate(expression: str) -> str:
    """Evaluate mathematical expressions safely."""
    try:
        # Safe evaluation
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

def get_current_datetime(format_type: str = "full") -> str:
    """Get current date/time in various formats."""
    now = datetime.datetime.now()
    formats = {
        "full": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A"),
    }
    return formats.get(format_type, formats["full"])

def text_analyzer(text: str) -> str:
    """Analyze text and return statistics."""
    try:
        stats = {
            "characters": len(text),
            "words": len(text.split()),
            "sentences": text.count('.') + text.count('!') + text.count('?'),
            "uppercase": sum(1 for c in text if c.isupper()),
            "lowercase": sum(1 for c in text if c.islower()),
        }
        return json.dumps(stats, indent=2)
    except Exception as e:
        return f"Analysis error: {str(e)}"

def search_knowledge(query: str) -> str:
    """Search a simulated knowledge base."""
    knowledge = {
        "langchain": "LangChain is a framework for developing applications powered by language models.",
        "bedrock": "Amazon Bedrock is a fully managed service for foundation models.",
        "agent": "An agent is an autonomous entity that uses an LLM to decide actions.",
        "memory": "Memory allows agents to retain context across conversations.",
        "streaming": "Streaming provides real-time token generation for better UX.",
    }
    
    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return value
    
    return f"No knowledge found for: {query}"

def unit_converter(conversion: str) -> str:
    """Convert between common units."""
    try:
        parts = conversion.lower().split()
        if len(parts) != 4 or parts[2] != 'to':
            return "Format: 'value unit1 to unit2'"
        
        value = float(parts[0])
        from_unit, to_unit = parts[1], parts[3]
        
        conversions = {
            ('c', 'f'): lambda x: (x * 9/5) + 32,
            ('f', 'c'): lambda x: (x - 32) * 5/9,
            ('km', 'mi'): lambda x: x * 0.621371,
            ('mi', 'km'): lambda x: x / 0.621371,
        }
        
        key = (from_unit, to_unit)
        if key in conversions:
            result = conversions[key](value)
            return f"{value} {from_unit} = {result:.2f} {to_unit}"
        return f"Conversion {from_unit} to {to_unit} not supported"
    except Exception as e:
        return f"Conversion error: {str(e)}"

# Create tools
tools = [
    Tool(
        name="Calculator",
        func=calculate,
        description="Evaluate math expressions. Input: expression like '2+2' or '10*5'"
    ),
    Tool(
        name="DateTime",
        func=get_current_datetime,
        description="Get current date/time. Input: 'full', 'date', 'time', or 'day'"
    ),
    Tool(
        name="TextAnalyzer",
        func=text_analyzer,
        description="Analyze text statistics. Input: text to analyze"
    ),
    Tool(
        name="KnowledgeSearch",
        func=search_knowledge,
        description="Search knowledge base. Input: search query"
    ),
    Tool(
        name="UnitConverter",
        func=unit_converter,
        description="Convert units. Input: 'value unit1 to unit2' (e.g., '100 c to f')"
    ),
]

# ============================================================================
# 3. MEMORY CONFIGURATION
# ============================================================================
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
    k=5  # Remember last 5 interactions
)

# ============================================================================
# 4. AGENT SETUP
# ============================================================================
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant with access to various tools. Use them wisely to help the user."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Initialize model
llm = AgentModelConfig.get_model(mode="balanced", streaming=True)

# Create agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=False,
    handle_parsing_errors=True,
    max_iterations=5
)

# ============================================================================
# 5. INTERACTIVE AGENT SESSION
# ============================================================================
print("Complete Agent initialized with:")
print("✓ Dynamic model configuration (balanced mode)")
print("✓ 5 comprehensive tools")
print("✓ Conversation memory (last 5 interactions)")
print("✓ Streaming enabled")
print("✓ Error handling")
print("\n" + "="*60 + "\n")

# Test queries demonstrating all features
test_queries = [
    "What is the current date and time?",
    "Calculate 25 * 4 + 10",
    "Search for information about LangChain",
    "Analyze this text: 'Hello World! This is a test.'",
    "What did I ask you to calculate earlier?",  # Tests memory
]

for i, query in enumerate(test_queries, 1):
    print(f"\n{'='*60}")
    print(f"Query {i}: {query}")
    print('='*60)
    
    try:
        response = agent_executor.invoke({"input": query})
        print(f"\n✓ Final Answer: {response['output']}\n")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}\n")

# ============================================================================
# 6. DEMONSTRATE MEMORY
# ============================================================================
print("\n" + "="*60)
print("Memory Contents (Last 5 Interactions)")
print("="*60)
memory_vars = memory.load_memory_variables({})
if memory_vars.get('chat_history'):
    for msg in memory_vars['chat_history'][-10:]:  # Show last 10 messages
        msg_type = msg.__class__.__name__
        print(f"{msg_type}: {msg.content[:100]}...")
else:
    print("No memory stored")

# ============================================================================
# 7. SUMMARY
# ============================================================================
print("\n" + "="*60)
print("✓ Complete Agent Demo Finished!")
print("="*60)
print("\nThis agent demonstrates:")
print("1. ✓ Dynamic Model Configuration - Balanced mode with streaming")
print("2. ✓ Multiple Tools - Calculator, DateTime, TextAnalyzer, Knowledge, Converter")
print("3. ✓ Short-Term Memory - Remembers last 5 interactions")
print("4. ✓ Streaming - Real-time response generation")
print("5. ✓ Error Handling - Graceful failure management")
print("6. ✓ Tool Selection - Intelligent tool usage based on query")
print("\nYou now have a production-ready agent template!")
