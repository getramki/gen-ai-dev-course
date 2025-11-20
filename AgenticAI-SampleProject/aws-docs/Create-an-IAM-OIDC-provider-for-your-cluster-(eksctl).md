Create OIDC provider (eksctl)

1. Version 0.214.0 or later of the eksctl command line tool installed on your device or AWS CloudShell. To install or update eksctl, see Installation in the eksctl documentation.

2. Determine the OIDC issuer ID for your cluster.

Retrieve your cluster’s OIDC issuer ID and store it in a variable. Replace <my-cluster> with your own value.

```bash
cluster_name=<my-cluster>
oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
echo $oidc_id
```
3. Determine whether an IAM OIDC provider with your cluster’s issuer ID is already in your account.

```bash
aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4
```
If output is returned, then you already have an IAM OIDC provider for your cluster and you can skip the next step. If no output is returned, then you must create an IAM OIDC provider for your cluster.

4. Create an IAM OIDC identity provider for your cluster with the following command.

```bash
eksctl utils associate-iam-oidc-provider --cluster $cluster_name --approve
```