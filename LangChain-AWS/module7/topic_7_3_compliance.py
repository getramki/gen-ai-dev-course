"""
Module 7.3: Compliance and Governance
Regulatory compliance and governance frameworks for LangChain applications.
"""

import json
import boto3
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import hashlib
import uuid

class ComplianceFramework(Enum):
    GDPR = "gdpr"
    HIPAA = "hipaa"
    SOX = "sox"
    PCI_DSS = "pci_dss"
    ISO27001 = "iso27001"

class DataClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

@dataclass
class ComplianceEvent:
    event_id: str
    timestamp: datetime
    event_type: str
    user_id: str
    resource: str
    action: str
    classification: DataClassification
    compliance_frameworks: List[ComplianceFramework]
    metadata: Dict[str, Any]

class ComplianceManager:
    """Manages compliance requirements and audit trails."""
    
    def __init__(self, frameworks: List[ComplianceFramework]):
        self.frameworks = frameworks
        self.audit_trail = []
        self.data_retention_policies = {}
        self.cloudtrail = boto3.client('cloudtrail')
        self.s3 = boto3.client('s3')
        
        # Setup retention policies
        self._setup_retention_policies()
    
    def _setup_retention_policies(self):
        """Setup data retention policies by framework."""
        self.data_retention_policies = {
            ComplianceFramework.GDPR: {
                'max_retention_days': 2555,  # 7 years
                'deletion_required': True,
                'consent_required': True
            },
            ComplianceFramework.HIPAA: {
                'max_retention_days': 2190,  # 6 years
                'encryption_required': True,
                'access_logging': True
            },
            ComplianceFramework.SOX: {
                'max_retention_days': 2555,  # 7 years
                'immutable_storage': True,
                'audit_trail': True
            }
        }
    
    def log_compliance_event(self, event: ComplianceEvent):
        """Log compliance event for audit trail."""
        self.audit_trail.append(event)
        
        # Store in CloudTrail for immutable audit
        try:
            self.cloudtrail.put_events(
                Records=[{
                    'EventTime': event.timestamp,
                    'EventName': event.event_type,
                    'EventSource': 'langchain.compliance',
                    'UserIdentity': {'type': 'User', 'userName': event.user_id},
                    'Resources': [{'resourceName': event.resource}],
                    'CloudTrailEvent': json.dumps({
                        'event_id': event.event_id,
                        'action': event.action,
                        'classification': event.classification.value,
                        'frameworks': [f.value for f in event.compliance_frameworks],
                        'metadata': event.metadata
                    })
                }]
            )
        except Exception as e:
            print(f"Failed to log to CloudTrail: {e}")
    
    def check_data_retention(self, data_created: datetime, classification: DataClassification) -> Dict[str, Any]:
        """Check if data meets retention requirements."""
        results = {}
        
        for framework in self.frameworks:
            policy = self.data_retention_policies.get(framework, {})
            max_days = policy.get('max_retention_days', 365)
            
            age_days = (datetime.utcnow() - data_created).days
            
            results[framework.value] = {
                'compliant': age_days <= max_days,
                'age_days': age_days,
                'max_days': max_days,
                'action_required': age_days > max_days
            }
        
        return results
    
    def generate_compliance_report(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate compliance report for specified period."""
        
        # Filter events by date range
        period_events = [
            event for event in self.audit_trail
            if start_date <= event.timestamp <= end_date
        ]
        
        # Analyze by framework
        framework_stats = {}
        for framework in self.frameworks:
            framework_events = [
                event for event in period_events
                if framework in event.compliance_frameworks
            ]
            
            framework_stats[framework.value] = {
                'total_events': len(framework_events),
                'event_types': list(set(event.event_type for event in framework_events)),
                'users': list(set(event.user_id for event in framework_events)),
                'classifications': list(set(event.classification.value for event in framework_events))
            }
        
        return {
            'report_period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'total_events': len(period_events),
            'framework_statistics': framework_stats,
            'compliance_status': self._assess_compliance_status(period_events)
        }
    
    def _assess_compliance_status(self, events: List[ComplianceEvent]) -> Dict[str, Any]:
        """Assess overall compliance status."""
        
        # Check for violations
        violations = []
        warnings = []
        
        for event in events:
            # Check for high-risk activities
            if event.classification == DataClassification.RESTRICTED:
                if 'export' in event.action.lower():
                    violations.append(f"Restricted data export: {event.event_id}")
            
            # Check for missing encryption
            if ComplianceFramework.HIPAA in event.compliance_frameworks:
                if not event.metadata.get('encrypted', False):
                    warnings.append(f"Unencrypted HIPAA data: {event.event_id}")
        
        return {
            'status': 'compliant' if not violations else 'non_compliant',
            'violations': violations,
            'warnings': warnings,
            'risk_score': len(violations) * 10 + len(warnings) * 2
        }

class DataGovernance:
    """Data governance and privacy controls."""
    
    def __init__(self):
        self.data_catalog = {}
        self.privacy_policies = {}
        self.consent_records = {}
    
    def register_data_asset(self, asset_id: str, classification: DataClassification, 
                          metadata: Dict[str, Any]):
        """Register data asset in governance catalog."""
        self.data_catalog[asset_id] = {
            'classification': classification,
            'created_date': datetime.utcnow(),
            'metadata': metadata,
            'access_count': 0,
            'last_accessed': None
        }
    
    def record_data_access(self, asset_id: str, user_id: str, purpose: str):
        """Record data access for governance tracking."""
        if asset_id in self.data_catalog:
            self.data_catalog[asset_id]['access_count'] += 1
            self.data_catalog[asset_id]['last_accessed'] = datetime.utcnow()
            
            # Log access event
            access_record = {
                'timestamp': datetime.utcnow(),
                'asset_id': asset_id,
                'user_id': user_id,
                'purpose': purpose,
                'classification': self.data_catalog[asset_id]['classification'].value
            }
            
            return access_record
    
    def check_consent_requirements(self, user_id: str, data_types: List[str]) -> Dict[str, Any]:
        """Check if user consent is required for data processing."""
        
        consent_status = {}
        for data_type in data_types:
            consent_status[data_type] = {
                'required': data_type in ['personal_data', 'sensitive_data'],
                'granted': self.consent_records.get(f"{user_id}:{data_type}", False),
                'expires': None  # Would track consent expiration
            }
        
        return {
            'user_id': user_id,
            'consent_status': consent_status,
            'processing_allowed': all(
                not status['required'] or status['granted'] 
                for status in consent_status.values()
            )
        }
    
    def anonymize_data(self, data: Dict[str, Any], fields_to_anonymize: List[str]) -> Dict[str, Any]:
        """Anonymize sensitive data fields."""
        anonymized = data.copy()
        
        for field in fields_to_anonymize:
            if field in anonymized:
                # Simple anonymization (hash)
                original_value = str(anonymized[field])
                anonymized[field] = hashlib.sha256(original_value.encode()).hexdigest()[:8]
        
        return anonymized

class RegulatoryReporting:
    """Automated regulatory reporting capabilities."""
    
    def __init__(self, compliance_manager: ComplianceManager):
        self.compliance_manager = compliance_manager
        self.report_templates = {}
        self._setup_report_templates()
    
    def _setup_report_templates(self):
        """Setup regulatory report templates."""
        self.report_templates = {
            ComplianceFramework.GDPR: {
                'required_fields': ['data_subject_requests', 'breach_notifications', 'consent_records'],
                'frequency': 'annual',
                'retention_period': 2555  # 7 years
            },
            ComplianceFramework.HIPAA: {
                'required_fields': ['access_logs', 'security_incidents', 'risk_assessments'],
                'frequency': 'annual',
                'retention_period': 2190  # 6 years
            }
        }
    
    def generate_regulatory_report(self, framework: ComplianceFramework, 
                                 period_start: datetime, period_end: datetime) -> Dict[str, Any]:
        """Generate regulatory compliance report."""
        
        template = self.report_templates.get(framework, {})
        compliance_report = self.compliance_manager.generate_compliance_report(
            period_start, period_end
        )
        
        # Framework-specific report generation
        if framework == ComplianceFramework.GDPR:
            return self._generate_gdpr_report(compliance_report, period_start, period_end)
        elif framework == ComplianceFramework.HIPAA:
            return self._generate_hipaa_report(compliance_report, period_start, period_end)
        else:
            return compliance_report
    
    def _generate_gdpr_report(self, base_report: Dict[str, Any], 
                            start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate GDPR-specific report."""
        return {
            **base_report,
            'gdpr_specific': {
                'data_subject_requests': 0,  # Would count actual requests
                'breach_notifications': 0,   # Would count breaches
                'consent_withdrawals': 0,    # Would count withdrawals
                'right_to_be_forgotten': 0   # Would count deletion requests
            }
        }
    
    def _generate_hipaa_report(self, base_report: Dict[str, Any], 
                             start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate HIPAA-specific report."""
        return {
            **base_report,
            'hipaa_specific': {
                'phi_access_logs': base_report['total_events'],
                'security_incidents': len(base_report['compliance_status']['violations']),
                'risk_assessments_completed': 1,  # Would track actual assessments
                'business_associate_agreements': 0  # Would track BAAs
            }
        }

def demonstrate_compliance_governance():
    """Demonstrate compliance and governance features."""
    
    print("=== Compliance and Governance Demo ===\n")
    
    # 1. Setup compliance manager
    frameworks = [ComplianceFramework.GDPR, ComplianceFramework.HIPAA]
    compliance_mgr = ComplianceManager(frameworks)
    
    print("1. Compliance Framework Setup:")
    for framework in frameworks:
        print(f"✓ {framework.value.upper()} compliance enabled")
    print()
    
    # 2. Log compliance events
    print("2. Compliance Event Logging:")
    
    events = [
        ComplianceEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            event_type="data_access",
            user_id="user123",
            resource="patient_records",
            action="read",
            classification=DataClassification.RESTRICTED,
            compliance_frameworks=[ComplianceFramework.HIPAA],
            metadata={"encrypted": True, "purpose": "treatment"}
        ),
        ComplianceEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            event_type="data_export",
            user_id="analyst456",
            resource="customer_data",
            action="export",
            classification=DataClassification.CONFIDENTIAL,
            compliance_frameworks=[ComplianceFramework.GDPR],
            metadata={"anonymized": True, "consent": True}
        )
    ]
    
    for event in events:
        compliance_mgr.log_compliance_event(event)
        print(f"✓ Logged {event.event_type} event for {event.resource}")
    
    print()
    
    # 3. Data governance
    print("3. Data Governance:")
    governance = DataGovernance()
    
    # Register data assets
    governance.register_data_asset(
        "customer_db",
        DataClassification.CONFIDENTIAL,
        {"contains_pii": True, "region": "us-east-1"}
    )
    
    # Record access
    access_record = governance.record_data_access(
        "customer_db", "user123", "analytics"
    )
    
    print(f"✓ Data asset registered: customer_db")
    print(f"✓ Access recorded: {access_record['user_id']} at {access_record['timestamp']}")
    
    # Check consent
    consent_check = governance.check_consent_requirements(
        "user123", ["personal_data", "marketing_data"]
    )
    print(f"✓ Consent check: Processing allowed = {consent_check['processing_allowed']}")
    print()
    
    # 4. Generate compliance report
    print("4. Compliance Reporting:")
    
    report_start = datetime.utcnow() - timedelta(days=30)
    report_end = datetime.utcnow()
    
    report = compliance_mgr.generate_compliance_report(report_start, report_end)
    
    print(f"Report period: {report['report_period']['start'][:10]} to {report['report_period']['end'][:10]}")
    print(f"Total events: {report['total_events']}")
    print(f"Compliance status: {report['compliance_status']['status']}")
    print(f"Risk score: {report['compliance_status']['risk_score']}")
    print()
    
    # 5. Regulatory reporting
    print("5. Regulatory Reporting:")
    
    regulatory_reporter = RegulatoryReporting(compliance_mgr)
    
    gdpr_report = regulatory_reporter.generate_regulatory_report(
        ComplianceFramework.GDPR, report_start, report_end
    )
    
    hipaa_report = regulatory_reporter.generate_regulatory_report(
        ComplianceFramework.HIPAA, report_start, report_end
    )
    
    print("✓ GDPR report generated")
    print(f"  - Data subject requests: {gdpr_report['gdpr_specific']['data_subject_requests']}")
    print(f"  - Breach notifications: {gdpr_report['gdpr_specific']['breach_notifications']}")
    
    print("✓ HIPAA report generated")
    print(f"  - PHI access logs: {hipaa_report['hipaa_specific']['phi_access_logs']}")
    print(f"  - Security incidents: {hipaa_report['hipaa_specific']['security_incidents']}")
    print()
    
    # 6. Data anonymization
    print("6. Data Anonymization:")
    
    sample_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "ssn": "123-45-6789",
        "age": 35
    }
    
    anonymized = governance.anonymize_data(
        sample_data, 
        ["name", "email", "ssn"]
    )
    
    print("Original data:")
    for key, value in sample_data.items():
        print(f"  {key}: {value}")
    
    print("Anonymized data:")
    for key, value in anonymized.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    demonstrate_compliance_governance()