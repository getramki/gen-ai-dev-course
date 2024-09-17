import openai
import os

# Set up your OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Common code to get response from OpenAI
def generate_response(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

prompt = "Once upon a time, in a land far, far away,"

print("\nText Generation Example:")
print(generate_response(prompt))