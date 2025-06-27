"""
Tests for the Agent Coordinator core logic
"""

import pytest
import asyncio
from datetime import datetime
from src.coordinator import AgentCoordinator
from src.models import CoordinationRequest, User, RequestPriority

@pytest.fixture
def coordinator():
    """Fixture to create a coordinator instance"""
    return AgentCoordinator()

@pytest.fixture
def test_user():
    """Fixture to create a test user"""
    return User(
        user_id="test-123",
        email="test@worzl.com",
        name="Test User",
        roles=["user"],
        is_admin=False,
        created_at=datetime.utcnow()
    )

@pytest.fixture
def test_request():
    """Fixture to create a test coordination request"""
    return CoordinationRequest(
        query="What are the latest SEO trends?",
        priority=RequestPriority.MEDIUM
    )

@pytest.mark.asyncio
async def test_coordinator_initialization(coordinator):
    """Test coordinator initialization"""
    await coordinator.initialize()
    assert len(coordinator.agents) > 0

@pytest.mark.asyncio
async def test_process_request(coordinator, test_request, test_user):
    """Test basic request processing"""
    await coordinator.initialize()
    response = await coordinator.process_request(test_request, test_user)
    
    assert response.request_id is not None
    assert response.synthesized_response is not None
    assert len(response.agent_responses) > 0
    assert response.quality_score >= 0.0 and response.quality_score <= 1.0

@pytest.mark.asyncio
async def test_get_system_health(coordinator):
    """Test system health check"""
    await coordinator.initialize()
    health = await coordinator.get_system_health()
    
    assert health.status == "healthy"
    assert len(health.agents) > 0
    assert health.uptime_percentage > 0

@pytest.mark.asyncio
async def test_get_agent_status(coordinator):
    """Test agent status retrieval"""
    await coordinator.initialize()
    statuses = await coordinator.get_agent_status()
    
    assert len(statuses) > 0
    for status in statuses:
        assert status.agent_id is not None
        assert status.agent_type is not None

if __name__ == "__main__":
    pytest.main([__file__])
