"""
Module 7.4: Data Privacy and Security
Privacy-preserving AI and advanced security implementations.
"""

import boto3
import hashlib
import secrets
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate

class PrivacyPreservingLLM:
    """LLM service with privacy-preserving features."""
    
    def __init__(self):
        self.llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            model_kwargs={"temperature": 0.1, "max_tokens": 1000}
        )
        self.pii_detector = PIIDetector()
        self.data_anonymizer = DataAnonymizer()
    
    def process_with_privacy(self, query: str, user_id: str) -> Dict[str, Any]:
        """Process query with privacy protection."""
        
        # 1. Detect PII in query
        pii_detected = self.pii_detector.detect_pii(query)
        
        # 2. Anonymize if PII found
        if pii_detected['has_pii']:
            anonymized_query = self.data_anonymizer.anonymize_text(query)
            privacy_applied = True
        else:
            anonymized_query = query
            privacy_applied = False
        
        # 3. Process with LLM
        prompt = ChatPromptTemplate.from_template(
            "Process this query while maintaining privacy: {query}"
        )
        
        try:
            chain = prompt | self.llm
            result = chain.invoke({'query': anonymized_query})
            
            # 4. Post-process response
            response = self._sanitize_response(result.content)
            
            return {
                'success': True,
                'response': response,
                'privacy_applied': privacy_applied,
                'pii_detected': pii_detected,
                'user_id_hash': hashlib.sha256(user_id.encode()).hexdigest()[:8]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'privacy_applied': privacy_applied
            }
    
    def _sanitize_response(self, response: str) -> str:
        """Sanitize LLM response to remove potential PII."""
        # Simple sanitization - in production, use more sophisticated methods
        sanitized = response
        
        # Remove potential phone numbers
        import re
        phone_pattern = r'\b\d{3}-\d{3}-\d{4}\b'
        sanitized = re.sub(phone_pattern, '[PHONE-REDACTED]', sanitized)
        
        # Remove potential emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        sanitized = re.sub(email_pattern, '[EMAIL-REDACTED]', sanitized)
        
        return sanitized

class PIIDetector:
    """Detect personally identifiable information in text."""
    
    def __init__(self):
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}-\d{3}-\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
        }
    
    def detect_pii(self, text: str) -> Dict[str, Any]:
        """Detect PII in text."""
        import re
        
        detected = {}
        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                detected[pii_type] = len(matches)
        
        return {
            'has_pii': bool(detected),
            'types_detected': list(detected.keys()),
            'counts': detected
        }

class DataAnonymizer:
    """Anonymize sensitive data while preserving utility."""
    
    def __init__(self):
        self.replacement_map = {}
    
    def anonymize_text(self, text: str) -> str:
        """Anonymize PII in text."""
        import re
        
        anonymized = text
        
        # Email anonymization
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        anonymized = re.sub(email_pattern, '[EMAIL]', anonymized)
        
        # Phone anonymization
        phone_pattern = r'\b\d{3}-\d{3}-\d{4}\b'
        anonymized = re.sub(phone_pattern, '[PHONE]', anonymized)
        
        # SSN anonymization
        ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        anonymized = re.sub(ssn_pattern, '[SSN]', anonymized)
        
        return anonymized
    
    def k_anonymize(self, data: List[Dict], k: int, quasi_identifiers: List[str]) -> List[Dict]:
        """Apply k-anonymity to dataset."""
        # Simplified k-anonymity implementation
        anonymized_data = []
        
        for record in data:
            anonymized_record = record.copy()
            
            # Generalize quasi-identifiers
            for qi in quasi_identifiers:
                if qi in anonymized_record:
                    if isinstance(anonymized_record[qi], int):
                        # Age generalization: 25-34, 35-44, etc.
                        age = anonymized_record[qi]
                        age_group = f"{(age // 10) * 10}-{(age // 10) * 10 + 9}"
                        anonymized_record[qi] = age_group
                    elif isinstance(anonymized_record[qi], str):
                        # String generalization
                        anonymized_record[qi] = anonymized_record[qi][:2] + "*"
            
            anonymized_data.append(anonymized_record)
        
        return anonymized_data

