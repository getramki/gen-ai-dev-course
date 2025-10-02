"""
Topic 4.3: System Messages and Role-based Interactions (6 minutes)

Learning Goals:
- Master advanced system message patterns for ChatBedrockConverse
- Implement dynamic persona and role management
- Optimize system messages for different conversation types
- Create adaptive behavior based on context and user needs
"""

from langchain_aws.chat_models import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import Dict, List

def setup_system_message_chat():
    """Initialize ChatBedrockConverse for system message examples"""
    
    print("=== System Message Chat Setup ===\n")
    
    try:
        chat = ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=200,
            temperature=0.7
        )
        
        print("✅ ChatBedrockConverse initialized for system message testing")
        return chat
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return None

def demonstrate_persona_system_messages(chat):
    """Show different persona implementations with system messages"""
    
    print("=== Persona System Messages ===\n")
    
    if not chat:
        print("❌ Chat not available")
        return
    
    personas = [
        {
            "name": "Technical Expert",
            "system_message": "You are a senior software engineer with 15 years of experience. Provide detailed, technical explanations with code examples when relevant. Be precise and professional.",
            "test_question": "How do I optimize database queries?"
        },
        {
            "name": "Friendly Teacher",
            "system_message": "You are a patient, encouraging teacher who explains complex topics in simple terms. Use analogies and examples. Always be supportive and positive.",
            "test_question": "How do I optimize database queries?"
        },
        {
            "name": "Business Consultant",
            "system_message": "You are a strategic business consultant focused on ROI and practical outcomes. Frame technical solutions in business terms and emphasize value and efficiency.",
            "test_question": "How do I optimize database queries?"
        }
    ]
    
    for persona in personas:
        print(f"Testing {persona['name']} Persona:")
        
        messages = [
            SystemMessage(content=persona['system_message']),
            HumanMessage(content=persona['test_question'])
        ]
        
        try:
            response = chat.invoke(messages)
            print(f"Response: {response.content[:120]}...")
            print(f"Tone: {persona['name']} characteristics evident")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        print()

def implement_dynamic_system_messages():
    """Implement system messages that adapt based on context"""
    
    print("=== Dynamic System Messages ===\n")
    
    class DynamicSystemMessageManager:
        """Manage system messages based on context and user profile"""
        
        def __init__(self):
            self.base_personas = {
                "helper": "You are a helpful assistant who provides clear, accurate information.",
                "expert": "You are a domain expert who provides detailed, authoritative answers.",
                "teacher": "You are a patient teacher who explains concepts step by step.",
                "consultant": "You are a strategic consultant focused on practical solutions."
            }
            
            self.context_modifiers = {
                "beginner": "The user is new to this topic. Use simple language and provide basic explanations.",
                "intermediate": "The user has some knowledge. Provide balanced detail and practical examples.",
                "advanced": "The user is experienced. Focus on nuanced details and advanced concepts.",
                "urgent": "The user needs a quick solution. Be concise and action-oriented."
            }
            
            self.domain_expertise = {
                "technology": "Focus on technical accuracy, best practices, and implementation details.",
                "business": "Emphasize ROI, efficiency, and strategic implications.",
                "education": "Use pedagogical approaches with clear learning objectives.",
                "creative": "Encourage innovation and out-of-the-box thinking."
            }
        
        def generate_system_message(self, persona="helper", user_level="intermediate", domain="technology", context_flags=None):
            """Generate dynamic system message based on parameters"""
            
            # Start with base persona
            system_parts = [self.base_personas.get(persona, self.base_personas["helper"])]
            
            # Add user level context
            if user_level in self.context_modifiers:
                system_parts.append(self.context_modifiers[user_level])
            
            # Add domain expertise
            if domain in self.domain_expertise:
                system_parts.append(self.domain_expertise[domain])
            
            # Add context flags
            if context_flags:
                for flag in context_flags:
                    if flag in self.context_modifiers:
                        system_parts.append(self.context_modifiers[flag])
            
            return " ".join(system_parts)
        
        def adapt_to_conversation_history(self, messages):
            """Adapt system message based on conversation history"""
            
            # Analyze conversation for adaptation cues
            user_messages = [msg.content for msg in messages if isinstance(msg, HumanMessage)]
            
            # Detect user expertise level
            technical_terms = ["algorithm", "implementation", "optimization", "architecture"]
            basic_questions = ["what is", "how do I", "can you explain", "help me understand"]
            
            user_text = " ".join(user_messages).lower()
            
            if any(term in user_text for term in technical_terms):
                user_level = "advanced"
            elif any(question in user_text for question in basic_questions):
                user_level = "beginner"
            else:
                user_level = "intermediate"
            
            # Detect urgency
            urgent_indicators = ["urgent", "quickly", "asap", "deadline", "emergency"]
            context_flags = []
            if any(indicator in user_text for indicator in urgent_indicators):
                context_flags.append("urgent")
            
            return self.generate_system_message(
                persona="expert",
                user_level=user_level,
                domain="technology",
                context_flags=context_flags
            )
    
    # Test dynamic system message generation
    manager = DynamicSystemMessageManager()
    
    test_scenarios = [
        {
            "name": "Beginner User",
            "params": {"persona": "teacher", "user_level": "beginner", "domain": "technology"}
        },
        {
            "name": "Expert Consultant",
            "params": {"persona": "consultant", "user_level": "advanced", "domain": "business"}
        },
        {
            "name": "Urgent Help",
            "params": {"persona": "helper", "user_level": "intermediate", "domain": "technology", "context_flags": ["urgent"]}
        }
    ]
    
    for scenario in test_scenarios:
        print(f"Scenario: {scenario['name']}")
        system_msg = manager.generate_system_message(**scenario['params'])
        print(f"System Message: {system_msg[:100]}...")
        print()

