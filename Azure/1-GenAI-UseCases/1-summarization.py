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

text = (
    "Generative AI is a type of artificial intelligence that can create new content, "
    "such as text, images, and music. It uses machine learning models to generate data "
    "that is similar to the data it was trained on. This technology has a wide range of "
    "applications, including content creation, data augmentation, and more."
)

print("Summarization Example:")
print(generate_response(text))