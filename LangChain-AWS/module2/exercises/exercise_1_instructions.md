# Exercise 1: Complete AWS Environment Setup

## 🎯 **Objective**
Set up and verify complete AWS environment for LangChain integration with comprehensive validation and troubleshooting.

**Time**: 5 minutes  
**Difficulty**: Beginner  
**File**: `exercise_1_aws_setup.py`

## 📋 **Step-by-Step Instructions**

### Step 1: Environment Configuration (1 minute)
Create `.env` file with AWS credentials:
```bash
# Copy template and add your credentials
cp .env.template .env
# Edit .env with your AWS credentials
```

**Required variables**:
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key  
- `AWS_DEFAULT_REGION` - Default region (us-east-1 recommended)

**Alternative**: Use AWS CLI profile instead of environment variables

### Step 2: Implement AWSSetupValidator Class (2 minutes)
Create the validator class with these methods:

**`load_environment()`**:
- Load environment variables using `python-dotenv`
- Check for both environment variables and AWS profiles
- Return configuration dictionary

**`test_aws_connectivity()`**:
- Use `boto3.client('sts')` to test basic connectivity
- Call `get_caller_identity()` to verify credentials
- Store account ID and user ARN

**`test_bedrock_access()`**:
- Create `boto3.client('bedrock')` 
- Call `list_foundation_models()` to test service access
- Count available models

### Step 3: Model Access Validation (1.5 minutes)
**`test_model_access()`**:
- Test specific models: Claude-3 Haiku and Sonnet
- Use `bedrock-runtime` client with `invoke_model()`
- Handle `AccessDeniedException` vs `ValidationException`
- ValidationException means model exists but request format is wrong (good!)

**Test payload for Claude**:
```python
test_body = json.dumps({
    "prompt": "\n\nHuman: Hi\n\nAssistant:",
    "max_tokens_to_sample": 1
})
```

### Step 4: Configuration File Creation (30 seconds)
**`create_config_file()`**:
- Save validation results to `aws_config.json`
- Include region settings, available models, and test results
- Use for future module configurations

### Step 5: Report Generation and Scoring (30 seconds)
**`generate_setup_report()`**:
- Display formatted results for each validation step
- Show specific error messages for failed checks
- Provide actionable next steps

**`get_setup_score()`**:
- Calculate percentage of successful validations
- Return score out of 5 total checks

## ✅ **Expected Output**
```
=== AWS Setup Validation Report ===

Environment: ✅
  Method: environment_vars
  Region: us-east-1

AWS Connectivity: ✅
  Account: 123456789012
  User: arn:aws:iam::123456789012:user/username

Bedrock Service: ✅
  Available Models: 15
  Sample: anthropic.claude-3-sonnet, amazon.titan-text-express-v1

Model Access:
  ✅ anthropic.claude-3-haiku-20240307-v1:0
  ✅ anthropic.claude-3-sonnet-20240229-v1:0

Configuration File: ✅
  Saved to: aws_config.json

Setup Score: 5/5 (100%)
🚀 Perfect! AWS environment is fully configured.
```

## 🔧 **Common Issues**

**Issue**: No AWS credentials found
**Solution**: 
```bash
aws configure
# OR set environment variables in .env file
```

**Issue**: Access denied to Bedrock
**Solution**: 
- Check IAM permissions for `bedrock:*` actions
- Verify region supports Bedrock service

**Issue**: Model access denied
**Solution**:
- Go to AWS Console → Bedrock → Model access
- Request access for Claude models
- Wait for approval (usually immediate)

**Issue**: Region not supported
**Solution**: Use supported regions: us-east-1, us-west-2, eu-west-1

## 🚀 **Challenge Extensions**
1. **Multi-region Testing**: Test Bedrock availability across multiple regions
2. **Permission Validation**: Check specific IAM permissions programmatically
3. **Cost Estimation**: Add pricing information for different models
4. **Automated Fixes**: Implement automatic model access requests
5. **Health Monitoring**: Create ongoing health check system

### Multi-region Extension Hint:
```python
def test_multiple_regions(self):
    regions = ['us-east-1', 'us-west-2', 'eu-west-1']
    for region in regions:
        # Test Bedrock availability in each region
        pass
```

## 📋 **Completion Checklist**
- [ ] Environment variables or AWS profile configured
- [ ] AWS connectivity test passes
- [ ] Bedrock service accessible
- [ ] At least one Claude model accessible
- [ ] Configuration file created successfully
- [ ] Setup score is 80% or higher
- [ ] All error messages are actionable

## 🎓 **Learning Outcomes**
After completing this exercise, you will understand:
- AWS credential management best practices
- Bedrock service architecture and permissions
- Model access request process
- Programmatic AWS service validation
- Configuration management for ML applications
- Error handling for cloud service integration