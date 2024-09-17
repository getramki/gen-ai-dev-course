import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = "https://rk-aiworks.openai.azure.com/"
    )
deployment_name='gpt-35-turbo-instruct'

# Example 4: Contextual prompt
contextual_prompt = """
You are a travel guide. Provide a brief itinerary for a 3-day trip to Paris.
Day 1:
"""
# Generate the completion
response = client.completions.create(model=deployment_name, prompt=contextual_prompt, max_tokens=100)

# Print the generated completion
print(response.choices[0].text)