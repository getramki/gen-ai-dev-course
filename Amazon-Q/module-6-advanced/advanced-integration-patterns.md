# Advanced Integration Patterns with Amazon Q

## Enterprise-Level Integration Strategies

---

## 1. Microservices Architecture Patterns

### Service Mesh Integration

#### Istio Configuration Generation
```yaml
# Amazon Q can generate complete service mesh configurations
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: user-service
  namespace: ecommerce
spec:
  hosts:
  - user-service
  http:
  - match:
    - headers:
        version:
          exact: v2
    route:
    - destination:
        host: user-service
        subset: v2
      weight: 100
  - route:
    - destination:
        host: user-service
        subset: v1
      weight: 100
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: user-service
  namespace: ecommerce
spec:
  host: user-service
  trafficPolicy:
    circuitBreaker:
      consecutiveErrors: 3
      interval: 30s
      baseEjectionTime: 30s
    retryPolicy:
      attempts: 3
      perTryTimeout: 2s
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

#### Event-Driven Communication
```python
# Amazon Q generates event-driven patterns
from dataclasses import dataclass, asdict
from typing import Dict, Any, List
from datetime import datetime
import json
import asyncio
from abc import ABC, abstractmethod

@dataclass
class DomainEvent:
    """Base domain event class"""
    event_id: str
    event_type: str
    aggregate_id: str
    aggregate_type: str
    event_data: Dict[str, Any]
    event_version: int
    occurred_at: datetime
    correlation_id: str
    causation_id: str = None

class EventStore(ABC):
    """Abstract event store interface"""
    
    @abstractmethod
    async def append_events(self, stream_id: str, events: List[DomainEvent], expected_version: int):
        pass
    
    @abstractmethod
    async def get_events(self, stream_id: str, from_version: int = 0) -> List[DomainEvent]:
        pass

class EventBus(ABC):
    """Abstract event bus interface"""
    
    @abstractmethod
    async def publish(self, events: List[DomainEvent]):
        pass
    
    @abstractmethod
    async def subscribe(self, event_type: str, handler):
        pass