class SecureDataStorage:
    """Secure storage with encryption and access controls."""
    
    def __init__(self, kms_key_id: str = None):
        self.kms = boto3.client('kms')
        self.s3 = boto3.client('s3')
        self.kms_key_id = kms_key_id
        self.local_encryption_key = self._generate_local_key()
    
    def _generate_local_key(self) -> bytes:
        """Generate local encryption key."""
        password = secrets.token_bytes(32)
        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def encrypt_data(self, data: str, use_kms: bool = True) -> Dict[str, Any]:
        """Encrypt data using KMS or local encryption."""
        
        if use_kms and self.kms_key_id:
            try:
                response = self.kms.encrypt(
                    KeyId=self.kms_key_id,
                    Plaintext=data.encode('utf-8')
                )
                return {
                    'encrypted_data': base64.b64encode(response['CiphertextBlob']).decode(),
                    'encryption_method': 'kms',
                    'key_id': self.kms_key_id
                }
            except Exception as e:
                print(f"KMS encryption failed: {e}, falling back to local")
        
        # Local encryption fallback
        fernet = Fernet(self.local_encryption_key)
        encrypted = fernet.encrypt(data.encode('utf-8'))
        
        return {
            'encrypted_data': base64.b64encode(encrypted).decode(),
            'encryption_method': 'local',
            'key_id': 'local'
        }
    
    def decrypt_data(self, encrypted_data: str, encryption_method: str, key_id: str) -> str:
        """Decrypt data."""
        
        if encryption_method == 'kms':
            try:
                ciphertext_blob = base64.b64decode(encrypted_data)
                response = self.kms.decrypt(CiphertextBlob=ciphertext_blob)
                return response['Plaintext'].decode('utf-8')
            except Exception as e:
                raise Exception(f"KMS decryption failed: {e}")
        
        elif encryption_method == 'local':
            fernet = Fernet(self.local_encryption_key)
            encrypted_bytes = base64.b64decode(encrypted_data)
            decrypted = fernet.decrypt(encrypted_bytes)
            return decrypted.decode('utf-8')
        
        else:
            raise Exception(f"Unknown encryption method: {encryption_method}")
    
    def store_securely(self, bucket: str, key: str, data: str, 
                      metadata: Dict[str, str] = None) -> Dict[str, Any]:
        """Store data securely in S3 with encryption."""
        
        # Encrypt data
        encrypted = self.encrypt_data(data)
        
        # Store in S3 with server-side encryption
        try:
            self.s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=encrypted['encrypted_data'],
                ServerSideEncryption='aws:kms',
                SSEKMSKeyId=self.kms_key_id if self.kms_key_id else None,
                Metadata=metadata or {}
            )
            
            return {
                'success': True,
                'bucket': bucket,
                'key': key,
                'encryption_info': encrypted
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

class AccessControlManager:
    """Fine-grained access control for sensitive operations."""
    
    def __init__(self):
        self.access_policies = {}
        self.access_log = []
    
    def create_policy(self, policy_name: str, rules: List[Dict[str, Any]]):
        """Create access control policy."""
        self.access_policies[policy_name] = {
            'rules': rules,
            'created': datetime.utcnow(),
            'active': True
        }
    
    def check_access(self, user_id: str, resource: str, action: str, 
                    context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Check if user has access to perform action on resource."""
        
        access_granted = False
        applied_policies = []
        
        for policy_name, policy in self.access_policies.items():
            if not policy['active']:
                continue
            
            for rule in policy['rules']:
                if self._rule_matches(rule, user_id, resource, action, context):
                    access_granted = rule.get('allow', False)
                    applied_policies.append(policy_name)
                    break
        
        # Log access attempt
        log_entry = {
            'timestamp': datetime.utcnow(),
            'user_id': user_id,
            'resource': resource,
            'action': action,
            'granted': access_granted,
            'policies_applied': applied_policies,
            'context': context or {}
        }
        self.access_log.append(log_entry)
        
        return {
            'access_granted': access_granted,
            'policies_applied': applied_policies,
            'log_entry_id': len(self.access_log) - 1
        }
    
    def _rule_matches(self, rule: Dict[str, Any], user_id: str, resource: str, 
                     action: str, context: Dict[str, Any]) -> bool:
        """Check if access rule matches the request."""
        
        # Check user match
        if 'users' in rule and user_id not in rule['users']:
            return False
        
        # Check resource match
        if 'resources' in rule and resource not in rule['resources']:
            return False
        
        # Check action match
        if 'actions' in rule and action not in rule['actions']:
            return False
        
        # Check context conditions
        if 'conditions' in rule and context:
            for condition_key, condition_value in rule['conditions'].items():
                if context.get(condition_key) != condition_value:
                    return False
        
        return True

def demonstrate_privacy_security():
    """Demonstrate privacy and security features."""
    
    print("=== Data Privacy and Security Demo ===\n")
    
    # 1. Privacy-preserving LLM
    print("1. Privacy-Preserving LLM:")
    privacy_llm = PrivacyPreservingLLM()
    
    test_query = "My email is john.doe@example.com and my phone is 555-123-4567. Can you help me?"
    
    result = privacy_llm.process_with_privacy(test_query, "user123")
    
    print(f"Original query: {test_query}")
    print(f"Privacy applied: {result['privacy_applied']}")
    print(f"PII detected: {result['pii_detected']['has_pii']}")
    if result['pii_detected']['has_pii']:
        print(f"PII types: {result['pii_detected']['types_detected']}")
    print()
    
    # 2. Data anonymization
    print("2. Data Anonymization:")
    anonymizer = DataAnonymizer()
    
    sample_data = [
        {'name': 'John Doe', 'age': 28, 'city': 'New York'},
        {'name': 'Jane Smith', 'age': 32, 'city': 'Los Angeles'},
        {'name': 'Bob Johnson', 'age': 29, 'city': 'Chicago'}
    ]
    
    k_anonymous = anonymizer.k_anonymize(sample_data, k=2, quasi_identifiers=['age', 'name'])
    
    print("Original data:")
    for record in sample_data:
        print(f"  {record}")
    
    print("K-anonymized data (k=2):")
    for record in k_anonymous:
        print(f"  {record}")
    print()
    
    # 3. Secure data storage
    print("3. Secure Data Storage:")
    secure_storage = SecureDataStorage()
    
    sensitive_data = "Patient medical record: John Doe has diabetes"
    encrypted = secure_storage.encrypt_data(sensitive_data, use_kms=False)
    
    print(f"Original: {sensitive_data}")
    print(f"Encrypted: {encrypted['encrypted_data'][:50]}...")
    print(f"Method: {encrypted['encryption_method']}")
    
    # Decrypt
    decrypted = secure_storage.decrypt_data(
        encrypted['encrypted_data'],
        encrypted['encryption_method'],
        encrypted['key_id']
    )
    print(f"Decrypted: {decrypted}")
    print()
    
    # 4. Access control
    print("4. Access Control:")
    access_mgr = AccessControlManager()
    
    # Create policies
    access_mgr.create_policy('medical_data_policy', [
        {
            'users': ['doctor123', 'nurse456'],
            'resources': ['patient_records'],
            'actions': ['read', 'write'],
            'allow': True,
            'conditions': {'department': 'cardiology'}
        },
        {
            'users': ['intern789'],
            'resources': ['patient_records'],
            'actions': ['read'],
            'allow': True,
            'conditions': {'supervised': True}
        }
    ])
    
    # Test access
    test_cases = [
        ('doctor123', 'patient_records', 'read', {'department': 'cardiology'}),
        ('intern789', 'patient_records', 'write', {'supervised': True}),
        ('external_user', 'patient_records', 'read', {})
    ]
    
    for user, resource, action, context in test_cases:
        access_result = access_mgr.check_access(user, resource, action, context)
        print(f"User {user} {action} {resource}: {'✓' if access_result['access_granted'] else '✗'}")
    
    print()
    
    # 5. Privacy metrics
    print("5. Privacy Metrics:")
    
    # Calculate privacy metrics
    total_queries = 10
    pii_detected_queries = 3
    anonymized_queries = 3
    
    privacy_metrics = {
        'pii_detection_rate': (pii_detected_queries / total_queries) * 100,
        'anonymization_rate': (anonymized_queries / total_queries) * 100,
        'privacy_compliance_score': 95.5,  # Would be calculated based on various factors
        'data_minimization_score': 88.2   # Would measure data collection minimization
    }
    
    print("Privacy Performance Metrics:")
    for metric, value in privacy_metrics.items():
        print(f"  {metric}: {value}%")

if __name__ == "__main__":
    demonstrate_privacy_security()