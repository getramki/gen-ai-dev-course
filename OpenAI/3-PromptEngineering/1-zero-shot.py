import openai
import os

# Set up your OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_type = 'openai'
# Define the prompt and the possible labels
prompt = "Translate the following English text to French: 'Hello, how are you?'"
labels = ["English", "French", "Spanish"]

# Generate the completion
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.3
)

# Print the generated completion
print(response.choices[0].message.content.strip())