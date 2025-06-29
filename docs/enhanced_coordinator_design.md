# Enhanced Coordinator Agent: Client Card Integration & Intelligent Data Brokering

## Executive Summary

This document outlines the necessary updates to the existing Agent Coordinator to support the client card system and implement intelligent data brokering capabilities. The enhanced coordinator will serve as the central hub for client knowledge management and contextual agent coordination.

## Current Coordinator Analysis

### Existing Strengths:
- ✅ FastAPI foundation with async support
- ✅ Request routing and load balancing
- ✅ Agent status monitoring
- ✅ JWT-based authentication
- ✅ Quality metrics tracking
- ✅ Circuit breaker patterns

### Integration Requirements:
- **Client Card System Integration**
- **Intelligent Data Brokering**
- **Context-Aware Agent Routing**
- **Client Privacy Controls**
- **Audit Trail Enhancement**

## Enhanced Coordinator Architecture

### 1. Updated Data Models

```python
# New models to add to models.py

class ClientCardType(str, Enum):
    """Types of client cards"""
    CLIENT_PROFILE = "client_profile"
    BRAND_GUIDELINES = "brand_guidelines"
    TARGET_AUDIENCE = "target_audience"
    PRODUCT_SERVICE = "product_service"
    REGULATORY_COMPLIANCE = "regulatory_compliance"
    CONTENT_BRIEF = "content_brief"
    PROJECT_BRIEF = "project_brief"
    CONFIGURATION_ACCESS = "configuration_access"

class DataExposureLevel(str, Enum):
    """Levels of data exposure for agents"""
    FULL_ACCESS = "full_access"
    SUMMARY_ONLY = "summary_only"
    DEMOGRAPHICS_ONLY = "demographics_only"
    TONE_AND_MESSAGING_ONLY = "tone_and_messaging_only"
    TECHNICAL_ONLY = "technical_only"
    NONE = "none"

class ClientCard(BaseModel):
    """Base client card model"""
    card_id: str
    client_id: str
    card_type: ClientCardType
    version: str
    created_at: datetime
    updated_at: datetime
    created_by: str
    is_active: bool = True
    data: Dict[str, Any]
    privacy_level: str = "standard"
    audit_trail: List[Dict[str, Any]] = []

class ClientKnowledgeTree(BaseModel):
    """Hierarchical client knowledge structure"""
    client_id: str
    client_name: str
    
    # Level 1: Core Cards
    client_profile_card: Optional[ClientCard] = None
    brand_guidelines_card: Optional[ClientCard] = None
    target_audience_card: Optional[ClientCard] = None
    
    # Level 2: Derived Knowledge
    content_strategy: Dict[str, Any] = {}
    seo_strategy: Dict[str, Any] = {}
    project_methodologies: Dict[str, Any] = {}
    
    # Level 3: Execution Knowledge
    content_performance: Dict[str, Any] = {}
    workflow_preferences: Dict[str, Any] = {}
    success_patterns: Dict[str, Any] = {}
    
    # Level 4: Predictive Knowledge
    recommended_strategies: List[Dict[str, Any]] = []
    opportunity_identification: List[Dict[str, Any]] = []
    risk_assessments: Dict[str, Any] = {}

class AgentDataRequest(BaseModel):
    """Request for client data by an agent"""
    agent_id: str
    agent_type: AgentType
    client_id: str
    requested_data_types: List[ClientCardType]
    task_context: Dict[str, Any]
    sensitivity_level: str = "standard"

class ClientContextResponse(BaseModel):
    """Filtered client context for agents"""
    client_id: str
    agent_id: str
    filtered_context: Dict[str, Any]
    exposure_levels: Dict[str, DataExposureLevel]
    access_granted_at: datetime
    expires_at: Optional[datetime] = None

class CoordinationRequestEnhanced(CoordinationRequest):
    """Enhanced coordination request with client context"""
    client_id: Optional[str] = None
    requires_client_context: bool = False
    context_sensitivity: str = "standard"
    client_permissions_override: Optional[Dict[str, Any]] = None
```

