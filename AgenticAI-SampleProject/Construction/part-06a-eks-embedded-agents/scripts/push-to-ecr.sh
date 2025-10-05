#!/bin/bash
set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

echo "🚀 Pushing Part 4 images to ECR..."
echo "Registry: ${ECR_REGISTRY}"

# Login to ECR
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}

# Create ECR repositories if they don't exist
echo "📦 Creating ECR repositories..."
for repo in construction-purchase-agent construction-cement-agent construction-steel-agent; do
    aws ecr describe-repositories --repository-names ${repo} --region ${AWS_REGION} 2>/dev/null || \
    aws ecr create-repository --repository-name ${repo} --region ${AWS_REGION}
done

# Tag and push images
echo "🏷️ Tagging and pushing images..."

# Purchase Agent
docker tag construction-purchase-agent:latest ${ECR_REGISTRY}/construction-purchase-agent:latest
docker push ${ECR_REGISTRY}/construction-purchase-agent:latest

# Cement Agent
docker tag construction-cement-agent:latest ${ECR_REGISTRY}/construction-cement-agent:latest
docker push ${ECR_REGISTRY}/construction-cement-agent:latest

# Steel Agent
docker tag construction-steel-agent:latest ${ECR_REGISTRY}/construction-steel-agent:latest
docker push ${ECR_REGISTRY}/construction-steel-agent:latest

echo "✅ All images pushed to ECR!"
echo ""
echo "📋 ECR Image URIs:"
echo "Purchase: ${ECR_REGISTRY}/construction-purchase-agent:latest"
echo "Cement: ${ECR_REGISTRY}/construction-cement-agent:latest"
echo "Steel: ${ECR_REGISTRY}/construction-steel-agent:latest"