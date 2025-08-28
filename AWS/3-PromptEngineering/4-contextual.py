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

context = """
The Apollo program was a series of space missions conducted by NASA in the 1960s and 1970s. 
Its primary goal was to land humans on the Moon and bring them safely back to Earth. 
The program was initiated by President John F. Kennedy in 1961 and culminated with the successful 
Apollo 11 mission in 1969, when Neil Armstrong became the first person to walk on the Moon.
"""

prompt = f"""
Given the following context about the Apollo program, answer the question below:

{context}

Question: What was the main objective of the Apollo program, and in which year was this objective achieved?
"""
# Asynchronous main function
async def main():
    response = await get_completion(prompt)
    print(response)

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())