#!/bin/bash

BUCKET_NAME="agentcore-source-bucket"

echo "Creating separate source archives for each agent..."
cd ../

# Purchase Agent
echo "Creating purchase agent archive..."
cd agentcore-agents/purchase_agent
zip -r ../../purchase-agent-source.zip .
cd ../..
aws s3 cp purchase-agent-source.zip s3://$BUCKET_NAME/purchase-agent-source.zip --region us-east-1
rm purchase-agent-source.zip

# Cement Agent
echo "Creating cement agent archive..."
cd agentcore-agents/cement_agent
zip -r ../../cement-agent-source.zip .
cd ../..
aws s3 cp cement-agent-source.zip s3://$BUCKET_NAME/cement-agent-source.zip --region us-east-1
rm cement-agent-source.zip

# Steel Agent
echo "Creating steel agent archive..."
cd agentcore-agents/steel_agent
zip -r ../../steel-agent-source.zip .
cd ../..
aws s3 cp steel-agent-source.zip s3://$BUCKET_NAME/steel-agent-source.zip --region us-east-1
rm steel-agent-source.zip

echo "All agent sources uploaded to S3:"
echo "- s3://$BUCKET_NAME/purchase-agent-source.zip"
echo "- s3://$BUCKET_NAME/cement-agent-source.zip"
echo "- s3://$BUCKET_NAME/steel-agent-source.zip"