class UserAggregate:
    """User aggregate with event sourcing"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.version = 0
        self.uncommitted_events: List[DomainEvent] = []
        self.username = None
        self.email = None
        self.is_active = True
    
    def create_user(self, username: str, email: str, correlation_id: str):
        """Create new user with event"""
        if self.version > 0:
            raise ValueError("User already exists")
        
        event = DomainEvent(
            event_id=str(uuid.uuid4()),
            event_type="UserCreated",
            aggregate_id=self.user_id,
            aggregate_type="User",
            event_data={
                "username": username,
                "email": email
            },
            event_version=1,
            occurred_at=datetime.utcnow(),
            correlation_id=correlation_id
        )
        
        self._apply_event(event)
        self.uncommitted_events.append(event)
    
    def _apply_event(self, event: DomainEvent):
        """Apply event to aggregate state"""
        if event.event_type == "UserCreated":
            self.username = event.event_data["username"]
            self.email = event.event_data["email"]
            self.version = event.event_version
        elif event.event_type == "UserDeactivated":
            self.is_active = False
            self.version = event.event_version
```

### API Gateway Patterns

#### Kong Configuration
```yaml
# Amazon Q generates API Gateway configurations
apiVersion: configuration.konghq.com/v1
kind: KongIngress
metadata:
  name: user-service-kong
proxy:
  connect_timeout: 10000
  retries: 3
  read_timeout: 10000
  write_timeout: 10000
route:
  methods:
  - GET
  - POST
  - PUT
  - DELETE
  regex_priority: 0
  strip_path: false
  preserve_host: true
upstream:
  algorithm: round-robin
  hash_on: none
  hash_fallback: none
  healthchecks:
    active:
      concurrency: 10
      healthy:
        http_statuses:
        - 200
        - 302
        interval: 0
        successes: 0
      http_path: "/health"
      timeout: 1
      unhealthy:
        http_failures: 0
        http_statuses:
        - 429
        - 404
        - 500
        - 501
        - 502
        - 503
        - 504
        - 505
        interval: 0
        tcp_failures: 0
        timeouts: 0
```

---

## 2. Cloud-Native Integration Patterns

### AWS Lambda with Event Bridge
```python
# Amazon Q generates serverless event-driven architectures
import json
import boto3
from typing import Dict, Any
from datetime import datetime

class EventBridgePublisher:
    """Publish events to AWS EventBridge"""
    
    def __init__(self, event_bus_name: str):
        self.event_bridge = boto3.client('events')
        self.event_bus_name = event_bus_name
    
    async def publish_event(self, event_type: str, source: str, detail: Dict[str, Any]):
        """Publish event to EventBridge"""
        
        event_entry = {
            'Source': source,
            'DetailType': event_type,
            'Detail': json.dumps(detail),
            'EventBusName': self.event_bus_name,
            'Time': datetime.utcnow()
        }
        
        response = self.event_bridge.put_events(
            Entries=[event_entry]
        )
        
        return response

def lambda_handler(event, context):
    """Lambda function handler for user events"""
    
    try:
        # Parse the incoming event
        event_detail = json.loads(event['Records'][0]['body'])
        
        # Process based on event type
        if event_detail['event_type'] == 'UserCreated':
            return handle_user_created(event_detail)
        elif event_detail['event_type'] == 'UserUpdated':
            return handle_user_updated(event_detail)
        else:
            print(f"Unknown event type: {event_detail['event_type']}")
            return {'statusCode': 200}
    
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def handle_user_created(event_detail: Dict[str, Any]):
    """Handle user creation event"""
    
    user_data = event_detail['data']
    
    # Send welcome email
    send_welcome_email(user_data['email'], user_data['username'])
    
    # Create user profile
    create_user_profile(user_data['user_id'])
    
    # Publish follow-up events
    publisher = EventBridgePublisher('user-events')
    publisher.publish_event(
        event_type='UserOnboardingStarted',
        source='user-service',
        detail={'user_id': user_data['user_id']}
    )
    
    return {'statusCode': 200}
```

### Kubernetes Operators
```python
# Amazon Q generates Kubernetes operators
import kopf
import kubernetes
from typing import Dict, Any

@kopf.on.create('ecommerce.io', 'v1', 'applications')
def create_application(spec: Dict[str, Any], name: str, namespace: str, **kwargs):
    """Handle application creation"""
    
    # Create deployment
    deployment = create_deployment_manifest(spec, name, namespace)
    kubernetes.client.AppsV1Api().create_namespaced_deployment(
        namespace=namespace,
        body=deployment
    )
    
    # Create service
    service = create_service_manifest(spec, name, namespace)
    kubernetes.client.CoreV1Api().create_namespaced_service(
        namespace=namespace,
        body=service
    )
    
    # Create ingress if specified
    if spec.get('ingress', {}).get('enabled', False):
        ingress = create_ingress_manifest(spec, name, namespace)
        kubernetes.client.NetworkingV1Api().create_namespaced_ingress(
            namespace=namespace,
            body=ingress
        )
    
    return {'status': 'created'}

def create_deployment_manifest(spec: Dict[str, Any], name: str, namespace: str):
    """Create Kubernetes deployment manifest"""
    
    return {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': name,
            'namespace': namespace,
            'labels': {
                'app': name,
                'managed-by': 'ecommerce-operator'
            }
        },
        'spec': {
            'replicas': spec.get('replicas', 3),
            'selector': {
                'matchLabels': {
                    'app': name
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'app': name
                    }
                },
                'spec': {
                    'containers': [{
                        'name': name,
                        'image': spec['image'],
                        'ports': [{
                            'containerPort': spec.get('port', 8080)
                        }],
                        'resources': spec.get('resources', {
                            'requests': {
                                'memory': '128Mi',
                                'cpu': '100m'
                            },
                            'limits': {
                                'memory': '256Mi',
                                'cpu': '200m'
                            }
                        }),
                        'env': [
                            {'name': k, 'value': v} 
                            for k, v in spec.get('env', {}).items()
                        ]
                    }]
                }
            }
        }
    }
```

---

## 3. Data Integration Patterns

### Event Sourcing with CQRS
```python
# Amazon Q generates CQRS implementation
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import asyncio
from dataclasses import dataclass

class Command(ABC):
    """Base command class"""
    pass

class Query(ABC):
    """Base query class"""
    pass

@dataclass
class CreateUserCommand(Command):
    username: str
    email: str
    password: str
    correlation_id: str

@dataclass
class GetUserQuery(Query):
    user_id: str

class CommandHandler(ABC):
    """Abstract command handler"""
    
    @abstractmethod
    async def handle(self, command: Command) -> Any:
        pass

class QueryHandler(ABC):
    """Abstract query handler"""
    
    @abstractmethod
    async def handle(self, query: Query) -> Any:
        pass

class CreateUserCommandHandler(CommandHandler):
    """Handle user creation commands"""
    
    def __init__(self, event_store: EventStore, event_bus: EventBus):
        self.event_store = event_store
        self.event_bus = event_bus
    
    async def handle(self, command: CreateUserCommand) -> str:
        # Create aggregate
        user_id = str(uuid.uuid4())
        user = UserAggregate(user_id)
        
        # Execute business logic
        user.create_user(
            username=command.username,
            email=command.email,
            correlation_id=command.correlation_id
        )
        
        # Persist events
        await self.event_store.append_events(
            stream_id=f"user-{user_id}",
            events=user.uncommitted_events,
            expected_version=0
        )
        
        # Publish events
        await self.event_bus.publish(user.uncommitted_events)
        
        return user_id

class UserProjection:
    """User read model projection"""
    
    def __init__(self, read_store):
        self.read_store = read_store
    
    async def handle_user_created(self, event: DomainEvent):
        """Handle UserCreated event"""
        
        user_data = {
            'user_id': event.aggregate_id,
            'username': event.event_data['username'],
            'email': event.event_data['email'],
            'created_at': event.occurred_at,
            'is_active': True
        }
        
        await self.read_store.insert('users', user_data)
    
    async def handle_user_updated(self, event: DomainEvent):
        """Handle UserUpdated event"""
        
        await self.read_store.update(
            'users',
            {'user_id': event.aggregate_id},
            event.event_data
        )
```

### Stream Processing with Kafka
```python
# Amazon Q generates Kafka stream processing
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import asyncio
from typing import Dict, Any, Callable

class EventStreamProcessor:
    """Process events from Kafka streams"""
    
    def __init__(self, bootstrap_servers: List[str]):
        self.bootstrap_servers = bootstrap_servers
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        self.handlers: Dict[str, List[Callable]] = {}
    
    def register_handler(self, event_type: str, handler: Callable):
        """Register event handler"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    async def publish_event(self, topic: str, event: Dict[str, Any], key: str = None):
        """Publish event to Kafka topic"""
        
        try:
            future = self.producer.send(topic, value=event, key=key)
            record_metadata = future.get(timeout=10)
            
            return {
                'topic': record_metadata.topic,
                'partition': record_metadata.partition,
                'offset': record_metadata.offset
            }
        
        except KafkaError as e:
            print(f"Failed to publish event: {e}")
            raise
    
    async def start_consuming(self, topics: List[str], group_id: str):
        """Start consuming events from topics"""
        
        consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            auto_offset_reset='earliest'
        )
        
        try:
            for message in consumer:
                event = message.value
                event_type = event.get('event_type')
                
                if event_type in self.handlers:
                    for handler in self.handlers[event_type]:
                        try:
                            await handler(event)
                        except Exception as e:
                            print(f"Error handling event {event_type}: {e}")
        
        except KeyboardInterrupt:
            print("Stopping consumer...")
        finally:
            consumer.close()

