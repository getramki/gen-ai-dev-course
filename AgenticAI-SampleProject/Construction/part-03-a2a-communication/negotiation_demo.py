"""A2A Inter-Agent Negotiation Demo with proper agent-to-agent communication."""

import asyncio
import logging
import json
from datetime import datetime
from uuid import uuid4
import httpx
import os

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    MessageSendParams,
    SendMessageRequest,
)

# Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"{log_dir}/negotiation_{timestamp}.log"
contract_file = f"{log_dir}/final_contract_{timestamp}.json"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ConversationLogger:
    """Logs all agent conversations and LLM reasoning."""
    
    def __init__(self, log_file):
        self.log_file = log_file
        self.conversations = []
    
    def log_interaction(self, from_agent, to_agent, message_type, content, reasoning=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "from_agent": from_agent,
            "to_agent": to_agent,
            "type": message_type,
            "content": content,
            "llm_reasoning": reasoning
        }
        self.conversations.append(entry)
        
        with open(self.log_file, 'a') as f:
            f.write(f"{json.dumps(entry, indent=2)}\n")
        
        logger.info(f"[{from_agent} → {to_agent}] {message_type}: {content[:100]}...")
        if reasoning:
            logger.info(f"[LLM REASONING] {reasoning[:100]}...")

class A2AProcurementOrchestrator:
    """Orchestrates A2A procurement negotiations between agents."""
    
    def __init__(self, conversation_logger):
        self.logger = conversation_logger
        self.agents = {}
        self.agent_cards = {}
        self.negotiation_state = {
            "cement": {"cycle": 0, "proposals": [], "final_price": None},
            "steel": {"cycle": 0, "proposals": [], "final_price": None}
        }
        self.max_cycles = 4
    
    async def connect_agent(self, name, url):
        """Connect to an A2A agent and get its card."""
        httpx_client = httpx.AsyncClient(timeout=120.0)
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=url)
        agent_card = await resolver.get_agent_card()
        client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)
        
        self.agents[name] = {
            'client': client,
            'card': agent_card,
            'url': url,
            'httpx_client': httpx_client
        }
        self.agent_cards[name] = agent_card
        
        self.logger.log_interaction("SYSTEM", name, "CONNECTED", f"Agent connected: {agent_card.name}")
        return True
    
    async def send_message(self, from_agent, to_agent, message, reasoning=None):
        """Send message between agents with streaming support."""
        if to_agent not in self.agents:
            raise ValueError(f"Agent {to_agent} not connected")
        
        self.logger.log_interaction(from_agent, to_agent, "REQUEST", message, reasoning)
        
        agent = self.agents[to_agent]
        
        # Use streaming for better response handling
        from a2a.types import SendStreamingMessageRequest
        streaming_request = SendStreamingMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(
                message={
                    'role': 'user',
                    'parts': [{'kind': 'text', 'text': message}],
                    'message_id': uuid4().hex,
                }
            )
        )
        
        stream_response = agent['client'].send_message_streaming(streaming_request)
        
        final_content = "No response"
        task_id = None
        
        async for chunk in stream_response:
            if hasattr(chunk, 'root') and chunk.root and hasattr(chunk.root, 'result'):
                result = chunk.root.result
                
                # Get task ID
                if hasattr(result, 'id'):
                    task_id = result.id
                elif hasattr(result, 'task_id'):
                    task_id = result.task_id
                
                # Handle TaskArtifactUpdateEvent (contains full response)
                if hasattr(result, 'artifact') and result.artifact:
                    if hasattr(result.artifact, 'parts') and result.artifact.parts:
                        for part in result.artifact.parts:
                            if hasattr(part.root, 'text'):
                                final_content = part.root.text
                                break
                
                # Handle TaskStatusUpdateEvent (status messages)
                elif hasattr(result, 'status') and result.status:
                    if hasattr(result.status, 'message') and result.status.message:
                        if hasattr(result.status.message, 'parts') and result.status.message.parts:
                            for part in result.status.message.parts:
                                if hasattr(part.root, 'text'):
                                    final_content = part.root.text
                
                # Check if final
                if hasattr(result, 'final') and result.final:
                    break
                elif 'completed' in str(chunk).lower() or 'input-required' in str(chunk).lower():
                    break
        
        self.logger.log_interaction(to_agent, from_agent, "RESPONSE", final_content)
        return final_content, task_id
    
    def analyze_agent_requirements(self, agent_name):
        """Analyze agent card to determine RFP format requirements."""
        card = self.agent_cards[agent_name]
        
        requirements = {
            "agent_name": card.name,
            "skills": [skill.name for skill in card.skills],
            "examples": []
        }
        
        for skill in card.skills:
            requirements["examples"].extend(skill.examples)
        
        reasoning = f"Analyzed {agent_name} agent card. Skills: {requirements['skills']}. Examples show they need detailed quantity, grade, delivery, and pricing information."
        
        self.logger.log_interaction("PURCHASE", "SYSTEM", "ANALYSIS", f"Agent requirements for {agent_name}", reasoning)
        
        return requirements
    
    def format_rfp_for_agent(self, agent_name, project_details):
        """Format RFP based on agent's requirements."""
        requirements = self.analyze_agent_requirements(agent_name)
        
        if agent_name == "cement":
            rfp = f"""
RFP - CEMENT SUPPLY CONTRACT

Based on your agent card analysis, you specialize in: {', '.join(requirements['skills'])}

PROJECT DETAILS:
- Project Name: {project_details['project_name']}
- Cement Quantity: {project_details['cement_quantity']} tons
- Grade Required: {project_details['cement_grade']}
- Delivery Location: {project_details['location']}
- Delivery Timeline: {project_details['delivery_timeline']}
- Budget Allocation: ${project_details['cement_budget']:,}
- Payment Terms: {project_details['payment_terms']}

REQUIREMENTS:
- Provide detailed quote with unit price breakdown
- Include delivery schedule and logistics
- Specify quality certifications included
- Indicate negotiation flexibility (if any)
- Confirm compliance with Grade {project_details['cement_grade']} specifications

Please respond with your proposal in the format you prefer based on your capabilities.
"""
        else:  # steel
            rfp = f"""
RFP - STEEL SUPPLY CONTRACT

Based on your agent card analysis, you specialize in: {', '.join(requirements['skills'])}

PROJECT DETAILS:
- Project Name: {project_details['project_name']}
- Steel Quantity: {project_details['steel_quantity']} tons
- Grade Required: {project_details['steel_grade']}
- Steel Types: {project_details['steel_types']}
- Delivery Location: {project_details['location']}
- Delivery Timeline: {project_details['delivery_timeline']}
- Budget Allocation: ${project_details['steel_budget']:,}
- Payment Terms: {project_details['payment_terms']}

REQUIREMENTS:
- Provide detailed quote with unit price breakdown
- Include material specifications and certifications
- Specify delivery schedule and logistics
- Indicate quality testing and compliance measures
- Confirm Grade {project_details['steel_grade']} availability

Please respond with your proposal in the format you prefer based on your capabilities.
"""
        
        reasoning = f"Formatted RFP for {agent_name} based on their agent card requirements. Included all necessary project details and specifications they need for accurate quoting."
        
        return rfp, reasoning
    
    async def negotiate_with_supplier(self, supplier, current_proposal, cycle, project_details):
        """Conduct negotiation cycle with supplier."""
        cycle_num = cycle + 1
        
        if supplier == "cement":
            budget = project_details['cement_budget']
            material = "cement"
        else:
            budget = project_details['steel_budget']
            material = "steel"
        
        negotiation_message = f"""
NEGOTIATION CYCLE {cycle_num}/{self.max_cycles} - {material.upper()} SUPPLIER

CURRENT SITUATION:
- Your previous response: {current_proposal[:200]}...
- Our budget allocation: ${budget:,}
- Negotiation cycle: {cycle_num} of {self.max_cycles}

NEGOTIATION REQUEST:
"""
        
        if cycle_num == 1:
            negotiation_message += f"""
- We need a competitive quote for this {material} supply
- Can you provide volume discount for this quantity?
- Confirm your best pricing and delivery terms
- What flexibility do you have on payment terms?
"""
        elif cycle_num == 2:
            negotiation_message += f"""
- Can you improve on your initial quote by 3-5%?
- We're comparing multiple suppliers
- Faster delivery would be valued
- Any additional services you can include?
"""
        elif cycle_num == 3:
            negotiation_message += f"""
- This is a significant order - can you do better on pricing?
- We need your final best offer
- Confirm all terms are firm and binding
- Any last improvements you can make?
"""
        else:  # Final cycle
            negotiation_message += f"""
- FINAL NEGOTIATION ROUND
- We need your absolute best and final offer
- This is our last opportunity to reach agreement
- Please confirm if you can meet our requirements within budget
- Contract award decision will be made after this round
"""
        
        reasoning = f"Negotiation cycle {cycle_num} with {supplier}. Strategy: {'Initial competitive request' if cycle_num == 1 else 'Incremental pressure for better terms' if cycle_num < 4 else 'Final ultimatum for best offer'}. Budget constraint: ${budget:,}."
        
        response, task_id = await self.send_message("PURCHASE", supplier, negotiation_message, reasoning)
        
        # Update negotiation state
        self.negotiation_state[supplier]["cycle"] = cycle_num
        self.negotiation_state[supplier]["proposals"].append({
            "cycle": cycle_num,
            "response": response,
            "task_id": task_id
        })
        
        return response, task_id
    
    async def finalize_contract(self, supplier, final_terms):
        """Finalize contract with supplier."""
        contract_message = f"""
CONTRACT FINALIZATION - {supplier.upper()} SUPPLIER

FINAL AGREED TERMS:
{final_terms}

NEXT STEPS:
- Please confirm acceptance of these final terms
- Indicate contract signing readiness
- Provide any final documentation requirements
- Confirm project start timeline

This represents our final negotiated agreement. Please confirm acceptance to proceed with contract execution.
"""
        
        reasoning = f"Finalizing contract with {supplier} supplier. All negotiation cycles completed. Moving to contract acceptance phase."
        
        response, task_id = await self.send_message("PURCHASE", supplier, contract_message, reasoning)
        return response, task_id
    
    def save_final_contract(self, project_details, cement_terms, steel_terms):
        """Save final contract details to file."""
        contract = {
            "contract_id": f"CONTRACT_{timestamp}",
            "timestamp": datetime.now().isoformat(),
            "project_details": project_details,
            "cement_contract": {
                "supplier": "Cement Sales Agent",
                "negotiation_cycles": self.negotiation_state["cement"]["cycle"],
                "final_terms": cement_terms,
                "proposals_history": self.negotiation_state["cement"]["proposals"]
            },
            "steel_contract": {
                "supplier": "Steel Sales Agent", 
                "negotiation_cycles": self.negotiation_state["steel"]["cycle"],
                "final_terms": steel_terms,
                "proposals_history": self.negotiation_state["steel"]["proposals"]
            },
            "total_budget": project_details['cement_budget'] + project_details['steel_budget'],
            "contract_status": "NEGOTIATED"
        }
        
        with open(contract_file, 'w') as f:
            json.dump(contract, f, indent=2)
        
        self.logger.log_interaction("SYSTEM", "CONTRACT", "SAVED", f"Final contract saved to {contract_file}")
        return contract
    
    async def close_all(self):
        """Close all agent connections."""
        for name, agent in self.agents.items():
            await agent['httpx_client'].aclose()

