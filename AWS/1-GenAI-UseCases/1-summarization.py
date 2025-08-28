import json
import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('/home/ramakrishna/Code/GenAI-for-Dev-Course/AWS/.env')

def create_bedrock_client():
    """Create and return an Amazon Bedrock client."""
    region = os.environ.get("AWS_REGION", "us-west-2")

    # os.environ['AWS_BEARER_TOKEN_BEDROCK'] = os.environ.get("AWS_BEARER_TOKEN_BEDROCK")
    # Read 'AWS_BEARER_TOKEN_BEDROCK' from environment variables in the .env file in the parent directory
    bearer_token = os.environ.get("AWS_BEARER_TOKEN_BEDROCK")

    # Use Bearer Token for authentication
    if bearer_token:
        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region,
            aws_access_key_id=bearer_token,
            aws_secret_access_key=bearer_token,
            aws_session_token=bearer_token,
        )
        return bedrock_client
    else:
        print("Error: 'AWS_BEARER_TOKEN_BEDROCK' not found in environment variables.")
        return None
    
    # return boto3.client("bedrock-runtime", region_name=region)

def generate_response(client, prompt, model_id="amazon.titan-text-express-v1", max_tokens=500, temperature=0.3):
    """Generate a response using Amazon Bedrock Titan Express LLM."""
    try:
        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": max_tokens,
                "temperature": temperature,
                "topP": 1,
                "stopSequences": []
            }
        })

        response = client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get("body").read())
        return response_body.get("results")[0].get("outputText").strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

def main():
    client = create_bedrock_client()
    
    text = (
        "Generative AI is a type of artificial intelligence that can create new content, "
        "such as text, images, and music. It uses machine learning models to generate data "
        "that is similar to the data it was trained on. This technology has a wide range of "
        "applications, including content creation, data augmentation, and more."
    )

    prompt = f"Please summarize the following text:\n\n{text}"

    print("Summarization Example:")
    summary = generate_response(client, prompt)
    if summary:
        print(summary)
    else:
        print("Failed to generate summary.")

if __name__ == "__main__":
    main()
