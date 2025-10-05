#!/bin/bash
set -e

echo "🚀 Deploying Construction Agents to EKS..."

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
echo "Getting ALB endpoints..."
PURCHASE_ALB=$(kubectl get ingress purchase-agent-ingress -n part-a-purchase-ns -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
CEMENT_ALB=$(kubectl get ingress cement-agent-ingress -n part-a-cement-ns -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
STEEL_ALB=$(kubectl get ingress steel-agent-ingress -n part-a-steel-ns -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

echo "Purchase Agent: http://$PURCHASE_ALB"
echo "Cement Agent: http://$CEMENT_ALB"
echo "Steel Agent: http://$STEEL_ALB"

# Update ConfigMaps with actual ALB endpoints
echo ""
echo "🔄 Updating ConfigMaps with ALB endpoints..."
kubectl patch configmap alb-endpoints -n part-a-purchase-ns --patch "{\"data\":{\"purchase-endpoint\":\"http://$PURCHASE_ALB\",\"cement-endpoint\":\"http://$CEMENT_ALB\",\"steel-endpoint\":\"http://$STEEL_ALB\"}}"
kubectl patch configmap alb-endpoints -n part-a-cement-ns --patch "{\"data\":{\"purchase-endpoint\":\"http://$PURCHASE_ALB\",\"cement-endpoint\":\"http://$CEMENT_ALB\",\"steel-endpoint\":\"http://$STEEL_ALB\"}}"
kubectl patch configmap alb-endpoints -n part-a-steel-ns --patch "{\"data\":{\"purchase-endpoint\":\"http://$PURCHASE_ALB\",\"cement-endpoint\":\"http://$CEMENT_ALB\",\"steel-endpoint\":\"http://$STEEL_ALB\"}}"

echo "✅ ConfigMaps updated! Restart deployments to pick up new endpoints."
echo "kubectl rollout restart deployment/purchase-agent -n part-a-purchase-ns"
echo "kubectl rollout restart deployment/cement-agent -n part-a-cement-ns"
echo "kubectl rollout restart deployment/steel-agent -n part-a-steel-ns"