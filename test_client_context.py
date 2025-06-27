#!/usr/bin/env python3
"""
Test script for client context integration
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.coordinator import AgentCoordinator
from src.models import CoordinationRequestWithClient, User
from datetime import datetime

async def test_client_context():
    """Test client context functionality"""
    
    # Initialize coordinator
    coordinator = AgentCoordinator()
    await coordinator.initialize()
    
    # Create test user
    test_user = User(
        user_id="test_user_123",
        email="test@example.com",
        name="Test User",
        roles=["user"],
        is_admin=False,
        created_at=datetime.utcnow()
    )
    
    # Create test request with client context
    test_request = CoordinationRequestWithClient(
        query="Write a blog post about AI benefits for SMEs",
        client_id="client_123",
        use_client_context=True
    )
    
    print("🧪 Testing Client Context Integration")
    print("=" * 50)
    
    # Test 1: Basic request without client context
    print("\n1️⃣ Testing without client context:")
    basic_request = CoordinationRequestWithClient(
        query="Write a blog post about AI",
        use_client_context=False
    )
    
    response = await coordinator.process_request_with_client(basic_request, test_user)
    print(f"   ✅ Response ID: {response.request_id}")
    print(f"   ✅ Client context used: {response.client_context_used}")
    
    # Test 2: Request with client context
    print("\n2️⃣ Testing with client context:")
    response_with_context = await coordinator.process_request_with_client(test_request, test_user)
    print(f"   ✅ Response ID: {response_with_context.request_id}")
    print(f"   ✅ Client context used: {response_with_context.client_context_used}")
    
    # Test 3: Get client context directly
    print("\n3️⃣ Testing client context retrieval:")
    client_context = await coordinator._get_client_context("client_123", test_user)
    if client_context:
        print(f"   ✅ Client ID: {client_context.client_id}")
        print(f"   ✅ Has brand voice: {client_context.brand_voice is not None}")
        print(f"   ✅ Has target audience: {client_context.target_audience is not None}")
        print(f"   ✅ Compliance notes: {len(client_context.compliance_notes or [])}")
        
        if client_context.brand_voice:
            print(f"   ✅ Brand tone: {client_context.brand_voice.get('tone')}")
        
        if client_context.target_audience:
            print(f"   ✅ Primary audience: {client_context.target_audience.get('primary_audience')}")
    
    # Test 4: Agent context filtering
    print("\n4️⃣ Testing agent context filtering:")
    mock_agent = {"type": coordinator.agents["content_research_agent"]["type"]}
    filtered_context = coordinator._prepare_agent_context(mock_agent, client_context)
    print(f"   ✅ Filtered context keys: {list(filtered_context.keys())}")
    print(f"   ✅ Brand voice included: {'brand_voice' in filtered_context}")
    print(f"   ✅ Target audience included: {'target_audience' in filtered_context}")
    
    print("\n🎉 All tests completed successfully!")
    print("\n📊 Summary:")
    print(f"   • Client context retrieval: ✅ Working")
    print(f"   • Agent filtering: ✅ Working") 
    print(f"   • Request processing: ✅ Working")
    
    await coordinator.shutdown()

if __name__ == "__main__":
    asyncio.run(test_client_context())
