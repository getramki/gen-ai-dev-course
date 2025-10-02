# Exercise 1: IAM Security and Access Control for Amazon Bedrock

## Objective
Learn to implement secure IAM policies and access controls for Amazon Bedrock applications, following the principle of least privilege.

## Learning Goals
- Create IAM roles with minimal required permissions
- Implement resource-based access controls
- Set up cross-account access securely
- Configure service-linked roles for Bedrock

## Prerequisites
- AWS CLI configured with administrative permissions
- Basic understanding of IAM concepts
- Access to AWS Management Console

## Step-by-Step Instructions

### Step 1: Create a Bedrock Service Role

1. **Create IAM Role for Bedrock Application**
   ```bash
   aws iam create-role \
     --role-name BedrockApplicationRole \
     --assume-role-policy-document file://trust-policy.json
   ```

2. **Attach the custom policy**
   ```bash
   aws iam attach-role-policy \
     --role-name BedrockApplicationRole \
     --policy-arn arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):policy/BedrockMinimalAccessPolicy
   ```

### Step 2: Configure Cross-Account Access

1. **Create cross-account trust policy**
2. **Set up resource sharing with specific accounts**
3. **Test cross-account access**

### Step 3: Implement Resource-Based Policies

1. **Create model-specific access policies**
2. **Configure region-based restrictions**
3. **Set up time-based access controls**

### Step 4: Test and Validate

1. **Test role assumption**
2. **Validate minimal permissions**
3. **Verify access restrictions**

## Security Best Practices Implemented

- ✅ Principle of least privilege
- ✅ Resource-based access control
- ✅ Cross-account security
- ✅ Temporary credentials usage
- ✅ Regular permission auditing

## Expected Outcomes

After completing this exercise, you will have:
- A secure IAM role for Bedrock applications
- Understanding of resource-based policies
- Knowledge of cross-account access patterns
- Ability to audit and monitor IAM usage

## Troubleshooting

Common issues and solutions:
- **Access Denied**: Check policy attachments and trust relationships
- **Cross-Account Issues**: Verify external ID and account numbers
- **Permission Errors**: Review CloudTrail logs for detailed error information

## Next Steps

Proceed to Exercise 2 to learn about content filtering and guardrails.