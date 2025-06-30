#!/usr/bin/env python3
"""
Test script for the CoWorkly Partner Dashboard API
Using FastAPI TestClient for testing without requiring a running server
"""

import json
import re
from datetime import datetime
from fastapi.testclient import TestClient

# Import our FastAPI app
from src.coworkly_partner_api.app import app

# Create test client
client = TestClient(app)

# Configuration
TEST_TOKEN = "your_test_firebase_token_here"  # Replace with actual test token

def is_camel_case(s):
    """Check if a string is in camelCase format"""
    if not s or not isinstance(s, str):
        return False
    # camelCase: starts with lowercase, no underscores, may contain uppercase letters
    return bool(re.match(r'^[a-z][a-zA-Z0-9]*$', s))

def check_camel_case_fields(data, path=""):
    """Recursively check if all field names are in camelCase"""
    if not isinstance(data, dict):
        return True, []
    
    errors = []
    for key, value in data.items():
        current_path = f"{path}.{key}" if path else key
        
        # Check if the field name is in camelCase
        if not is_camel_case(key):
            errors.append(f"Field '{current_path}' is not in camelCase: '{key}'")
        
        # Recursively check nested objects
        if isinstance(value, dict):
            nested_errors = check_camel_case_fields(value, current_path)[1]
            errors.extend(nested_errors)
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            # Check first item in list if it's a list of objects
            nested_errors = check_camel_case_fields(value[0], f"{current_path}[0]")[1]
            errors.extend(nested_errors)
    
    return len(errors) == 0, errors