### 2. Enhanced Coordinator Class

```python
# Enhanced coordinator.py

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import uuid
import json
from .client_card_manager import ClientCardManager
from .data_broker import IntelligentDataBroker
from .context_optimizer import ContextOptimizer

class EnhancedAgentCoordinator:
    """
    Enhanced coordinator with client card integration and intelligent data brokering
    """
    
    def __init__(self):
        # Existing agent pool (enhanced)
        self.agents = {
            "research_content_agent": {
                "type": AgentType.CONTENT_RESEARCH,
                "status": AgentStatusEnum.HEALTHY,
                "endpoint": "http://research-content-agent/api",
                "client_data_requirements": [
                    ClientCardType.BRAND_GUIDELINES,
                    ClientCardType.TARGET_AUDIENCE,
                    ClientCardType.CONTENT_BRIEF
                ],
                "data_exposure_config": {
                    ClientCardType.BRAND_GUIDELINES: DataExposureLevel.FULL_ACCESS,
                    ClientCardType.TARGET_AUDIENCE: DataExposureLevel.FULL_ACCESS,
                    ClientCardType.REGULATORY_COMPLIANCE: DataExposureLevel.SUMMARY_ONLY
                },
                "last_health_check": datetime.utcnow(),
                "current_load": 0,
                "max_capacity": 100,
                "average_response_time": 0.5
            },
            "technical_seo_agent": {
                "type": AgentType.TECHNICAL_SEO,
                "status": AgentStatusEnum.HEALTHY,
                "endpoint": "http://technical-seo-agent/api",
                "client_data_requirements": [
                    ClientCardType.CLIENT_PROFILE,
                    ClientCardType.BRAND_GUIDELINES,
                    ClientCardType.CONFIGURATION_ACCESS
                ],
                "data_exposure_config": {
                    ClientCardType.BRAND_GUIDELINES: DataExposureLevel.TONE_AND_MESSAGING_ONLY,
                    ClientCardType.TARGET_AUDIENCE: DataExposureLevel.DEMOGRAPHICS_ONLY,
                    ClientCardType.CONFIGURATION_ACCESS: DataExposureLevel.TECHNICAL_ONLY
                },
                "last_health_check": datetime.utcnow(),
                "current_load": 0,
                "max_capacity": 100,
                "average_response_time": 0.5
            },
            "social_media_agent": {
                "type": AgentType.SOCIAL_MEDIA,
                "status": AgentStatusEnum.HEALTHY,
                "endpoint": "http://social-media-agent/api",
                "client_data_requirements": [
                    ClientCardType.BRAND_GUIDELINES,
                    ClientCardType.TARGET_AUDIENCE,
                    ClientCardType.CONFIGURATION_ACCESS
                ],
                "data_exposure_config": {
                    ClientCardType.BRAND_GUIDELINES: DataExposureLevel.FULL_ACCESS,
                    ClientCardType.TARGET_AUDIENCE: DataExposureLevel.FULL_ACCESS,
                    ClientCardType.CONFIGURATION_ACCESS: DataExposureLevel.FULL_ACCESS
                },
                "last_health_check": datetime.utcnow(),
                "current_load": 0,
                "max_capacity": 100,
                "average_response_time": 0.5
            }
        }
        
        # Initialize new components
        self.client_card_manager = ClientCardManager()
        self.data_broker = IntelligentDataBroker()
        self.context_optimizer = ContextOptimizer()
        
        # Client knowledge trees cache
        self.knowledge_trees_cache = {}
        self.cache_ttl = timedelta(minutes=15)

    async def process_request_with_context(
        self, 
        request: CoordinationRequestEnhanced, 
        user: User
    ) -> CoordinationResponse:
        """
        Enhanced request processing with client context integration
        """
        request_id = str(uuid.uuid4())
        
        # Step 1: Get client context if required
        client_context = None
        if request.requires_client_context and request.client_id:
            client_context = await self._get_client_context(
                client_id=request.client_id,
                user=user,
                sensitivity_level=request.context_sensitivity
            )
        
        # Step 2: Enhanced routing with context awareness
        routing_decision = await self._route_request_with_context(
            request=request,
            client_context=client_context,
            user=user
        )
        
        # Step 3: Prepare agent-specific contexts
        agent_contexts = await self._prepare_agent_contexts(
            selected_agents=routing_decision["selected_agents"],
            client_context=client_context,
            request=request
        )
        
        # Step 4: Execute agents with contextual data
        agent_responses = await self._execute_agents_with_context(
            routing_decision=routing_decision,
            agent_contexts=agent_contexts,
            request=request
        )
        
        # Step 5: Synthesize responses with context awareness
        synthesized_response = await self._synthesize_responses_with_context(
            agent_responses=agent_responses,
            client_context=client_context,
            request=request
        )
        
        # Step 6: Update knowledge tree based on execution
        if client_context:
            await self._update_knowledge_tree(
                client_id=request.client_id,
                agent_responses=agent_responses,
                synthesized_response=synthesized_response
            )
        
        return CoordinationResponse(
            request_id=request_id,
            routing_decision=routing_decision,
            agent_responses=agent_responses,
            synthesized_response=synthesized_response,
            total_processing_time=random.uniform(0.1, 3.0),
            quality_score=random.uniform(0.7, 1.0),
            client_context_used=client_context is not None
        )

    async def _get_client_context(
        self, 
        client_id: str, 
        user: User, 
        sensitivity_level: str = "standard"
    ) -> Optional[ClientKnowledgeTree]:
        """
        Retrieve and validate client context with proper authorization
        """
        # Check cache first
        cache_key = f"{client_id}:{sensitivity_level}"
        if cache_key in self.knowledge_trees_cache:
            cached_entry = self.knowledge_trees_cache[cache_key]
            if datetime.utcnow() - cached_entry["timestamp"] < self.cache_ttl:
                return cached_entry["knowledge_tree"]
        
        # Validate user has access to client data
        has_access = await self._validate_user_client_access(user, client_id)
        if not has_access:
            logger.warning(f"User {user.user_id} attempted unauthorized access to client {client_id}")
            return None
        
        # Retrieve knowledge tree
        knowledge_tree = await self.client_card_manager.get_client_knowledge_tree(client_id)
        
        # Cache the result
        self.knowledge_trees_cache[cache_key] = {
            "knowledge_tree": knowledge_tree,
            "timestamp": datetime.utcnow()
        }
        
        return knowledge_tree

    async def _route_request_with_context(
        self, 
        request: CoordinationRequestEnhanced, 
        client_context: Optional[ClientKnowledgeTree],
        user: User
    ) -> Dict[str, Any]:
        """
        Enhanced routing that considers client context and agent capabilities
        """
        # Analyze request to determine required agent types
        required_agent_types = await self._analyze_request_requirements(request)
        
        # Filter agents based on availability and client context requirements
        suitable_agents = []
        for agent_id, agent_config in self.agents.items():
            if agent_config["type"] in required_agent_types:
                if await self._validate_agent_for_client_context(agent_config, client_context):
                    suitable_agents.append(agent_config)
        
        # Apply intelligent selection based on client preferences and performance
        selected_agents = await self._select_optimal_agents(
            suitable_agents=suitable_agents,
            client_context=client_context,
            request=request
        )
        
        return {
            "selected_agents": selected_agents,
            "reasoning": f"Selected {len(selected_agents)} agents based on context and capabilities",
            "client_context_considered": client_context is not None,
            "routing_strategy": "context_aware_optimal"
        }

    async def _prepare_agent_contexts(
        self, 
        selected_agents: List[Dict[str, Any]], 
        client_context: Optional[ClientKnowledgeTree],
        request: CoordinationRequestEnhanced
    ) -> Dict[str, Dict[str, Any]]:
        """
        Prepare agent-specific contexts using intelligent data brokering
        """
        agent_contexts = {}
        
        for agent in selected_agents:
            agent_type = agent["type"]
            
            if client_context:
                # Create agent data request
                data_request = AgentDataRequest(
                    agent_id=agent["type"].value,
                    agent_type=agent_type,
                    client_id=client_context.client_id,
                    requested_data_types=agent.get("client_data_requirements", []),
                    task_context=request.context or {},
                    sensitivity_level=request.context_sensitivity
                )
                
                # Apply intelligent data brokering
                filtered_context = await self.data_broker.get_agent_context(
                    data_request=data_request,
                    knowledge_tree=client_context,
                    exposure_config=agent.get("data_exposure_config", {})
                )
                
                agent_contexts[agent_type.value] = filtered_context
            else:
                agent_contexts[agent_type.value] = {}
        
        return agent_contexts

    async def _execute_agents_with_context(
        self, 
        routing_decision: Dict[str, Any], 
        agent_contexts: Dict[str, Dict[str, Any]],
        request: CoordinationRequestEnhanced
    ) -> List[AgentResponse]:
        """
        Execute agents with their specific contextual data
        """
        agent_responses = []
        
        for agent in routing_decision["selected_agents"]:
            agent_type = agent["type"]
            agent_context = agent_contexts.get(agent_type.value, {})
            
            # Prepare enhanced request payload
            enhanced_payload = {
                "query": request.query,
                "context": request.context or {},
                "client_context": agent_context,
                "priority": request.priority,
                "max_response_time": request.max_response_time
            }
            
            # Execute agent (simulated for now)
            response = await self._call_agent(agent, enhanced_payload)
            agent_responses.append(response)
        
        return agent_responses

    async def _synthesize_responses_with_context(
        self, 
        agent_responses: List[AgentResponse], 
        client_context: Optional[ClientKnowledgeTree],
        request: CoordinationRequestEnhanced
    ) -> str:
        """
        Synthesize agent responses considering client context and brand guidelines
        """
        if not client_context:
            return self._basic_synthesis(agent_responses)
        
        # Get brand guidelines for synthesis
        brand_guidelines = None
        if client_context.brand_guidelines_card:
            brand_guidelines = client_context.brand_guidelines_card.data
        
        # Apply context-aware synthesis
        synthesized_response = await self.context_optimizer.synthesize_with_brand_awareness(
            agent_responses=agent_responses,
            brand_guidelines=brand_guidelines,
            client_preferences=client_context.workflow_preferences
        )
        
        return synthesized_response

    async def _update_knowledge_tree(
        self, 
        client_id: str, 
        agent_responses: List[AgentResponse],
        synthesized_response: str
    ):
        """
        Update client knowledge tree based on agent execution results
        """
        # Extract performance metrics
        performance_data = {
            "response_quality": sum(r.confidence for r in agent_responses) / len(agent_responses),
            "processing_time": sum(r.processing_time for r in agent_responses),
            "agent_types_used": [r.agent_type.value for r in agent_responses],
            "execution_timestamp": datetime.utcnow().isoformat()
        }
        
        # Update knowledge tree
        await self.client_card_manager.update_knowledge_tree_performance(
            client_id=client_id,
            performance_data=performance_data
        )
        
        # Clear cache for this client
        cache_keys_to_remove = [k for k in self.knowledge_trees_cache.keys() if k.startswith(client_id)]
        for key in cache_keys_to_remove:
            del self.knowledge_trees_cache[key]

    # Additional helper methods...
    async def _validate_user_client_access(self, user: User, client_id: str) -> bool:
        """Validate user has access to client data"""
        # Implementation for user access validation
        return True  # Simplified for now

    async def _analyze_request_requirements(self, request: CoordinationRequestEnhanced) -> List[AgentType]:
        """Analyze request to determine required agent types"""
        # Simple keyword-based analysis (enhance with NLP later)
        query_lower = request.query.lower()
        required_agents = []
        
        if any(word in query_lower for word in ["content", "article", "blog", "write"]):
            required_agents.append(AgentType.CONTENT_RESEARCH)
        
        if any(word in query_lower for word in ["seo", "optimization", "ranking", "technical"]):
            required_agents.append(AgentType.TECHNICAL_SEO)
        
        if any(word in query_lower for word in ["social", "media", "post", "facebook", "twitter"]):
            required_agents.append(AgentType.SOCIAL_MEDIA)
        
        if any(word in query_lower for word in ["project", "plan", "timeline", "roadmap"]):
            required_agents.append(AgentType.PROJECT_PLANNING)
        
        return required_agents or [AgentType.CONTENT_RESEARCH]  # Default fallback

# Additional supporting classes would be implemented:
# - ClientCardManager: Handles client card CRUD operations
# - IntelligentDataBroker: Implements smart data filtering
# - ContextOptimizer: Optimizes contexts for specific agents
```