async def run_procurement_negotiation():
    """Run complete procurement negotiation flow."""
    print("A2A Inter-Agent Procurement Negotiation")
    print("=" * 60)
    
    # Setup logging
    conv_log_file = f"{log_dir}/conversation_{timestamp}.json"
    conversation_logger = ConversationLogger(conv_log_file)
    
    # Initialize orchestrator
    orchestrator = A2AProcurementOrchestrator(conversation_logger)
    
    # Connect to agents
    agents_config = [
        ("purchase", "http://localhost:10001"),
        ("cement", "http://localhost:10002"),
        ("steel", "http://localhost:10003")
    ]
    
    print("\nConnecting to agents...")
    for name, url in agents_config:
        try:
            await orchestrator.connect_agent(name, url)
            print(f"✅ Connected to {name} agent")
        except Exception as e:
            print(f"❌ Failed to connect to {name} agent: {e}")
            return
    
    # Project details from client
    project_details = {
        "project_name": "Downtown Construction Complex",
        "cement_quantity": 1000,
        "cement_grade": "42.5 OPC",
        "cement_budget": 55000,
        "steel_quantity": 100,
        "steel_grade": "Grade A",
        "steel_types": "Rebar and structural steel",
        "steel_budget": 75000,
        "location": "Downtown construction site",
        "delivery_timeline": "Within 14 days",
        "payment_terms": "30 days net"
    }
    
    try:
        print("\n" + "="*80)
        print("PHASE 1: CLIENT REQUEST TO PURCHASE AGENT")
        print("="*80)
        
        # Step 1: Client sends request to purchase agent
        client_request = f"""
PROCUREMENT REQUEST - {project_details['project_name']}

CEMENT REQUIREMENTS:
- Quantity: {project_details['cement_quantity']} tons
- Grade: {project_details['cement_grade']}
- Budget: ${project_details['cement_budget']:,}

STEEL REQUIREMENTS:
- Quantity: {project_details['steel_quantity']} tons
- Grade: {project_details['steel_grade']}
- Types: {project_details['steel_types']}
- Budget: ${project_details['steel_budget']:,}

GENERAL TERMS:
- Delivery: {project_details['delivery_timeline']}
- Location: {project_details['location']}
- Payment: {project_details['payment_terms']}
- Total Budget: ${project_details['cement_budget'] + project_details['steel_budget']:,}

Please coordinate with cement and steel suppliers to get best proposals and negotiate favorable contracts.
"""
        
        reasoning = "Client initiating procurement process. Purchase agent needs to analyze requirements, connect with suppliers, and manage negotiation process."
        
        purchase_response, _ = await orchestrator.send_message("CLIENT", "purchase", client_request, reasoning)
        
        print("\n" + "="*80)
        print("PHASE 2: PURCHASE AGENT ANALYZES SUPPLIER REQUIREMENTS")
        print("="*80)
        
        # Step 2: Purchase agent analyzes supplier agent cards
        cement_requirements = orchestrator.analyze_agent_requirements("cement")
        steel_requirements = orchestrator.analyze_agent_requirements("steel")
        
        print("\n" + "="*80)
        print("PHASE 3: PURCHASE AGENT SENDS RFPs TO SUPPLIERS")
        print("="*80)
        
        # Step 3: Send formatted RFPs to suppliers
        cement_rfp, cement_reasoning = orchestrator.format_rfp_for_agent("cement", project_details)
        steel_rfp, steel_reasoning = orchestrator.format_rfp_for_agent("steel", project_details)
        
        cement_initial, _ = await orchestrator.send_message("PURCHASE", "cement", cement_rfp, cement_reasoning)
        steel_initial, _ = await orchestrator.send_message("PURCHASE", "steel", steel_rfp, steel_reasoning)
        
        print("\n" + "="*80)
        print("PHASE 4: NEGOTIATION CYCLES (4-5 ROUNDS)")
        print("="*80)
        
        # Step 4: Conduct negotiation cycles
        for cycle in range(orchestrator.max_cycles):
            print(f"\n--- NEGOTIATION CYCLE {cycle + 1} ---")
            
            # Negotiate with cement supplier
            cement_response, _ = await orchestrator.negotiate_with_supplier("cement", cement_initial, cycle, project_details)
            
            # Negotiate with steel supplier  
            steel_response, _ = await orchestrator.negotiate_with_supplier("steel", steel_initial, cycle, project_details)
            
            # Brief pause between cycles
            await asyncio.sleep(1)
        
        print("\n" + "="*80)
        print("PHASE 5: CONTRACT FINALIZATION")
        print("="*80)
        
        # Step 5: Finalize contracts
        cement_final_terms = f"""
- Quantity: {project_details['cement_quantity']} tons {project_details['cement_grade']}
- Budget: ${project_details['cement_budget']:,}
- Delivery: {project_details['delivery_timeline']}
- Payment: {project_details['payment_terms']}
- Negotiation cycles completed: {orchestrator.negotiation_state['cement']['cycle']}
"""
        
        steel_final_terms = f"""
- Quantity: {project_details['steel_quantity']} tons {project_details['steel_grade']}
- Types: {project_details['steel_types']}
- Budget: ${project_details['steel_budget']:,}
- Delivery: {project_details['delivery_timeline']}
- Payment: {project_details['payment_terms']}
- Negotiation cycles completed: {orchestrator.negotiation_state['steel']['cycle']}
"""
        
        cement_final, _ = await orchestrator.finalize_contract("cement", cement_final_terms)
        steel_final, _ = await orchestrator.finalize_contract("steel", steel_final_terms)
        
        # Step 6: Save final contract
        final_contract = orchestrator.save_final_contract(project_details, cement_final_terms, steel_final_terms)
        
        print("\n" + "="*80)
        print("NEGOTIATION COMPLETE")
        print("="*80)
        print(f"✅ Cement negotiations: {orchestrator.negotiation_state['cement']['cycle']} cycles")
        print(f"✅ Steel negotiations: {orchestrator.negotiation_state['steel']['cycle']} cycles")
        print(f"✅ Final contract saved: {contract_file}")
        print(f"✅ Conversation log: {conv_log_file}")
        print(f"✅ Detailed logs: {log_file}")
        
    except Exception as e:
        logger.error(f"Error during negotiation: {e}")
        print(f"❌ Negotiation failed: {e}")
    finally:
        await orchestrator.close_all()

if __name__ == "__main__":
    asyncio.run(run_procurement_negotiation())