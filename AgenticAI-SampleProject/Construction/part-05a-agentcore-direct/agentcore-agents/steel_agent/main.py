#!/usr/bin/env python3
"""
AgentCore Steel Agent - Runtime Service Contract Compliant
HTTP Protocol: /invocations (POST), /ping (GET)
Port: 8080, Host: 0.0.0.0, Platform: ARM64
"""

import json
import logging
import os
import time
from typing import Any, Dict, Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn

from langchain_aws import ChatBedrock
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AgentCore HTTP Protocol Models
class InvocationRequest(BaseModel):
    """Standard AgentCore invocation request."""
    prompt: str

class InvocationResponse(BaseModel):
    """Standard AgentCore invocation response."""
    response: str
    status: str = "success"

class PingResponse(BaseModel):
    """AgentCore ping response."""
    status: str  # "Healthy" or "HealthyBusy"
    time_of_last_update: int

# LangChain Tools
@tool
def calculate_steel_pricing(quantity: int, grade: str, base_price: float, margin_target: float):
    """Calculate steel pricing with profit optimization."""
    
    # Grade multipliers for premium steel
    grade_multipliers = {
        "TMT 500": 1.0,
        "TMT 550": 1.12,
        "TMT 600": 1.25,
        "HYSD": 0.95,
        "MS Round": 0.85
    }
    
    multiplier = grade_multipliers.get(grade, 1.0)
    unit_price = base_price * multiplier
    
    # Volume discounts for bulk orders
    if quantity >= 1000:
        volume_discount = 0.10
    elif quantity >= 500:
        volume_discount = 0.07
    elif quantity >= 200:
        volume_discount = 0.04
    elif quantity >= 100:
        volume_discount = 0.02
    else:
        volume_discount = 0.0
    
    discounted_price = unit_price * (1 - volume_discount)
    target_price = discounted_price * (1 + margin_target)
    total_cost = target_price * quantity
    
    # Inventory carrying cost
    inventory_cost = total_cost * 0.02  # 2% inventory carrying cost
    
    return {
        "unit_price": round(target_price, 2),
        "total_cost": round(total_cost, 2),
        "volume_discount": volume_discount * 100,
        "margin_achieved": margin_target * 100,
        "grade_premium": (multiplier - 1) * 100,
        "inventory_cost": round(inventory_cost, 2),
        "pricing_breakdown": {
            "base_price": base_price,
            "grade_multiplier": multiplier,
            "volume_discount_pct": volume_discount * 100,
            "target_margin_pct": margin_target * 100,
            "inventory_carrying_cost": round(inventory_cost, 2)
        }
    }

@tool
def optimize_steel_quote(customer_budget: float, quantity: int, grade: str, cycle: int):
    """Optimize steel quote based on negotiation cycle and market conditions."""
    
    # Premium steel base pricing
    base_prices = {
        "TMT 500": 650, 
        "TMT 550": 720, 
        "TMT 600": 800, 
        "HYSD": 620, 
        "MS Round": 580
    }
    base_price = base_prices.get(grade, 650)
    
    # Aggressive margin strategy for premium steel
    if cycle == 1:
        margin = 0.30  # 30% initial premium margin
    elif cycle == 2:
        margin = 0.25  # 25% second round
    elif cycle == 3:
        margin = 0.20  # 20% third round
    elif cycle == 4:
        margin = 0.15  # 15% fourth round
    else:
        margin = 0.12  # 12% final margin
    
    pricing = calculate_steel_pricing(quantity, grade, base_price, margin)
    
    # Market competitiveness analysis
    budget_per_ton = customer_budget / quantity if quantity > 0 else 0
    market_analysis = {
        "customer_budget_per_ton": round(budget_per_ton, 2),
        "our_price_per_ton": pricing["unit_price"],
        "premium_positioning": "justified" if pricing["unit_price"] <= budget_per_ton * 1.10 else "aggressive",
        "grade_advantage": f"Premium {grade} steel with superior strength"
    }
    
    # Strategic negotiation approach
    if pricing["total_cost"] > customer_budget * 1.05:
        if cycle < 3:
            strategy = "emphasize_quality_premium"
        else:
            strategy = "flexible_payment_terms"
    elif pricing["total_cost"] > customer_budget:
        strategy = "minor_concession_with_value_add"
    else:
        strategy = "maintain_premium_positioning"
    
    # Final recommendation logic
    if cycle >= 4:
        recommendation = "final_offer"
    elif pricing["total_cost"] <= customer_budget * 1.02:
        recommendation = "close_deal"
    else:
        recommendation = "continue_with_value_proposition"
    
    return {
        **pricing,
        "negotiation_cycle": cycle,
        "market_analysis": market_analysis,
        "strategy": strategy,
        "value_proposition": f"Premium {grade} steel with guaranteed quality and timely delivery",
        "final_recommendation": recommendation
    }

