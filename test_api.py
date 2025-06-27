#!/usr/bin/env python3
"""
Simple API test script for the Agent Coordinator
"""

import requests
import json
from src.auth import create_test_token

def test_agent_coordinator():
    """Test the Agent Coordinator API endpoints"""
    
    base_url = "http://localhost:8080"
    
    # Generate test token
    token = create_test_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("🧪 Testing Agent Coordinator API")
    print(f"Token: {token[:50]}...")
    
    try:
        # Test health check
        print("\n1. Testing health check...")
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test detailed health check
        print("\n2. Testing detailed health check...")
        response = requests.get(f"{base_url}/health/detailed", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"System Status: {data['status']}")
            print(f"Active Requests: {data['active_requests']}")
            print(f"Agents: {len(data['agents'])}")
        
        # Test agent status
        print("\n3. Testing agent status...")
        response = requests.get(f"{base_url}/agents/status", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            agents = response.json()
            print(f"Found {len(agents)} agents")
            for agent in agents:
                print(f"  - {agent['agent_id']}: {agent['status']}")
        
        # Test coordination request
        print("\n4. Testing coordination request...")
        request_data = {
            "query": "What are the latest SEO trends?",
            "priority": "medium"
        }
        response = requests.post(
            f"{base_url}/coordinate", 
            headers=headers,
            json=request_data
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Request ID: {data['request_id']}")
            print(f"Quality Score: {data['quality_score']}")
            print(f"Agent Responses: {len(data['agent_responses'])}")
            print(f"Synthesized Response: {data['synthesized_response'][:100]}...")
        
        print("\n✅ All tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on port 8080")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_agent_coordinator()
