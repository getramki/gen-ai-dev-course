# Exercise 1: Multi-Agent System

## Objective
Build and deploy a coordinated system of AI agents that work together to solve complex tasks through role specialization and workflow orchestration.

## Time Estimate
15 minutes

## Prerequisites
- Completed previous modules
- AWS Bedrock access configured
- Understanding of LangChain patterns

## Step-by-Step Instructions

### Step 1: Understand the Agent Architecture
1. **Review the agent roles**:
   - **Coordinator**: Task planning and orchestration
   - **Researcher**: Information gathering and fact-finding
   - **Analyst**: Data analysis and insight generation
   - **Writer**: Content creation and synthesis
   - **Reviewer**: Quality assurance and validation

2. **Examine the task flow**:
   - Tasks have dependencies and execution order
   - Agents communicate through structured responses
   - Context is passed between dependent tasks

### Step 2: Run the Basic Multi-Agent System
```bash
cd module6
python exercise_1_multi_agent.py
```

**Expected Output**:
- Workflow planning by coordinator
- Sequential task execution by specialized agents
- Final comprehensive report
- System status and metrics

### Step 3: Customize Agent Behaviors
1. **Modify agent prompts** in the `create_prompt` method:
   ```python
   # Add domain-specific instructions
   role_instructions[AgentRole.RESEARCHER] += """
   - Focus on recent developments (last 2 years)
   - Include statistical data when available
   - Verify information from multiple sources
   """
   ```

2. **Test with different workflows**:
   ```python
   workflows = [
       "Analyze market trends for electric vehicles",
       "Create a business plan for a tech startup",
       "Research and summarize climate change solutions"
   ]
   ```

### Step 4: Implement Advanced Features
1. **Add parallel task execution**:
   ```python
   def execute_parallel_tasks(self, task_ids: List[str]):
       # Execute independent tasks simultaneously
       with ThreadPoolExecutor() as executor:
           futures = {executor.submit(self.execute_task, tid): tid 
                     for tid in task_ids}
           results = {}
           for future in as_completed(futures):
               task_id = futures[future]
               results[task_id] = future.result()
       return results
   ```

2. **Add agent specialization**:
   ```python
   class SpecializedAgent(Agent):
       def __init__(self, role, name, domain_expertise):
           super().__init__(role, name)
           self.domain_expertise = domain_expertise
           # Adjust model parameters for specialization
           self.llm.model_kwargs["temperature"] = 0.05  # More focused
   ```

### Step 5: Monitor and Debug
1. **Check execution logs**:
   ```python
   for log_entry in system.execution_log:
       print(f"Task: {log_entry['task_id']}")
       print(f"Agent: {log_entry['agent']}")
       print(f"Success: {log_entry['success']}")
       print(f"Confidence: {log_entry['confidence']}")
   ```

2. **Analyze agent performance**:
   ```python
   status = system.get_system_status()
   success_rate = status['task_counts']['completed'] / status['task_counts']['total']
   print(f"Overall success rate: {success_rate:.2%}")
   ```

### Step 6: Create Custom Workflows
1. **Design a domain-specific workflow**:
   ```python
   # Example: Software development workflow
   dev_tasks = [
       ("requirements", "Analyze requirements and create specifications", []),
       ("architecture", "Design system architecture", ["requirements"]),
       ("implementation", "Create implementation plan", ["architecture"]),
       ("testing", "Design testing strategy", ["implementation"]),
       ("deployment", "Plan deployment approach", ["testing"])
   ]
   ```

2. **Add workflow templates**:
   ```python
   WORKFLOW_TEMPLATES = {
       "research_report": [
           ("research", "researcher"),
           ("analysis", "analyst"),
           ("writing", "writer"),
           ("review", "reviewer")
       ],
       "business_analysis": [
           ("market_research", "researcher"),
           ("competitive_analysis", "analyst"),
           ("strategy_writing", "writer"),
           ("plan_review", "reviewer")
       ]
   }
   ```

## Expected Output

### Successful Execution
```
=== Multi-Agent System Demo ===

Starting workflow: Research and analyze the impact of artificial intelligence on modern education

Executing task: research
Task research completed successfully

Executing task: analysis  
Task analysis completed successfully

Executing task: writing
Task writing completed successfully

Executing task: review
Task review completed successfully

=== Workflow Results ===
Workflow: Research and analyze the impact of artificial intelligence on modern education
Success: True

=== Task Results ===
Planning: ✓
Research: ✓
  Result: AI in education encompasses personalized learning platforms, intelligent tutoring systems...
Analysis: ✓
  Result: Key insights show 40% improvement in student engagement with AI-powered tools...
Writing: ✓
  Result: Comprehensive Report: The Impact of AI on Modern Education...
Review: ✓
  Result: The report demonstrates thorough research and analysis. Recommendations include...

=== System Status ===
{
  "task_counts": {
    "total": 5,
    "pending": 0,
    "in_progress": 0,
    "completed": 5,
    "failed": 0
  },
  "agent_stats": {
    "coordinator": {"role": "coordinator", "completed_tasks": 1},
    "researcher": {"role": "researcher", "completed_tasks": 1},
    "analyst": {"role": "analyst", "completed_tasks": 1},
    "writer": {"role": "writer", "completed_tasks": 1},
    "reviewer": {"role": "reviewer", "completed_tasks": 1}
  },
  "total_executions": 5
}
```

## Common Issues and Solutions

### Issue 1: Agent Task Failures
**Problem**: Agents fail to complete tasks
**Solution**: 
- Check model availability and permissions
- Verify prompt formatting and JSON parsing
- Add retry logic with exponential backoff

### Issue 2: Dependency Resolution
**Problem**: Tasks execute out of order
**Solution**:
- Verify dependency definitions are correct
- Check `can_execute_task` logic
- Add dependency validation

### Issue 3: Context Passing
**Problem**: Agents don't receive proper context
**Solution**:
- Ensure completed tasks store results properly
- Verify context building in `execute_task`
- Add context validation

## Challenge Extensions

### Extension 1: Dynamic Agent Creation
Create agents dynamically based on task requirements:
```python
def create_specialized_agent(self, task_type: str, domain: str):
    agent_name = f"{domain}_{task_type}_agent"
    return Agent(AgentRole.ANALYST, agent_name)
```

### Extension 2: Agent Learning
Implement agent improvement based on feedback:
```python
class LearningAgent(Agent):
    def __init__(self, role, name):
        super().__init__(role, name)
        self.performance_history = []
    
    def update_from_feedback(self, feedback: str):
        # Adjust behavior based on feedback
        pass
```

### Extension 3: Workflow Optimization
Add workflow optimization based on execution patterns:
```python
def optimize_workflow(self, workflow_history: List[Dict]):
    # Analyze patterns and suggest improvements
    # Reorder tasks for better efficiency
    # Identify bottlenecks
    pass
```

## Completion Checklist
- [ ] Multi-agent system executes successfully
- [ ] All agent roles function correctly
- [ ] Task dependencies are properly handled
- [ ] Workflow produces coherent final output
- [ ] System status and metrics are accurate
- [ ] Custom workflow created and tested
- [ ] Advanced features implemented (optional)

## Learning Outcomes
After completing this exercise, you will understand:
- Multi-agent system architecture and coordination
- Task dependency management and execution ordering
- Agent specialization and role-based processing
- Workflow orchestration and monitoring
- Context passing between agents
- System scalability and performance considerations

## Next Steps
- Proceed to Exercise 2: Production Deployment
- Explore agent communication protocols
- Implement more sophisticated coordination patterns
- Add real-time monitoring and alerting