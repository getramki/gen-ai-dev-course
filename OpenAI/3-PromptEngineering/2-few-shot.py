import openai
import os

# Set up your OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")

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
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": few_shot_prompt}
    ],
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.3
)

# Print the generated completion
print("Few-shot learning response:", response.choices[0].message.content.strip())