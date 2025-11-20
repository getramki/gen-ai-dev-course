#!/bin/bash
set -e

echo "🚀 Deploying Construction Agents to EKS..."

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check if AWS Load Balancer Controller is installed
if ! kubectl get deployment aws-load-balancer-controller -n kube-system &>/dev/null; then
    echo "❌ AWS Load Balancer Controller not found!"
    echo "Please run: ./create-cluster.sh or ./setup-alb-controller.sh <cluster-name> <region>"
    exit 1
fi
echo "✅ AWS Load Balancer Controller found"

# Check if subnets are tagged
CLUSTER_NAME=$(kubectl config current-context | cut -d'/' -f2 | cut -d'.' -f1 | sed 's/.*@//')
echo "Using cluster name: $CLUSTER_NAME"
VPC_ID=$(aws eks describe-cluster --name $CLUSTER_NAME --query "cluster.resourcesVpcConfig.vpcId" --output text)
TAGGED_SUBNETS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=tag-key,Values=kubernetes.io/role/elb" --query "Subnets[0].SubnetId" --output text)
if [ "$TAGGED_SUBNETS" = "None" ]; then
    echo "⚠️ Subnets not tagged for ALB controller. Running subnet tagging..."
    ./tag-subnets.sh
else
    echo "✅ Subnets properly tagged"
fi

# Update image URIs with current AWS Account ID
echo "🔄 Updating ECR image URIs..."
./update-image-uris.sh

# Apply namespaces
echo "📦 Creating namespaces..."
kubectl apply -f ../kubernetes/namespaces/namespaces.yaml

# Apply ConfigMaps
echo "⚙️ Creating ConfigMaps..."
kubectl apply -f ../kubernetes/configmaps/alb-endpoints.yaml

# Apply deployments
echo "🔧 Deploying agents..."
kubectl apply -f ../kubernetes/deployments/

# Apply services
echo "🌐 Creating services..."
kubectl apply -f ../kubernetes/services/services.yaml

# Apply ingress
echo "🔗 Setting up ingress..."
kubectl apply -f ../kubernetes/ingress/ingress.yaml

# Wait for ingress to be ready
echo "⏳ Waiting for ingress to be ready..."
sleep 180

# Apply HPA
echo "📈 Configuring autoscaling..."
kubectl apply -f ../kubernetes/hpa/hpa.yaml

# Wait for deployments
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/purchase-agent -n part-a-purchase-ns
kubectl wait --for=condition=available --timeout=300s deployment/cement-agent -n part-a-cement-ns
kubectl wait --for=condition=available --timeout=300s deployment/steel-agent -n part-a-steel-ns

echo "✅ Deployment complete!"
echo ""
echo "📊 Status:"
kubectl get pods -n part-a-purchase-ns
kubectl get pods -n part-a-cement-ns
kubectl get pods -n part-a-steel-ns
echo ""
echo "🔗 ALB Endpoints:"
echo "Getting ALB endpoint..."
ALB_HOSTNAME=$(kubectl get ingress construction-agents-ingress -n part-a-purchase-ns -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

echo "ALB DNS Name: $ALB_HOSTNAME"
echo "Purchase Agent: http://$ALB_HOSTNAME/purchase"
echo "Cement Agent: http://$ALB_HOSTNAME/cement"
echo "Steel Agent: http://$ALB_HOSTNAME/steel"

# Update ConfigMaps with actual ALB endpoints
echo ""
echo "🔄 Updating ConfigMaps with ALB endpoints..."
kubectl patch configmap alb-endpoints -n part-a-purchase-ns --patch "{\"data\":{\"purchase-endpoint\":\"http://$ALB_HOSTNAME/purchase\",\"cement-endpoint\":\"http://$ALB_HOSTNAME/cement\",\"steel-endpoint\":\"http://$ALB_HOSTNAME/steel\"}}"
kubectl patch configmap alb-endpoints -n part-a-cement-ns --patch "{\"data\":{\"purchase-endpoint\":\"http://$ALB_HOSTNAME/purchase\",\"cement-endpoint\":\"http://$ALB_HOSTNAME/cement\",\"steel-endpoint\":\"http://$ALB_HOSTNAME/steel\"}}"
kubectl patch configmap alb-endpoints -n part-a-steel-ns --patch "{\"data\":{\"purchase-endpoint\":\"http://$ALB_HOSTNAME/purchase\",\"cement-endpoint\":\"http://$ALB_HOSTNAME/cement\",\"steel-endpoint\":\"http://$ALB_HOSTNAME/steel\"}}"

echo "✅ ConfigMaps updated! Restart deployments to pick up new endpoints."
echo "kubectl rollout restart deployment/purchase-agent -n part-a-purchase-ns"
echo "kubectl rollout restart deployment/cement-agent -n part-a-cement-ns"
echo "kubectl rollout restart deployment/steel-agent -n part-a-steel-ns"