# Usage example
async def handle_user_created(event: Dict[str, Any]):
    """Handle user created event"""
    user_data = event['data']
    
    # Send welcome email
    await send_welcome_email(user_data['email'])
    
    # Create user profile
    await create_user_profile(user_data['user_id'])

# Setup stream processor
processor = EventStreamProcessor(['localhost:9092'])
processor.register_handler('UserCreated', handle_user_created)

# Start consuming
await processor.start_consuming(['user-events'], 'user-service-group')
```

---

## 4. Security Integration Patterns

### Zero Trust Architecture
```python
# Amazon Q generates zero trust security patterns
from typing import Dict, Any, List, Optional
import jwt
from datetime import datetime, timedelta
import hashlib
import hmac

class ZeroTrustAuthenticator:
    """Zero trust authentication and authorization"""
    
    def __init__(self, secret_key: str, policy_engine):
        self.secret_key = secret_key
        self.policy_engine = policy_engine
    
    def create_access_token(self, user_id: str, roles: List[str], 
                          device_id: str, ip_address: str) -> str:
        """Create short-lived access token"""
        
        payload = {
            'user_id': user_id,
            'roles': roles,
            'device_id': device_id,
            'ip_address': ip_address,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=15),  # Short expiration
            'jti': self._generate_jti(user_id, device_id)
        }
        
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def validate_request(self, token: str, resource: str, 
                        action: str, context: Dict[str, Any]) -> bool:
        """Validate request with zero trust principles"""
        
        try:
            # Decode and validate token
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            # Check device trust
            if not self._is_device_trusted(payload['device_id']):
                return False
            
            # Check location/IP
            if not self._is_location_allowed(payload['ip_address'], context.get('current_ip')):
                return False
            
            # Check behavioral patterns
            if not self._is_behavior_normal(payload['user_id'], context):
                return False
            
            # Check policy authorization
            return self.policy_engine.authorize(
                user_id=payload['user_id'],
                roles=payload['roles'],
                resource=resource,
                action=action,
                context=context
            )
        
        except jwt.InvalidTokenError:
            return False
    
    def _generate_jti(self, user_id: str, device_id: str) -> str:
        """Generate unique token identifier"""
        data = f"{user_id}:{device_id}:{datetime.utcnow().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _is_device_trusted(self, device_id: str) -> bool:
        """Check if device is trusted"""
        # Implement device trust verification
        return True  # Simplified
    
    def _is_location_allowed(self, token_ip: str, current_ip: str) -> bool:
        """Check if location change is allowed"""
        # Implement geolocation verification
        return token_ip == current_ip  # Simplified
    
    def _is_behavior_normal(self, user_id: str, context: Dict[str, Any]) -> bool:
        """Check for behavioral anomalies"""
        # Implement behavioral analysis
        return True  # Simplified

