#!/bin/bash
set -e

CLUSTER_NAME=${1:-"construction-agents"}
AWS_REGION=${2:-"us-east-1"}

echo "🚀 Creating EKS cluster: $CLUSTER_NAME in region: $AWS_REGION"

# Create EKS cluster
echo "📦 Creating EKS cluster..."
cd ../eksctl/
eksctl create cluster -f cluster-config.yaml
cd ../scripts/

# Disable Extended Support
echo "⚙️ Disabling Extended Support..."
aws eks update-cluster-config \
    --name $CLUSTER_NAME \
    --upgrade-policy supportType=STANDARD

# Tag subnets for ALB controller
echo "🏷️ Tagging subnets for ALB controller..."
./tag-subnets.sh

# Setup AWS Load Balancer Controller
echo "🔧 Setting up AWS Load Balancer Controller..."
./setup-alb-controller.sh $CLUSTER_NAME $AWS_REGION

echo "✅ Cluster setup complete!"
echo "Next steps:"
echo "1. Push images to ECR: ./push-to-ecr.sh"
echo "2. Deploy agents: ./deploy.sh"