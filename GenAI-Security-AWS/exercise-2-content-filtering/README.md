# Exercise 2: Content Filtering and Guardrails

## Objective
Implement Amazon Bedrock Guardrails and custom content filtering to prevent harmful, inappropriate, or policy-violating content in LLM applications.

## Learning Goals
- Configure Amazon Bedrock Guardrails
- Implement custom content filters
- Set up real-time content monitoring
- Create content moderation workflows
- Handle blocked content gracefully

## Prerequisites
- Completed Exercise 1 (IAM Security)
- Amazon Bedrock access configured
- Understanding of content moderation concepts

## Step-by-Step Instructions

### Step 1: Create Amazon Bedrock Guardrails

1. **Configure Content Filters**
   - Set up hate speech detection
   - Configure violence and self-harm filters
   - Implement sexual content filtering
   - Add misconduct prevention

2. **Set Up Topic Filters**
   - Define blocked topics
   - Configure topic-based restrictions
   - Implement contextual filtering

3. **Configure Word Filters**
   - Create profanity filters
   - Add custom blocked words
   - Set up regex-based filtering

### Step 2: Implement Custom Content Filtering

1. **Create pre-processing filters**
2. **Set up post-processing validation**
3. **Implement content scoring system**

### Step 3: Real-time Monitoring Setup

1. **Configure CloudWatch metrics**
2. **Set up alerting for policy violations**
3. **Create content audit logs**

### Step 4: Test Content Filtering

1. **Test with various content types**
2. **Validate filter effectiveness**
3. **Measure performance impact**

## Security Controls Implemented

- ✅ Hate speech prevention
- ✅ Violence and self-harm filtering
- ✅ Sexual content blocking
- ✅ Custom topic restrictions
- ✅ Real-time monitoring
- ✅ Audit logging

## Expected Outcomes

After completing this exercise, you will have:
- Configured Bedrock Guardrails for content safety
- Implemented custom content filtering logic
- Set up monitoring and alerting for content violations
- Created a robust content moderation system

## Testing Scenarios

Test your implementation with:
- Inappropriate content requests
- Edge cases and boundary conditions
- Performance under load
- False positive handling

## Next Steps

Proceed to Exercise 3 for monitoring, auditing, and compliance implementation.