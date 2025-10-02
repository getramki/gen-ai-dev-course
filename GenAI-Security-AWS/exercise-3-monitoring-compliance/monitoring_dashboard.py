#!/usr/bin/env python3
"""
CloudWatch Monitoring Dashboard for Bedrock Security
This script creates comprehensive monitoring and alerting for Bedrock applications.
"""

import boto3
import json
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

class BedrockMonitoringSetup:
    def __init__(self, region='us-east-1'):
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.sns = boto3.client('sns', region_name=region)
        self.logs = boto3.client('logs', region_name=region)
        self.region = region
    
    def create_log_group(self, log_group_name='/aws/bedrock/security'):
        """Create CloudWatch Log Group for Bedrock security events"""
        try:
            self.logs.create_log_group(
                logGroupName=log_group_name,
                retentionInDays=90
            )
            print(f"✅ Created log group: {log_group_name}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                print(f"⚠️  Log group {log_group_name} already exists")
            else:
                print(f"❌ Failed to create log group: {e}")
                raise
    
    def create_custom_metrics(self):
        """Create custom CloudWatch metrics for Bedrock monitoring"""
        metrics = [
            {
                'MetricName': 'BedrockInvocations',
                'Namespace': 'Bedrock/Security',
                'Dimensions': [
                    {'Name': 'ModelId', 'Value': 'anthropic.claude-3-sonnet-20240229-v1:0'}
                ],
                'Value': 1,
                'Unit': 'Count'
            },
            {
                'MetricName': 'GuardrailInterventions',
                'Namespace': 'Bedrock/Security',
                'Dimensions': [
                    {'Name': 'InterventionType', 'Value': 'ContentPolicy'}
                ],
                'Value': 1,
                'Unit': 'Count'
            },
            {
                'MetricName': 'ResponseLatency',
                'Namespace': 'Bedrock/Security',
                'Value': 500,
                'Unit': 'Milliseconds'
            }
        ]
        
        try:
            for metric in metrics:
                self.cloudwatch.put_metric_data(
                    Namespace=metric['Namespace'],
                    MetricData=[{
                        'MetricName': metric['MetricName'],
                        'Dimensions': metric.get('Dimensions', []),
                        'Value': metric['Value'],
                        'Unit': metric['Unit'],
                        'Timestamp': datetime.utcnow()
                    }]
                )
            print("✅ Created custom metrics")
        except ClientError as e:
            print(f"❌ Failed to create metrics: {e}")
            raise
    
    def create_sns_topic(self, topic_name='bedrock-security-alerts'):
        """Create SNS topic for security alerts"""
        try:
            response = self.sns.create_topic(Name=topic_name)
            topic_arn = response['TopicArn']
            print(f"✅ Created SNS topic: {topic_arn}")
            return topic_arn
        except ClientError as e:
            print(f"❌ Failed to create SNS topic: {e}")
            raise
    
    def create_alarms(self, sns_topic_arn):
        """Create CloudWatch alarms for security monitoring"""
        alarms = [
            {
                'AlarmName': 'BedrockHighInvocationRate',
                'ComparisonOperator': 'GreaterThanThreshold',
                'EvaluationPeriods': 2,
                'MetricName': 'BedrockInvocations',
                'Namespace': 'Bedrock/Security',
                'Period': 300,
                'Statistic': 'Sum',
                'Threshold': 100.0,
                'ActionsEnabled': True,
                'AlarmActions': [sns_topic_arn],
                'AlarmDescription': 'Alert when Bedrock invocation rate is unusually high',
                'Unit': 'Count'
            },
            {
                'AlarmName': 'BedrockGuardrailInterventions',
                'ComparisonOperator': 'GreaterThanThreshold',
                'EvaluationPeriods': 1,
                'MetricName': 'GuardrailInterventions',
                'Namespace': 'Bedrock/Security',
                'Period': 300,
                'Statistic': 'Sum',
                'Threshold': 5.0,
                'ActionsEnabled': True,
                'AlarmActions': [sns_topic_arn],
                'AlarmDescription': 'Alert when guardrail interventions exceed threshold',
                'Unit': 'Count'
            },
            {
                'AlarmName': 'BedrockHighLatency',
                'ComparisonOperator': 'GreaterThanThreshold',
                'EvaluationPeriods': 3,
                'MetricName': 'ResponseLatency',
                'Namespace': 'Bedrock/Security',
                'Period': 300,
                'Statistic': 'Average',
                'Threshold': 2000.0,
                'ActionsEnabled': True,
                'AlarmActions': [sns_topic_arn],
                'AlarmDescription': 'Alert when response latency is high',
                'Unit': 'Milliseconds'
            }
        ]
        
        for alarm in alarms:
            try:
                self.cloudwatch.put_metric_alarm(**alarm)
                print(f"✅ Created alarm: {alarm['AlarmName']}")
            except ClientError as e:
                print(f"❌ Failed to create alarm {alarm['AlarmName']}: {e}")
    
    def create_dashboard(self):
        """Create CloudWatch dashboard for Bedrock security monitoring"""
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "x": 0,
                    "y": 0,
                    "width": 12,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            ["Bedrock/Security", "BedrockInvocations"],
                            [".", "GuardrailInterventions"]
                        ],
                        "period": 300,
                        "stat": "Sum",
                        "region": self.region,
                        "title": "Bedrock Usage and Security Events"
                    }
                },
                {
                    "type": "metric",
                    "x": 0,
                    "y": 6,
                    "width": 12,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            ["Bedrock/Security", "ResponseLatency"]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": self.region,
                        "title": "Response Latency"
                    }
                },
                {
                    "type": "log",
                    "x": 0,
                    "y": 12,
                    "width": 24,
                    "height": 6,
                    "properties": {
                        "query": f"SOURCE '/aws/bedrock/security'\n| fields @timestamp, @message\n| filter @message like /GUARDRAIL_INTERVENTION/\n| sort @timestamp desc\n| limit 20",
                        "region": self.region,
                        "title": "Recent Guardrail Interventions",
                        "view": "table"
                    }
                }
            ]
        }
        
        try:
            self.cloudwatch.put_dashboard(
                DashboardName='BedrockSecurityDashboard',
                DashboardBody=json.dumps(dashboard_body)
            )
            print("✅ Created CloudWatch dashboard: BedrockSecurityDashboard")
        except ClientError as e:
            print(f"❌ Failed to create dashboard: {e}")
            raise
    
    def setup_complete_monitoring(self):
        """Complete monitoring setup for Bedrock security"""
        print("🚀 Starting Bedrock Security Monitoring Setup...")
        
        # Create log group
        self.create_log_group()
        
        # Create custom metrics
        self.create_custom_metrics()
        
        # Create SNS topic
        sns_topic_arn = self.create_sns_topic()
        
        # Create alarms
        self.create_alarms(sns_topic_arn)
        
        # Create dashboard
        self.create_dashboard()
        
        print("\n📋 Monitoring Setup Summary:")
        print(f"Log Group: /aws/bedrock/security")
        print(f"SNS Topic: {sns_topic_arn}")
        print(f"Dashboard: BedrockSecurityDashboard")
        print("✅ Monitoring setup completed successfully!")
        
        return {
            'log_group': '/aws/bedrock/security',
            'sns_topic_arn': sns_topic_arn,
            'dashboard_name': 'BedrockSecurityDashboard'
        }

if __name__ == "__main__":
    setup = BedrockMonitoringSetup()
    result = setup.setup_complete_monitoring()