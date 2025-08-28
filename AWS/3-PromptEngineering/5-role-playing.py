import boto3
import json
import asyncio

bedrock = boto3.client('bedrock-runtime')

async def get_completion(prompt, model="amazon.titan-text-express-v1"):
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

role_prompt = """
You are a seasoned detective in a noir-style mystery novel. You've just arrived at a crime scene 
in a dimly lit alley. Describe what you see and your initial thoughts on the case.
"""

# Asynchronous main function
async def main():
    response = await get_completion(role_prompt)
    print(response)

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())