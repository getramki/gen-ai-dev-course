"""
Exercise 1: Multi-Agent System
Build a coordinated system of AI agents that work together to solve complex tasks.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import time

class AgentRole(Enum):
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"
    REVIEWER = "reviewer"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    id: str
    description: str
    assigned_agent: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class Agent:
    """Base agent class with specialized capabilities."""
    
    def __init__(self, role: AgentRole, name: str):
        self.role = role
        self.name = name
        self.llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            model_kwargs={"temperature": 0.1, "max_tokens": 1000}
        )
        self.completed_tasks = []
    
    def create_prompt(self, task_description: str, context: Dict[str, Any] = None) -> ChatPromptTemplate:
        """Create role-specific prompt for the task."""
        
        role_instructions = {
            AgentRole.COORDINATOR: "You are a task coordinator. Break down complex tasks and provide clear action plans.",
            AgentRole.RESEARCHER: "You are a researcher. Gather information and provide comprehensive research findings.",
            AgentRole.ANALYST: "You are an analyst. Analyze information and provide insights and conclusions.",
            AgentRole.WRITER: "You are a writer. Create well-structured, clear, and engaging content.",
            AgentRole.REVIEWER: "You are a reviewer. Review content for quality, accuracy, and completeness."
        }
        
        context_str = ""
        if context:
            # Format context without JSON to avoid template variable conflicts
            context_parts = []
            for key, value in context.items():
                context_parts.append(f"{key}: {str(value)[:200]}..." if len(str(value)) > 200 else f"{key}: {value}")
            context_str = f"\nContext from previous tasks:\n" + "\n".join(context_parts)
        
        prompt_text = f"""
{role_instructions[self.role]}

Task: {task_description}
{context_str}

Please complete this task and provide a clear, detailed response.
"""
        
        return ChatPromptTemplate.from_template(prompt_text)
    
    def execute_task(self, task: Task, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a task and return response."""
        
        try:
            prompt = self.create_prompt(task.description, context)
            chain = prompt | self.llm | StrOutputParser()
            
            result = chain.invoke({})
            self.completed_tasks.append(task.id)
            
            return {
                "success": True,
                "result": result,
                "confidence": 0.8
            }
            
        except Exception as e:
            return {
                "success": False,
                "result": f"Error executing task: {str(e)}",
                "confidence": 0.0
            }

