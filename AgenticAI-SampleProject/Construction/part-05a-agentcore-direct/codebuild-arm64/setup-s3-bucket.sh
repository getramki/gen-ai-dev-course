#!/bin/bash

BUCKET_NAME="agentcore-source-bucket"
REGION="us-east-1"

echo "Creating S3 bucket for source code..."

aws s3 mb s3://$BUCKET_NAME --region $REGION

echo "Setting bucket policy for CodeBuild access..."
cat > bucket-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion"
      ],
      "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
    }
  ]
}
EOF

aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://bucket-policy.json
rm bucket-policy.json

echo "S3 bucket created: s3://$BUCKET_NAME"