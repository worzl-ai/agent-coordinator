#!/usr/bin/env python3
"""
Test API endpoints for client context integration
"""

import requests
import json
import time

# Test configuration
BASE_URL = "http://localhost:8080"
TEST_TOKEN = "your-test-token-here"  # Replace with actual test token

def test_endpoints():
    """Test the new client context API endpoints"""
    
    headers = {
        "Authorization": f"Bearer {TEST_TOKEN}",
        "Content-Type": "application/json"
    }
    
    print("🌐 Testing Client Context API Endpoints")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1️⃣ Testing basic health check:")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   ✅ Status: {response.status_code}")
        print(f"   ✅ Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   💡 Make sure the server is running: python run_dev.py")
        return
    
    # Test 2: Client context preview
    print("\n2️⃣ Testing client context preview:")
    try:
        response = requests.get(f"{BASE_URL}/clients/client_123/context", headers=headers)
        print(f"   ✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Client ID: {data.get('client_id')}")
            print(f"   ✅ Has brand voice: {data.get('has_brand_voice')}")
            print(f"   ✅ Has target audience: {data.get('has_target_audience')}")
            print(f"   ✅ Preview: {data.get('preview')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Client-aware coordination
    print("\n3️⃣ Testing client-aware coordination:")
    try:
        payload = {
            "query": "Write a blog post about AI benefits for SMEs",
            "client_id": "client_123",
            "use_client_context": True,
            "priority": "medium"
        }
        
        response = requests.post(f"{BASE_URL}/coordinate/client", headers=headers, json=payload)
        print(f"   ✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Request ID: {data.get('request_id')}")
            print(f"   ✅ Client context used: {data.get('client_context_used')}")
            print(f"   ✅ Processing time: {data.get('total_processing_time'):.2f}s")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Regular coordination (for comparison)
    print("\n4️⃣ Testing regular coordination:")
    try:
        payload = {
            "query": "Write a blog post about AI",
            "priority": "medium"
        }
        
        response = requests.post(f"{BASE_URL}/coordinate", headers=headers, json=payload)
        print(f"   ✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Request ID: {data.get('request_id')}")
            print(f"   ✅ Processing time: {data.get('total_processing_time'):.2f}s")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n📋 API Testing Complete!")
    print("\n💡 To test manually:")
    print(f"   • Health: curl {BASE_URL}/health")
    print(f"   • Docs: {BASE_URL}/docs")
    print(f"   • Context: curl -H 'Authorization: Bearer {TEST_TOKEN}' {BASE_URL}/clients/client_123/context")

if __name__ == "__main__":
    test_endpoints()
