"""Purchase Agent A2A Server."""

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

from .agent import PurchaseAgent
from .agent_executor import PurchaseAgentExecutor

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MissingConfigError(Exception):
    """Exception for missing configuration."""

@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=10001)
def main(host, port):
    """Starts the Purchase Agent A2A server."""
    try:
        # Validate AWS credentials for Bedrock
        if not os.getenv('AWS_ACCESS_KEY_ID') and not os.getenv('AWS_PROFILE'):
            logger.warning('AWS credentials not found in environment. Ensure AWS CLI is configured.')
            
        capabilities = AgentCapabilities(streaming=True, push_notifications=True)
        
        # Define procurement skills
        procurement_skill = AgentSkill(
            id='construction_procurement',
            name='Construction Material Procurement',
            description='Optimizes procurement of cement and steel for construction projects',
            tags=['procurement', 'construction', 'cost optimization', 'materials'],
            examples=[
                'I need 1000 tons of cement and 100 tons of steel within $130k budget',
                'Evaluate this supplier quote for cement delivery',
                'What is the best procurement strategy for this project?'
            ],
        )
        
        negotiation_skill = AgentSkill(
            id='supplier_negotiation',
            name='Supplier Negotiation',
            description='Negotiates with suppliers to achieve optimal pricing within budget constraints',
            tags=['negotiation', 'suppliers', 'pricing', 'contracts'],
            examples=[
                'Negotiate better terms with cement supplier',
                'Counter-offer on steel pricing quote',
                'Finalize contract with selected supplier'
            ],
        )
        
        agent_card = AgentCard(
            name='Construction Purchase Agent',
            description='Specialized agent for construction material procurement and supplier negotiation with cost optimization',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            default_input_modes=PurchaseAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=PurchaseAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[procurement_skill, negotiation_skill],
        )
        
        # Setup A2A server components
        httpx_client = httpx.AsyncClient()
        push_config_store = InMemoryPushNotificationConfigStore()
        push_sender = BasePushNotificationSender(
            httpx_client=httpx_client,
            config_store=push_config_store
        )
        
        request_handler = DefaultRequestHandler(
            agent_executor=PurchaseAgentExecutor(),
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
        
        logger.info(f"Starting Purchase Agent A2A server on {host}:{port}")
        logger.info("Skills: Construction Procurement, Supplier Negotiation")
        logger.info("Capabilities: Cost optimization, Budget management, Contract negotiation")
        logger.info("Agent card available at: GET /")
        
        uvicorn.run(server, host=host, port=port)
        
    except MissingConfigError as e:
        logger.error(f'Configuration Error: {e}')
        sys.exit(1)
    except Exception as e:
        logger.error(f'Server startup error: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()