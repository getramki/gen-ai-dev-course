import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = "https://rk-aiworks.openai.azure.com/"
    )
deployment_name='gpt-35-turbo-instruct'

# Example 7: meta prompting - Meta Prompting is an advanced prompting technique that focuses on the structural and syntactical aspects of tasks and problems 
# rather than their specific content details. This goal with meta prompting is to construct a more abstract, 
# structured way of interacting with large language models (LLMs), emphasizing the form and pattern of information over traditional content-centric methods. For example, let's say we want to generate a Python function that calculates the factorial of a number. 

# Instead of providing the specific content like "Write a Python function to calculate the factorial of a number", 
# we can use meta prompting to guide the model with a more abstract instruction like "Write a Python function that takes a number as input and returns its factorial".

# Example 7: meta prompting 
meta_prompt = """
Write a Python function that takes a number as input and returns its factorial.
"""
# Generate the completion
response = client.completions.create(model=deployment_name, prompt=meta_prompt, max_tokens=200)

# Print the generated completion
print(response.choices[0].text)