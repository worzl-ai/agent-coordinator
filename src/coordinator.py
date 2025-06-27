"""
Agent Coordinator - Core Logic
Handles request routing and agent management
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import uuid
from .models import (
    CoordinationRequest, 
    CoordinationResponse, 
    AgentStatus,
    AgentType,
    RoutingDecision,
    SystemHealth,
    QualityMetrics,
    User,
    AgentResponse,
    AgentStatusEnum,
    CoordinationRequestWithClient,
    CoordinationResponseWithClient,
    ClientContext,
    ClientCardType
)
import logging
import random

logger = logging.getLogger(__name__)

class AgentCoordinator:
    """
    Main class responsible for coordinating agent requests
    """

    def __init__(self):
        # Example agent pool
        self.agents = {
            "content_research_agent": {
                "type": AgentType.CONTENT_RESEARCH,
                "status": AgentStatusEnum.HEALTHY,
                "endpoint": "http://content-research-agent/api",
                "last_health_check": datetime.utcnow(),
                "current_load": 0,
                "max_capacity": 100,
                "average_response_time": 0.5
            },
            "technical_seo_agent": {
                "type": AgentType.TECHNICAL_SEO,
                "status": AgentStatusEnum.HEALTHY,
                "endpoint": "http://technical-seo-agent/api",
                "last_health_check": datetime.utcnow(),
                "current_load": 0,
                "max_capacity": 100,
                "average_response_time": 0.5
            }
            # Add more agents as needed
        }

    async def initialize(self):
        """
        Perform any startup initialization
        """
        logger.info("Initializing agents...")
        # Placeholder for any startup tasks

    async def shutdown(self):
        """
        Perform any shutdown cleanup
        """
        logger.info("Cleaning up resources...")
        # Placeholder for any cleanup tasks

    async def get_system_health(self) -> SystemHealth:
        """
        Return detailed system health information
        """
        return SystemHealth(
            status="healthy",
            timestamp=datetime.utcnow(),
            agents=[self._get_agent_status(agent_id) for agent_id in self.agents],
            active_requests=sum(agent["current_load"] for agent in self.agents.values()),
            total_requests_today=random.randint(0, 1000),  # Simulated value
            average_response_time=random.uniform(0.1, 1.0),  # Simulated value
            system_load=random.uniform(0.1, 1.0),  # Simulated value
            uptime_percentage=99.9
        )

    async def process_request(self, request: CoordinationRequest, user: User) -> CoordinationResponse:
        """
        Main method for processing coordination requests
        """
        request_id = str(uuid.uuid4())
        routing_decision = self._route_request(request)
        agent_responses = await self._gather_agent_responses(routing_decision)
        synthesized_response = self._synthesize_responses(agent_responses)

        return CoordinationResponse(
            request_id=request_id,
            routing_decision=routing_decision,
            agent_responses=agent_responses,
            synthesized_response=synthesized_response,
            total_processing_time=random.uniform(0.1, 3.0),  # Simulated
            quality_score=random.uniform(0.7, 1.0)  # Simulated quality score
        )

    async def get_agent_status(self, agent_id: Optional[str] = None) -> List[AgentStatus]:
        """
        Get status of specified or all agents
        """
        if agent_id:
            return [self._get_agent_status(agent_id)]
        else:
            return [self._get_agent_status(aid) for aid in self.agents]

    def _route_request(self, request: CoordinationRequest) -> Dict[str, Any]:
        """
        Handle intelligent request routing logic
        """
        # Simple load balancing logic example
        available_agents = [
            aid for aid, agent in self.agents.items() 
            if agent["status"] == AgentStatusEnum.HEALTHY and agent["current_load"] < agent["max_capacity"]
        ]
        selected_agent = random.choice(available_agents)  # Pick a random healthy agent

        return {"selected_agents": [self.agents[selected_agent]], "reasoning": "Random selection for demo."}

    async def _gather_agent_responses(self, routing_decision: Dict[str, Any]) -> List[AgentResponse]:
        """
        Gather responses from the selected agents
        """
        # Simulated agent response
        return [
            AgentResponse(
                agent_id=agent["type"].value,
                agent_type=agent["type"],
                response="Simulated response",
                confidence=0.9,
                processing_time=random.uniform(0.1, 1.0)
            ) for agent in routing_decision["selected_agents"]
        ]

    def _synthesize_responses(self, agent_responses: List[AgentResponse]) -> str:
        """
        Synthesize responses into a single cohesive output
        """
        combined_responses = "\n".join([response.response for response in agent_responses])
        return f"Synthesized Response: \n{combined_responses}"

    def _get_agent_status(self, agent_id: str) -> AgentStatus:
        """
        Get the status of a specific agent
        """
        agent = self.agents.get(agent_id)
        if not agent:
            raise ValueError("Agent not found")

        return AgentStatus(
            agent_id=agent_id,
            agent_type=agent["type"],
            status=agent["status"],
            last_health_check=agent["last_health_check"],
            current_load=agent["current_load"],
            max_capacity=agent["max_capacity"],
            average_response_time=agent["average_response_time"],
            success_rate=random.uniform(0.8, 1.0),  # Simulated value
            version="1.0.0",
            endpoint_url=agent["endpoint"]
        )

    async def get_quality_metrics(self) -> QualityMetrics:
        """Get system quality metrics"""
        return QualityMetrics(
            response_accuracy=random.uniform(0.8, 1.0),
            user_satisfaction=random.uniform(3.5, 5.0),
            sla_compliance=random.uniform(0.95, 1.0),
            error_rate=random.uniform(0.0, 0.05),
            recommendation_acceptance=random.uniform(0.7, 0.9)
        )

    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get detailed performance metrics"""
        return {
            "requests_per_minute": random.uniform(10, 100),
            "average_response_time": random.uniform(0.1, 2.0),
            "p95_response_time": random.uniform(1.0, 3.0),
            "p99_response_time": random.uniform(2.0, 5.0),
            "error_rate": random.uniform(0.0, 0.05),
            "active_connections": random.randint(0, 50),
            "memory_usage": random.uniform(0.3, 0.8),
            "cpu_usage": random.uniform(0.2, 0.7)
        }

    async def restart_agent(self, agent_id: str) -> bool:
        """Restart a specific agent"""
        if agent_id in self.agents:
            logger.info(f"Restarting agent {agent_id}")
            # In production, this would trigger actual agent restart
            self.agents[agent_id]["status"] = AgentStatusEnum.HEALTHY
            self.agents[agent_id]["current_load"] = 0
            return True
        return False

    async def enter_maintenance_mode(self):
        """Enter system maintenance mode"""
        logger.info("Entering maintenance mode")
        for agent_id in self.agents:
            self.agents[agent_id]["status"] = AgentStatusEnum.MAINTENANCE
    
    # CLIENT CONTEXT METHODS
    
    async def process_request_with_client(
        self, 
        request: CoordinationRequestWithClient, 
        user: User
    ) -> CoordinationResponseWithClient:
        """Enhanced request processing with optional client context"""
        
        # Get client context if requested
        client_context = None
        if request.use_client_context and request.client_id:
            client_context = await self._get_client_context(request.client_id, user)
        
        # Use existing processing with enhanced payload
        request_id = str(uuid.uuid4())
        routing_decision = self._route_request(request)
        
        # Enhance agent responses with client context
        agent_responses = await self._gather_agent_responses_with_context(
            routing_decision, 
            client_context
        )
        
        synthesized_response = self._synthesize_responses(agent_responses)
        
        return CoordinationResponseWithClient(
            request_id=request_id,
            routing_decision=routing_decision,
            agent_responses=agent_responses,
            synthesized_response=synthesized_response,
            total_processing_time=random.uniform(0.1, 3.0),
            quality_score=random.uniform(0.7, 1.0),
            client_context_used=client_context is not None
        )
    
    async def _get_client_context(self, client_id: str, user: User) -> Optional[ClientContext]:
        """Retrieve client context with basic filtering"""
        
        # Validate user has access to this client
        if not await self._validate_client_access(user, client_id):
            logger.warning(f"User {user.user_id} denied access to client {client_id}")
            return None
        
        # Get client data (placeholder - would integrate with your client card system)
        client_data = await self._fetch_client_data(client_id)
        
        if not client_data:
            logger.warning(f"No client data found for client {client_id}")
            return None
        
        # Create filtered context
        return ClientContext(
            client_id=client_id,
            brand_voice=self._filter_brand_data(client_data.get("brand_guidelines")),
            target_audience=self._filter_audience_data(client_data.get("target_audience")),
            compliance_notes=client_data.get("compliance_requirements", [])
        )
    
    async def _gather_agent_responses_with_context(
        self, 
        routing_decision: Dict[str, Any], 
        client_context: Optional[ClientContext]
    ) -> List[AgentResponse]:
        """Enhanced agent execution with client context"""
        
        responses = []
        for agent in routing_decision["selected_agents"]:
            
            # Prepare agent-specific context
            agent_context = self._prepare_agent_context(agent, client_context)
            
            # Simulate agent call with context (replace with actual HTTP calls)
            response = AgentResponse(
                agent_id=agent["type"].value,
                agent_type=agent["type"],
                response=f"Response with context: {agent_context}",
                confidence=0.9,
                processing_time=random.uniform(0.1, 1.0),
                metadata={"client_context_used": client_context is not None}
            )
            responses.append(response)
        
        return responses
    
    def _prepare_agent_context(
        self, 
        agent: Dict[str, Any], 
        client_context: Optional[ClientContext]
    ) -> Dict[str, Any]:
        """Prepare filtered context for specific agent"""
        
        if not client_context:
            return {}
        
        agent_type = agent["type"]
        
        # Agent-specific filtering rules
        if agent_type == AgentType.CONTENT_RESEARCH:
            return {
                "brand_voice": client_context.brand_voice,
                "target_audience": client_context.target_audience,
                "compliance_notes": client_context.compliance_notes
            }
        elif agent_type == AgentType.TECHNICAL_SEO:
            return {
                "brand_voice": client_context.brand_voice.get("tone") if client_context.brand_voice else None,
                "compliance_notes": client_context.compliance_notes
            }
        else:
            return {"client_id": client_context.client_id}
    
    # Helper methods (implement based on your client card system)
    async def _validate_client_access(self, user: User, client_id: str) -> bool:
        """Validate user can access this client's data"""
        from .client_storage import client_storage_service
        
        # Get list of clients this user can access
        accessible_clients = await client_storage_service.list_client_ids(user.user_id)
        
        if client_id in accessible_clients:
            logger.info(f"Access granted for user {user.user_id} to client {client_id}")
            return True
        else:
            logger.warning(f"Access denied for user {user.user_id} to client {client_id}")
            return False
    
    async def _fetch_client_data(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Fetch client data from your card system"""
        from .client_storage import client_storage_service
        
        logger.info(f"Fetching client data for {client_id}")
        return await client_storage_service.get_client_data(client_id)
    
    def _filter_brand_data(self, brand_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Filter brand data for agent consumption"""
        if not brand_data:
            return None
        
        return {
            "tone": brand_data.get("tone"),
            "voice": brand_data.get("voice"),
            "restrictions": brand_data.get("avoid_words", []),
            "messaging_pillars": brand_data.get("messaging_pillars", [])
        }
    
    def _filter_audience_data(self, audience_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Filter audience data for agent consumption"""
        if not audience_data:
            return None
        
        return {
            "primary_audience": audience_data.get("primary"),
            "demographics": {
                "age_range": audience_data.get("age_range"),
                "interests": audience_data.get("interests", [])
            }
        }

