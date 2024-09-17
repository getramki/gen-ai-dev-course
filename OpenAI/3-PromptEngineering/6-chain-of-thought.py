import openai
import os

# Set up your OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Example 6: Chain of thought prompting
chain_of_thought_prompt = """
Solve the following math problem step by step:
If a train travels at a speed of 60 miles per hour and it takes 2 hours to reach its destination, how far did the train travel?
"""

# Example 6: chain of thought prompt
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": chain_of_thought_prompt}
    ],
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.3
)

# Print the generated completion
print("Contextual prompt response:", response.choices[0].message.content.strip())