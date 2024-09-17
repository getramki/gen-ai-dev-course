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

# Example for Automatic Reasoning and Tool-Use (ART)

# Function to simulate using a tool based on the reasoning step
def use_tool(tool_name, input_data):
    # Simulate tool usage (e.g., a calculator, web search, etc.)
    if tool_name == "calculator":
        return eval(input_data)
    elif tool_name == "web_search":
        return f"Results for '{input_data}'"
    else:
        return "Tool not recognized"

# Initial task
initial_prompt = "Calculate the sum of the first 10 prime numbers."
reasoning_step = generate_response(f"Step-by-step reasoning to solve: {initial_prompt}")
print("Reasoning Step:", reasoning_step)

# Use a tool based on the reasoning step
tool_prompt = "Use a calculator to find the sum of the first 10 prime numbers."
tool_result = use_tool("calculator", "2 + 3 + 5 + 7 + 11 + 13 + 17 + 19 + 23 + 29")
print("Tool Result:", tool_result)

# Integrate the tool result into the final response
final_prompt = f"Based on the tool result ({tool_result}), provide the final answer to the task: {initial_prompt}"
final_response = generate_response(final_prompt)
print("Final Response:", final_response)