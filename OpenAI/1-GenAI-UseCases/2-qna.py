import openai
import os

# Set up your OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_type = 'openai'

# Common code to get response from OpenAI
def generate_response(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You wil answer the question from the given context only"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

context = (
    "Generative AI is a type of artificial intelligence that can create new content, "
    "such as text, images, and music. It uses machine learning models to generate data "
    "that is similar to the data it was trained on. This technology has a wide range of "
    "applications, including content creation, data augmentation, and more."
)
question = "What is Generative AI?"

prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"

print("\nQuestion and Answering Example:")
print(f"Question: {question}")
print(f"Answer: {generate_response(prompt)}")