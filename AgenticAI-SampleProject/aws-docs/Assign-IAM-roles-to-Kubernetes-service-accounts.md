Step 1: Create IAM Policy

If you want to associate an existing IAM policy to your IAM role, skip to the next step.

1. Create an IAM policy. You can create your own policy, or copy an AWS managed policy that already grants some of the permissions that you need and customize it to your specific requirements. For more information, see Creating IAM policies in the IAM User Guide.

2. Create a file that includes the permissions for the AWS services that you want your Pods to access. For a list of all actions for all AWS services, see the Service Authorization Reference.

You can run the following command to create an example policy file that allows read-only access to an Amazon S3 bucket. You can optionally store configuration information or a bootstrap script in this bucket, and the containers in your Pod can read the file from the bucket and load it into your application. If you want to create this example policy, copy the following contents to your device. Replace my-pod-secrets-bucket with your bucket name and run the command.

```bash
cat >my-policy.json <<EOF
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-pod-secrets-bucket"
        }
    ]
}
EOF
```
3. Create the IAM policy.

```bash
aws iam create-policy --policy-name my-policy --policy-document file://my-policy.json
```

Step 2: Create and associate IAM Role

Create an IAM role and associate it with a Kubernetes service account. You can use either eksctl or the AWS CLI.

Create and associate role (eksctl)
This eksctl command creates a Kubernetes service account in the specified namespace, creates an IAM role (if it doesn’t exist) with the specified name, attaches an existing IAM policy ARN to the role, and annotates the service account with the IAM role ARN. Be sure to replace the sample placeholder values in this command with your specific values. To install or update eksctl, see Installation in the eksctl documentation.

```bash
eksctl create iamserviceaccount --name my-service-account --namespace default --cluster my-cluster --role-name my-role \
    --attach-policy-arn arn:aws:iam::111122223333:policy/my-policy --approve
```
Important
If the role or service account already exist, the previous command might fail. eksctl has different options that you can provide in those situations. For more information run eksctl create iamserviceaccount --help.

Create and associate role (AWS CLI)
If you have an existing Kubernetes service account that you want to assume an IAM role, then you can skip this step.

1. Create a Kubernetes service account. Copy the following contents to your device. Replace my-service-account with your desired name and default with a different namespace, if necessary. If you change default, the namespace must already exist.

```bash
cat >my-service-account.yaml <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service-account
  namespace: default
EOF
kubectl apply -f my-service-account.yaml
```
2. Set your AWS account ID to an environment variable with the following command.

```bash
account_id=$(aws sts get-caller-identity --query "Account" --output text)
```
3. Set your cluster’s OIDC identity provider to an environment variable with the following command. Replace my-cluster with the name of your cluster.

```bash
oidc_provider=$(aws eks describe-cluster --name my-cluster --region $AWS_REGION --query "cluster.identity.oidc.issuer" --output text | sed -e "s/^https:\/\///")
```
4. Set variables for the namespace and name of the service account. Replace my-service-account with the Kubernetes service account that you want to assume the role. Replace default with the namespace of the service account.

```bash
export namespace=default
export service_account=my-service-
```
5. Run the following command to create a trust policy file for the IAM role. If you want to allow all service accounts within a namespace to use the role, then copy the following contents to your device. Replace StringEquals with StringLike and replace $service_account with *. You can add multiple entries in the StringEquals or StringLike conditions to allow multiple service accounts or namespaces to assume the role. To allow roles from a different AWS account than the account that your cluster is in to assume the role, see Authenticate to another account with IRSA for more information.

```bash
cat >trust-relationship.json <<EOF
{
  "Version": "2012-10-17",		 	 	 
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::$account_id:oidc-provider/$oidc_provider"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "$oidc_provider:aud": "sts.amazonaws.com",
          "$oidc_provider:sub": "system:serviceaccount:$namespace:$service_account"
        }
      }
    }
  ]
}
EOF
```
6. Create the role. Replace my-role with a name for your IAM role, and my-role-description with a description for your role.

```bash
aws iam create-role --role-name my-role --assume-role-policy-document file://trust-relationship.json --description "my-role-description"
```

7. Attach an IAM policy to your role. Replace my-role with the name of your IAM role and my-policy with the name of an existing policy that you created.

```bash
aws iam attach-role-policy --role-name my-role --policy-arn=arn:aws:iam::$account_id:policy/my-policy
```
8. Annotate your service account with the Amazon Resource Name (ARN) of the IAM role that you want the service account to assume. Replace my-role with the name of your existing IAM role. Suppose that you allowed a role from a different AWS account than the account that your cluster is in to assume the role in a previous step. Then, make sure to specify the AWS account and role from the other account. For more information, see Authenticate to another account with IRSA.

```bash
kubectl annotate serviceaccount -n $namespace $service_account eks.amazonaws.com/role-arn=arn:aws:iam::$account_id:role/my-role
```
9. (Optional) Configure the AWS Security Token Service endpoint for a service account. AWS recommends using a regional AWS STS endpoint instead of the global endpoint. This reduces latency, provides built-in redundancy, and increases session token validity.

Step 3: Confirm configuration

1. Confirm that the IAM role’s trust policy is configured correctly.

```bash
aws iam get-role --role-name my-role --query Role.AssumeRolePolicyDocument
```
An example output is as follows.
```json
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:default:my-service-account",
                    "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com"
                }
            }
        }
    ]
}
```
2. Confirm that the policy that you attached to your role in a previous step is attached to the role.

```bash
aws iam list-attached-role-policies --role-name my-role --query "AttachedPolicies[].PolicyArn" --output text
```
An example output is as follows.

```bash
arn:aws:iam::111122223333:policy/my-policy
```
3. Set a variable to store the Amazon Resource Name (ARN) of the policy that you want to use. Replace my-policy with the name of the policy that you want to confirm permissions for.

```bash
export policy_arn=arn:aws:iam::111122223333:policy/my-policy
```
4. View the default version of the policy.

```bash
aws iam get-policy --policy-arn $policy_arn
```
An example output is as follows.
```json
{
    "Policy": {
        "PolicyName": "my-policy",
        "PolicyId": "EXAMPLEBIOWGLDEXAMPLE",
        "Arn": "arn:aws:iam::111122223333:policy/my-policy",
        "Path": "/",
        "DefaultVersionId": "v1",
        [...]
    }
}
```
5. View the policy contents to make sure that the policy includes all the permissions that your Pod needs. If necessary, replace 1 in the following command with the version that’s returned in the previous output.


```bash
aws iam get-policy-version --policy-arn $policy_arn --version-id v1
```
An example output is as follows.
```json
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-pod-secrets-bucket"
        }
    ]
}
```
If you created the example policy in a previous step, then your output is the same. If you created a different policy, then the example content is different.

6. Confirm that the Kubernetes service account is annotated with the role.

```bash
kubectl describe serviceaccount my-service-account -n default
```
An example output is as follows.
```bash
Name:                my-service-account
Namespace:           default
Annotations:         eks.amazonaws.com/role-arn: arn:aws:iam::111122223333:role/my-role
Image pull secrets:  <none>
Mountable secrets:   my-service-account-token-qqjfl
Tokens:              my-service-account-token-qqjfl
[...]
```