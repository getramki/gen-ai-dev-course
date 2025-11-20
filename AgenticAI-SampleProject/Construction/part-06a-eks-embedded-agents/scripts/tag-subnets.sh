#!/bin/bash
set -e

echo "🏷️ Adding required tags to EKS subnets for ALB controller..."

CLUSTER_NAME="construction-agents"
VPC_ID=$(aws eks describe-cluster --name $CLUSTER_NAME --query "cluster.resourcesVpcConfig.vpcId" --output text)
echo "Cluster VPC ID: $VPC_ID"

# Get all subnets in the VPC
SUBNETS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[*].SubnetId" --output text)

echo "Found subnets: $SUBNETS"

# Tag each subnet
for subnet in $SUBNETS; do
    echo "Processing subnet: $subnet"
    
    # Check if subnet has internet gateway route (public subnet)
    ROUTE_TABLE=$(aws ec2 describe-route-tables --filters "Name=association.subnet-id,Values=$subnet" --query "RouteTables[0].RouteTableId" --output text)
    
    if [ "$ROUTE_TABLE" != "None" ]; then
        # Check if route table has internet gateway route
        IGW_ROUTE=$(aws ec2 describe-route-tables --route-table-ids $ROUTE_TABLE --query "RouteTables[0].Routes[?GatewayId!=null && starts_with(GatewayId, 'igw-')]" --output text)
        
        if [ -n "$IGW_ROUTE" ]; then
            echo "  Tagging $subnet as public subnet (elb)"
            aws ec2 create-tags --resources $subnet --tags Key=kubernetes.io/role/elb,Value=1
        else
            echo "  Tagging $subnet as private subnet (internal-elb)"
            aws ec2 create-tags --resources $subnet --tags Key=kubernetes.io/role/internal-elb,Value=1
        fi
    else
        echo "  Tagging $subnet as private subnet (internal-elb) - no route table"
        aws ec2 create-tags --resources $subnet --tags Key=kubernetes.io/role/internal-elb,Value=1
    fi
done

echo "✅ Subnet tagging complete!"

# Verify tags
echo ""
echo "Verifying tags..."
./check-subnet-tags.sh