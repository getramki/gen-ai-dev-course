import boto3
import json
import asyncio

# Set up the Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # Replace with your preferred region
)

# Define the prompt
prompt = "Translate the following English text to Hindi: 'Hello, how are you?'"

# Generate the completion
async def generate_response(prompt):
    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 100,
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
