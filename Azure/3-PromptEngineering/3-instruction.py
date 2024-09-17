import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = "https://rk-aiworks.openai.azure.com/"
    )
deployment_name='gpt-35-turbo-instruct'

# Example 3: Instruction-based prompt
instruction_prompt = "You are a helpful assistant. Explain the concept of machine learning in simple terms."

# Generate the completion
response = client.completions.create(model=deployment_name, prompt=instruction_prompt, max_tokens=10)

# Print the generated completion
print(response.choices[0].text)