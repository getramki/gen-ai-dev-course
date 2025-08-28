import random

class MetaPromptGenerator:
    def __init__(self):
        self.roles = [
            "an expert in explaining complex concepts",
            "a creative storyteller",
            "a professional technical writer",
            "a knowledgeable historian",
            "an experienced data analyst"
        ]
        
        self.tasks = [
            "explain a concept",
            "write a short story",
            "describe a process",
            "analyze historical events",
            "interpret data trends"
        ]
        
        self.output_formats = [
            "a concise paragraph",
            "a list of key points",
            "a step-by-step guide",
            "a comparative analysis",
            "a brief summary"
        ]
        
        self.additional_instructions = [
            "Use simple language suitable for a general audience.",
            "Include relevant examples to illustrate your points.",
            "Focus on the most important aspects of the topic.",
            "Provide context to help understand the bigger picture.",
            "Use analogies to make complex ideas more relatable."
        ]

    def generate_meta_prompt(self, topic):
        role = random.choice(self.roles)
        task = random.choice(self.tasks)
        output_format = random.choice(self.output_formats)
        instruction = random.choice(self.additional_instructions)

        meta_prompt = f"""
You are {role}. Your task is to {task} about '{topic}'. Please follow these guidelines:

1. Present your response as {output_format}.
2. {instruction}
3. Aim for clarity and conciseness in your explanation.
4. Limit your response to about 150 words.

Based on these instructions, please proceed with your task regarding '{topic}':
"""
        return meta_prompt

def main():
    generator = MetaPromptGenerator()
    
    while True:
        topic = input("Enter a topic for the meta prompt (or 'quit' to exit): ")
        if topic.lower() == 'quit':
            break
        
        meta_prompt = generator.generate_meta_prompt(topic)
        print("\nGenerated Meta Prompt:")
        print(meta_prompt)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
