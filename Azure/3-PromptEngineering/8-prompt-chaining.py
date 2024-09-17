import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = "https://rk-aiworks.openai.azure.com/"
    )
deployment_name='gpt-35-turbo-instruct'

# Common code to get response from OpenAI
def generate_response(prompt):
    # Generate the completion
    response = client.completions.create(model=deployment_name, prompt=prompt, max_tokens=200)
    return response.choices[0].text

# Example 8: Prompt Chaining - Prompt chaining is a technique that involves using the output of one prompt as the input for the next prompt.
# Initial prompt
initial_prompt = "Write an outline for a blog post about the benefits of AI in healthcare."

# Generate the outline
outline = generate_response(initial_prompt)
print("Outline:", outline)

# Use the outline to generate the introduction
intro_prompt = f"Using the following outline, write an introduction for the blog post:\n\n{outline}\n\nIntroduction:"
introduction = generate_response(intro_prompt)
print("Introduction:", introduction)

# Use the introduction to generate the first section
section_prompt = f"Using the following introduction, write the first section of the blog post:\n\n{introduction}\n\nFirst Section:"
first_section = generate_response(section_prompt)
print("First Section:", first_section)