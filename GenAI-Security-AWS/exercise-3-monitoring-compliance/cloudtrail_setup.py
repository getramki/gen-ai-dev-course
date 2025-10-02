#!/usr/bin/env python3
"""
CloudTrail Setup for Bedrock Auditing
This script configures CloudTrail to audit all Bedrock API calls and activities.
"""

import boto3
import json
from botocore.exceptions import ClientError

class BedrockCloudTrailSetup:
    def __init__(self, region='us-east-1'):
        self.cloudtrail = boto3.client('cloudtrail', region_name=region)
        self.s3 = boto3.client('s3', region_name=region)
        self.sts = boto3.client('sts', region_name=region)
        self.region = region
        self.account_id = self.sts.get_caller_identity()['Account']
    
    def create_s3_bucket_for_logs(self, bucket_name=None):
        """Create S3 bucket for CloudTrail logs"""
        if not bucket_name:
            bucket_name = f"bedrock-audit-logs-{self.account_id}-{self.region}"
        
        try:
            if self.region == 'us-east-1':
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                self.s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.region}
                )
            
            print(f"✅ Created S3 bucket: {bucket_name}")
            
            # Configure bucket policy for CloudTrail
            self._configure_bucket_policy(bucket_name)
            
            return bucket_name
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                print(f"⚠️  Bucket {bucket_name} already exists")
                return bucket_name
            else:
                print(f"❌ Failed to create bucket: {e}")
                raise
    
    def _configure_bucket_policy(self, bucket_name):
        """Configure S3 bucket policy for CloudTrail"""
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AWSCloudTrailAclCheck",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "cloudtrail.amazonaws.com"
                    },
                    "Action": "s3:GetBucketAcl",
                    "Resource": f"arn:aws:s3:::{bucket_name}",
                    "Condition": {
                        "StringEquals": {
                            "AWS:SourceArn": f"arn:aws:cloudtrail:{self.region}:{self.account_id}:trail/bedrock-audit-trail"
                        }
                    }
                },
                {
                    "Sid": "AWSCloudTrailWrite",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "cloudtrail.amazonaws.com"
                    },
                    "Action": "s3:PutObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                    "Condition": {
                        "StringEquals": {
                            "s3:x-amz-acl": "bucket-owner-full-control",
                            "AWS:SourceArn": f"arn:aws:cloudtrail:{self.region}:{self.account_id}:trail/bedrock-audit-trail"
                        }
                    }
                }
            ]
        }
        
        try:
            self.s3.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(bucket_policy)
            )
            print(f"✅ Configured bucket policy for {bucket_name}")
        except ClientError as e:
            print(f"❌ Failed to configure bucket policy: {e}")
            raise
    
    def create_cloudtrail(self, bucket_name, trail_name='bedrock-audit-trail'):
        """Create CloudTrail for Bedrock auditing"""
        try:
            response = self.cloudtrail.create_trail(
                Name=trail_name,
                S3BucketName=bucket_name,
                IncludeGlobalServiceEvents=True,
                IsMultiRegionTrail=True,
                EnableLogFileValidation=True
            )
            
            trail_arn = response['TrailARN']
            print(f"✅ Created CloudTrail: {trail_arn}")
            
            # Configure event selectors for Bedrock
            self._configure_bedrock_event_selectors(trail_name)
            
            # Start logging
            self.cloudtrail.start_logging(Name=trail_name)
            print(f"✅ Started logging for trail: {trail_name}")
            
            return trail_arn
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'TrailAlreadyExistsException':
                print(f"⚠️  Trail {trail_name} already exists")
                return f"arn:aws:cloudtrail:{self.region}:{self.account_id}:trail/{trail_name}"
            else:
                print(f"❌ Failed to create CloudTrail: {e}")
                raise
    
    def _configure_bedrock_event_selectors(self, trail_name):
        """Configure event selectors specifically for Bedrock"""
        event_selectors = [
            {
                'ReadWriteType': 'All',
                'IncludeManagementEvents': True,
                'DataResources': [
                    {
                        'Type': 'AWS::Bedrock::Model',
                        'Values': ['arn:aws:bedrock:*']
                    },
                    {
                        'Type': 'AWS::Bedrock::Guardrail',
                        'Values': ['arn:aws:bedrock:*']
                    }
                ]
            }
        ]
        
        try:
            self.cloudtrail.put_event_selectors(
                TrailName=trail_name,
                EventSelectors=event_selectors
            )
            print("✅ Configured Bedrock event selectors")
        except ClientError as e:
            print(f"❌ Failed to configure event selectors: {e}")
            raise
    
    def create_insight_selectors(self, trail_name):
        """Create insight selectors for anomaly detection"""
        insight_selectors = [
            {
                'InsightType': 'ApiCallRateInsight'
            }
        ]
        
        try:
            self.cloudtrail.put_insight_selectors(
                TrailName=trail_name,
                InsightSelectors=insight_selectors
            )
            print("✅ Configured CloudTrail Insights")
        except ClientError as e:
            print(f"❌ Failed to configure insights: {e}")
            raise
    
    def setup_complete_auditing(self):
        """Complete CloudTrail setup for Bedrock auditing"""
        print("🚀 Starting Bedrock CloudTrail Auditing Setup...")
        
        # Create S3 bucket
        bucket_name = self.create_s3_bucket_for_logs()
        
        # Create CloudTrail
        trail_arn = self.create_cloudtrail(bucket_name)
        
        # Configure insights
        self.create_insight_selectors('bedrock-audit-trail')
        
        print("\n📋 Auditing Setup Summary:")
        print(f"S3 Bucket: {bucket_name}")
        print(f"CloudTrail ARN: {trail_arn}")
        print("✅ CloudTrail auditing setup completed successfully!")
        
        return {
            'bucket_name': bucket_name,
            'trail_arn': trail_arn
        }

if __name__ == "__main__":
    setup = BedrockCloudTrailSetup()
    result = setup.setup_complete_auditing()