import openai
import os

# Set up your OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_type = 'openai'
role_playing_prompt = "You are a customer support agent. Help the customer troubleshoot their internet connection issue."

# Example 5: Role-playing prompt
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": role_playing_prompt}
    ],
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.3
)

# Print the generated completion
print("Contextual prompt response:", response.choices[0].message.content.strip())