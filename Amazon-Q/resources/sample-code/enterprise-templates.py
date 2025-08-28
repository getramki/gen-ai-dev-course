# Enterprise-Level Code Templates for Module 6

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, TypeVar, Generic
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import asyncio
import logging
from enum import Enum

# Domain-Driven Design Base Classes
T = TypeVar('T')

class AggregateRoot(ABC):
    """Base aggregate root for DDD implementation"""
    
    def __init__(self):
        self.id: Optional[str] = None
        self.version: int = 0
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()
        self._domain_events: List['DomainEvent'] = []
    
    def generate_id(self) -> str:
        """Generate unique identifier"""
        return str(uuid.uuid4())
    
    def add_domain_event(self, event: 'DomainEvent'):
        """Add domain event to aggregate"""
        self._domain_events.append(event)
    
    def clear_domain_events(self):
        """Clear domain events after publishing"""
        self._domain_events.clear()
    
    @property
    def domain_events(self) -> List['DomainEvent']:
        """Get domain events"""
        return self._domain_events.copy()
    
    def increment_version(self):
        """Increment aggregate version"""
        self.version += 1
        self.updated_at = datetime.utcnow()

@dataclass
class DomainEvent:
    """Base domain event"""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    aggregate_id: str = ""
    aggregate_type: str = ""
    event_data: Dict[str, Any] = field(default_factory=dict)
    event_version: int = 1
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    correlation_id: str = ""
    causation_id: Optional[str] = None

class ValueObject(ABC):
    """Base value object"""
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

# Repository Pattern
class Repository(ABC, Generic[T]):
    """Generic repository interface"""
    
    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save entity"""
        pass
    
    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Delete entity"""
        pass
    
    @abstractmethod
    async def find_by_criteria(self, criteria: Dict[str, Any]) -> List[T]:
        """Find entities by criteria"""
        pass

# Unit of Work Pattern
class UnitOfWork(ABC):
    """Unit of work interface"""
    
    @abstractmethod
    async def begin_transaction(self):
        """Begin transaction"""
        pass
    
    @abstractmethod
    async def commit(self):
        """Commit transaction"""
        pass
    
    @abstractmethod
    async def rollback(self):
        """Rollback transaction"""
        pass
    
    @abstractmethod
    def get_repository(self, entity_type: type) -> Repository:
        """Get repository for entity type"""
        pass

# Command Query Responsibility Segregation (CQRS)
class Command(ABC):
    """Base command"""
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))

class Query(ABC):
    """Base query"""
    pass

class CommandHandler(ABC, Generic[T]):
    """Base command handler"""
    
    @abstractmethod
    async def handle(self, command: T) -> Any:
        """Handle command"""
        pass

class QueryHandler(ABC, Generic[T]):
    """Base query handler"""
    
    @abstractmethod
    async def handle(self, query: T) -> Any:
        """Handle query"""
        pass

# Event Sourcing
class EventStore(ABC):
    """Event store interface"""
    
    @abstractmethod
    async def append_events(self, stream_id: str, events: List[DomainEvent], expected_version: int):
        """Append events to stream"""
        pass
    
    @abstractmethod
    async def get_events(self, stream_id: str, from_version: int = 0) -> List[DomainEvent]:
        """Get events from stream"""
        pass
    
    @abstractmethod
    async def get_snapshot(self, stream_id: str) -> Optional[Dict[str, Any]]:
        """Get aggregate snapshot"""
        pass
    
    @abstractmethod
    async def save_snapshot(self, stream_id: str, snapshot: Dict[str, Any], version: int):
        """Save aggregate snapshot"""
        pass

# Microservices Communication
class MessageBus(ABC):
    """Message bus interface"""
    
    @abstractmethod
    async def publish(self, message: Any, topic: str):
        """Publish message to topic"""
        pass
    
    @abstractmethod
    async def subscribe(self, topic: str, handler):
        """Subscribe to topic"""
        pass

