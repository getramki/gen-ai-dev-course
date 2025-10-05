#!/bin/bash

BUCKET_NAME="agentcore-source-bucket"
PROJECT_NAME="agentcore-arm64-builder"

echo "Cleaning up CodeBuild resources..."

# Delete CodeBuild project from us-west-2
echo "Deleting CodeBuild project from us-west-2..."
aws codebuild delete-project --name $PROJECT_NAME --region us-west-2

# Delete CodeBuild project from us-east-1 (if exists)
echo "Deleting CodeBuild project from us-east-1..."
aws codebuild delete-project --name $PROJECT_NAME --region us-east-1

# Empty and delete S3 bucket from us-west-2
echo "Emptying S3 bucket in us-west-2..."
aws s3 rm s3://$BUCKET_NAME --recursive --region us-west-2
echo "Deleting S3 bucket from us-west-2..."
aws s3 rb s3://$BUCKET_NAME --region us-west-2

# Empty and delete S3 bucket from us-east-1 (if exists)
echo "Emptying S3 bucket in us-east-1..."
aws s3 rm s3://$BUCKET_NAME --recursive --region us-east-1
echo "Deleting S3 bucket from us-east-1..."
aws s3 rb s3://$BUCKET_NAME --region us-east-1

echo "Cleanup completed"