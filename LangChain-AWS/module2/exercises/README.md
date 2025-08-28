# Module 2 Exercises

## Overview
This directory contains hands-on exercises for Module 2: Setup and Environment.

## Exercise Files

### 📝 **Exercise 1: Complete AWS Environment Setup**
- **Code File**: `exercise_1_aws_setup.py`
- **Instructions**: `exercise_1_instructions.md`
- **Time**: 5 minutes
- **Focus**: AWS credentials, Bedrock access, model permissions

### 📝 **Exercise 2: LangChain-Bedrock Integration Test**
- **Code File**: `exercise_2_langchain_test.py`
- **Instructions**: `exercise_2_instructions.md`
- **Time**: 5 minutes
- **Focus**: ChatBedrock vs ChatBedrockConverse, integration testing

## Prerequisites

### Before Starting:
- [ ] AWS Account with Bedrock access
- [ ] AWS CLI installed and configured
- [ ] Python 3.8+ with virtual environment
- [ ] Module 1 completed successfully

### Required Permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:ListFoundationModels",
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "*"
    }
  ]
}
```

## Quick Start

### Setup Environment
```bash
# Navigate to module2
cd module2

# Install dependencies
pip install -r requirements.txt

# Configure AWS (choose one method)
aws configure
# OR create .env file with credentials
```

### Run Exercises
```bash
# Navigate to exercises
cd exercises

# Run Exercise 1 - AWS Setup
python exercise_1_aws_setup.py

# Run Exercise 2 - Integration Test
python exercise_2_langchain_test.py
```

## Exercise Workflow

### Exercise 1: AWS Environment Setup
1. **Configure credentials** (environment variables or AWS profile)
2. **Test connectivity** with AWS STS service
3. **Verify Bedrock access** and list available models
4. **Test model permissions** for Claude models
5. **Generate configuration** file for future use

### Exercise 2: LangChain Integration
1. **Initialize both chat models** (ChatBedrock and ChatBedrockConverse)
2. **Test basic invocation** with simple messages
3. **Verify conversation flow** with multi-turn dialogue
4. **Test prompt templates** and chain composition
5. **Validate streaming** capabilities
6. **Compare performance** and generate report

## Expected Outcomes

### After Exercise 1:
- ✅ AWS credentials properly configured
- ✅ Bedrock service accessible
- ✅ Claude models available for use
- ✅ Configuration file created
- ✅ Setup score ≥ 80%

### After Exercise 2:
- ✅ Both ChatBedrock and ChatBedrockConverse working
- ✅ LangChain chains functional with Bedrock
- ✅ Streaming responses operational
- ✅ Performance metrics collected
- ✅ Integration test score ≥ 80%

## Troubleshooting

### Common Issues:

**AWS Credentials Not Found**:
```bash
# Solution 1: Use AWS CLI
aws configure

# Solution 2: Environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

**Bedrock Access Denied**:
- Check IAM permissions for Bedrock actions
- Verify region supports Bedrock (us-east-1, us-west-2, eu-west-1)

**Model Access Denied**:
- Go to AWS Console → Bedrock → Model access
- Request access for Claude models
- Wait for approval (usually immediate)

**Import Errors**:
```bash
# Reinstall LangChain AWS integration
pip install --upgrade langchain-aws boto3
```

## Success Criteria

### Module 2 Completion Requirements:
- [ ] Exercise 1 setup score ≥ 80%
- [ ] Exercise 2 integration score ≥ 80%
- [ ] Both ChatBedrock and ChatBedrockConverse functional
- [ ] Configuration files created successfully
- [ ] No critical errors in test reports

## Next Steps

After completing Module 2:
- **Module 3**: ChatBedrock Fundamentals
- **Module 4**: ChatBedrockConverse Advanced Features
- **Module 5**: Practical Applications
- **Module 6**: Advanced Patterns and Production

## Files Generated

After successful completion, you should have:
- `aws_config.json` - AWS configuration and validation results
- Test reports showing integration status
- Working examples of both chat model types

## Support Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [LangChain AWS Integration](https://python.langchain.com/docs/integrations/providers/aws)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)