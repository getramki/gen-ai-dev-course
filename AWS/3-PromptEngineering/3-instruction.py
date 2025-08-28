import boto3
import json
import asyncio

# Set up the Bedrock client
bedrock = boto3.client('bedrock-runtime')

async def get_completion(prompt, model="amazon.titan-text-express-v1"):
    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 4096,
            "stopSequences": [],
            "temperature": 0,
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

# Example usage
prompt = "Summarize the main ideas of the French Revolution in 3 bullet points."

# Asynchronous main function
async def main():
    response = await get_completion(prompt)
    print(response)

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())