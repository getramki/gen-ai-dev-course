#!/bin/bash
set -e

echo "🗑️ Deleting Construction Agents from EKS..."

# Delete HPA
echo "📉 Removing autoscaling..."
kubectl delete -f ../kubernetes/hpa/hpa.yaml --ignore-not-found=true

# Delete ingress with timeout
echo "🔗 Removing ingress and services..."
kubectl delete -f ../kubernetes/ingress/ingress.yaml --ignore-not-found=true --timeout=30s || {
    echo "⚠️ Ingress deletion timed out, force removing finalizers..."
    kubectl patch ingress construction-agents-ingress -n part-a-purchase-ns -p '{"metadata":{"finalizers":[]}}' --type=merge || true
    kubectl delete service construction-cement-agent construction-steel-agent construction-purchase-agent -n part-a-purchase-ns --force --grace-period=0 || true
    kubectl delete ingress construction-agents-ingress -n part-a-purchase-ns --force --grace-period=0 || true
}

# Delete original services
echo "🌐 Removing original services..."
kubectl delete -f ../kubernetes/services/services.yaml --ignore-not-found=true --timeout=30s || true

# Delete deployments
echo "🔧 Removing agents..."
kubectl delete -f ../kubernetes/deployments/ --ignore-not-found=true

# Delete ConfigMaps
echo "⚙️ Removing ConfigMaps..."
kubectl delete -f ../kubernetes/configmaps/alb-endpoints.yaml --ignore-not-found=true

# Delete namespaces with timeout
echo "📦 Removing namespaces..."
kubectl delete -f ../kubernetes/namespaces/namespaces.yaml --ignore-not-found=true --timeout=60s || {
    echo "⚠️ Namespace deletion timed out, force cleaning..."
    # Remove finalizers from stuck namespaces
    kubectl patch namespace part-a-purchase-ns -p '{"metadata":{"finalizers":[]}}' --type=merge || true
    kubectl patch namespace part-a-cement-ns -p '{"metadata":{"finalizers":[]}}' --type=merge || true
    kubectl patch namespace part-a-steel-ns -p '{"metadata":{"finalizers":[]}}' --type=merge || true
    # Force delete namespaces
    kubectl delete namespace part-a-purchase-ns part-a-cement-ns part-a-steel-ns --force --grace-period=0 || true
}

echo "✅ Deletion complete!"