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
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# In this example: ThoughtNode Class: Represents a node in the Tree of Thoughts, with each node containing a thought and references to its parent and children. 
# generate_response Function: Uses OpenAI’s API to generate responses based on the given prompt. 
# Tree Expansion: Starts with an initial thought and expands the tree by generating new thoughts based on the previous ones.
# Class to represent a node in the thought tree

class ThoughtNode:
    def __init__(self, thought, parent=None):
        self.thought = thought
        self.parent = parent
        self.children = []

    def add_child(self, child_thought):
        child_node = ThoughtNode(child_thought, parent=self)
        self.children.append(child_node)
        return child_node
    

# Initial thought
initial_prompt = "Generate ideas for a new AI project."
root = ThoughtNode(generate_response(initial_prompt))
print("Root Thought:", root.thought)

# Expand the tree with new thoughts
first_child = root.add_child(generate_response(f"Expand on the idea: {root.thought}"))
print("First Child Thought:", first_child.thought)

second_child = root.add_child(generate_response(f"Expand on the idea: {root.thought}"))
print("Second Child Thought:", second_child.thought)

# Further expand the tree
first_grandchild = first_child.add_child(generate_response(f"Expand on the idea: {first_child.thought}"))
print("First Grandchild Thought:", first_grandchild.thought)

second_grandchild = second_child.add_child(generate_response(f"Expand on the idea: {second_child.thought}"))
print("Second Grandchild Thought:", second_grandchild.thought)