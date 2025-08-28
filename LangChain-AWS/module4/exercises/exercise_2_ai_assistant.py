"""
Exercise 2: Specialized AI Assistant with Personas

Task: Build a sophisticated AI assistant system that:
1. Implements multiple specialized personas with dynamic switching
2. Adapts behavior based on conversation context and user profile
3. Provides role-based expertise across different domains
4. Includes performance monitoring and persona effectiveness tracking

Time: 7 minutes
"""

from langchain_aws.chat_models import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from datetime import datetime
from typing import Dict, List, Optional
import json

class SpecializedAIAssistant:
    """Advanced AI assistant with multiple specialized personas"""
    
    def __init__(self):
        self.chat = self._initialize_chat()
        self.current_persona = "general"
        self.conversation_history = []
        self.user_profile = {
            "expertise_level": "intermediate",
            "preferred_communication_style": "balanced",
            "domain_interests": [],
            "interaction_history": []
        }
        self.persona_performance = {}
        
        # Define specialized personas
        self.personas = self._initialize_personas()
    
    def _initialize_chat(self):
        """Initialize ChatBedrockConverse"""
        return ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=300,
            temperature=0.7
        )
    
    def _initialize_personas(self):
        """Define specialized AI personas"""
        return {
            "general": {
                "name": "General Assistant",
                "system_message": "You are a helpful, knowledgeable assistant who provides clear, accurate information across various topics.",
                "expertise_domains": ["general"],
                "communication_style": "balanced",
                "specialties": ["general knowledge", "basic problem solving"]
            },
            "technical_expert": {
                "name": "Technical Expert",
                "system_message": "You are a senior technical expert with deep knowledge in software development, system architecture, and engineering best practices. Provide detailed, accurate technical guidance with code examples when relevant.",
                "expertise_domains": ["technology", "programming", "engineering"],
                "communication_style": "technical",
                "specialties": ["software development", "system design", "debugging", "architecture"]
            },
            "business_consultant": {
                "name": "Business Consultant",
                "system_message": "You are a strategic business consultant focused on practical outcomes, ROI, and business value. Frame technical solutions in business terms and emphasize efficiency and strategic impact.",
                "expertise_domains": ["business", "strategy", "management"],
                "communication_style": "strategic",
                "specialties": ["business strategy", "ROI analysis", "project management", "decision making"]
            },
            "creative_mentor": {
                "name": "Creative Mentor",
                "system_message": "You are a creative mentor who encourages innovative thinking and out-of-the-box solutions. Use analogies, storytelling, and creative approaches to explain concepts and inspire new ideas.",
                "expertise_domains": ["creative", "design", "innovation"],
                "communication_style": "inspiring",
                "specialties": ["creative thinking", "innovation", "design", "storytelling"]
            },
            "educator": {
                "name": "Patient Educator",
                "system_message": "You are a patient, encouraging educator who breaks down complex topics into understandable parts. Use examples, analogies, and step-by-step explanations. Always check for understanding and provide encouragement.",
                "expertise_domains": ["education", "learning", "training"],
                "communication_style": "pedagogical",
                "specialties": ["teaching", "curriculum design", "learning assessment", "skill development"]
            },
            "researcher": {
                "name": "Research Analyst",
                "system_message": "You are a thorough research analyst who provides evidence-based insights, cites sources when possible, and presents balanced perspectives on complex topics. Focus on accuracy and comprehensive analysis.",
                "expertise_domains": ["research", "analysis", "data"],
                "communication_style": "analytical",
                "specialties": ["data analysis", "research methodology", "critical thinking", "evidence evaluation"]
            }
        }
    
    def _detect_optimal_persona(self, user_input):
        """Detect optimal persona based on user input and context"""
        
        input_lower = user_input.lower()
        
        # Domain keyword mapping
        domain_keywords = {
            "technical_expert": ["code", "programming", "software", "algorithm", "debug", "architecture", "api", "database"],
            "business_consultant": ["business", "strategy", "roi", "profit", "market", "revenue", "cost", "efficiency"],
            "creative_mentor": ["creative", "design", "innovative", "brainstorm", "idea", "artistic", "inspiration"],
            "educator": ["learn", "teach", "explain", "understand", "study", "course", "tutorial", "beginner"],
            "researcher": ["research", "analyze", "data", "study", "evidence", "statistics", "findings", "methodology"]
        }
        
        # Score each persona based on keyword matches
        persona_scores = {}
        for persona, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in input_lower)
            if score > 0:
                persona_scores[persona] = score
        
        # Return highest scoring persona or general if no matches
        if persona_scores:
            return max(persona_scores.items(), key=lambda x: x[1])[0]
        
        return "general"
    
    def _adapt_persona_to_user_profile(self, base_persona):
        """Adapt persona based on user profile"""
        
        persona_config = self.personas[base_persona].copy()
        
        # Adapt communication style based on user expertise
        if self.user_profile["expertise_level"] == "beginner":
            persona_config["system_message"] += " Use simple language and provide basic explanations with examples."
        elif self.user_profile["expertise_level"] == "advanced":
            persona_config["system_message"] += " Provide detailed, technical information and assume advanced knowledge."
        
        # Adapt based on preferred communication style
        if self.user_profile["preferred_communication_style"] == "concise":
            persona_config["system_message"] += " Be concise and direct in your responses."
        elif self.user_profile["preferred_communication_style"] == "detailed":
            persona_config["system_message"] += " Provide comprehensive, detailed explanations."
        
        return persona_config
    
    def _update_user_profile(self, user_input, persona_used):
        """Update user profile based on interaction"""
        
        # Track domain interests
        input_lower = user_input.lower()
        domains = self.personas[persona_used]["expertise_domains"]
        
        for domain in domains:
            if domain not in self.user_profile["domain_interests"]:
                self.user_profile["domain_interests"].append(domain)
        
        # Update interaction history
        self.user_profile["interaction_history"].append({
            "timestamp": datetime.now().isoformat(),
            "persona_used": persona_used,
            "input_length": len(user_input),
            "domains": domains
        })
        
        # Adapt expertise level based on interaction patterns
        if len(self.user_profile["interaction_history"]) >= 5:
            recent_personas = [h["persona_used"] for h in self.user_profile["interaction_history"][-5:]]
            if recent_personas.count("technical_expert") >= 3:
                self.user_profile["expertise_level"] = "advanced"
            elif recent_personas.count("educator") >= 3:
                self.user_profile["expertise_level"] = "beginner"
    
    def _track_persona_performance(self, persona, response_length, processing_time):
        """Track persona performance metrics"""
        
        if persona not in self.persona_performance:
            self.persona_performance[persona] = {
                "usage_count": 0,
                "total_response_length": 0,
                "total_processing_time": 0,
                "avg_response_length": 0,
                "avg_processing_time": 0
            }
        
        stats = self.persona_performance[persona]
        stats["usage_count"] += 1
        stats["total_response_length"] += response_length
        stats["total_processing_time"] += processing_time
        stats["avg_response_length"] = stats["total_response_length"] / stats["usage_count"]
        stats["avg_processing_time"] = stats["total_processing_time"] / stats["usage_count"]
    
    def send_message(self, user_input, force_persona=None):
        """Send message with automatic or forced persona selection"""
        
        start_time = datetime.now()
        
        # Determine persona to use
        if force_persona and force_persona in self.personas:
            selected_persona = force_persona
        else:
            selected_persona = self._detect_optimal_persona(user_input)
        
        # Adapt persona to user profile
        persona_config = self._adapt_persona_to_user_profile(selected_persona)
        
        # Update current persona
        self.current_persona = selected_persona
        
        # Build conversation context
        messages = []
        
        # Add adapted system message
        messages.append(SystemMessage(content=persona_config["system_message"]))
        
        # Add recent conversation history (last 6 messages)
        recent_history = self.conversation_history[-6:] if len(self.conversation_history) > 6 else self.conversation_history
        messages.extend(recent_history)
        
        # Add current user message
        user_message = HumanMessage(content=user_input)
        messages.append(user_message)
        
        try:
            # Get AI response
            response = self.chat.invoke(messages)
            
            # Add messages to conversation history
            self.conversation_history.append(user_message)
            self.conversation_history.append(response)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Update user profile and track performance
            self._update_user_profile(user_input, selected_persona)
            self._track_persona_performance(selected_persona, len(response.content), processing_time)
            
            return {
                "response": response.content,
                "persona_used": selected_persona,
                "persona_name": persona_config["name"],
                "processing_time": processing_time,
                "user_profile": self.user_profile.copy(),
                "conversation_length": len(self.conversation_history)
            }
            
        except Exception as e:
            return {"error": f"Assistant failed: {e}"}
    
    def switch_persona(self, new_persona):
        """Manually switch to a specific persona"""
        
        if new_persona in self.personas:
            self.current_persona = new_persona
            return f"Switched to {self.personas[new_persona]['name']}"
        else:
            available = ", ".join(self.personas.keys())
            return f"Persona '{new_persona}' not found. Available: {available}"
    
    def get_persona_analytics(self):
        """Get comprehensive persona usage analytics"""
        
        return {
            "current_persona": self.current_persona,
            "available_personas": list(self.personas.keys()),
            "user_profile": self.user_profile,
            "persona_performance": self.persona_performance,
            "conversation_stats": {
                "total_messages": len(self.conversation_history),
                "conversation_duration": len(self.user_profile["interaction_history"])
            }
        }
    
    def get_persona_recommendations(self, query):
        """Get persona recommendations for a specific query"""
        
        optimal_persona = self._detect_optimal_persona(query)
        
        recommendations = []
        for persona_id, persona_info in self.personas.items():
            score = 0
            
            # Score based on domain match
            query_lower = query.lower()
            for domain in persona_info["expertise_domains"]:
                if domain in query_lower:
                    score += 2
            
            # Score based on specialties
            for specialty in persona_info["specialties"]:
                if any(word in query_lower for word in specialty.split()):
                    score += 1
            
            if score > 0:
                recommendations.append({
                    "persona": persona_id,
                    "name": persona_info["name"],
                    "score": score,
                    "specialties": persona_info["specialties"]
                })
        
        # Sort by score
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "query": query,
            "optimal_persona": optimal_persona,
            "recommendations": recommendations[:3]  # Top 3
        }

