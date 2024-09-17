# Importing necessary libraries
import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Function to demonstrate different prompt engineering techniques
def get_answer(prompt, model="gpt-4"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

# Example 1: Zero-shot learning
zero_shot_prompt = "Translate the following English text to French: 'Hello, how are you?'"
zero_shot_response = get_answer(zero_shot_prompt)
print("Zero-shot learning response:", zero_shot_response)

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
few_shot_response = get_answer(few_shot_prompt)
print("Few-shot learning response:", few_shot_response)

# Example 3: Instruction-based prompt
instruction_prompt = "You are a helpful assistant. Explain the concept of machine learning in simple terms."
instruction_response = get_answer(instruction_prompt)
print("Instruction-based prompt response:", instruction_response)

# Example 4: Contextual prompt
contextual_prompt = """
You are a travel guide. Provide a brief itinerary for a 3-day trip to Paris.
Day 1:
"""
contextual_response = get_answer(contextual_prompt)
print("Contextual prompt response:", contextual_response)

# Example 5: Role-playing prompt
role_playing_prompt = "You are a customer support agent. Help the customer troubleshoot their internet connection issue."
role_playing_response = get_answer(role_playing_prompt)
print("Role-playing prompt response:", role_playing_response)

# Example 6: Chain of thought prompting
chain_of_thought_prompt = """
Solve the following math problem step by step:
If a train travels at a speed of 60 miles per hour and it takes 2 hours to reach its destination, how far did the train travel?
"""
chain_of_thought_response = get_answer(chain_of_thought_prompt)
print("Chain of thought prompting response:", chain_of_thought_response)