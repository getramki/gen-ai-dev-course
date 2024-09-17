import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = "https://rk-aiworks.openai.azure.com/"
    )
deployment_name='gpt-35-turbo-instruct'

role_playing_prompt = "You are a customer support agent. Help the customer troubleshoot their internet connection issue."

# Generate the completion
response = client.completions.create(model=deployment_name, prompt=role_playing_prompt, max_tokens=200)

# Print the generated completion
print(response.choices[0].text)