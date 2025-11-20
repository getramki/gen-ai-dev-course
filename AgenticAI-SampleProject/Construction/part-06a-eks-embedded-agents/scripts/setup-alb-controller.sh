#!/bin/bash
set -e

# Variables - Update these with your cluster details
CLUSTER_NAME=${1:-"construction-agents"}
AWS_REGION=${2:-"us-east-1"}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)

echo "🚀 Setting up AWS Load Balancer Controller for EKS cluster: $CLUSTER_NAME"
echo "📍 Region: $AWS_REGION"
echo "🔑 Account ID: $AWS_ACCOUNT_ID"

# Verify cluster exists
echo "🔍 Verifying cluster exists..."
aws eks describe-cluster --name $CLUSTER_NAME --region $AWS_REGION --query "cluster.name" --output text

# Step 1: Create IAM OIDC provider
echo "🔐 Creating IAM OIDC provider..."
# Verify cluster exists first
echo "Checking if cluster exists..."
aws eks describe-cluster --name $CLUSTER_NAME --region $AWS_REGION --query "cluster.name" --output text
oidc_id=$(aws eks describe-cluster --name $CLUSTER_NAME --region $AWS_REGION --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
echo "OIDC ID: $oidc_id"

# Check if OIDC provider already exists
existing_provider=$(aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4 || echo "")
if [ -z "$existing_provider" ]; then
    echo "Creating OIDC provider..."
    eksctl utils associate-iam-oidc-provider --cluster $CLUSTER_NAME --region $AWS_REGION --approve
else
    echo "OIDC provider already exists"
fi

# Step 2: Download IAM policy
echo "📄 Downloading IAM policy..."
# curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.13.3/docs/install/iam_policy.json

# Step 3: Create IAM policy (if it doesn't exist)
echo "📋 Creating IAM policy..."
policy_exists=$(aws iam get-policy --policy-arn arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy 2>/dev/null || echo "")
if [ -z "$policy_exists" ]; then
    aws iam create-policy \
        --policy-name AWSLoadBalancerControllerIAMPolicy \
        --policy-document file://iam_policy.json
    echo "IAM policy created"
else
    echo "IAM policy already exists"
fi

# Step 4: Create service account and IAM role
echo "👤 Creating service account and IAM role..."
eksctl create iamserviceaccount \
    --cluster=$CLUSTER_NAME \
    --namespace=kube-system \
    --name=aws-load-balancer-controller \
    --attach-policy-arn=arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy \
    --override-existing-serviceaccounts \
    --region $AWS_REGION \
    --approve

# Step 5: Add Helm repository
echo "📦 Adding Helm repository..."
helm repo add eks https://aws.github.io/eks-charts
helm repo update eks

# Step 6: Install AWS Load Balancer Controller
echo "🔧 Installing AWS Load Balancer Controller..."
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=$CLUSTER_NAME \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --version 1.13.0

# Step 7: Verify installation
echo "✅ Verifying installation..."
kubectl wait --for=condition=available --timeout=300s deployment/aws-load-balancer-controller -n kube-system

echo "🎉 AWS Load Balancer Controller setup complete!"
echo ""
echo "📊 Controller status:"
kubectl get deployment -n kube-system aws-load-balancer-controller

# Cleanup
# rm -f iam_policy.json