### 3. Supporting Components

#### Client Card Manager
```python
class ClientCardManager:
    """Manages client card operations and knowledge tree construction"""
    
    async def get_client_knowledge_tree(self, client_id: str) -> ClientKnowledgeTree:
        """Construct knowledge tree from client cards"""
        pass
    
    async def update_knowledge_tree_performance(self, client_id: str, performance_data: Dict[str, Any]):
        """Update knowledge tree with performance data"""
        pass
```

#### Intelligent Data Broker
```python
class IntelligentDataBroker:
    """Implements intelligent data filtering and exposure control"""
    
    async def get_agent_context(
        self, 
        data_request: AgentDataRequest,
        knowledge_tree: ClientKnowledgeTree,
        exposure_config: Dict[ClientCardType, DataExposureLevel]
    ) -> Dict[str, Any]:
        """Apply intelligent filtering based on agent requirements and privacy settings"""
        pass
```

## Implementation Plan

### Phase 1: Core Integration (Weeks 1-2)
1. **Update Models**: Add new Pydantic models for client cards and data brokering
2. **Enhance Coordinator**: Integrate client context retrieval and filtering
3. **Basic Data Broker**: Implement intelligent data exposure controls
4. **Testing**: Unit tests for new functionality

### Phase 2: Advanced Features (Weeks 3-4)
1. **Context Optimization**: Implement agent-specific context optimization
2. **Knowledge Tree Updates**: Real-time learning from agent performance
3. **Privacy Controls**: Granular client privacy and consent management
4. **Performance Monitoring**: Enhanced metrics with client context awareness

