#!/bin/bash
set -e

# Get AWS Account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=${AWS_REGION:-us-east-1}

echo "🔄 Updating deployment manifests with ECR URIs..."
echo "Account ID: ${AWS_ACCOUNT_ID}"
echo "Region: ${AWS_REGION}"

# Update deployment files with actual ECR URIs
sed -i "s/\${AWS_ACCOUNT_ID}/${AWS_ACCOUNT_ID}/g" ../kubernetes/deployments/*.yaml

echo "✅ Deployment manifests updated with ECR image URIs!"