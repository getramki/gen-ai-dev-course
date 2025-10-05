# Part 6-A: EKS Deployment with Embedded Agents

## Overview
Deploy Part 4 agents to Amazon EKS with A2A communication across subdomains. Each agent runs in separate namespaces with embedded LangChain tools and external A2A communication.

## Architecture
```
EKS Cluster
├── part-a-purchase-ns → Purchase Agent ALB
├── part-a-cement-ns → Cement Agent ALB  
└── part-a-steel-ns → Steel Agent ALB
```

**A2A Communication**: Each agent gets dedicated ALB endpoint for inter-agent communication

## Prerequisites
- AWS CLI configured with ECR permissions
- eksctl installed
- kubectl installed
- Docker images from Part 4 built
- ECR repositories access

## Quick Start
```bash
# 1. Build Part 4 images (if not already built)
cd ../part-04-local-deployment/scripts/
./build.sh

# 2. Push images to ECR
cd ../../part-06a-eks-embedded-agents/scripts/
./push-to-ecr.sh

# 3. Create EKS cluster
cd ../eksctl/
eksctl create cluster -f cluster-config.yaml

# 4. Deploy agents (creates ALBs and updates endpoints)
cd ../scripts/
./deploy.sh

# 3. Restart deployments to pick up ALB endpoints
kubectl rollout restart deployment/purchase-agent -n part-a-purchase-ns
kubectl rollout restart deployment/cement-agent -n part-a-cement-ns
kubectl rollout restart deployment/steel-agent -n part-a-steel-ns

# 4. Wait for rollout completion
kubectl rollout status deployment/purchase-agent -n part-a-purchase-ns
kubectl rollout status deployment/cement-agent -n part-a-cement-ns
kubectl rollout status deployment/steel-agent -n part-a-steel-ns

# 5. Test negotiation
python negotiation_demo.py

# 6. Test autoscaling
./test-autoscaling.sh
```

## Components
- **EKS Cluster**: Multi-AZ cluster with managed node groups
- **Namespaces**: Isolated environments for each agent
- **ALB Ingress**: Separate Application Load Balancer per agent
- **ConfigMaps**: Dynamic ALB endpoint configuration
- **HPA**: Horizontal Pod Autoscaling
- **A2A Communication**: Cross-ALB agent communication

## ALB Endpoints
After deployment, each agent gets a unique ALB endpoint:
```bash
# View ALB endpoints
kubectl get ingress -A

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