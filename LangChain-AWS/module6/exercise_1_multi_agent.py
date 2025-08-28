"""
Exercise 1: Multi-Agent System
Build a coordinated system of AI agents that work together to solve complex tasks.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field
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

class AgentResponse(BaseModel):
    """Structured response from an agent."""
    success: bool = Field(description="Whether the task was completed successfully")
    result: str = Field(description="The result or output of the task")
    next_actions: List[str] = Field(description="Suggested next actions or tasks")
    confidence: float = Field(description="Confidence in the result (0-1)")

class Agent:
    """Base agent class with specialized capabilities."""
    
    def __init__(self, role: AgentRole, name: str):
        self.role = role
        self.name = name
        self.llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            model_kwargs={"temperature": 0.1, "max_tokens": 1500}
        )
        self.completed_tasks = []
    
    def create_prompt(self, task_description: str, context: Dict[str, Any] = None) -> ChatPromptTemplate:
        """Create role-specific prompt for the task."""
        
        role_instructions = {
            AgentRole.COORDINATOR: """You are a Coordinator Agent. Your role is to:
- Break down complex tasks into smaller subtasks
- Assign tasks to appropriate agents
- Monitor progress and coordinate between agents
- Ensure all dependencies are met""",
            
            AgentRole.RESEARCHER: """You are a Research Agent. Your role is to:
- Gather relevant information on topics
- Find facts, data, and evidence
- Provide comprehensive background research
- Cite sources when possible""",
            
            AgentRole.ANALYST: """You are an Analysis Agent. Your role is to:
- Analyze data and information
- Identify patterns and insights
- Draw conclusions from evidence
- Provide structured analysis""",
            
            AgentRole.WRITER: """You are a Writing Agent. Your role is to:
- Create well-structured content
- Synthesize information into coherent text
- Adapt writing style to requirements
- Ensure clarity and readability""",
            
            AgentRole.REVIEWER: """You are a Review Agent. Your role is to:
- Review and critique work from other agents
- Check for accuracy and completeness
- Suggest improvements
- Ensure quality standards are met"""
        }
        
        base_prompt = f"""
{role_instructions[self.role]}

Task: {task_description}

Context: {json.dumps(context or {}, indent=2)}

Provide your response in JSON format with:
- success: boolean indicating if task was completed
- result: your output or findings
- next_actions: list of suggested next steps
- confidence: your confidence level (0-1)
"""
        
        return ChatPromptTemplate.from_template(base_prompt)
    
    def execute_task(self, task: Task, context: Dict[str, Any] = None) -> AgentResponse:
        """Execute a task and return structured response."""
        
        try:
            prompt = self.create_prompt(task.description, context)
            chain = prompt | self.llm | PydanticOutputParser(pydantic_object=AgentResponse)
            
            response = chain.invoke({})
            self.completed_tasks.append(task.id)
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                result=f"Error executing task: {str(e)}",
                next_actions=["Retry task with different approach"],
                confidence=0.0
            )

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
            return {"error": f"Task {task_id} not found"}
        
        task = self.tasks[task_id]
        
        # Check dependencies
        if not self.can_execute_task(task):
            return {"error": f"Dependencies not met for task {task_id}"}
        
        # Check if agent is assigned
        if not task.assigned_agent or task.assigned_agent not in self.agents:
            return {"error": f"No valid agent assigned to task {task_id}"}
        
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
        if response.success:
            task.status = TaskStatus.COMPLETED
            task.result = response.result
        else:
            task.status = TaskStatus.FAILED
            task.result = response.result
        
        # Log execution
        log_entry = {
            "task_id": task_id,
            "agent": task.assigned_agent,
            "success": response.success,
            "execution_time": execution_time,
            "confidence": response.confidence,
            "next_actions": response.next_actions
        }
        self.execution_log.append(log_entry)
        
        return {
            "task_id": task_id,
            "success": response.success,
            "result": response.result,
            "next_actions": response.next_actions,
            "execution_time": execution_time
        }
    
    def execute_workflow(self, workflow_description: str) -> Dict[str, Any]:
        """Execute a complete workflow by coordinating multiple agents."""
        
        print(f"Starting workflow: {workflow_description}")
        
        # Step 1: Coordinator breaks down the workflow
        coordinator_task = self.create_task(
            "workflow_planning",
            f"Break down this workflow into specific tasks: {workflow_description}"
        )
        self.assign_task("workflow_planning", "coordinator")
        
        planning_result = self.execute_task("workflow_planning")
        if not planning_result["success"]:
            return {"error": "Failed to plan workflow", "details": planning_result}
        
        # Step 2: Execute suggested next actions
        results = {"planning": planning_result}
        
        # For demo, create a typical research workflow
        research_tasks = [
            ("research", "Research the main topic and gather key information", []),
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
    print(f"Workflow: {result['workflow_description']}")
    print(f"Success: {all(r.get('success', False) for r in result['results'].values() if isinstance(r, dict))}")
    
    print("\n=== Task Results ===")
    for task_name, task_result in result['results'].items():
        if isinstance(task_result, dict) and 'success' in task_result:
            print(f"{task_name.title()}: {'✓' if task_result['success'] else '✗'}")
            if task_result['success']:
                print(f"  Result: {task_result['result'][:100]}...")
            print()
    
    print("=== System Status ===")
    status = system.get_system_status()
    print(json.dumps(status, indent=2))
    
    print("\n=== Final Output ===")
    print(result['final_output'][:500] + "..." if len(result['final_output']) > 500 else result['final_output'])

if __name__ == "__main__":
    demonstrate_multi_agent_system()