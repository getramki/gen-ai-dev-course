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

context = (
    "Generative AI is a type of artificial intelligence that can create new content, "
    "such as text, images, and music. It uses machine learning models to generate data "
    "that is similar to the data it was trained on. This technology has a wide range of "
    "applications, including content creation, data augmentation, and more."
)
question = "What is Generative AI?"

prompt = f"""You will answer the question from the given context only.

Context: {context}
Question: {question}
Answer:"""

print("\nQuestion and Answering Example:")
print(f"Question: {question}")
print(f"Answer: {generate_response(prompt)}")
