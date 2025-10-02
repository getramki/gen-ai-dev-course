#!/usr/bin/env python3
"""
Interactive Agent Loop Demo - Strands Agents Framework
Enhanced version with user interaction and configuration
"""

import asyncio
import sys
from agent_loop_demo import SimpleAgent, AgentState
from config import AGENT_CONFIG, DEMO_SCENARIOS


class InteractiveAgent(SimpleAgent):
    """Enhanced agent with interactive capabilities"""
    
    def __init__(self):
        super().__init__(AGENT_CONFIG["name"])
        self.max_iterations = AGENT_CONFIG["max_iterations"]
        self.debug_mode = AGENT_CONFIG["debug_mode"]
    
    async def interactive_session(self):
        """Run an interactive session with the user"""
        print("🤖 Interactive Agent Loop Demo")
        print("=" * 40)
        print("Type 'quit' to exit, 'demo' for automated demo, or ask me anything!")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'demo':
                    await self.run_demo_scenarios()
                    continue
                elif user_input.lower() == 'memory':
                    self.show_memory()
                    continue
                elif not user_input:
                    continue
                
                # Run agent loop
                response = await self.run_loop(user_input)
                print(f"Agent: {response}\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def run_demo_scenarios(self):
        """Run predefined demo scenarios"""
        print("\n🎬 Running Demo Scenarios")
        print("=" * 30)
        
        for i, scenario in enumerate(DEMO_SCENARIOS, 1):
            print(f"\n📋 Scenario {i}: {scenario['name']}")
            print(f"Input: {scenario['input']}")
            
            response = await self.run_loop(scenario['input'])
            print(f"Response: {response}")
            
            # Reset state
            self.state = AgentState.IDLE
            
            # Pause between scenarios
            await asyncio.sleep(1)
        
        print("\n✅ All demo scenarios completed!")
    
    def show_memory(self):
        """Display agent's memory"""
        print("\n📚 Agent Memory:")
        if not self.memory:
            print("  (No memories stored)")
        else:
            for i, msg in enumerate(self.memory, 1):
                print(f"  {i}. {msg.sender}: {msg.content}")
        print()


async def main():
    """Main interactive demo"""
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        # Run automated demo
        agent = InteractiveAgent()
        await agent.run_demo_scenarios()
    else:
        # Run interactive session
        agent = InteractiveAgent()
        await agent.interactive_session()


if __name__ == "__main__":
    asyncio.run(main())