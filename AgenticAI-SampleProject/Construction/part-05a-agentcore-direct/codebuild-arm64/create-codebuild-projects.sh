#!/bin/bash

SERVICE_ROLE="arn:aws:iam::910673207244:role/CodeBuildServiceRole"
BUCKET_NAME="agentcore-source-bucket"

echo "Creating separate CodeBuild projects for each agent..."

# Purchase Agent Project
aws codebuild create-project \
  --name agentcore-purchase-builder \
  --description "Build ARM64 image for Purchase Agent" \
  --service-role $SERVICE_ROLE \
  --artifacts type=NO_ARTIFACTS \
  --environment type=ARM_CONTAINER,image=aws/codebuild/amazonlinux2-aarch64-standard:3.0,computeType=BUILD_GENERAL1_LARGE,environmentVariables='[{name=AWS_DEFAULT_REGION,value=us-east-1},{name=AWS_ACCOUNT_ID,value=910673207244}]' \
  --source type=S3,location=$BUCKET_NAME/purchase-agent-source.zip \
  --region us-east-1

# Cement Agent Project  
aws codebuild create-project \
  --name agentcore-cement-builder \
  --description "Build ARM64 image for Cement Agent" \
  --service-role $SERVICE_ROLE \
  --artifacts type=NO_ARTIFACTS \
  --environment type=ARM_CONTAINER,image=aws/codebuild/amazonlinux2-aarch64-standard:3.0,computeType=BUILD_GENERAL1_LARGE,environmentVariables='[{name=AWS_DEFAULT_REGION,value=us-east-1},{name=AWS_ACCOUNT_ID,value=910673207244}]' \
  --source type=S3,location=$BUCKET_NAME/cement-agent-source.zip \
  --region us-east-1

# Steel Agent Project
aws codebuild create-project \
  --name agentcore-steel-builder \
  --description "Build ARM64 image for Steel Agent" \
  --service-role $SERVICE_ROLE \
  --artifacts type=NO_ARTIFACTS \
  --environment type=ARM_CONTAINER,image=aws/codebuild/amazonlinux2-aarch64-standard:3.0,computeType=BUILD_GENERAL1_LARGE,environmentVariables='[{name=AWS_DEFAULT_REGION,value=us-east-1},{name=AWS_ACCOUNT_ID,value=910673207244}]' \
  --source type=S3,location=$BUCKET_NAME/steel-agent-source.zip \
  --region us-east-1

echo "CodeBuild projects created:"
echo "- agentcore-purchase-builder"
echo "- agentcore-cement-builder" 
echo "- agentcore-steel-builder"

echo ""
echo "To start builds:"
echo "aws codebuild start-build --project-name agentcore-purchase-builder --region us-east-1"
echo "aws codebuild start-build --project-name agentcore-cement-builder --region us-east-1"
echo "aws codebuild start-build --project-name agentcore-steel-builder --region us-east-1"