def run_specialized_assistant_demo():
    """Run comprehensive specialized assistant demo"""
    
    print("=== Specialized AI Assistant Demo ===\n")
    
    assistant = SpecializedAIAssistant()
    
    # Demo scenarios with different domains
    demo_scenarios = [
        {
            "query": "I need help debugging a Python function that's not working correctly.",
            "expected_persona": "technical_expert"
        },
        {
            "query": "What's the ROI analysis for implementing a new CRM system?",
            "expected_persona": "business_consultant"
        },
        {
            "query": "I want to learn about machine learning algorithms step by step.",
            "expected_persona": "educator"
        },
        {
            "query": "How can I brainstorm innovative features for my mobile app?",
            "expected_persona": "creative_mentor"
        },
        {
            "query": "What research methodology should I use for my data analysis project?",
            "expected_persona": "researcher"
        }
    ]
    
    print("Testing automatic persona selection and adaptation...\n")
    
    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"Scenario {i}: {scenario['query']}")
        
        # Get persona recommendations
        recommendations = assistant.get_persona_recommendations(scenario['query'])
        print(f"🎯 Recommended persona: {recommendations['optimal_persona']}")
        
        # Send message
        result = assistant.send_message(scenario['query'])
        
        if "error" in result:
            print(f"❌ {result['error']}")
            continue
        
        print(f"🤖 {result['persona_name']}: {result['response'][:100]}...")
        print(f"📊 Processing time: {result['processing_time']:.2f}s")
        print(f"👤 User expertise level: {result['user_profile']['expertise_level']}")
        print()
    
    # Show final analytics
    analytics = assistant.get_persona_analytics()
    print("📈 Final Assistant Analytics:")
    print(f"   Total interactions: {analytics['conversation_stats']['conversation_duration']}")
    print(f"   User interests: {analytics['user_profile']['domain_interests']}")
    print(f"   Current expertise level: {analytics['user_profile']['expertise_level']}")
    
    print("\n🎭 Persona Usage Statistics:")
    for persona, stats in analytics['persona_performance'].items():
        if stats['usage_count'] > 0:
            print(f"   {persona}: {stats['usage_count']} uses, avg response: {stats['avg_response_length']:.0f} chars")

def test_persona_switching():
    """Test manual persona switching functionality"""
    
    print("\n=== Persona Switching Test ===\n")
    
    assistant = SpecializedAIAssistant()
    
    # Test manual switching
    test_query = "Explain artificial intelligence."
    
    personas_to_test = ["technical_expert", "educator", "creative_mentor"]
    
    for persona in personas_to_test:
        print(f"Testing with {persona} persona:")
        
        result = assistant.send_message(test_query, force_persona=persona)
        
        if "error" not in result:
            print(f"🤖 {result['persona_name']}: {result['response'][:80]}...")
        else:
            print(f"❌ {result['error']}")
        
        print()

if __name__ == "__main__":
    run_specialized_assistant_demo()
    test_persona_switching()
    
    print("\n" + "="*50)
    print("✅ Exercise 2 Complete!")
    print("Advanced Features Implemented:")
    print("• Multiple specialized personas with domain expertise")
    print("• Automatic persona selection based on query analysis")
    print("• Dynamic user profile adaptation and learning")
    print("• Performance tracking and analytics for each persona")
    print("• Manual persona switching and recommendation system")
    print("="*50)