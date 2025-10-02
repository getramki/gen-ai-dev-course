#!/usr/bin/env python3
"""
IAM Security Setup for Amazon Bedrock
This script creates secure IAM roles and policies for Bedrock applications.
"""

import boto3
import json
import os
from botocore.exceptions import ClientError

class BedrockIAMSetup:
    def __init__(self, region='us-east-1'):
        self.iam = boto3.client('iam', region_name=region)
        self.sts = boto3.client('sts', region_name=region)
        self.account_id = self.sts.get_caller_identity()['Account']
    
    def create_bedrock_policy(self):
        """Create minimal access policy for Bedrock"""
        with open('bedrock-minimal-policy.json', 'r') as f:
            policy_document = f.read()
        
        policy_name = 'BedrockMinimalAccessPolicy'
        
        try:
            response = self.iam.create_policy(
                PolicyName=policy_name,
                PolicyDocument=policy_document,
                Description='Minimal access policy for Amazon Bedrock applications'
            )
            print(f"✅ Created policy: {response['Policy']['Arn']}")
            return response['Policy']['Arn']
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print(f"⚠️  Policy {policy_name} already exists")
                return f"arn:aws:iam::{self.account_id}:policy/{policy_name}"
            raise
    
    def create_bedrock_role(self):
        """Create IAM role for Bedrock applications"""
        # Update trust policy with actual account ID
        with open('trust-policy.json', 'r') as f:
            trust_policy = f.read().replace('ACCOUNT-ID', self.account_id)
        
        role_name = 'BedrockApplicationRole'
        
        try:
            response = self.iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=trust_policy,
                Description='IAM role for Amazon Bedrock applications'
            )
            print(f"✅ Created role: {response['Role']['Arn']}")
            return response['Role']['Arn']
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print(f"⚠️  Role {role_name} already exists")
                return f"arn:aws:iam::{self.account_id}:role/{role_name}"
            raise
    
    def attach_policy_to_role(self, policy_arn, role_name='BedrockApplicationRole'):
        """Attach policy to role"""
        try:
            self.iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            print(f"✅ Attached policy to role: {role_name}")
        except ClientError as e:
            print(f"❌ Error attaching policy: {e}")
            raise
    
    def test_role_assumption(self, role_arn):
        """Test if the role can be assumed"""
        try:
            response = self.sts.assume_role(
                RoleArn=role_arn,
                RoleSessionName='BedrockSecurityTest',
                ExternalId='unique-external-id'
            )
            print("✅ Role assumption test successful")
            return response['Credentials']
        except ClientError as e:
            print(f"❌ Role assumption failed: {e}")
            return None
    
    def setup_complete_iam(self):
        """Complete IAM setup process"""
        print("🚀 Starting Bedrock IAM Security Setup...")
        
        # Create policy
        policy_arn = self.create_bedrock_policy()
        
        # Create role
        role_arn = self.create_bedrock_role()
        
        # Attach policy to role
        self.attach_policy_to_role(policy_arn)
        
        # Test role assumption
        credentials = self.test_role_assumption(role_arn)
        
        print("\n📋 Setup Summary:")
        print(f"Policy ARN: {policy_arn}")
        print(f"Role ARN: {role_arn}")
        print("✅ IAM setup completed successfully!")
        
        return {
            'policy_arn': policy_arn,
            'role_arn': role_arn,
            'credentials': credentials
        }

if __name__ == "__main__":
    setup = BedrockIAMSetup()
    result = setup.setup_complete_iam()