class PolicyEngine:
    """Attribute-based access control (ABAC) policy engine"""
    
    def __init__(self):
        self.policies = []
    
    def add_policy(self, policy: Dict[str, Any]):
        """Add access control policy"""
        self.policies.append(policy)
    
    def authorize(self, user_id: str, roles: List[str], 
                 resource: str, action: str, context: Dict[str, Any]) -> bool:
        """Evaluate authorization policies"""
        
        for policy in self.policies:
            if self._matches_policy(policy, user_id, roles, resource, action, context):
                return policy.get('effect') == 'allow'
        
        return False  # Deny by default
    
    def _matches_policy(self, policy: Dict[str, Any], user_id: str, 
                       roles: List[str], resource: str, action: str, 
                       context: Dict[str, Any]) -> bool:
        """Check if policy matches request"""
        
        # Check subject (user/role)
        if not self._matches_subject(policy.get('subject', {}), user_id, roles):
            return False
        
        # Check resource
        if not self._matches_resource(policy.get('resource', {}), resource):
            return False
        
        # Check action
        if not self._matches_action(policy.get('action', {}), action):
            return False
        
        # Check conditions
        if not self._matches_conditions(policy.get('conditions', {}), context):
            return False
        
        return True
```

---

## 5. Observability Integration Patterns

### Distributed Tracing
```python
# Amazon Q generates distributed tracing implementation
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import logging
from typing import Dict, Any, Optional
from functools import wraps

class DistributedTracing:
    """Distributed tracing setup and utilities"""
    
    def __init__(self, service_name: str, jaeger_endpoint: str):
        self.service_name = service_name
        
        # Configure tracer
        trace.set_tracer_provider(TracerProvider())
        tracer = trace.get_tracer_provider()
        
        # Configure Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name="localhost",
            agent_port=6831,
        )
        
        span_processor = BatchSpanProcessor(jaeger_exporter)
        tracer.add_span_processor(span_processor)
        
        self.tracer = trace.get_tracer(service_name)
        
        # Auto-instrument Flask and requests
        FlaskInstrumentor().instrument()
        RequestsInstrumentor().instrument()
    
    def trace_method(self, operation_name: str = None):
        """Decorator to trace method execution"""
        
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                span_name = operation_name or f"{func.__module__}.{func.__name__}"
                
                with self.tracer.start_as_current_span(span_name) as span:
                    try:
                        # Add method attributes
                        span.set_attribute("method.name", func.__name__)
                        span.set_attribute("method.module", func.__module__)
                        
                        # Execute method
                        result = func(*args, **kwargs)
                        
                        # Add result attributes if applicable
                        if hasattr(result, '__len__'):
                            span.set_attribute("result.length", len(result))
                        
                        return result
                    
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                        raise
            
            return wrapper
        return decorator
    
    def add_span_attributes(self, attributes: Dict[str, Any]):
        """Add attributes to current span"""
        current_span = trace.get_current_span()
        if current_span:
            for key, value in attributes.items():
                current_span.set_attribute(key, str(value))
    
    def add_span_event(self, name: str, attributes: Dict[str, Any] = None):
        """Add event to current span"""
        current_span = trace.get_current_span()
        if current_span:
            current_span.add_event(name, attributes or {})

# Usage example
tracing = DistributedTracing("user-service", "http://jaeger:14268")

@tracing.trace_method("user.create")
def create_user(user_data: Dict[str, Any]) -> str:
    """Create new user with tracing"""
    
    # Add custom attributes
    tracing.add_span_attributes({
        "user.email": user_data.get("email"),
        "user.username": user_data.get("username")
    })
    
    # Add events
    tracing.add_span_event("validation.started")
    
    # Validate user data
    if not validate_user_data(user_data):
        raise ValueError("Invalid user data")
    
    tracing.add_span_event("validation.completed")
    tracing.add_span_event("database.save.started")
    
    # Save to database
    user_id = save_user_to_database(user_data)
    
    tracing.add_span_event("database.save.completed", {
        "user.id": user_id
    })
    
    return user_id
```

These advanced integration patterns demonstrate how Amazon Q can help generate enterprise-level code that follows industry best practices for microservices, cloud-native applications, security, and observability. Each pattern provides a foundation that can be extended and customized for specific organizational needs.