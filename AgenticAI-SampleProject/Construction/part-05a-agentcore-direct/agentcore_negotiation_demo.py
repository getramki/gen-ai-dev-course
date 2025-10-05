"""AgentCore Inter-Agent Negotiation Demo for hosted agents."""

import asyncio
import logging
import json
import boto3
import os
from datetime import datetime
from uuid import uuid4

# Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"{log_dir}/agentcore_negotiation_{timestamp}.log"
contract_file = f"{log_dir}/agentcore_contract_{timestamp}.json"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AgentCoreConversationLogger:
    """Logs all AgentCore agent conversations."""
    
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
            "reasoning": reasoning
        }
        self.conversations.append(entry)
        
        with open(self.log_file, 'a') as f:
            f.write(f"{json.dumps(entry, indent=2)}\n")
        
        logger.info(f"[{from_agent} → {to_agent}] {message_type}: {content[:100]}...")
        if reasoning:
            logger.info(f"[REASONING] {reasoning[:100]}...")

class AgentCoreProcurementOrchestrator:
    """Orchestrates procurement negotiations with AgentCore hosted agents."""
    
    def __init__(self, conversation_logger):
        self.logger = conversation_logger
        self.agents = {}
        self.negotiation_state = {
            "cement": {"cycle": 0, "proposals": [], "final_price": None},
            "steel": {"cycle": 0, "proposals": [], "final_price": None}
        }
        self.max_cycles = 4
        self.bedrock_client = boto3.client('bedrock-agentcore', region_name='us-east-1')
    
    def register_agent(self, name, agent_runtime_arn):
        """Register AgentCore agent ARN."""
        self.agents[name] = {
            'arn': agent_runtime_arn,
            'name': name
        }
        self.logger.log_interaction("SYSTEM", name, "REGISTERED", f"AgentCore agent registered: {agent_runtime_arn}")
        return True
    
    def send_message(self, from_agent, to_agent, message, reasoning=None):
        """Send message to AgentCore agent via bedrock-agentcore client."""
        if to_agent not in self.agents:
            raise ValueError(f"Agent {to_agent} not registered")
        
        self.logger.log_interaction(from_agent, to_agent, "REQUEST", message, reasoning)
        
        agent = self.agents[to_agent]
        
        try:
            # Prepare the payload
            payload = json.dumps({
                "input": {"prompt": message}
            })
            session_id = f"session_{uuid4().hex[:33]}"  # Must be 33+ chars
            
            # Invoke the agent
            response = self.bedrock_client.invoke_agent_runtime(
                agentRuntimeArn=agent['arn'],
                runtimeSessionId=session_id,
                payload=payload,
                qualifier="DEFAULT"
            )
            
            # Process response
            response_body = response['response'].read()
            response_data = json.loads(response_body)
            response_text = str(response_data)
            
            self.logger.log_interaction(to_agent, from_agent, "RESPONSE", response_text)
            return response_text
            
        except Exception as e:
            error_msg = f"Error communicating with {to_agent}: {str(e)}"
            self.logger.log_interaction(to_agent, from_agent, "ERROR", error_msg)
            return error_msg
    
    def format_rfp_for_agent(self, agent_name, project_details):
        """Format RFP for AgentCore agent."""
        
        if agent_name == "cement":
            rfp = f"""
RFP - CEMENT SUPPLY CONTRACT

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

Please respond with your proposal including pricing, delivery terms, and any value-added services.
"""
        else:  # steel
            rfp = f"""
RFP - STEEL SUPPLY CONTRACT

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

Please respond with your proposal including pricing, delivery terms, and quality assurances.
"""
        
        reasoning = f"Formatted RFP for {agent_name} AgentCore agent with all necessary project details and specifications."
        
        return rfp, reasoning
    
    async def negotiate_with_supplier(self, supplier, current_proposal, cycle, project_details):
        """Conduct negotiation cycle with AgentCore supplier."""
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
        
        response = self.send_message("PURCHASE", supplier, negotiation_message, reasoning)
        
        # Update negotiation state
        self.negotiation_state[supplier]["cycle"] = cycle_num
        self.negotiation_state[supplier]["proposals"].append({
            "cycle": cycle_num,
            "response": response
        })
        
        return response
    
    def finalize_contract(self, supplier, final_terms):
        """Finalize contract with AgentCore supplier."""
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
        
        response = self.send_message("PURCHASE", supplier, contract_message, reasoning)
        return response
    
    def save_final_contract(self, project_details, cement_terms, steel_terms):
        """Save final contract details to file."""
        contract = {
            "contract_id": f"AGENTCORE_CONTRACT_{timestamp}",
            "timestamp": datetime.now().isoformat(),
            "project_details": project_details,
            "cement_contract": {
                "supplier": "AgentCore Cement Agent",
                "negotiation_cycles": self.negotiation_state["cement"]["cycle"],
                "final_terms": cement_terms,
                "proposals_history": self.negotiation_state["cement"]["proposals"]
            },
            "steel_contract": {
                "supplier": "AgentCore Steel Agent", 
                "negotiation_cycles": self.negotiation_state["steel"]["cycle"],
                "final_terms": steel_terms,
                "proposals_history": self.negotiation_state["steel"]["proposals"]
            },
            "total_budget": project_details['cement_budget'] + project_details['steel_budget'],
            "contract_status": "NEGOTIATED_AGENTCORE"
        }
        
        with open(contract_file, 'w') as f:
            json.dump(contract, f, indent=2)
        
        self.logger.log_interaction("SYSTEM", "CONTRACT", "SAVED", f"Final AgentCore contract saved to {contract_file}")
        return contract
    
    def close(self):
        """Close bedrock client (no action needed)."""
        pass

