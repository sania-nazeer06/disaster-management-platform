"""Quick smoke tests for the disaster management API"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_register():
    """Test user registration"""
    print("\n1. Testing user registration...")
    data = {
        "name": "Test Faculty",
        "email": "faculty@test.com",
        "password": "password123",
        "role": "faculty"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"   Status: {response.status_code}")
    print(f"   Raw response: {response.text}")
    if response.status_code == 200 or response.status_code == 201:
        print(f"   Response: {response.json()}")
        return response.json()
    return None

def test_login():
    """Test user login"""
    print("\n2. Testing login...")
    data = {
        "email": "faculty@test.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Response: {result}")
    return result.get('access_token')

def test_create_safe_zone(token):
    """Test creating a safe zone (protected endpoint)"""
    print("\n3. Testing create safe zone (protected)...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Emergency Shelter A",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "description": "Main community center with backup power"
    }
    response = requests.post(f"{BASE_URL}/safe_zones", json=data, headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")

def test_list_safe_zones():
    """Test listing safe zones (public endpoint)"""
    print("\n4. Testing list safe zones (public)...")
    response = requests.get(f"{BASE_URL}/safe_zones")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")

def test_create_disaster(token):
    """Test creating disaster info"""
    print("\n5. Testing create disaster info (protected)...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "disaster_type": "Earthquake",
        "info": "Drop, Cover, and Hold On. Move away from windows.",
        "video_link": "https://youtube.com/watch?v=example"
    }
    response = requests.post(f"{BASE_URL}/disasters", json=data, headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")

if __name__ == "__main__":
    print("="*60)
    print("Disaster Management API - Smoke Tests")
    print("="*60)
    
    try:
        # Run tests
        test_register()
        token = test_login()
        
        if token:
            test_create_safe_zone(token)
            test_list_safe_zones()
            test_create_disaster(token)
            
            print("\n" + "="*60)
            print("✓ All smoke tests completed!")
            print("="*60)
        else:
            print("\n✗ Login failed - cannot proceed with protected endpoints")
            
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to Flask server at http://127.0.0.1:5000")
        print("   Make sure the server is running (python app.py)")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
