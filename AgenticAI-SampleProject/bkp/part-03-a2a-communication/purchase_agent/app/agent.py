"""Purchase Agent using LangGraph + Bedrock + MCP, extending Part 1 & Part 2."""

import os
import sys
from collections.abc import AsyncIterable
from typing import Any, Literal
from datetime import datetime

from langchain_aws import ChatBedrock
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

memory = MemorySaver()

@tool
def calculate_procurement_cost(cement_tons: int, cement_price: float, steel_tons: int, steel_price: float):
    """Calculate total procurement cost for construction materials.
    
    Args:
        cement_tons: Quantity of cement in tons
        cement_price: Price per ton of cement
        steel_tons: Quantity of steel in tons  
        steel_price: Price per ton of steel
        
    Returns:
        Dictionary with cost breakdown and optimization suggestions
    """
    cement_cost = cement_tons * cement_price
    steel_cost = steel_tons * steel_price
    total_cost = cement_cost + steel_cost
    
    # Cost optimization suggestions
    suggestions = []
    if cement_price > 160:
        suggestions.append("Cement price above market average - negotiate for better rates")
    if steel_price > 700:
        suggestions.append("Steel price high - consider alternative suppliers")
        
    return {
        "cement_cost": cement_cost,
        "steel_cost": steel_cost,
        "total_cost": total_cost,
        "cost_breakdown": f"Cement: ${cement_cost:,.2f}, Steel: ${steel_cost:,.2f}",
        "optimization_suggestions": suggestions
    }

@tool
def evaluate_supplier_quote(supplier_name: str, quoted_price: float, budget: float, cycle: int):
    """Evaluate supplier quote for procurement decision.
    
    Args:
        supplier_name: Name of the supplier
        quoted_price: Total quoted price
        budget: Available budget
        cycle: Current negotiation cycle
        
    Returns:
        Evaluation result with recommendation
    """
    budget_utilization = (quoted_price / budget) * 100
    savings = budget - quoted_price
    savings_pct = (savings / budget) * 100
    
    # Decision logic based on cycle and budget
    if cycle >= 5:
        recommendation = "accept"  # Auto-accept at max cycles
        reason = "Maximum negotiation cycles reached"
    elif quoted_price <= budget * 0.85:
        recommendation = "accept"
        reason = f"Excellent savings of {savings_pct:.1f}%"
    elif quoted_price <= budget * 0.95:
        recommendation = "negotiate" if cycle < 4 else "accept"
        reason = f"Good value, attempt negotiation in cycle {cycle}"
    else:
        recommendation = "reject" if cycle < 3 else "negotiate"
        reason = "Price exceeds budget targets"
        
    return {
        "supplier": supplier_name,
        "budget_utilization": budget_utilization,
        "savings": savings,
        "savings_percentage": savings_pct,
        "recommendation": recommendation,
        "reason": reason,
        "cycle": cycle
    }

class ResponseFormat(BaseModel):
    """Procurement response format."""
    status: Literal['input_required', 'completed', 'error'] = 'input_required'
    message: str
    procurement_data: dict = {}

class PurchaseAgent:
    """Purchase Agent for construction procurement using LangGraph + Bedrock + MCP."""
    
    SYSTEM_INSTRUCTION = (
        'You are a Construction Company Purchase Agent specializing in procurement optimization. '
        'When you receive a procurement request with cement and steel requirements, ALWAYS: '
        '1. Extract quantities, grades, and budget information '
        '2. Use calculate_procurement_cost tool with estimated market prices (cement: $50-60/ton, steel: $600-800/ton) '
        '3. Provide detailed cost breakdown and recommendations '
        '4. Suggest negotiation strategies and supplier evaluation criteria '
        'Your goal is to minimize costs while ensuring quality materials within budget constraints.'
    )
    
    FORMAT_INSTRUCTION = (
        'Set status to input_required if more information is needed for procurement decisions. '
        'Set status to error if there are issues with supplier quotes or budget constraints. '
        'Set status to completed when procurement decision is finalized with cost breakdown.'
    )
    
    def __init__(self):
        # Initialize Bedrock LLM
        self.model = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            region_name="us-east-1"
        )
        
        # Initialize basic constraints
        self.max_budget = 500000
        self.max_cement_price = 180
        self.max_steel_price = 750
        
        self.tools = [calculate_procurement_cost, evaluate_supplier_quote]
        
        # Create LangGraph agent with system message
        self.graph = create_react_agent(
            self.model,
            self.tools,
            checkpointer=memory,
            state_modifier=self.SYSTEM_INSTRUCTION
        )
        
    async def stream(self, query: str, context_id: str) -> AsyncIterable[dict[str, Any]]:
        """Stream procurement processing with LangGraph workflow."""
        inputs = {'messages': [('user', query)]}
        config = {'configurable': {'thread_id': context_id}}
        
        for item in self.graph.stream(inputs, config, stream_mode='values'):
            message = item['messages'][-1]
            if (
                isinstance(message, AIMessage)
                and message.tool_calls
                and len(message.tool_calls) > 0
            ):
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': 'Analyzing procurement requirements and costs...',
                }
            elif isinstance(message, ToolMessage):
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': 'Processing supplier quotes and budget analysis...',
                }
                
        yield self.get_agent_response(config)
        
    def get_agent_response(self, config):
        """Get final agent response with procurement decision."""
        current_state = self.graph.get_state(config)
        messages = current_state.values.get('messages', [])
        
        # Get the last AI message
        last_message = None
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                last_message = msg
                break
        
        if last_message and last_message.content:
            # Check if it's a detailed procurement analysis
            content = last_message.content
            if any(keyword in content.lower() for keyword in ['cost', 'budget', 'procurement', 'analysis', 'quote', 'price']):
                return {
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': content,
                    'procurement_data': {'analysis': 'completed'}
                }
            else:
                return {
                    'is_task_complete': False,
                    'require_user_input': True,
                    'content': content,
                }
        
        # Check if tools were used successfully
        tool_results = []
        for msg in messages:
            if isinstance(msg, ToolMessage):
                tool_results.append(msg.content)
        
        if tool_results:
            # Tools were used, provide analysis
            analysis = "Procurement analysis completed. " + " ".join(tool_results)
            return {
                'is_task_complete': True,
                'require_user_input': False,
                'content': analysis,
                'procurement_data': {'tool_results': tool_results}
            }
                
        return {
            'is_task_complete': False,
            'require_user_input': True,
            'content': 'Unable to process procurement request. Please provide material requirements and budget.',
        }
        
    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']