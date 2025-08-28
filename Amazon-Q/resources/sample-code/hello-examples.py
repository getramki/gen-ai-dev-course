# Sample Hello World Examples for Module 1

# Basic Hello World
print("Hello, World!")

# Function-based Hello World
def say_hello(name="World"):
    """Simple greeting function"""
    return f"Hello, {name}!"

# Class-based Hello World
class Greeter:
    def __init__(self, greeting="Hello"):
        self.greeting = greeting
    
    def greet(self, name="World"):
        return f"{self.greeting}, {name}!"

# Interactive Hello World
def interactive_hello():
    name = input("What's your name? ")
    print(f"Hello, {name}! Welcome to Amazon Q Developer course!")

# Multiple language greetings
greetings = {
    'english': 'Hello',
    'spanish': 'Hola',
    'french': 'Bonjour',
    'german': 'Hallo',
    'japanese': 'Konnichiwa'
}

def multilingual_hello(language='english', name='World'):
    greeting = greetings.get(language.lower(), 'Hello')
    return f"{greeting}, {name}!"

if __name__ == "__main__":
    # Test the functions
    print(say_hello())
    print(say_hello("Student"))
    
    greeter = Greeter()
    print(greeter.greet("Amazon Q User"))
    
    print(multilingual_hello('spanish', 'Estudiante'))