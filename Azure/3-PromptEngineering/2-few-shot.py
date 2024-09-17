import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = "https://rk-aiworks.openai.azure.com/"
    )
deployment_name='gpt-35-turbo-instruct'

# Example 2: Few-shot learning
few_shot_prompt = """
Translate the following English text to French:
English: 'Good morning'
French: 'Bonjour'

English: 'Good night'
French: 'Bonne nuit'

English: 'How are you?'
French:
"""

# Generate the completion
response = client.completions.create(model=deployment_name, prompt=few_shot_prompt, max_tokens=10)

# Print the generated completion
print(response.choices[0].text)