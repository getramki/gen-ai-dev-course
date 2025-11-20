#!/usr/bin/env python3
"""
EKS-based Negotiation Demo for Part 6-A
Demonstrates A2A communication across EKS-deployed agents via ALB
"""

import asyncio
import json
import logging
from datetime import datetime
from uuid import uuid4
import aiohttp
from typing import Dict, Any
import os

# Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"{log_dir}/eks_negotiation_{timestamp}.log"
contract_file = f"{log_dir}/eks_final_contract_{timestamp}.json"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EKSProcurementOrchestrator:
    """Orchestrates procurement negotiations with EKS-deployed agents via ALB."""
    
    def __init__(self):
        self.alb_base_url = "http://k8s-constructionagent-e21a474cac-638980136.us-east-1.elb.amazonaws.com"
        self.agent_cards = {}
        self.negotiation_state = {
            "cement": {"cycle": 0, "proposals": [], "final_price": None},
            "steel": {"cycle": 0, "proposals": [], "final_price": None}
        }
        self.max_cycles = 4
    
    async def connect_agents(self):
        """Connect to agents and get their cards like local version."""
        services = ["purchase", "cement", "steel"]
        
        for service in services:
            try:
                card = await self.get_agent_card(service)
                self.agent_cards[service] = card
                logger.info(f"Connected to {service}: {card.get('name', 'Unknown')}")
                print(f"✅ Connected to {service} agent: {card.get('name', 'Unknown')}")
            except Exception as e:
                logger.error(f"Failed to connect to {service}: {e}")
                print(f"❌ Failed to connect to {service}: {e}")
                raise
    
    async def get_agent_card(self, service: str) -> Dict:
        """Get agent card from EKS agent."""
        url = f"{self.alb_base_url}/{service}/.well-known/agent-card.json"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    text = await response.text()
                    raise Exception(f"Failed to get agent card: {response.status}, {text}")
                return await response.json()
    
    async def send_message(self, service: str, message: str) -> str:
        """Send message to EKS agent using JSONRPC like local version."""
        url = f"{self.alb_base_url}/{service}/"
        
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid4()),
            "method": "send_message",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"kind": "text", "text": message}],
                    "message_id": uuid4().hex
                }
            }
        }
        
        logger.info(f"Sending to {service}: {message[:100]}...")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    text = await response.text()
                    raise Exception(f"{response.status}, message='{text}', url='{url}'")
                
                result = await response.json()
                
                # Handle JSONRPC response
                if 'result' in result:
                    return str(result['result'])
                elif 'error' in result:
                    raise Exception(f"JSONRPC error: {result['error']}")
                else:
                    return str(result)
    
    def format_rfp_for_agent(self, agent_name: str, project_details: Dict) -> str:
        """Format RFP based on agent type."""
        if agent_name == "cement":
            return f"""
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

Please respond with your proposal.
"""
        else:  # steel
            return f"""
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

Please respond with your proposal.
"""
    
    async def negotiate_with_supplier(self, supplier: str, cycle: int, project_details: Dict) -> str:
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
        
        response = await self.send_message(supplier, negotiation_message)
        
        # Update negotiation state
        self.negotiation_state[supplier]["cycle"] = cycle_num
        self.negotiation_state[supplier]["proposals"].append({
            "cycle": cycle_num,
            "response": response
        })
        
        return response
    
    async def finalize_contract(self, supplier: str, final_terms: str) -> str:
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
        
        response = await self.send_message(supplier, contract_message)
        return response
    
    def save_final_contract(self, project_details: Dict, cement_terms: str, steel_terms: str) -> Dict:
        """Save final contract details to file."""
        contract = {
            "contract_id": f"EKS_CONTRACT_{timestamp}",
            "timestamp": datetime.now().isoformat(),
            "project_details": project_details,
            "cement_contract": {
                "supplier": "EKS Cement Agent",
                "negotiation_cycles": self.negotiation_state["cement"]["cycle"],
                "final_terms": cement_terms,
                "proposals_history": self.negotiation_state["cement"]["proposals"]
            },
            "steel_contract": {
                "supplier": "EKS Steel Agent", 
                "negotiation_cycles": self.negotiation_state["steel"]["cycle"],
                "final_terms": steel_terms,
                "proposals_history": self.negotiation_state["steel"]["proposals"]
            },
            "total_budget": project_details['cement_budget'] + project_details['steel_budget'],
            "contract_status": "NEGOTIATED",
            "deployment": "EKS_ALB"
        }
        
        with open(contract_file, 'w') as f:
            json.dump(contract, f, indent=2)
        
        logger.info(f"Final contract saved to {contract_file}")
        return contract

