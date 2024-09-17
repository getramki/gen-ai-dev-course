import openai
import os

# Set up your OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_type = 'openai'
# Example 4: Contextual prompt
contextual_prompt = """
You are a travel guide. Provide a brief itinerary for a 3-day trip to Paris.
Day 1:
"""
# Generate the completion
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": contextual_prompt}
    ],
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.3
)

# Print the generated completion
print("Contextual prompt response:", response.choices[0].message.content.strip())