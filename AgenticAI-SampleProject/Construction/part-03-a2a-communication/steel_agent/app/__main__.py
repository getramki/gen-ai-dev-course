"""Steel Sales Agent A2A Server."""

import logging
import os
import sys

import click
import httpx
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import (
    BasePushNotificationSender,
    InMemoryPushNotificationConfigStore,
    InMemoryTaskStore,
)
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from dotenv import load_dotenv

from .agent import SteelAgent
from .agent_executor import SteelAgentExecutor

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=10003)
def main(host, port):
    """Starts the Steel Sales Agent A2A server."""
    try:
        capabilities = AgentCapabilities(streaming=True, push_notifications=True)
        
        # Define steel sales skills
        pricing_skill = AgentSkill(
            id='steel_pricing',
            name='Premium Steel Pricing & Quotes',
            description='Generates competitive premium steel quotes with profit optimization',
            tags=['steel', 'premium', 'pricing', 'quotes', 'profit optimization'],
            examples=[
                'Quote 100 tons of premium steel for construction project',
                'Calculate pricing for Grade A steel delivery',
                'Provide competitive steel quote with quality specifications'
            ],
        )
        
        negotiation_skill = AgentSkill(
            id='steel_negotiation',
            name='Steel Sales Negotiation',
            description='Negotiates premium steel sales while maintaining higher profit margins',
            tags=['negotiation', 'premium steel', 'margins', 'contracts'],
            examples=[
                'Evaluate counter-offer on premium steel pricing',
                'Negotiate better terms while maintaining 30% margin',
                'Finalize premium steel supply contract'
            ],
        )
        
        agent_card = AgentCard(
            name='Steel Sales Agent',
            description='Specialized agent for premium steel sales with profit maximization and quality-focused pricing strategies',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            default_input_modes=SteelAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=SteelAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[pricing_skill, negotiation_skill],
        )
        
        # Setup A2A server components
        httpx_client = httpx.AsyncClient()
        push_config_store = InMemoryPushNotificationConfigStore()
        push_sender = BasePushNotificationSender(
            httpx_client=httpx_client,
            config_store=push_config_store
        )
        
        request_handler = DefaultRequestHandler(
            agent_executor=SteelAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_config_store=push_config_store,
            push_sender=push_sender
        )
        
        # Create A2A server
        app = A2AStarletteApplication(
            agent_card=agent_card, 
            http_handler=request_handler
        )
        
        # Build the server and add agent card endpoint
        server = app.build()
        
        # Add GET endpoint for agent card
        @server.route('/', methods=['GET'])
        async def get_agent_card(request):
            from starlette.responses import JSONResponse
            return JSONResponse(agent_card.model_dump())
        
        logger.info(f"Starting Steel Sales Agent A2A server on {host}:{port}")
        logger.info("Skills: Premium Steel Pricing, Sales Negotiation")
        logger.info("Capabilities: Profit optimization, Quality focus, Premium margins")
        logger.info("Agent card available at: GET /")
        
        uvicorn.run(server, host=host, port=port)
        
    except Exception as e:
        logger.error(f'Server startup error: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()