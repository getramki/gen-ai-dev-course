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
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# Example 8: Prompt Chaining - Prompt chaining is a technique that involves using the output of one prompt as the input for the next prompt.
# Initial prompt
initial_prompt = "Write an outline for a blog post about the benefits of AI in healthcare."

# Generate the outline
outline = generate_response(initial_prompt)
print("Outline:", outline)

# Use the outline to generate the introduction
intro_prompt = f"Using the following outline, write an introduction for the blog post:\n\n{outline}\n\nIntroduction:"
introduction = generate_response(intro_prompt)
print("Introduction:", introduction)

# Use the introduction to generate the first section
section_prompt = f"Using the following introduction, write the first section of the blog post:\n\n{introduction}\n\nFirst Section:"
first_section = generate_response(section_prompt)
print("First Section:", first_section)