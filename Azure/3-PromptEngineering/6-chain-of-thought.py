import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = "https://rk-aiworks.openai.azure.com/"
    )
deployment_name='gpt-35-turbo-instruct'

# Example 6: Chain of thought prompting
chain_of_thought_prompt = """
Solve the following math problem step by step:
If a train travels at a speed of 60 miles per hour and it takes 2 hours to reach its destination, how far did the train travel?
"""
# Generate the completion
response = client.completions.create(model=deployment_name, prompt=chain_of_thought_prompt, max_tokens=200)

# Print the generated completion
print(response.choices[0].text)