def demonstrate_role_based_interactions(chat):
    """Show role-based interaction patterns"""
    
    print("=== Role-based Interactions ===\n")
    
    if not chat:
        print("❌ Chat not available")
        return
    
    # Multi-role conversation scenario
    roles = [
        {
            "role": "Project Manager",
            "system_message": "You are a project manager focused on timelines, resources, and deliverables. Ask clarifying questions about scope and constraints.",
            "context": "planning a software project"
        },
        {
            "role": "Technical Architect", 
            "system_message": "You are a technical architect concerned with system design, scalability, and technical feasibility. Focus on architecture decisions.",
            "context": "designing system architecture"
        },
        {
            "role": "UX Designer",
            "system_message": "You are a UX designer focused on user experience, usability, and design principles. Consider user needs and interface design.",
            "context": "improving user experience"
        }
    ]
    
    user_request = "We need to build a new customer dashboard for our e-commerce platform."
    
    for role_info in roles:
        print(f"Role: {role_info['role']}")
        print(f"Context: {role_info['context']}")
        
        messages = [
            SystemMessage(content=role_info['system_message']),
            HumanMessage(content=user_request)
        ]
        
        try:
            response = chat.invoke(messages)
            print(f"Response: {response.content[:100]}...")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        print()

def implement_context_aware_system_messages():
    """Implement system messages that adapt to conversation context"""
    
    print("=== Context-Aware System Messages ===\n")
    
    class ContextAwareSystemManager:
        """Manage system messages based on conversation context"""
        
        def __init__(self):
            self.conversation_types = {
                "troubleshooting": "You are a technical support specialist. Focus on diagnosing problems systematically and providing step-by-step solutions.",
                "learning": "You are an educational mentor. Break down complex topics into digestible parts and check for understanding.",
                "brainstorming": "You are a creative facilitator. Encourage diverse ideas and build upon suggestions constructively.",
                "decision_making": "You are a strategic advisor. Present options clearly with pros/cons and help evaluate trade-offs."
            }
            
            self.conversation_stage_modifiers = {
                "opening": "Start with a warm greeting and establish the user's needs.",
                "exploration": "Ask probing questions to understand the full context.",
                "solution": "Provide detailed, actionable recommendations.",
                "closure": "Summarize key points and confirm next steps."
            }
        
        def detect_conversation_type(self, messages):
            """Detect conversation type from message content"""
            
            user_content = " ".join([msg.content for msg in messages if isinstance(msg, HumanMessage)]).lower()
            
            type_indicators = {
                "troubleshooting": ["error", "problem", "not working", "issue", "bug", "fix"],
                "learning": ["learn", "understand", "explain", "teach", "how does", "what is"],
                "brainstorming": ["ideas", "suggestions", "creative", "brainstorm", "think of"],
                "decision_making": ["should I", "which option", "decide", "choose", "recommend"]
            }
            
            for conv_type, indicators in type_indicators.items():
                if any(indicator in user_content for indicator in indicators):
                    return conv_type
            
            return "learning"  # Default
        
        def get_stage_modifier(self, message_count):
            """Get conversation stage based on message count"""
            if message_count <= 2:
                return "opening"
            elif message_count <= 6:
                return "exploration"
            elif message_count <= 10:
                return "solution"
            else:
                return "closure"
        
        def generate_contextual_system_message(self, messages):
            """Generate system message based on conversation context"""
            
            conv_type = self.detect_conversation_type(messages)
            stage = self.get_stage_modifier(len(messages))
            
            base_message = self.conversation_types[conv_type]
            stage_modifier = self.conversation_stage_modifiers[stage]
            
            return f"{base_message} {stage_modifier}"
    
    # Test context-aware system messages
    manager = ContextAwareSystemManager()
    
    test_conversations = [
        {
            "name": "Troubleshooting Scenario",
            "messages": [
                HumanMessage(content="My Python code is throwing an error and I can't figure out why."),
                HumanMessage(content="The error says 'KeyError: name' but I'm not sure what that means.")
            ]
        },
        {
            "name": "Learning Scenario", 
            "messages": [
                HumanMessage(content="I want to learn about machine learning algorithms."),
                HumanMessage(content="Can you explain how neural networks work?")
            ]
        }
    ]
    
    for scenario in test_conversations:
        print(f"Scenario: {scenario['name']}")
        
        system_msg = manager.generate_contextual_system_message(scenario['messages'])
        conv_type = manager.detect_conversation_type(scenario['messages'])
        stage = manager.get_stage_modifier(len(scenario['messages']))
        
        print(f"Detected Type: {conv_type}")
        print(f"Stage: {stage}")
        print(f"System Message: {system_msg[:100]}...")
        print()