async def run_eks_procurement_negotiation():
    """Run complete EKS procurement negotiation flow."""
    print("EKS A2A Inter-Agent Procurement Negotiation")
    print("=" * 60)
    
    # Initialize orchestrator
    orchestrator = EKSProcurementOrchestrator()
    
    print(f"\n🔗 Using ALB: {orchestrator.alb_base_url}")
    print("📍 Path routing: /purchase, /cement, /steel")
    
    # Connect to agents first
    print("\n🔌 Connecting to EKS agents...")
    await orchestrator.connect_agents()
    
    # Project details
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
        
        purchase_response = await orchestrator.send_message("purchase", client_request)
        print(f"✅ Purchase agent response received")
        
        print("\n" + "="*80)
        print("PHASE 2: PURCHASE AGENT SENDS RFPs TO SUPPLIERS")
        print("="*80)
        
        # Step 2: Send RFPs to suppliers
        cement_rfp = orchestrator.format_rfp_for_agent("cement", project_details)
        steel_rfp = orchestrator.format_rfp_for_agent("steel", project_details)
        
        cement_initial = await orchestrator.send_message("cement", cement_rfp)
        steel_initial = await orchestrator.send_message("steel", steel_rfp)
        
        print(f"✅ Cement RFP response received")
        print(f"✅ Steel RFP response received")
        
        print("\n" + "="*80)
        print("PHASE 3: NEGOTIATION CYCLES (4 ROUNDS)")
        print("="*80)
        
        # Step 3: Conduct negotiation cycles
        for cycle in range(orchestrator.max_cycles):
            print(f"\n--- NEGOTIATION CYCLE {cycle + 1} ---")
            
            # Negotiate with cement supplier
            cement_response = await orchestrator.negotiate_with_supplier("cement", cycle, project_details)
            print(f"✅ Cement cycle {cycle + 1} complete")
            
            # Negotiate with steel supplier  
            steel_response = await orchestrator.negotiate_with_supplier("steel", cycle, project_details)
            print(f"✅ Steel cycle {cycle + 1} complete")
            
            # Brief pause between cycles
            await asyncio.sleep(2)
        
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
        
        cement_final = await orchestrator.finalize_contract("cement", cement_final_terms)
        steel_final = await orchestrator.finalize_contract("steel", steel_final_terms)
        
        # Step 5: Save final contract
        final_contract = orchestrator.save_final_contract(project_details, cement_final_terms, steel_final_terms)
        
        print("\n" + "="*80)
        print("EKS NEGOTIATION COMPLETE")
        print("="*80)
        print(f"✅ Cement negotiations: {orchestrator.negotiation_state['cement']['cycle']} cycles")
        print(f"✅ Steel negotiations: {orchestrator.negotiation_state['steel']['cycle']} cycles")
        print(f"✅ Final contract saved: {contract_file}")
        print(f"✅ Detailed logs: {log_file}")
        print(f"💰 Total Budget: ${project_details['cement_budget'] + project_details['steel_budget']:,}")
        
    except Exception as e:
        logger.error(f"Error during EKS negotiation: {e}")
        print(f"❌ EKS Negotiation failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_eks_procurement_negotiation())