class AgentCoreSteelAgent:
    """AgentCore HTTP Protocol compliant Steel Agent."""
    
    def __init__(self):
        # Initialize Bedrock LLM
        self.model = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )
        
        self.tools = [calculate_steel_pricing, optimize_steel_quote]
        self.memory = MemorySaver()
        
        # Create LangGraph agent
        self.graph = create_react_agent(
            self.model,
            self.tools,
            checkpointer=self.memory
        )
        
        self.last_update = int(time.time())
        self.status = "Healthy"

    async def process_invocation(self, request: InvocationRequest) -> InvocationResponse:
        """Process invocation request (non-streaming)."""
        try:
            self.status = "HealthyBusy"
            self.last_update = int(time.time())
            
            # Process with LangGraph
            session_id = f"session_{int(time.time())}"
            config = {'configurable': {'thread_id': session_id}}
            inputs = {'messages': [('user', request.prompt)]}
            
            # Run the graph
            result = None
            for item in self.graph.stream(inputs, config, stream_mode='values'):
                result = item
            
            # Extract final response
            if result and 'messages' in result:
                last_message = result['messages'][-1]
                if isinstance(last_message, AIMessage):
                    response_text = last_message.content
                else:
                    response_text = str(last_message)
            else:
                response_text = "Premium steel analysis completed successfully"
            
            self.status = "Healthy"
            self.last_update = int(time.time())
            
            return InvocationResponse(
                response=response_text,
                status="success"
            )
            
        except Exception as e:
            logger.error(f"Invocation failed: {e}")
            self.status = "Healthy"
            self.last_update = int(time.time())
            
            return InvocationResponse(
                response=f"Error processing request: {str(e)}",
                status="error"
            )

    async def stream_invocation(self, request: InvocationRequest):
        """Process invocation request (streaming SSE)."""
        try:
            self.status = "HealthyBusy"
            self.last_update = int(time.time())
            
            # Initial event
            yield f"data: {json.dumps({'event': 'Analyzing premium steel pricing and positioning...'})}\n\n"
            
            # Process with streaming
            session_id = f"session_{int(time.time())}"
            config = {'configurable': {'thread_id': session_id}}
            inputs = {'messages': [('user', request.prompt)]}
            
            for item in self.graph.stream(inputs, config, stream_mode='values'):
                if 'messages' in item and item['messages']:
                    last_message = item['messages'][-1]
                    
                    if isinstance(last_message, AIMessage) and last_message.tool_calls:
                        yield f"data: {json.dumps({'event': 'Calculating premium steel pricing with margin optimization...'})}\n\n"
                    elif isinstance(last_message, ToolMessage):
                        yield f"data: {json.dumps({'event': 'Developing competitive strategy and value proposition...'})}\n\n"
                    elif isinstance(last_message, AIMessage) and last_message.content:
                        # Final response
                        yield f"data: {json.dumps({'event': last_message.content})}\n\n"
                        break
            
            self.status = "Healthy"
            self.last_update = int(time.time())
            
        except Exception as e:
            logger.error(f"Streaming invocation failed: {e}")
            self.status = "Healthy"
            self.last_update = int(time.time())
            yield f"data: {json.dumps({'event': f'Error: {str(e)}'})}\n\n"

    def get_ping_status(self) -> PingResponse:
        """Get agent health status."""
        return PingResponse(
            status=self.status,
            time_of_last_update=self.last_update
        )

# FastAPI Application - AgentCore HTTP Protocol
app = FastAPI(title="AgentCore Steel Agent", version="1.0.0")
agent = AgentCoreSteelAgent()

@app.post("/invocations")
async def invocations(request: Request):
    """Primary agent interaction endpoint - JSON input, JSON/SSE output."""
    try:
        body = await request.json()
        invocation_request = InvocationRequest(**body)
        
        # Check if client accepts streaming
        accept_header = request.headers.get("accept", "")
        if "text/event-stream" in accept_header:
            # Return streaming response
            return StreamingResponse(
                agent.stream_invocation(invocation_request),
                media_type="text/event-stream",
                headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
            )
        else:
            # Return JSON response
            response = await agent.process_invocation(invocation_request)
            return JSONResponse(content=response.model_dump())
            
    except Exception as e:
        logger.error(f"Invocations endpoint error: {e}")
        return JSONResponse(
            status_code=500,
            content={"response": f"Error: {str(e)}", "status": "error"}
        )

@app.get("/ping")
async def ping():
    """Health check endpoint - verifies agent is operational."""
    ping_response = agent.get_ping_status()
    return JSONResponse(content=ping_response.model_dump())

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))  # AgentCore standard port
    uvicorn.run(app, host="0.0.0.0", port=port)