def demonstrate_system_message_optimization():
    """Show system message optimization techniques"""
    
    print("=== System Message Optimization ===\n")
    
    optimization_techniques = {
        "Clarity": {
            "principle": "Use clear, specific language",
            "example": "You are a Python expert who provides working code examples with explanations.",
            "avoid": "You are good at programming and help people."
        },
        "Specificity": {
            "principle": "Define specific behaviors and constraints",
            "example": "Respond in exactly 3 bullet points. Each point should be actionable and include a specific example.",
            "avoid": "Give me some good advice."
        },
        "Context Setting": {
            "principle": "Establish relevant context and constraints",
            "example": "You are helping a startup CTO make technology decisions. Consider budget constraints and rapid scaling needs.",
            "avoid": "You are a technology advisor."
        },
        "Tone Definition": {
            "principle": "Specify desired communication style",
            "example": "Communicate in a friendly, encouraging tone. Use simple analogies to explain complex concepts.",
            "avoid": "Be helpful and nice."
        }
    }
    
    for technique, details in optimization_techniques.items():
        print(f"🎯 {technique}:")
        print(f"   Principle: {details['principle']}")
        print(f"   ✅ Good: {details['example']}")
        print(f"   ❌ Avoid: {details['avoid']}")
        print()

if __name__ == "__main__":
    print("Module 4.3: System Messages and Role-based Interactions\n")
    
    # Setup
    chat = setup_system_message_chat()
    
    # Demonstrations
    demonstrate_persona_system_messages(chat)
    implement_dynamic_system_messages()
    demonstrate_role_based_interactions(chat)
    implement_context_aware_system_messages()
    demonstrate_system_message_optimization()
    
    # Summary
    print("="*50)
    print("✅ Topic 4.3 Complete!")
    print("Key Takeaways:")
    print("• System messages define AI personality and behavior")
    print("• Dynamic adaptation improves conversation quality")
    print("• Role-based interactions enable specialized responses")
    print("• Context awareness enhances user experience")
    print("🚀 Ready for Topic 4.4: Performance Comparison!")
    print("="*50)