class ServiceRegistry(ABC):
    """Service registry interface"""
    
    @abstractmethod
    async def register_service(self, service_name: str, service_url: str, health_check_url: str):
        """Register service"""
        pass
    
    @abstractmethod
    async def discover_service(self, service_name: str) -> Optional[str]:
        """Discover service URL"""
        pass
    
    @abstractmethod
    async def health_check(self, service_name: str) -> bool:
        """Check service health"""
        pass

# Circuit Breaker Pattern
class CircuitBreakerState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """Circuit breaker implementation"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60, expected_exception: type = Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitBreakerState.CLOSED
    
    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        
        if self.state == CircuitBreakerState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitBreakerState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            self._on_success()
            return result
        
        except self.expected_exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset"""
        return (
            self.last_failure_time and
            (datetime.utcnow() - self.last_failure_time).seconds >= self.recovery_timeout
        )
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

# Saga Pattern for Distributed Transactions
class SagaStep(ABC):
    """Base saga step"""
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute saga step"""
        pass
    
    @abstractmethod
    async def compensate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Compensate saga step"""
        pass

class SagaOrchestrator:
    """Saga orchestrator for distributed transactions"""
    
    def __init__(self):
        self.steps: List[SagaStep] = []
        self.executed_steps: List[SagaStep] = []
    
    def add_step(self, step: SagaStep):
        """Add step to saga"""
        self.steps.append(step)
    
    async def execute(self, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute saga"""
        context = initial_context.copy()
        
        try:
            for step in self.steps:
                context = await step.execute(context)
                self.executed_steps.append(step)
            
            return context
        
        except Exception as e:
            # Compensate in reverse order
            await self._compensate(context)
            raise e
    
    async def _compensate(self, context: Dict[str, Any]):
        """Compensate executed steps"""
        for step in reversed(self.executed_steps):
            try:
                await step.compensate(context)
            except Exception as e:
                logging.error(f"Compensation failed for step {step.__class__.__name__}: {e}")

# API Gateway Pattern
class RateLimiter:
    """Rate limiter implementation"""
    
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, List[datetime]] = {}
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        now = datetime.utcnow()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Remove old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if (now - req_time).seconds < self.time_window
        ]
        
        # Check rate limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True

class APIGateway:
    """API Gateway implementation"""
    
    def __init__(self):
        self.routes: Dict[str, str] = {}
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
    
    def register_route(self, path: str, service_url: str, rate_limit: Optional[RateLimiter] = None):
        """Register route"""
        self.routes[path] = service_url
        
        if rate_limit:
            self.rate_limiters[path] = rate_limit
        
        self.circuit_breakers[path] = CircuitBreaker()
    
    async def route_request(self, path: str, client_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Route request to appropriate service"""
        
        if path not in self.routes:
            raise ValueError(f"Route not found: {path}")
        
        # Check rate limit
        if path in self.rate_limiters:
            if not self.rate_limiters[path].is_allowed(client_id):
                raise Exception("Rate limit exceeded")
        
        # Route through circuit breaker
        service_url = self.routes[path]
        circuit_breaker = self.circuit_breakers[path]
        
        return await circuit_breaker.call(self._call_service, service_url, request_data)
    
    async def _call_service(self, service_url: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Call downstream service"""
        # Implement actual service call
        pass

# Event-Driven Architecture
class EventBus:
    """In-memory event bus implementation"""
    
    def __init__(self):
        self.handlers: Dict[str, List[callable]] = {}
    
    def subscribe(self, event_type: str, handler: callable):
        """Subscribe to event type"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    async def publish(self, event: DomainEvent):
        """Publish event"""
        event_type = event.event_type
        
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception as e:
                    logging.error(f"Error handling event {event_type}: {e}")

# Monitoring and Observability
class MetricsCollector:
    """Metrics collection interface"""
    
    def __init__(self):
        self.counters: Dict[str, int] = {}
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = {}
    
    def increment_counter(self, name: str, value: int = 1, tags: Dict[str, str] = None):
        """Increment counter metric"""
        key = self._build_key(name, tags)
        self.counters[key] = self.counters.get(key, 0) + value
    
    def set_gauge(self, name: str, value: float, tags: Dict[str, str] = None):
        """Set gauge metric"""
        key = self._build_key(name, tags)
        self.gauges[key] = value
    
    def record_histogram(self, name: str, value: float, tags: Dict[str, str] = None):
        """Record histogram value"""
        key = self._build_key(name, tags)
        if key not in self.histograms:
            self.histograms[key] = []
        self.histograms[key].append(value)
    
    def _build_key(self, name: str, tags: Dict[str, str] = None) -> str:
        """Build metric key with tags"""
        if not tags:
            return name
        
        tag_string = ",".join([f"{k}={v}" for k, v in sorted(tags.items())])
        return f"{name}[{tag_string}]"

# Health Check System
class HealthCheck(ABC):
    """Base health check"""
    
    @abstractmethod
    async def check(self) -> Dict[str, Any]:
        """Perform health check"""
        pass

class DatabaseHealthCheck(HealthCheck):
    """Database health check"""
    
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    async def check(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            # Perform simple query
            await self.db_connection.execute("SELECT 1")
            return {
                "status": "healthy",
                "component": "database",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "component": "database",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

class HealthCheckRegistry:
    """Health check registry"""
    
    def __init__(self):
        self.checks: Dict[str, HealthCheck] = {}
    
    def register(self, name: str, health_check: HealthCheck):
        """Register health check"""
        self.checks[name] = health_check
    
    async def check_all(self) -> Dict[str, Any]:
        """Run all health checks"""
        results = {}
        overall_status = "healthy"
        
        for name, check in self.checks.items():
            try:
                result = await check.check()
                results[name] = result
                
                if result.get("status") != "healthy":
                    overall_status = "unhealthy"
            
            except Exception as e:
                results[name] = {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }
                overall_status = "unhealthy"
        
        return {
            "status": overall_status,
            "checks": results,
            "timestamp": datetime.utcnow().isoformat()
        }

# Configuration Management
class ConfigurationProvider(ABC):
    """Configuration provider interface"""
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any):
        """Set configuration value"""
        pass
    
    @abstractmethod
    def reload(self):
        """Reload configuration"""
        pass

class EnvironmentConfigProvider(ConfigurationProvider):
    """Environment-based configuration provider"""
    
    def __init__(self):
        import os
        self.config = dict(os.environ)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration from environment"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration (not supported for environment)"""
        raise NotImplementedError("Cannot set environment variables")
    
    def reload(self):
        """Reload environment variables"""
        import os
        self.config = dict(os.environ)

# Security Patterns
class SecurityContext:
    """Security context for request processing"""
    
    def __init__(self, user_id: str, roles: List[str], permissions: List[str]):
        self.user_id = user_id
        self.roles = roles
        self.permissions = permissions
        self.authenticated = True
    
    def has_role(self, role: str) -> bool:
        """Check if user has role"""
        return role in self.roles
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has permission"""
        return permission in self.permissions

class AuthorizationService:
    """Authorization service"""
    
    def __init__(self):
        self.role_permissions: Dict[str, List[str]] = {}
    
    def add_role_permissions(self, role: str, permissions: List[str]):
        """Add permissions to role"""
        if role not in self.role_permissions:
            self.role_permissions[role] = []
        self.role_permissions[role].extend(permissions)
    
    def authorize(self, security_context: SecurityContext, required_permission: str) -> bool:
        """Check authorization"""
        # Check direct permission
        if security_context.has_permission(required_permission):
            return True
        
        # Check role-based permissions
        for role in security_context.roles:
            role_perms = self.role_permissions.get(role, [])
            if required_permission in role_perms:
                return True
        
        return False

# These templates provide a foundation for enterprise-level applications
# using Amazon Q to generate production-ready code following industry best practices