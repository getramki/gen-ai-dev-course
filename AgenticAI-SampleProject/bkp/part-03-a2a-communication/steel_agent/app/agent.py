"""Steel Sales Agent using LangGraph + Bedrock + MCP, extending Part 1 & Part 2."""

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
def calculate_steel_quote(quantity_tons: int, base_cost_per_ton: float = 450, target_margin: float = 0.35):
    """Calculate steel quote with profit optimization.
    
    Args:
        quantity_tons: Quantity of steel in tons
        base_cost_per_ton: Base cost per ton (default $450)
        target_margin: Target profit margin (default 35%)
        
    Returns:
        Quote details with pricing and margin analysis
    """
    total_base_cost = quantity_tons * base_cost_per_ton
    target_price = total_base_cost * (1 + target_margin)
    unit_price = target_price / quantity_tons
    
    # Margin analysis for steel (higher margins than cement)
    min_margin = 0.25  # 25% minimum for steel
    min_price = total_base_cost * (1 + min_margin)
    max_discount = 0.12  # 12% max discount for steel
    
    return {
        "quantity_tons": quantity_tons,
        "unit_price": unit_price,
        "total_price": target_price,
        "base_cost": total_base_cost,
        "profit_margin": target_margin,
        "min_acceptable_price": min_price,
        "max_discount_available": max_discount,
        "quote_valid_days": 30,
        "steel_grade": "Premium Grade A"
    }

@tool
def evaluate_steel_negotiation(original_price: float, counter_offer: float, base_cost: float, cycle: int):
    """Evaluate counter-offer in steel negotiation cycle.
    
    Args:
        original_price: Original quoted price
        counter_offer: Counter-offer price from buyer
        base_cost: Base cost of steel materials
        cycle: Current negotiation cycle
        
    Returns:
        Negotiation decision and strategy for steel sales
    """
    margin_at_counter = (counter_offer - base_cost) / base_cost
    min_margin = 0.25  # 25% minimum margin for steel
    
    # Steel-specific decision logic (higher margins required)
    if cycle >= 5:
        decision = "accept"  # Auto-accept at max cycles
        reason = "Maximum negotiation cycles reached"
    elif margin_at_counter >= min_margin:
        decision = "accept"
        reason = f"Acceptable steel margin of {margin_at_counter*100:.1f}%"
    elif margin_at_counter >= 0.20:  # 20% emergency margin for steel
        decision = "counter" if cycle < 4 else "accept"
        final_price = base_cost * 1.25  # Counter at minimum margin
        reason = f"Counter-offer at minimum 25% steel margin: ${final_price:,.2f}"
    else:
        decision = "reject"
        reason = "Steel offer below minimum acceptable margin"
        
    return {
        "decision": decision,
        "reason": reason,
        "margin_at_offer": margin_at_counter,
        "min_margin_required": min_margin,
        "cycle": cycle,
        "counter_price": base_cost * 1.25 if decision == "counter" else None,
        "material_type": "Premium Steel Grade A"
    }

class ResponseFormat(BaseModel):
    """Steel sales response format."""
    status: Literal['input_required', 'completed', 'error'] = 'input_required'
    message: str
    quote_data: dict = {}

class SteelAgent:
    """Steel Sales Agent for profit-maximizing sales using LangGraph + Bedrock + MCP."""
    
    SYSTEM_INSTRUCTION = (
        'You are a Steel Company Sales Agent focused on maximizing profit margins in premium steel sales. '
        'When you receive an RFP or quote request, ALWAYS: '
        '1. Extract quantity, grade, steel types, delivery location, and budget information '
        '2. Use calculate_steel_quote tool with target 30-40% profit margins '
        '3. Provide detailed quote with unit prices, total cost, grade specifications '
        '4. Include quality certifications and premium positioning '
        'Target profit margins: 30-40%, minimum acceptable: 25%. Market price: $450-650/ton.'
    )
    
    FORMAT_INSTRUCTION = (
        'Set status to input_required if more details needed about steel specifications, quantity, or delivery. '
        'Set status to error if pricing constraints cannot be met or invalid steel parameters provided. '
        'Set status to completed when steel quote is finalized with pricing, grade, and delivery terms.'
    )
    
    def __init__(self):
        # Initialize Bedrock LLM
        self.model = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            region_name="us-east-1"
        )
        
        # Initialize steel business constraints
        self.min_margin = 0.25  # 25% minimum for steel
        self.target_margin = 0.35  # 35% target for steel
        self.max_discount = 0.12  # 12% max discount for steel
        
        self.tools = [calculate_steel_quote, evaluate_steel_negotiation]
        
        # Create LangGraph agent with system message
        self.graph = create_react_agent(
            self.model,
            self.tools,
            checkpointer=memory,
            state_modifier=self.SYSTEM_INSTRUCTION
        )
        
    async def stream(self, query: str, context_id: str) -> AsyncIterable[dict[str, Any]]:
        """Stream steel sales processing with LangGraph workflow."""
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
                    'content': 'Calculating premium steel pricing and profit margins...',
                }
            elif isinstance(message, ToolMessage):
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': 'Analyzing steel market conditions and negotiation strategy...',
                }
                
        yield self.get_agent_response(config)
        
    def get_agent_response(self, config):
        """Get final agent response with steel quote."""
        current_state = self.graph.get_state(config)
        messages = current_state.values.get('messages', [])
        
        # Get the last AI message
        last_message = None
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                last_message = msg
                break
        
        if last_message and last_message.content:
            # Check if it's a detailed steel quote
            content = last_message.content
            if any(keyword in content.lower() for keyword in ['quote', 'steel', 'price', 'cost', 'margin', 'grade']):
                return {
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': content,
                    'quote_data': {'quote': 'completed'}
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
            # Tools were used, provide quote
            quote = "Steel quote prepared. " + " ".join(tool_results)
            return {
                'is_task_complete': True,
                'require_user_input': False,
                'content': quote,
                'quote_data': {'tool_results': tool_results}
            }
                
        return {
            'is_task_complete': False,
            'require_user_input': True,
            'content': 'Unable to process steel quote request. Please provide steel grade, quantity and delivery requirements.',
        }
        
    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']