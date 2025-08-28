# Exercise 2: Specialized AI Assistant with Personas

## 🎯 **Objective**
Build a sophisticated AI assistant system with multiple specialized personas, automatic persona selection, and adaptive user profiling.

**Time**: 7 minutes  
**Difficulty**: Advanced  
**File**: `exercise_2_ai_assistant.py`

## 📋 **Step-by-Step Instructions**

### Step 1: Core Assistant Class Structure (2 minutes)
Create `SpecializedAIAssistant` class:
```python
class SpecializedAIAssistant:
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
        self.personas = self._initialize_personas()
```

### Step 2: Define Specialized Personas (1.5 minutes)
Implement `_initialize_personas()` with 6 personas:

**Technical Expert**:
- Domains: ["technology", "programming", "engineering"]
- System message: Focus on technical accuracy, code examples, best practices
- Specialties: software development, system design, debugging

**Business Consultant**:
- Domains: ["business", "strategy", "management"]
- System message: Frame solutions in business terms, emphasize ROI and efficiency
- Specialties: business strategy, ROI analysis, project management

**Creative Mentor**:
- Domains: ["creative", "design", "innovation"]
- System message: Encourage innovative thinking, use analogies and storytelling
- Specialties: creative thinking, innovation, design

**Educator**:
- Domains: ["education", "learning", "training"]
- System message: Patient teaching, step-by-step explanations, check understanding
- Specialties: teaching, curriculum design, skill development

**Researcher**:
- Domains: ["research", "analysis", "data"]
- System message: Evidence-based insights, balanced perspectives, cite sources
- Specialties: data analysis, research methodology, critical thinking

### Step 3: Automatic Persona Detection (1.5 minutes)
Implement `_detect_optimal_persona()` method:
- Create keyword mapping for each persona domain
- Score personas based on keyword matches in user input
- Return highest scoring persona or "general" as fallback

**Keyword Examples**:
```python
domain_keywords = {
    "technical_expert": ["code", "programming", "software", "debug", "api"],
    "business_consultant": ["business", "strategy", "roi", "profit", "market"],
    "creative_mentor": ["creative", "design", "brainstorm", "innovative"],
    "educator": ["learn", "teach", "explain", "understand", "study"],
    "researcher": ["research", "analyze", "data", "evidence", "methodology"]
}
```

### Step 4: User Profile Adaptation (1 minute)
Implement `_adapt_persona_to_user_profile()` and `_update_user_profile()`:

**Profile Adaptation**:
- Modify system message based on user expertise level (beginner/advanced)
- Adjust communication style (concise/detailed)
- Incorporate user preferences into persona behavior

**Profile Updates**:
- Track domain interests from persona usage
- Update expertise level based on interaction patterns
- Maintain interaction history with timestamps

### Step 5: Core Message Processing (1 minute)
Implement `send_message()` method:
1. Detect optimal persona (or use forced persona)
2. Adapt persona to user profile
3. Build conversation context with system message + history
4. Get ChatBedrockConverse response
5. Update conversation history and user profile
6. Track persona performance metrics
7. Return structured result with metadata

## ✅ **Expected Output**
```
=== Specialized AI Assistant Demo ===

Scenario 1: I need help debugging a Python function that's not working correctly.
🎯 Recommended persona: technical_expert
🤖 Technical Expert: I'd be happy to help you debug your Python function. To provide the most effective assistance...
📊 Processing time: 1.45s
👤 User expertise level: intermediate

Scenario 4: How can I brainstorm innovative features for my mobile app?
🎯 Recommended persona: creative_mentor
🤖 Creative Mentor: What an exciting challenge! Let's unlock your creative potential and explore some innovative directions...
📊 Processing time: 1.32s
👤 User expertise level: intermediate

📈 Final Assistant Analytics:
   Total interactions: 5
   User interests: ['technology', 'business', 'education', 'creative', 'research']
   Current expertise level: intermediate

🎭 Persona Usage Statistics:
   technical_expert: 1 uses, avg response: 287 chars
   business_consultant: 1 uses, avg response: 245 chars
   educator: 1 uses, avg response: 298 chars
```

## 🔧 **Common Issues**

**Issue**: Persona detection not working accurately
**Solution**: Refine keyword lists and scoring algorithm, add more domain-specific terms

**Issue**: User profile not adapting properly
**Solution**: Ensure `_update_user_profile()` is called after each interaction

**Issue**: System messages too generic
**Solution**: Make persona system messages more specific and actionable

**Issue**: Performance tracking inaccurate
**Solution**: Verify timing measurements and metric calculations

## 🚀 **Challenge Extensions**
1. **Sentiment-Aware Personas**: Adapt persona behavior based on user sentiment
2. **Learning Personas**: Personas that improve based on user feedback
3. **Multi-language Support**: Personas that adapt to different languages
4. **Context-Aware Switching**: Switch personas mid-conversation based on topic changes
5. **Persona Effectiveness Scoring**: Rate persona performance based on user satisfaction

### Sentiment-Aware Extension:
```python
def _analyze_user_sentiment(self, user_input):
    positive_indicators = ["great", "excellent", "love", "amazing"]
    negative_indicators = ["frustrated", "confused", "difficult", "problem"]
    
    pos_count = sum(1 for word in positive_indicators if word in user_input.lower())
    neg_count = sum(1 for word in negative_indicators if word in user_input.lower())
    
    if neg_count > pos_count:
        return "supportive"  # Use more encouraging persona
    return "standard"
```

### Context-Aware Switching Extension:
```python
def _detect_topic_shift(self, new_input, conversation_history):
    # Analyze if user has shifted to a different domain
    # Switch persona automatically if significant topic change detected
    pass
```

## 📋 **Completion Checklist**
- [ ] SpecializedAIAssistant class with all core components
- [ ] Six specialized personas with distinct characteristics
- [ ] Automatic persona detection based on keyword analysis
- [ ] User profile adaptation and learning system
- [ ] Performance tracking for each persona
- [ ] Manual persona switching functionality
- [ ] Persona recommendation system working
- [ ] Demo scenarios run successfully with appropriate persona selection
- [ ] Analytics show persona usage statistics
- [ ] Error handling prevents system crashes

## 🎓 **Learning Outcomes**
After completing this exercise, you will understand:
- Advanced persona system design and implementation
- Automatic context detection and persona selection
- User profiling and adaptive AI behavior
- Performance monitoring for AI system components
- Production-ready conversation management with multiple AI personalities
- Dynamic system message generation and optimization