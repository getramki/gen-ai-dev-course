#!/bin/bash
set -e

echo "🧪 Testing Horizontal Pod Autoscaling..."

# Check HPA status
echo "📊 Current HPA status:"
kubectl get hpa -A

# Generate load on purchase agent
echo "🔥 Generating load on purchase agent..."
kubectl run load-generator --image=busybox --restart=Never -n part-a-purchase-ns -- /bin/sh -c "while true; do wget -q -O- http://purchase-agent-service/health; done"

# Monitor scaling for 2 minutes
echo "👀 Monitoring scaling (2 minutes)..."
for i in {1..24}; do
    echo "--- Check $i/24 ---"
    kubectl get hpa purchase-agent-hpa -n part-a-purchase-ns
    kubectl get pods -n part-a-purchase-ns | grep purchase-agent
    sleep 5
done

# Cleanup load generator
echo "🧹 Cleaning up load generator..."
kubectl delete pod load-generator -n part-a-purchase-ns --ignore-not-found=true

echo "✅ Autoscaling test complete!"