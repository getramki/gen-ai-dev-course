import boto3
import json

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

text = "Generative AI can create new content such as text, images, and music."
target_language = "Hindi"
prompt = f"Translate the following text to {target_language}:\n\n{text}\n\nTranslation:"

print("\nTranslation Example:")
print(f"Original Text: {text}")
print(f"Translated Text: {generate_response(prompt)}")
