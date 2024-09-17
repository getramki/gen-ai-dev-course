import openai
import os

# Set up your OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Example 7: meta prompting - Meta Prompting is an advanced prompting technique that focuses on the structural and syntactical aspects of tasks and problems 
# rather than their specific content details. This goal with meta prompting is to construct a more abstract, 
# structured way of interacting with large language models (LLMs), emphasizing the form and pattern of information over traditional content-centric methods. For example, let's say we want to generate a Python function that calculates the factorial of a number. 

# Instead of providing the specific content like "Write a Python function to calculate the factorial of a number", 
# we can use meta prompting to guide the model with a more abstract instruction like "Write a Python function that takes a number as input and returns its factorial".

# Example 7: meta prompting 
meta_prompt = """
Write a Python function that takes a number as input and returns its factorial.
"""

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": meta_prompt}
    ],
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.3
)

# Print the generated completion
print("Contextual prompt response:", response.choices[0].message.content.strip())