### Phase 3: Production Features (Weeks 5-6)
1. **Caching Strategy**: Intelligent caching of client contexts
2. **Security Hardening**: Advanced security for client data access
3. **Audit Enhancements**: Comprehensive audit trails for data access
4. **Load Testing**: Performance testing with client context overhead

## Benefits of Enhanced Coordinator

### For Platform Operations:
- **Intelligent Routing**: Context-aware agent selection and optimization
- **Performance Optimization**: Cached client contexts reduce latency
- **Security Enhancement**: Granular data access controls and audit trails
- **Scalability**: Efficient handling of client-specific requirements

### For Agents:
- **Rich Context**: Agents receive optimized, relevant client data
- **Consistent Interface**: Standardized client context API
- **Performance**: Pre-processed contexts improve agent efficiency
- **Reliability**: Robust fallback and error handling

### For Clients:
- **Data Control**: Fine-grained control over data exposure to agents
- **Personalization**: All agent interactions informed by client specifics
- **Transparency**: Clear visibility into how their data is used
- **Consistency**: Unified brand voice across all agent outputs

## Conclusion

The enhanced coordinator transforms the existing system into an intelligent data broker that:

1. **Maintains** existing coordination capabilities while adding client context awareness
2. **Implements** sophisticated data filtering and privacy controls
3. **Optimizes** agent performance through contextual data delivery
4. **Provides** comprehensive audit trails and transparency
5. **Scales** efficiently with intelligent caching and context optimization

This evolution positions the coordinator as the central intelligence hub that makes the entire Worzl agent ecosystem significantly more effective and client-centric.
