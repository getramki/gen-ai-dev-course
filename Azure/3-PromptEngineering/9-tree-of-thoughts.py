import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = "https://rk-aiworks.openai.azure.com/"
    )
deployment_name='gpt-35-turbo-instruct'

# Common code to get response from Azure OpenAI
def generate_response(prompt):
    # Generate the completion
    response = client.completions.create(model=deployment_name, prompt=prompt, max_tokens=500)
    return response.choices[0].text


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