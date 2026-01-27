import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

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

def tree_of_thoughts(problem):
    # Step 1: Generate initial thoughts
    initial_thoughts_prompt = f"Generate 3 initial thoughts or approaches to solve the following problem:\n\n{problem}"
    initial_thoughts = get_completion(initial_thoughts_prompt)
    print("Initial Thoughts:")
    print(initial_thoughts)

    # Step 2: Expand on each thought
    expansion_prompt = f"Expand on each of the following thoughts related to the problem:\n\n{problem}\n\nThoughts:\n{initial_thoughts}"
    expanded_thoughts = get_completion(expansion_prompt)
    print("\nExpanded Thoughts:")
    print(expanded_thoughts)

    # Step 3: Evaluate and rank the approaches
    evaluation_prompt = f"Evaluate and rank the following approaches to solving the problem:\n\n{problem}\n\nApproaches:\n{expanded_thoughts}"
    evaluation = get_completion(evaluation_prompt)
    print("\nEvaluation and Ranking:")
    print(evaluation)

    # Step 4: Final solution
    solution_prompt = f"Based on the evaluation, provide a final solution to the problem:\n\n{problem}\n\nEvaluation:\n{evaluation}"
    final_solution = get_completion(solution_prompt)
    print("\nFinal Solution:")
    print(final_solution)

# Example usage
problem = "How can we reduce plastic waste in urban areas?"
tree_of_thoughts(problem)
