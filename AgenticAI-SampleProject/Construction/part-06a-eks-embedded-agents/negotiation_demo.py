#!/usr/bin/env python3
"""
EKS-based Negotiation Demo for Part 6-A
Demonstrates A2A communication across EKS-deployed agents via subdomains
"""

import asyncio
import json
import time
from datetime import datetime
import aiohttp
from typing import Dict, Any

class EKSNegotiationDemo:
    def __init__(self):
        # ALB endpoints will be discovered from kubectl
        self.endpoints = self._get_alb_endpoints()
    
    def _get_alb_endpoints(self) -> Dict[str, str]:
        """Get ALB endpoints from kubectl"""
        import subprocess
        
        def get_alb(namespace: str, ingress: str) -> str:
            try:
                result = subprocess.run([
                    "kubectl", "get", "ingress", ingress, "-n", namespace,
                    "-o", "jsonpath={.status.loadBalancer.ingress[0].hostname}"
                ], capture_output=True, text=True)
                return f"http://{result.stdout.strip()}"
            except:
                return f"http://localhost:800{['0','1','2'][['purchase','cement','steel'].index(namespace.split('-')[2])]}"
        
        return {
            "purchase": get_alb("part-a-purchase-ns", "purchase-agent-ingress"),
            "cement": get_alb("part-a-cement-ns", "cement-agent-ingress"),
            "steel": get_alb("part-a-steel-ns", "steel-agent-ingress")
        }
        
    async def send_a2a_message(self, endpoint: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send A2A message to EKS-deployed agent"""
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{endpoint}/a2a/message", json=message) as response:
                return await response.json()
    
    async def initiate_procurement(self) -> str:
        """Start procurement process via purchase agent"""
        rfq_message = {
            "type": "rfq",
            "requirements": {
                "cement": {"quantity": 1000, "budget": 50000},
                "steel": {"quantity": 500, "budget": 75000}
            },
            "max_cycles": 4,
            "timestamp": datetime.now().isoformat()
        }
        
        print("🏗️ Initiating procurement via EKS purchase agent...")
        response = await self.send_a2a_message(self.endpoints["purchase"], rfq_message)
        return response.get("negotiation_id")
    
    async def monitor_negotiation(self, negotiation_id: str):
        """Monitor negotiation progress across EKS agents"""
        print(f"👀 Monitoring negotiation {negotiation_id}...")
        
        for cycle in range(1, 5):
            print(f"\n--- Cycle {cycle} ---")
            
            # Check status from all agents
            for agent, endpoint in self.endpoints.items():
                try:
                    status_msg = {"type": "status", "negotiation_id": negotiation_id}
                    status = await self.send_a2a_message(endpoint, status_msg)
                    print(f"{agent.upper()}: {status.get('status', 'unknown')}")
                except Exception as e:
                    print(f"{agent.upper()}: Error - {e}")
            
            await asyncio.sleep(10)  # Wait between cycles
        
        print("\n✅ Negotiation monitoring complete!")
    
    async def get_final_contracts(self, negotiation_id: str):
        """Retrieve final contracts from EKS agents"""
        print("\n📋 Retrieving final contracts...")
        
        contracts = {}
        for agent, endpoint in self.endpoints.items():
            try:
                contract_msg = {"type": "get_contract", "negotiation_id": negotiation_id}
                contract = await self.send_a2a_message(endpoint, contract_msg)
                contracts[agent] = contract
                print(f"{agent.upper()}: ${contract.get('total_cost', 0):,}")
            except Exception as e:
                print(f"{agent.upper()}: Contract error - {e}")
        
        return contracts
    
    async def run_demo(self):
        """Run complete EKS negotiation demo"""
        print("🚀 Starting EKS Negotiation Demo")
        print("=" * 50)
        
        print("🔗 Using ALB Endpoints:")
        for agent, endpoint in self.endpoints.items():
            print(f"  {agent.upper()}: {endpoint}")
        
        try:
            # Start procurement
            negotiation_id = await self.initiate_procurement()
            if not negotiation_id:
                print("❌ Failed to start negotiation")
                return
            
            # Monitor progress
            await self.monitor_negotiation(negotiation_id)
            
            # Get final results
            contracts = await self.get_final_contracts(negotiation_id)
            
            # Summary
            total_cost = sum(c.get('total_cost', 0) for c in contracts.values())
            print(f"\n💰 Total Procurement Cost: ${total_cost:,}")
            print("🎉 EKS Demo Complete!")
            
        except Exception as e:
            print(f"❌ Demo failed: {e}")

async def main():
    demo = EKSNegotiationDemo()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main())