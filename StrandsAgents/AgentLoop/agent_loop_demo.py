#!/usr/bin/env python3
"""
Agent Loop Demo - Strands Agents Framework
Demonstrates the core Agent Loop concept with minimal implementation
"""

import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class AgentState(Enum):
    """Agent execution states"""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    OBSERVING = "observing"
    COMPLETED = "completed"


@dataclass
class Message:
    """Simple message structure for agent communication"""
    content: str
    sender: str = "user"
    timestamp: float = None


class SimpleAgent:
    """Minimal Agent implementation demonstrating the Agent Loop"""
    
    def __init__(self, name: str):
        self.name = name
        self.state = AgentState.IDLE
        self.memory: List[Message] = []
        self.max_iterations = 5
        
    async def think(self, input_message: str) -> str:
        """Think phase: Process input and decide on action"""
        self.state = AgentState.THINKING
        print(f"🤔 {self.name} is thinking about: '{input_message}'")
        
        # Simple decision logic
        if "hello" in input_message.lower():
            return "greet_user"
        elif "weather" in input_message.lower():
            return "check_weather"
        elif "time" in input_message.lower():
            return "get_time"
        else:
            return "general_response"
    
    async def act(self, action: str) -> str:
        """Act phase: Execute the decided action"""
        self.state = AgentState.ACTING
        print(f"🎯 {self.name} is executing action: {action}")
        
        actions = {
            "greet_user": "Hello! Nice to meet you!",
            "check_weather": "I'd check the weather, but I don't have access to weather APIs yet.",
            "get_time": "I'd tell you the time, but I need a time service connection.",
            "general_response": "I understand your message. How can I help you further?"
        }
        
        return actions.get(action, "I'm not sure how to handle that request.")
    
    async def observe(self, result: str) -> Dict[str, Any]:
        """Observe phase: Evaluate the result and update memory"""
        self.state = AgentState.OBSERVING
        print(f"👁️ {self.name} is observing result: '{result}'")
        
        # Store in memory
        self.memory.append(Message(content=result, sender=self.name))
        
        # Simple evaluation
        observation = {
            "success": len(result) > 0,
            "confidence": 0.8 if len(result) > 10 else 0.5,
            "needs_followup": "?" in result or "help" in result.lower()
        }
        
        return observation
    
    async def run_loop(self, user_input: str) -> str:
        """Main Agent Loop: Think -> Act -> Observe cycle"""
        print(f"\n🚀 Starting Agent Loop for: '{user_input}'")
        print("=" * 50)
        
        iteration = 0
        current_input = user_input
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            try:
                # THINK: Decide what to do
                action = await self.think(current_input)
                
                # ACT: Execute the action
                result = await self.act(action)
                
                # OBSERVE: Evaluate and learn
                observation = await self.observe(result)
                
                # Check if we should continue
                if observation["success"] and not observation["needs_followup"]:
                    self.state = AgentState.COMPLETED
                    print(f"\n✅ {self.name} completed successfully!")
                    return result
                
                # Prepare for next iteration if needed
                if observation["needs_followup"]:
                    current_input = "continue with previous task"
                
            except Exception as e:
                print(f"❌ Error in iteration {iteration}: {e}")
                break
        
        self.state = AgentState.COMPLETED
        return result if 'result' in locals() else "Task completed with limitations."


async def main():
    """Demo the Agent Loop with different scenarios"""
    print("🤖 Strands Agents - Agent Loop Demo")
    print("=" * 40)
    
    # Create agent
    agent = SimpleAgent("DemoAgent")
    
    # Test scenarios
    test_inputs = [
        "Hello there!",
        "What's the weather like?",
        "What time is it?",
        "Can you help me with something complex?"
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n🔄 Demo Scenario {i}")
        result = await agent.run_loop(user_input)
        print(f"📤 Final Response: {result}")
        print("\n" + "="*50)
        
        # Reset agent state
        agent.state = AgentState.IDLE
    
    # Show memory
    print("\n📚 Agent Memory:")
    for msg in agent.memory:
        print(f"  - {msg.sender}: {msg.content}")


if __name__ == "__main__":
    asyncio.run(main())