class MultiAgentSystem:
    """Orchestrates multiple agents to solve complex tasks."""
    
    def __init__(self):
        self.agents = {
            "coordinator": Agent(AgentRole.COORDINATOR, "TaskCoordinator"),
            "researcher": Agent(AgentRole.RESEARCHER, "InfoResearcher"),
            "analyst": Agent(AgentRole.ANALYST, "DataAnalyst"),
            "writer": Agent(AgentRole.WRITER, "ContentWriter"),
            "reviewer": Agent(AgentRole.REVIEWER, "QualityReviewer")
        }
        self.tasks = {}
        self.execution_log = []
    
    def create_task(self, task_id: str, description: str, dependencies: List[str] = None) -> Task:
        """Create a new task."""
        task = Task(
            id=task_id,
            description=description,
            dependencies=dependencies or []
        )
        self.tasks[task_id] = task
        return task
    
    def assign_task(self, task_id: str, agent_name: str):
        """Assign a task to a specific agent."""
        if task_id in self.tasks and agent_name in self.agents:
            self.tasks[task_id].assigned_agent = agent_name
    
    def can_execute_task(self, task: Task) -> bool:
        """Check if a task's dependencies are satisfied."""
        for dep_id in task.dependencies:
            if dep_id not in self.tasks or self.tasks[dep_id].status != TaskStatus.COMPLETED:
                return False
        return True
    
    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute a specific task."""
        
        if task_id not in self.tasks:
            return {"success": False, "error": f"Task {task_id} not found"}
        
        task = self.tasks[task_id]
        
        # Check dependencies
        if not self.can_execute_task(task):
            return {"success": False, "error": f"Dependencies not met for task {task_id}"}
        
        # Check if agent is assigned
        if not task.assigned_agent or task.assigned_agent not in self.agents:
            return {"success": False, "error": f"No valid agent assigned to task {task_id}"}
        
        # Execute task
        task.status = TaskStatus.IN_PROGRESS
        agent = self.agents[task.assigned_agent]
        
        # Gather context from completed dependencies
        context = {}
        for dep_id in task.dependencies:
            if dep_id in self.tasks and self.tasks[dep_id].result:
                context[f"dependency_{dep_id}"] = self.tasks[dep_id].result
        
        # Execute
        start_time = time.time()
        response = agent.execute_task(task, context)
        execution_time = time.time() - start_time
        
        # Update task
        if response["success"]:
            task.status = TaskStatus.COMPLETED
            task.result = response["result"]
        else:
            task.status = TaskStatus.FAILED
            task.result = response["result"]
        
        # Log execution
        log_entry = {
            "task_id": task_id,
            "agent": task.assigned_agent,
            "success": response["success"],
            "execution_time": execution_time
        }
        self.execution_log.append(log_entry)
        
        return {
            "task_id": task_id,
            "success": response["success"],
            "result": response["result"],
            "execution_time": execution_time
        }
    
    def execute_workflow(self, workflow_description: str) -> Dict[str, Any]:
        """Execute a complete workflow by coordinating multiple agents."""
        
        print(f"Starting workflow: {workflow_description}")
        
        # Skip coordinator planning and directly create research workflow
        results = {}
        
        # Create a typical research workflow
        research_tasks = [
            ("research", f"Research the topic: {workflow_description}", []),
            ("analysis", "Analyze the research findings and identify key insights", ["research"]),
            ("writing", "Write a comprehensive report based on the analysis", ["analysis"]),
            ("review", "Review the report for quality and accuracy", ["writing"])
        ]
        
        # Create and assign tasks
        for task_id, description, deps in research_tasks:
            self.create_task(task_id, description, deps)
            
            # Assign to appropriate agent
            agent_mapping = {
                "research": "researcher",
                "analysis": "analyst", 
                "writing": "writer",
                "review": "reviewer"
            }
            self.assign_task(task_id, agent_mapping[task_id])
        
        # Execute tasks in dependency order
        execution_order = ["research", "analysis", "writing", "review"]
        
        for task_id in execution_order:
            print(f"Executing task: {task_id}")
            result = self.execute_task(task_id)
            results[task_id] = result
            
            if not result["success"]:
                print(f"Task {task_id} failed: {result.get('result', 'Unknown error')}")
                break
            else:
                print(f"Task {task_id} completed successfully")
        
        return {
            "workflow_description": workflow_description,
            "results": results,
            "execution_log": self.execution_log,
            "final_output": results.get("review", {}).get("result", "Workflow incomplete")
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        
        task_counts = {
            "total": len(self.tasks),
            "pending": sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING),
            "in_progress": sum(1 for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS),
            "completed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED),
            "failed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
        }
        
        agent_stats = {}
        for name, agent in self.agents.items():
            agent_stats[name] = {
                "role": agent.role.value,
                "completed_tasks": len(agent.completed_tasks)
            }
        
        return {
            "task_counts": task_counts,
            "agent_stats": agent_stats,
            "total_executions": len(self.execution_log)
        }

def demonstrate_multi_agent_system():
    """Demonstrate the multi-agent system capabilities."""
    
    print("=== Multi-Agent System Demo ===\n")
    
    # Initialize system
    system = MultiAgentSystem()
    
    # Test workflow
    workflow = "Research and analyze the impact of artificial intelligence on modern education, then write a comprehensive report"
    
    # Execute workflow
    result = system.execute_workflow(workflow)
    
    print("\n=== Workflow Results ===")
    print(f"Workflow: {result.get('workflow_description', workflow)}")
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"Success: {all(r.get('success', False) for r in result.get('results', {}).values() if isinstance(r, dict))}")
    
    print("\n=== Task Results ===")
    for task_name, task_result in result.get('results', {}).items():
        if isinstance(task_result, dict) and 'success' in task_result:
            print(f"{task_name.title()}: {'✓' if task_result['success'] else '✗'}")
            if task_result['success']:
                print(f"  Result: {task_result['result'][:100]}...")
            print()
    
    print("=== System Status ===")
    status = system.get_system_status()
    print(json.dumps(status, indent=2))
    
    print("\n=== Final Output ===")
    final_output = result.get('final_output', 'No final output available')
    print(final_output[:500] + "..." if len(final_output) > 500 else final_output)

if __name__ == "__main__":
    demonstrate_multi_agent_system()