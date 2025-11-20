Prerequisites

Before starting this tutorial, you must complete the following steps:

Create an Amazon EKS cluster. To create one, see Get started with Amazon EKS.

Install Helm on your local machine.

Make sure that your Amazon VPC CNI plugin for Kubernetes, kube-proxy, and CoreDNS add-ons are at the minimum versions listed in Service account tokens.

Learn about AWS Elastic Load Balancing concepts. For more information, see the Elastic Load Balancing User Guide.

Learn about Kubernetes service and ingress resources.

Considerations
Before proceeding with the configuration steps on this page, consider the following:

The IAM policy and role (AmazonEKSLoadBalancerControllerRole) can be reused across multiple EKS clusters in the same AWS account.

If you’re installing the controller on the same cluster where the role (AmazonEKSLoadBalancerControllerRole) was originally created, go to Step 2: Install Load Balancer Controller after verifying the role exists.

If you’re using IAM Roles for Service Accounts (IRSA), IRSA must be set up for each cluster, and the OpenID Connect (OIDC) provider ARN in the role’s trust policy is specific to each EKS cluster. Additionally, if you’re installing the controller on a new cluster with an existing AmazonEKSLoadBalancerControllerRole, update the role’s trust policy to include the new cluster’s OIDC provider and create a new service account with the appropriate role annotation. To determine whether you already have an OIDC provider, or to create one, see Create an IAM OIDC provider for your cluster.

Step 1: Create IAM Role using eksctl

The following steps refer to the AWS Load Balancer Controller v2.13.3 release version. For more information about all releases, see the AWS Load Balancer Controller Release Page on GitHub.

1. Download an IAM policy for the AWS Load Balancer Controller that allows it to make calls to AWS APIs on your behalf.

```bash
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.13.3/docs/install/iam_policy.json
```
If you are a non-standard AWS partition, such as a Government or China region, review the policies on GitHub and download the appropriate policy for your region.

2. Create an IAM policy using the policy downloaded in the previous step.

```bash
aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json
```
Note
If you view the policy in the AWS Management Console, the console shows warnings for the ELB service, but not for the ELB v2 service. This happens because some of the actions in the policy exist for ELB v2, but not for ELB. You can ignore the warnings for ELB.

3. Replace the values for cluster name, region code, and account ID.

```bash
eksctl create iamserviceaccount \
    --cluster=<cluster-name> \
    --namespace=kube-system \
    --name=aws-load-balancer-controller \
    --attach-policy-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy \
    --override-existing-serviceaccounts \
    --region <aws-region-code> \
    --approve
```
Step 2: Install AWS Load Balancer Controller

1. Add the eks-charts Helm chart repository. AWS maintains this repository on GitHub.

```bash
helm repo add eks https://aws.github.io/eks-charts
```
2. Update your local repo to make sure that you have the most recent charts.

```bash
helm repo update eks
```
3. Install the AWS Load Balancer Controller.

If you’re deploying the controller to Amazon EC2 nodes that have restricted access to the Amazon EC2 instance metadata service (IMDS), or if you’re deploying to Fargate or Amazon EKS Hybrid Nodes, then add the following flags to the helm command that follows:

--set region=region-code

--set vpcId=vpc-xxxxxxxx

Replace my-cluster with the name of your cluster. In the following command, aws-load-balancer-controller is the Kubernetes service account that you created in a previous step.

For more information about configuring the helm chart, see values.yaml on GitHub.

```bash
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=my-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --version 1.13.0
```
Important
The deployed chart doesn’t receive security updates automatically. You need to manually upgrade to a newer chart when it becomes available. When upgrading, change install to upgrade in the previous command.

The helm install command automatically installs the custom resource definitions (CRDs) for the controller. The helm upgrade command does not. If you use helm upgrade, you must manually install the CRDs. Run the following command to install the CRDs:

```bash
wget https://raw.githubusercontent.com/aws/eks-charts/master/stable/aws-load-balancer-controller/crds/crds.yaml
kubectl apply -f crds.yaml
```
Step 3: Verify that the controller is installed

1. Verify that the controller is installed.

```bash
kubectl get deployment -n kube-system aws-load-balancer-controller
```
An example output is as follows.

```bash
NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
aws-load-balancer-controller   2/2     2            2           84s
```
You receive the previous output if you deployed using Helm. If you deployed using the Kubernetes manifest, you only have one replica.

2. Before using the controller to provision AWS resources, your cluster must meet specific requirements. For more information, see Route application and HTTP traffic with Application Load Balancers and Route TCP and UDP traffic with Network Load Balancers.