def run_agentcore_procurement_negotiation():
    """Run complete procurement negotiation with AgentCore agents."""
    print("AgentCore Inter-Agent Procurement Negotiation")
    print("=" * 60)
    
    # Setup logging
    conv_log_file = f"{log_dir}/agentcore_conversation_{timestamp}.json"
    conversation_logger = AgentCoreConversationLogger(conv_log_file)
    
    # Initialize orchestrator
    orchestrator = AgentCoreProcurementOrchestrator(conversation_logger)
    
    # Register AgentCore agents (replace with actual AgentCore ARNs)
    agents_config = [
        ("purchase", "arn:aws:bedrock-agentcore:us-east-1:910673207244:runtime/construction_purchase_agent-Wk2N3tEqL3"),
        ("cement", "arn:aws:bedrock-agentcore:us-east-1:910673207244:runtime/construction_cement_agent-symHaUHu6T"),
        ("steel", "arn:aws:bedrock-agentcore:us-east-1:910673207244:runtime/construction_steel_agent-nkXz898tUJ")
    ]
    
    print("\nRegistering AgentCore agents...")
    for name, arn in agents_config:
        orchestrator.register_agent(name, arn)
        print(f"✅ Registered {name} agent: {arn}")
    
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
        
        reasoning = "Client initiating procurement process with AgentCore purchase agent. Agent needs to analyze requirements and coordinate with suppliers."
        
        purchase_response = orchestrator.send_message("CLIENT", "purchase", client_request, reasoning)
        
        print("\n" + "="*80)
        print("PHASE 2: PURCHASE AGENT SENDS RFPs TO SUPPLIERS")
        print("="*80)
        
        # Step 2: Send formatted RFPs to suppliers
        cement_rfp, cement_reasoning = orchestrator.format_rfp_for_agent("cement", project_details)
        steel_rfp, steel_reasoning = orchestrator.format_rfp_for_agent("steel", project_details)
        
        cement_initial = orchestrator.send_message("PURCHASE", "cement", cement_rfp, cement_reasoning)
        steel_initial = orchestrator.send_message("PURCHASE", "steel", steel_rfp, steel_reasoning)
        
        print("\n" + "="*80)
        print("PHASE 3: NEGOTIATION CYCLES (4 ROUNDS)")
        print("="*80)
        
        # Step 3: Conduct negotiation cycles
        for cycle in range(orchestrator.max_cycles):
            print(f"\n--- NEGOTIATION CYCLE {cycle + 1} ---")
            
            # Negotiate with cement supplier
            cement_response = orchestrator.negotiate_with_supplier("cement", cement_initial, cycle, project_details)
            
            # Negotiate with steel supplier  
            steel_response = orchestrator.negotiate_with_supplier("steel", steel_initial, cycle, project_details)
            
            # Brief pause between cycles
            import time
            time.sleep(2)
        
        print("\n" + "="*80)
        print("PHASE 4: CONTRACT FINALIZATION")
        print("="*80)
        
        # Step 4: Finalize contracts
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
        
        cement_final = orchestrator.finalize_contract("cement", cement_final_terms)
        steel_final = orchestrator.finalize_contract("steel", steel_final_terms)
        
        # Step 5: Save final contract
        final_contract = orchestrator.save_final_contract(project_details, cement_final_terms, steel_final_terms)
        
        print("\n" + "="*80)
        print("AGENTCORE NEGOTIATION COMPLETE")
        print("="*80)
        print(f"✅ Cement negotiations: {orchestrator.negotiation_state['cement']['cycle']} cycles")
        print(f"✅ Steel negotiations: {orchestrator.negotiation_state['steel']['cycle']} cycles")
        print(f"✅ Final contract saved: {contract_file}")
        print(f"✅ Conversation log: {conv_log_file}")
        print(f"✅ Detailed logs: {log_file}")
        
    except Exception as e:
        logger.error(f"Error during AgentCore negotiation: {e}")
        print(f"❌ Negotiation failed: {e}")
    finally:
        orchestrator.close()

if __name__ == "__main__":
    print("AgentCore Negotiation Demo")
    print("Running with configured AgentCore ARNs...")
    print()
    
    run_agentcore_procurement_negotiation()