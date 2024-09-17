import openai
import os

# Set up your OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_type = 'openai'
# Example 3: Instruction-based prompt
instruction_prompt = "You are a helpful assistant. Explain the concept of machine learning in simple terms."

# Generate the completion
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": instruction_prompt}
    ],
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.3
)

# Print the generated completion
print("Instruction-based prompt response:", response.choices[0].message.content.strip())