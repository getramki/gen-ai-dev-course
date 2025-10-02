#!/usr/bin/env python3
"""
Compliance Reporting for Bedrock Security
This script generates compliance reports and tracks security metrics.
"""

import boto3
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

class BedrockComplianceReporter:
    def __init__(self, region='us-east-1'):
        self.cloudtrail = boto3.client('cloudtrail', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.logs = boto3.client('logs', region_name=region)
        self.region = region
    
    def get_api_usage_metrics(self, days=30):
        """Get Bedrock API usage metrics for compliance reporting"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        
        try:
            # Get CloudTrail events for Bedrock
            response = self.cloudtrail.lookup_events(
                LookupAttributes=[
                    {
                        'AttributeKey': 'EventSource',
                        'AttributeValue': 'bedrock.amazonaws.com'
                    }
                ],
                StartTime=start_time,
                EndTime=end_time
            )
            
            events = response.get('Events', [])
            
            # Process events for reporting
            api_calls = []
            for event in events:
                api_calls.append({
                    'timestamp': event['EventTime'],
                    'event_name': event['EventName'],
                    'user_identity': event.get('Username', 'Unknown'),
                    'source_ip': event.get('SourceIPAddress', 'Unknown'),
                    'user_agent': event.get('UserAgent', 'Unknown')
                })
            
            return api_calls
            
        except ClientError as e:
            print(f"❌ Failed to get API usage metrics: {e}")
            return []
    
    def get_guardrail_interventions(self, days=30):
        """Get guardrail intervention data for compliance reporting"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        
        log_group = '/aws/bedrock/security'
        
        try:
            # Query CloudWatch Logs for guardrail interventions
            query = """
            fields @timestamp, @message
            | filter @message like /GUARDRAIL_INTERVENTION/
            | parse @message /GUARDRAIL_INTERVENTION: (?<intervention_data>.*)/
            | sort @timestamp desc
            """
            
            response = self.logs.start_query(
                logGroupName=log_group,
                startTime=int(start_time.timestamp()),
                endTime=int(end_time.timestamp()),
                queryString=query
            )
            
            query_id = response['queryId']
            
            # Wait for query to complete and get results
            import time
            while True:
                result = self.logs.get_query_results(queryId=query_id)
                if result['status'] == 'Complete':
                    break
                time.sleep(1)
            
            interventions = []
            for result_row in result.get('results', []):
                row_data = {item['field']: item['value'] for item in result_row}
                if 'intervention_data' in row_data:
                    try:
                        intervention_info = json.loads(row_data['intervention_data'])
                        interventions.append(intervention_info)
                    except json.JSONDecodeError:
                        continue
            
            return interventions
            
        except ClientError as e:
            print(f"❌ Failed to get guardrail interventions: {e}")
            return []
    
    def generate_usage_report(self, api_calls):
        """Generate API usage compliance report"""
        if not api_calls:
            return "No API usage data available for the specified period."
        
        df = pd.DataFrame(api_calls)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Generate summary statistics
        report = {
            'total_api_calls': len(df),
            'unique_users': df['user_identity'].nunique(),
            'date_range': f"{df['timestamp'].min()} to {df['timestamp'].max()}",
            'most_common_apis': df['event_name'].value_counts().head(10).to_dict(),
            'daily_usage': df.groupby('date').size().to_dict()
        }
        
        return report
    
    def generate_security_report(self, interventions):
        """Generate security compliance report"""
        if not interventions:
            return "No security interventions recorded for the specified period."
        
        df = pd.DataFrame(interventions)
        
        # Generate security metrics
        report = {
            'total_interventions': len(df),
            'intervention_types': df.get('source', pd.Series()).value_counts().to_dict(),
            'blocked_content_categories': {},
            'compliance_score': self._calculate_compliance_score(interventions)
        }
        
        # Analyze assessments if available
        if 'assessments' in df.columns:
            assessments = []
            for assessment_list in df['assessments'].dropna():
                if isinstance(assessment_list, list):
                    assessments.extend(assessment_list)
            
            if assessments:
                assessment_df = pd.DataFrame(assessments)
                if 'policy' in assessment_df.columns:
                    report['blocked_content_categories'] = assessment_df['policy'].value_counts().to_dict()
        
        return report
    
    def _calculate_compliance_score(self, interventions):
        """Calculate compliance score based on intervention patterns"""
        if not interventions:
            return 100.0
        
        # Simple scoring: fewer interventions = higher compliance
        # In production, this would be more sophisticated
        total_requests = 1000  # This should come from actual metrics
        intervention_rate = len(interventions) / total_requests
        
        # Score decreases as intervention rate increases
        score = max(0, 100 - (intervention_rate * 100))
        return round(score, 2)
    
    def create_compliance_dashboard_data(self, days=30):
        """Create data for compliance dashboard visualization"""
        api_calls = self.get_api_usage_metrics(days)
        interventions = self.get_guardrail_interventions(days)
        
        usage_report = self.generate_usage_report(api_calls)
        security_report = self.generate_security_report(interventions)
        
        return {
            'usage_report': usage_report,
            'security_report': security_report,
            'raw_data': {
                'api_calls': api_calls,
                'interventions': interventions
            }
        }
    
    def generate_executive_summary(self, compliance_data):
        """Generate executive summary for compliance reporting"""
        usage = compliance_data['usage_report']
        security = compliance_data['security_report']
        
        summary = f"""
# Bedrock Security Compliance Report
## Executive Summary

### Usage Metrics
- **Total API Calls**: {usage.get('total_api_calls', 0):,}
- **Unique Users**: {usage.get('unique_users', 0)}
- **Reporting Period**: {usage.get('date_range', 'N/A')}

### Security Metrics
- **Security Interventions**: {security.get('total_interventions', 0)}
- **Compliance Score**: {security.get('compliance_score', 0)}%
- **Content Policy Violations**: {len(security.get('blocked_content_categories', {}))} categories

### Key Findings
- {'✅ Low intervention rate indicates good user compliance' if security.get('total_interventions', 0) < 10 else '⚠️ High intervention rate requires attention'}
- {'✅ Diverse user base accessing the system' if usage.get('unique_users', 0) > 5 else '⚠️ Limited user adoption'}
- {'✅ Consistent daily usage patterns' if len(usage.get('daily_usage', {})) > 7 else '⚠️ Irregular usage patterns'}

### Recommendations
1. Continue monitoring guardrail effectiveness
2. Review and update content policies as needed
3. Provide additional user training if intervention rates are high
4. Regular security audits and compliance reviews

---
*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*
        """
        
        return summary
    
    def export_compliance_report(self, output_file='bedrock_compliance_report.json'):
        """Export complete compliance report to file"""
        print("📊 Generating compliance report...")
        
        compliance_data = self.create_compliance_dashboard_data()
        executive_summary = self.generate_executive_summary(compliance_data)
        
        full_report = {
            'generated_at': datetime.now().isoformat(),
            'executive_summary': executive_summary,
            'detailed_data': compliance_data
        }
        
        with open(output_file, 'w') as f:
            json.dump(full_report, f, indent=2, default=str)
        
        print(f"✅ Compliance report exported to {output_file}")
        print("\n" + executive_summary)
        
        return full_report

if __name__ == "__main__":
    reporter = BedrockComplianceReporter()
    report = reporter.export_compliance_report()