# Part 6-A: EKS Deployment with Embedded Agents

## Overview
Deploy Part 4 agents to Amazon EKS with A2A communication. Each agent runs in separate namespaces with embedded LangChain tools and external A2A communication via a single ALB.

## Architecture
```
EKS Cluster
├── part-a-purchase-ns → Purchase Agent (/purchase)
├── part-a-cement-ns → Cement Agent (/cement)
└── part-a-steel-ns → Steel Agent (/steel)
     ↓
   Single ALB (Path-based routing)
```

**A2A Communication**: Single ALB with path-based routing for each agent

## Prerequisites
- AWS CLI configured with appropriate permissions
- eksctl installed (v0.214.0+)
- kubectl installed
- Helm installed
- Docker images from Part 4 built
- ECR repositories access

## Training Setup (Multiple Batches)
This setup is designed for conducting multiple training batches with complete cluster lifecycle management.

## Complete Setup (New Training Batch)

### 1. Initial Setup (One-time per batch)
```bash
# Build Part 4 images (if not already built)
cd ../part-04-local-deployment/scripts/
./build.sh

# Push images to ECR
cd ../../part-06a-eks-embedded-agents/scripts/
./push-to-ecr.sh

# Create complete EKS setup (cluster + ALB controller + subnet tags)
./create-cluster.sh construction-agents us-east-1
```

### 2. Deploy Applications
```bash
# Deploy agents (automatically checks prerequisites)
./deploy.sh

# Wait for ALB creation and get endpoints
echo "Waiting for ALB creation..."
sleep 60
kubectl get ingress -A

# Test the deployment
python negotiation_demo.py
./test-autoscaling.sh
```

### 3. Cleanup (End of batch)
```bash
# Complete cleanup (applications + cluster)
./cleanup-cluster.sh construction-agents
```

## Quick Commands
```bash
# Full setup
./create-cluster.sh && ./deploy.sh

# Full cleanup  
./cleanup-cluster.sh

# Redeploy applications only
./delete.sh && ./deploy.sh
```

## Components
- **EKS Cluster**: Multi-AZ cluster with managed node groups
- **Namespaces**: Isolated environments for each agent
- **ALB Ingress**: Single Application Load Balancer with path-based routing
- **ConfigMaps**: Dynamic ALB endpoint configuration
- **HPA**: Horizontal Pod Autoscaling
- **A2A Communication**: Cross-ALB agent communication

## ALB Endpoints
After deployment, agents share a single ALB with different ports:
```bash
# View ALB endpoint
kubectl get ingress construction-agents-ingress -n part-a-purchase-ns

# Check ConfigMap values
kubectl get configmap alb-endpoints -n part-a-purchase-ns -o yaml
```

## Monitoring
- CloudWatch Container Insights
- ALB access logs
- Kubernetes Dashboard
- Application logs via kubectl

## Troubleshooting
```bash
# Check ALB status
kubectl describe ingress -A

# Verify ConfigMap updates
kubectl get configmap alb-endpoints -A

# Check agent environment variables
kubectl exec -n part-a-purchase-ns deployment/purchase-agent -- env | grep A2A
```

## Cleanup
```bash
eksctl delete cluster construction-agents
```