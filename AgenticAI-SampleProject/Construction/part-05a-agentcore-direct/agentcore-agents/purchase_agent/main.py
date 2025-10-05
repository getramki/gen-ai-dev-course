#!/usr/bin/env python3
"""
AgentCore Purchase Agent - Runtime Service Contract Compliant
HTTP Protocol: /invocations (POST), /ping (GET)
Port: 8080, Host: 0.0.0.0, Platform: ARM64
"""

import json
import logging
import os
import time
from datetime import datetime
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
def calculate_procurement_cost(cement_tons: int, cement_price: float, steel_tons: int, steel_price: float):
    """Calculate total procurement cost for construction materials."""
    cement_cost = cement_tons * cement_price
    steel_cost = steel_tons * steel_price
    total_cost = cement_cost + steel_cost
    
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
    """Evaluate supplier quote for procurement decision."""
    budget_utilization = (quoted_price / budget) * 100
    savings = budget - quoted_price
    savings_pct = (savings / budget) * 100
    
    if cycle >= 5:
        recommendation = "accept"
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

class AgentCorePurchaseAgent:
    """AgentCore HTTP Protocol compliant Purchase Agent."""
    
    def __init__(self):
        # Initialize Bedrock LLM
        self.model = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )
        
        self.tools = [calculate_procurement_cost, evaluate_supplier_quote]
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
                response_text = "Procurement analysis completed successfully"
            
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
            yield f"data: {json.dumps({'event': 'Starting procurement analysis...'})}\n\n"
            
            # Process with streaming
            session_id = f"session_{int(time.time())}"
            config = {'configurable': {'thread_id': session_id}}
            inputs = {'messages': [('user', request.prompt)]}
            
            step_count = 0
            for item in self.graph.stream(inputs, config, stream_mode='values'):
                step_count += 1
                
                if 'messages' in item and item['messages']:
                    last_message = item['messages'][-1]
                    
                    if isinstance(last_message, AIMessage) and last_message.tool_calls:
                        yield f"data: {json.dumps({'event': 'Analyzing costs and evaluating suppliers...'})}\n\n"
                    elif isinstance(last_message, ToolMessage):
                        yield f"data: {json.dumps({'event': 'Processing supplier data and optimization...'})}\n\n"
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
app = FastAPI(title="AgentCore Purchase Agent", version="1.0.0")
agent = AgentCorePurchaseAgent()

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