"""
Data models for the Enterprise Agent Coordinator
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum

class RequestPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class AgentType(str, Enum):
    CONTENT_RESEARCH = "content_research"
    TECHNICAL_SEO = "technical_seo"
    PROJECT_PLANNING = "project_planning"
    BRD_GENERATION = "brd_generation"
    SOCIAL_MEDIA = "social_media"

class ClientCardType(str, Enum):
    """Types of client cards for data filtering"""
    BRAND_GUIDELINES = "brand_guidelines"
    TARGET_AUDIENCE = "target_audience"
    CLIENT_PROFILE = "client_profile"
    CONTENT_BRIEF = "content_brief"

class AgentStatusEnum(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    MAINTENANCE = "maintenance"

class CoordinationRequest(BaseModel):
    """Request model for agent coordination"""
    query: str = Field(..., description="User query to be processed")
    priority: RequestPriority = Field(default=RequestPriority.MEDIUM, description="Request priority level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context for the request")
    preferred_agents: Optional[List[AgentType]] = Field(default=None, description="Preferred agents for processing")
    max_response_time: Optional[int] = Field(default=30, description="Maximum response time in seconds")
    require_multi_agent: Optional[bool] = Field(default=False, description="Whether to require multiple agents")

class AgentResponse(BaseModel):
    """Response from a single agent"""
    agent_id: str
    agent_type: AgentType
    response: str
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level of the response")
    processing_time: float
    sources: Optional[List[str]] = Field(default=None, description="Sources used for the response")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class CoordinationResponse(BaseModel):
    """Response from the coordination system"""
    request_id: str
    routing_decision: Dict[str, Any]
    agent_responses: List[AgentResponse]
    synthesized_response: str
    total_processing_time: float
    quality_score: float = Field(..., ge=0.0, le=1.0)
    recommendations: Optional[List[str]] = Field(default=None)
    next_actions: Optional[List[str]] = Field(default=None)

class AgentStatus(BaseModel):
    """Status information for an agent"""
    agent_id: str
    agent_type: AgentType
    status: AgentStatusEnum
    last_health_check: datetime
    current_load: int = Field(..., ge=0, description="Current number of active requests")
    max_capacity: int = Field(..., ge=1, description="Maximum concurrent requests")
    average_response_time: float
    success_rate: float = Field(..., ge=0.0, le=1.0)
    version: str
    endpoint_url: str

class SystemHealth(BaseModel):
    """Overall system health status"""
    status: str
    timestamp: datetime
    agents: List[AgentStatus]
    active_requests: int
    total_requests_today: int
    average_response_time: float
    system_load: float = Field(..., ge=0.0, le=1.0)
    uptime_percentage: float = Field(..., ge=0.0, le=100.0)

class QualityMetrics(BaseModel):
    """Quality metrics for the system"""
    response_accuracy: float = Field(..., ge=0.0, le=1.0)
    user_satisfaction: float = Field(..., ge=0.0, le=5.0)
    sla_compliance: float = Field(..., ge=0.0, le=1.0)
    error_rate: float = Field(..., ge=0.0, le=1.0)
    recommendation_acceptance: float = Field(..., ge=0.0, le=1.0)

class RoutingDecision(BaseModel):
    """Details about routing decision"""
    selected_agents: List[AgentType]
    reasoning: str
    estimated_completion_time: float
    confidence: float = Field(..., ge=0.0, le=1.0)
    fallback_agents: Optional[List[AgentType]] = Field(default=None)

class WorkflowStep(BaseModel):
    """Individual step in a multi-agent workflow"""
    step_id: str
    agent_type: AgentType
    agent_id: str
    depends_on: Optional[List[str]] = Field(default=None, description="Step IDs this step depends on")
    parameters: Dict[str, Any]
    estimated_duration: float

class MultiAgentWorkflow(BaseModel):
    """Definition of a multi-agent workflow"""
    workflow_id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    total_estimated_duration: float
    created_at: datetime
    created_by: str

class User(BaseModel):
    """User model for authentication and authorization"""
    user_id: str
    email: str
    name: str
    roles: List[str]
    is_admin: bool = False
    created_at: datetime
    last_login: Optional[datetime] = None

class AuditLog(BaseModel):
    """Audit log entry"""
    log_id: str
    timestamp: datetime
    user_id: str
    action: str
    resource: str
    details: Dict[str, Any]
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class PerformanceMetrics(BaseModel):
    """Detailed performance metrics"""
    timestamp: datetime
    requests_per_minute: float
    average_response_time: float
    p95_response_time: float
    p99_response_time: float
    error_rate: float
    active_connections: int
    memory_usage: float
    cpu_usage: float
    
class CircuitBreakerState(BaseModel):
    """Circuit breaker state for an agent"""
    agent_id: str
    state: str  # CLOSED, OPEN, HALF_OPEN
    failure_count: int
    last_failure_time: Optional[datetime] = None
    next_attempt_time: Optional[datetime] = None
    success_threshold: int = 5
    failure_threshold: int = 10
    timeout_duration: int = 60  # seconds

# Client Context Models for Card Integration

class CoordinationRequestWithClient(CoordinationRequest):
    """Extended coordination request with client context"""
    client_id: Optional[str] = Field(default=None, description="Client ID for context retrieval")
    use_client_context: bool = Field(default=False, description="Whether to use client context")

class ClientContext(BaseModel):
    """Simplified client context for agents"""
    client_id: str
    brand_voice: Optional[Dict[str, Any]] = Field(default=None, description="Brand voice and tone guidelines")
    target_audience: Optional[Dict[str, Any]] = Field(default=None, description="Target audience information")
    compliance_notes: Optional[List[str]] = Field(default=None, description="Compliance requirements")
    
class CoordinationResponseWithClient(CoordinationResponse):
    """Extended response with client context info"""
    client_context_used: bool = Field(default=False, description="Whether client context was used in processing")
