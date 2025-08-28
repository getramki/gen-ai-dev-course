import boto3
import json
import os

# Set up the Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # Replace with your preferred region
)

# Common code to get response from Amazon Bedrock
def generate_response(prompt):
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

prompt = "Once upon a time, in a land far, far away,"

print("\nText Generation Example:")
print(generate_response(prompt))
