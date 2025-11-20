#!/bin/bash
set -e

CLUSTER_NAME=${1:-"construction-agents"}

echo "🗑️ Cleaning up EKS cluster: $CLUSTER_NAME"

# Delete applications first
echo "🔧 Deleting applications..."
./delete.sh || {
    echo "⚠️ Application deletion had issues, continuing with force cleanup..."
    # Force cleanup any remaining resources
    kubectl delete all --all -A --force --grace-period=0 || true
    kubectl delete namespace part-a-purchase-ns part-a-cement-ns part-a-steel-ns --force --grace-period=0 || true
}

# Wait for ALB cleanup
echo "⏳ Waiting for ALB cleanup..."
sleep 30

# Force cleanup any remaining ALB resources
echo "💥 Force cleaning ALB resources..."
VPC_ID=$(aws eks describe-cluster --name $CLUSTER_NAME --query "cluster.resourcesVpcConfig.vpcId" --output text 2>/dev/null || echo "")
if [ -n "$VPC_ID" ] && [ "$VPC_ID" != "None" ]; then
    # Delete any remaining load balancers
    aws elbv2 describe-load-balancers --query "LoadBalancers[?VpcId=='$VPC_ID'].LoadBalancerArn" --output text | xargs -r -n1 aws elbv2 delete-load-balancer --load-balancer-arn || true
    
    # Delete any remaining target groups
    aws elbv2 describe-target-groups --query "TargetGroups[?VpcId=='$VPC_ID'].TargetGroupArn" --output text | xargs -r -n1 aws elbv2 delete-target-group --target-group-arn || true
    
    # Wait for ALB resources to be deleted
    sleep 30
fi

# Delete cluster with force flag to handle VPC dependencies
echo "💥 Deleting EKS cluster..."
eksctl delete cluster $CLUSTER_NAME --force || {
    echo "⚠️ Cluster deletion failed, trying with disable-nodegroup-eviction..."
    eksctl delete cluster $CLUSTER_NAME --disable-nodegroup-eviction --force
}

echo "✅ Cluster cleanup complete!"