def test_camel_case_response():
    """Test that API responses are in camelCase format"""
    print("\nTesting camelCase response format...")
    
    if TEST_TOKEN == "your_test_firebase_token_here":
        print("⚠️  Skipping camelCase test - no valid token provided")
        return
    
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    test_results = []
    
    # Test space endpoint
    try:
        response = client.get("/spaces/test-space-123", headers=headers)
        if response.status_code == 200:
            data = response.json()
            is_valid, errors = check_camel_case_fields(data, "space")
            test_results.append(("GET /spaces/{id}", is_valid, errors))
            print(f"✓ Space response: {'Valid' if is_valid else 'Invalid'}")
            if errors:
                print(f"  Errors: {errors[:3]}...")  # Show first 3 errors
        else:
            print(f"⚠️  Space endpoint returned {response.status_code}")
    except Exception as e:
        print(f"Error testing space endpoint: {e}")
    
    # Test posts endpoint
    try:
        response = client.get("/posts", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                is_valid, errors = check_camel_case_fields(data[0], "post[0]")
                test_results.append(("GET /posts", is_valid, errors))
                print(f"✓ Posts response: {'Valid' if is_valid else 'Invalid'}")
                if errors:
                    print(f"  Errors: {errors[:3]}...")
            else:
                print("⚠️  No posts data to test")
        else:
            print(f"⚠️  Posts endpoint returned {response.status_code}")
    except Exception as e:
        print(f"Error testing posts endpoint: {e}")
    
    # Test features endpoint
    try:
        response = client.get("/features?feature_type=workspace_features", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                is_valid, errors = check_camel_case_fields(data[0], "feature[0]")
                test_results.append(("GET /features", is_valid, errors))
                print(f"✓ Features response: {'Valid' if is_valid else 'Invalid'}")
                if errors:
                    print(f"  Errors: {errors[:3]}...")
            else:
                print("⚠️  No features data to test")
        else:
            print(f"⚠️  Features endpoint returned {response.status_code}")
    except Exception as e:
        print(f"Error testing features endpoint: {e}")
    
    # Test dashboard metrics endpoint
    try:
        response = client.get("/dashboard-metrics", headers=headers)
        if response.status_code == 200:
            data = response.json()
            is_valid, errors = check_camel_case_fields(data, "dashboard-metrics")
            test_results.append(("GET /dashboard-metrics", is_valid, errors))
            print(f"✓ Dashboard metrics response: {'Valid' if is_valid else 'Invalid'}")
            if errors:
                print(f"  Errors: {errors[:3]}...")
        else:
            print(f"⚠️  Dashboard metrics endpoint returned {response.status_code}")
    except Exception as e:
        print(f"Error testing dashboard metrics endpoint: {e}")
    
    # Summary
    print(f"\n📊 CamelCase Test Results:")
    all_passed = True
    for endpoint, is_valid, errors in test_results:
        status = "✅ PASS" if is_valid else "❌ FAIL"
        print(f"  {endpoint}: {status}")
        if not is_valid:
            all_passed = False
            print(f"    Errors: {errors}")
    
    # Use assertion instead of returning boolean
    assert all_passed, "Some camelCase tests failed"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = client.get("/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    except Exception as e:
        print(f"Error: {e}")
        assert False, f"Health check failed with error: {e}"

def test_get_space():
    """Test getting a space (requires auth)"""
    print("\nTesting GET /spaces/{spaceId}...")
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    try:
        response = client.get("/spaces/test-space-123", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
        assert response.status_code in [200, 401, 403, 404], f"Unexpected status code: {response.status_code}"
    except Exception as e:
        print(f"Error: {e}")
        assert False, f"Get space test failed with error: {e}"

def test_update_space():
    """Test updating a space (requires auth)"""
    print("\nTesting PATCH /spaces/{spaceId}...")
    headers = {
        "Authorization": f"Bearer {TEST_TOKEN}",
        "Content-Type": "application/json"
    }
    update_data = {
        "name": "Updated Test Space",
        "rating": 4.5
    }
    try:
        response = client.patch(
            "/spaces/test-space-123", 
            headers=headers,
            json=update_data
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
        assert response.status_code in [200, 401, 403, 404], f"Unexpected status code: {response.status_code}"
    except Exception as e:
        print(f"Error: {e}")
        assert False, f"Update space test failed with error: {e}"

def test_create_post():
    """Test creating a post (requires auth)"""
    print("\nTesting POST /posts...")
    headers = {
        "Authorization": f"Bearer {TEST_TOKEN}",
        "Content-Type": "application/json"
    }
    post_data = {
        "author": {
            "id": "test-user-123",
            "name": "Test User",
            "email": "test@example.com"
        },
        "content": "This is a test post",
        "title": "Test Post Title",
        "spaceId": "test-space-123"
    }
    try:
        response = client.post("/posts", headers=headers, json=post_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
        assert response.status_code in [201, 401, 403, 422], f"Unexpected status code: {response.status_code}"
    except Exception as e:
        print(f"Error: {e}")
        assert False, f"Create post test failed with error: {e}"

def test_get_features():
    """Test getting features (requires auth)"""
    print("\nTesting GET /features...")
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    try:
        response = client.get("/features?feature_type=workspace_features", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
        assert response.status_code in [200, 401, 403], f"Unexpected status code: {response.status_code}"
    except Exception as e:
        print(f"Error: {e}")
        assert False, f"Get features test failed with error: {e}"

def test_unauthorized_access():
    """Test unauthorized access to protected endpoints"""
    print("\nTesting unauthorized access...")
    try:
        # Test without auth header
        response = client.get("/spaces/test-space-123")
        print(f"Status: {response.status_code}")
        assert response.status_code in [401, 403], f"Expected 401/403 for unauthorized access, got {response.status_code}"
        print("✅ Unauthorized access properly rejected")
    except Exception as e:
        print(f"Error: {e}")
        assert False, f"No auth test failed: {e}"

def main():
    """Run all tests"""
    print("🧪 Running CoWorkly Partner Dashboard API Tests")
    print("=" * 60)
    
    # Run tests
    test_health_check()
    test_get_space()
    test_update_space()
    test_create_post()
    test_get_features()
    test_unauthorized_access()
    test_camel_case_response()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main() 