import boto3
import json
import asyncio

# Set up the Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # Replace with your preferred region
)

# Define the prompt with chain-of-thought reasoning
prompt = """Solve the following math problem step by step:

Problem: If a train travels at 60 miles per hour for 2.5 hours, how far does it go?

Step 1: Identify the given information
- Speed of the train: 60 miles per hour
- Time of travel: 2.5 hours

Step 2: Recall the formula for distance
Distance = Speed × Time

Step 3: Plug in the values and calculate
Distance = 60 miles/hour × 2.5 hours

Step 4: Perform the multiplication
Distance = 150 miles

Therefore, the train travels 150 miles in 2.5 hours at 60 miles per hour.

Now, solve this problem using the same step-by-step approach:

Problem: If a car travels at 45 miles per hour for 3 hours, how far does it go?

Step 1:"""

# Generate the completion
async def generate_response(prompt):
    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 500,
            "stopSequences": [],
            "temperature": 0.3,
            "topP": 1
        }
    })

    response = bedrock.invoke_model(
        body=body,
        modelId='amazon.titan-text-express-v1',
        accept='application/json',
        contentType='application/json'
    )

    response_body = json.loads(response.get('body').read())
    return response_body.get('results')[0].get('outputText').strip()

# Asynchronous main function
async def main():
    response = await generate_response(prompt)
    print(response)

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
