import boto3
import json

bedrock = boto3.client('bedrock-runtime')

def get_completion(prompt, model="amazon.titan-text-express-v1"):
    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 4096,
            "stopSequences": [],
            "temperature": 0.7,
            "topP": 1
        }
    })

    response = bedrock.invoke_model(
        body=body,
        modelId=model,
        accept='application/json',
        contentType='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['results'][0]['outputText']

def automatic_reasoning_and_tool_use(task):
    # Step 1: Analyze the task
    analysis_prompt = f"Analyze the following task and break it down into subtasks:\n\n{task}"
    analysis = get_completion(analysis_prompt)
    print("Task Analysis:")
    print(analysis)

    # Step 2: Identify required tools or resources
    tools_prompt = f"Based on the following task analysis, identify the tools or resources needed:\n\n{analysis}"
    tools = get_completion(tools_prompt)
    print("\nRequired Tools and Resources:")
    print(tools)

    # Step 3: Generate a plan
    plan_prompt = f"Create a step-by-step plan to complete the task using the identified tools and resources:\n\nTask: {task}\n\nAnalysis: {analysis}\n\nTools and Resources: {tools}"
    plan = get_completion(plan_prompt)
    print("\nAction Plan:")
    print(plan)

    # Step 4: Execute the plan (simulated)
    execution_prompt = f"Simulate the execution of the following plan:\n\n{plan}"
    execution = get_completion(execution_prompt)
    print("\nPlan Execution:")
    print(execution)

    # Step 5: Evaluate the results
    evaluation_prompt = f"Evaluate the results of the executed plan:\n\nOriginal Task: {task}\n\nExecution Results: {execution}"
    evaluation = get_completion(evaluation_prompt)
    print("\nEvaluation:")
    print(evaluation)

# Example usage
task = "Organize a virtual team-building event for a remote team of 20 people."
automatic_reasoning_and_tool_use(task)
