#!/usr/bin/env python3
"""
Comprehensive API Test Suite
Tests all endpoints for proper error handling, 404s, and 422s
"""

import requests
import json
import time
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

BASE_URL = 'http://127.0.0.1:5000'

# Test counters
tests_passed = 0
tests_failed = 0
test_results = []

def print_test(name, passed, message=""):
    global tests_passed, tests_failed
    if passed:
        tests_passed += 1
        print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL} - {name}")
        test_results.append(("PASS", name, message))
    else:
        tests_failed += 1
        print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL} - {name}")
        if message:
            print(f"  {Fore.YELLOW}→ {message}{Style.RESET_ALL}")
        test_results.append(("FAIL", name, message))

def test_endpoint(method, endpoint, expected_status, data=None, token=None, test_name=None):
    """Generic endpoint tester"""
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            print_test(test_name or f"{method} {endpoint}", False, f"Unknown method: {method}")
            return None
        
        passed = response.status_code == expected_status
        msg = f"Expected {expected_status}, got {response.status_code}"
        if not passed:
            try:
                msg += f" - {response.json()}"
            except:
                msg += f" - {response.text[:100]}"
        
        print_test(test_name or f"{method} {endpoint} -> {expected_status}", passed, "" if passed else msg)
        return response
    except requests.exceptions.RequestException as e:
        print_test(test_name or f"{method} {endpoint}", False, f"Request failed: {str(e)}")
        return None

def main():
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"  COMPREHENSIVE API TEST SUITE")
    print(f"  Testing: {BASE_URL}")
    print(f"{'='*80}{Style.RESET_ALL}\n")

    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=2)
    except:
        print(f"{Fore.RED}ERROR: Cannot connect to server at {BASE_URL}")
        print(f"Make sure the server is running with: python app.py{Style.RESET_ALL}")
        return

    # Test variables
    test_token = None
    test_user_id = None
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    
    # ==========================================
    # 1. TEST 404 ERRORS - Non-existent endpoints
    # ==========================================
    print(f"\n{Fore.YELLOW}[1] Testing 404 Error Handling{Style.RESET_ALL}")
    test_endpoint('GET', '/nonexistent', 404, test_name="Non-existent endpoint")
    test_endpoint('GET', '/api/fake', 404, test_name="Fake API endpoint")
    test_endpoint('POST', '/wrong/path', 404, test_name="Wrong path POST")
    
    # ==========================================
    # 2. TEST AUTHENTICATION
    # ==========================================
    print(f"\n{Fore.YELLOW}[2] Testing Authentication{Style.RESET_ALL}")
    
    # Register new test user
    test_email = f"test_user_{int(time.time())}@example.com"
    register_data = {
        'name': 'Test User',
        'email': test_email,
        'password': 'testpass123',
        'role': 'student'
    }
    response = test_endpoint('POST', '/auth/register', 201, data=register_data, test_name="Register new user")
    
    # Login with valid credentials
    login_data = {
        'email': test_email,
        'password': 'testpass123'
    }
    response = test_endpoint('POST', '/auth/login', 200, data=login_data, test_name="Login with valid credentials")
    if response and response.status_code == 200:
        data = response.json()
        test_token = data.get('access_token')
        test_user_id = data.get('user', {}).get('id')
        print(f"  {Fore.GREEN}→ Got token for user ID: {test_user_id}{Style.RESET_ALL}")
    
    # Login with invalid credentials
    test_endpoint('POST', '/auth/login', 401, 
                 data={'email': test_email, 'password': 'wrongpass'},
                 test_name="Login with wrong password")
    
    # Login with missing fields
    test_endpoint('POST', '/auth/login', 400,
                 data={'email': test_email},
                 test_name="Login with missing password")
    
    # ==========================================
    # 3. TEST 422 TOKEN ERRORS
    # ==========================================
    print(f"\n{Fore.YELLOW}[3] Testing 422 Invalid Token Handling{Style.RESET_ALL}")
    
    # Protected endpoint with invalid token
    test_endpoint('GET', '/debug/token', 422, token=invalid_token, 
                 test_name="Protected endpoint with invalid token")
    
    # Protected endpoint without token
    test_endpoint('GET', '/debug/token', 401,
                 test_name="Protected endpoint without token")
    
    # Valid token test
    if test_token:
        test_endpoint('GET', '/debug/token', 200, token=test_token,
                     test_name="Protected endpoint with valid token")
    
    # ==========================================
    # 4. TEST SAFE ZONES
    # ==========================================
    print(f"\n{Fore.YELLOW}[4] Testing Safe Zones{Style.RESET_ALL}")
    
    # Get all safe zones (public endpoint)
    test_endpoint('GET', '/safe_zones', 200, test_name="Get all safe zones")
    
    # Get non-existent safe zone
    test_endpoint('GET', '/safe_zones/99999', 404, test_name="Get non-existent safe zone")
    
    if test_token:
        # Try to create safe zone as student (should fail - 403)
        zone_data = {
            'name': 'Test Zone',
            'latitude': 28.6139,
            'longitude': 77.2090,
            'description': 'Test zone'
        }
        test_endpoint('POST', '/safe_zones', 403, data=zone_data, token=test_token,
                     test_name="Create safe zone as student (should fail)")
        
        # Mark a safe zone
        test_endpoint('POST', '/safe_zones/1/mark', 201, token=test_token,
                     test_name="Mark safe zone")
        
        # Get marked zones
        test_endpoint('GET', '/safe_zones/marked', 200, token=test_token,
                     test_name="Get marked safe zones")
        
        # Unmark safe zone
        test_endpoint('DELETE', '/safe_zones/1/mark', 200, token=test_token,
                     test_name="Unmark safe zone")
    
    # ==========================================
    # 5. TEST DISASTERS
    # ==========================================
    print(f"\n{Fore.YELLOW}[5] Testing Disasters{Style.RESET_ALL}")
    
    # Get all disasters (public)
    test_endpoint('GET', '/disasters', 200, test_name="Get all disasters")
    
    # Get non-existent disaster
    test_endpoint('GET', '/disasters/99999', 404, test_name="Get non-existent disaster")
    
    # ==========================================
    # 6. TEST MODULES
    # ==========================================
    print(f"\n{Fore.YELLOW}[6] Testing Modules{Style.RESET_ALL}")
    
    # Get all modules (public)
    test_endpoint('GET', '/modules', 200, test_name="Get all modules")
    
    # Get non-existent module
    test_endpoint('GET', '/modules/99999', 404, test_name="Get non-existent module")
    
    # ==========================================
    # 7. TEST MESSAGES
    # ==========================================
    print(f"\n{Fore.YELLOW}[7] Testing Messages{Style.RESET_ALL}")
    
    if test_token:
        # Get inbox
        test_endpoint('GET', '/messages/inbox', 200, token=test_token,
                     test_name="Get message inbox")
        
        # Get sent messages
        test_endpoint('GET', '/messages/sent', 200, token=test_token,
                     test_name="Get sent messages")
    
    # ==========================================
    # 8. TEST DRILLS
    # ==========================================
    print(f"\n{Fore.YELLOW}[8] Testing Drills{Style.RESET_ALL}")
    
    # Get all drills (public)
    test_endpoint('GET', '/drills', 200, test_name="Get all drills")
    
    if test_token:
        # Get my participation
        test_endpoint('GET', '/drills/my-participation', 200, token=test_token,
                     test_name="Get my drill participation")
    
    # ==========================================
    # 9. TEST ALERTS
    # ==========================================
    print(f"\n{Fore.YELLOW}[9] Testing Alerts{Style.RESET_ALL}")
    
    # Get all alerts (public)
    test_endpoint('GET', '/alerts', 200, test_name="Get all alerts")
    
    # ==========================================
    # 10. TEST ACHIEVEMENTS & LEADERBOARD
    # ==========================================
    print(f"\n{Fore.YELLOW}[10] Testing Achievements & Leaderboard{Style.RESET_ALL}")
    
    if test_token:
        # Get my achievements
        test_endpoint('GET', '/achievements/my', 200, token=test_token,
                     test_name="Get my achievements")
        
        # Get leaderboard
        test_endpoint('GET', '/leaderboard', 200, token=test_token,
                     test_name="Get leaderboard")
    
    # ==========================================
    # 11. TEST EMERGENCY CONTACTS
    # ==========================================
    print(f"\n{Fore.YELLOW}[11] Testing Emergency Contacts{Style.RESET_ALL}")
    
    # Get emergency contacts (public)
    test_endpoint('GET', '/emergency-contacts', 200, test_name="Get emergency contacts")
    
    # ==========================================
    # 12. TEST ACTIVITIES
    # ==========================================
    print(f"\n{Fore.YELLOW}[12] Testing Recent Activities{Style.RESET_ALL}")
    
    if test_token:
        # Get recent activities
        test_endpoint('GET', '/activities/recent', 200, token=test_token,
                     test_name="Get recent activities")
    
    # ==========================================
    # SUMMARY
    # ==========================================
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"  TEST SUMMARY")
    print(f"{'='*80}{Style.RESET_ALL}\n")
    
    total_tests = tests_passed + tests_failed
    pass_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"{Fore.GREEN}Passed: {tests_passed}{Style.RESET_ALL}")
    print(f"{Fore.RED}Failed: {tests_failed}{Style.RESET_ALL}")
    print(f"Pass Rate: {pass_rate:.1f}%\n")
    
    if tests_failed > 0:
        print(f"{Fore.YELLOW}Failed Tests:{Style.RESET_ALL}")
        for status, name, msg in test_results:
            if status == "FAIL":
                print(f"  ✗ {name}")
                if msg:
                    print(f"    → {msg}")
    
    if tests_failed == 0:
        print(f"{Fore.GREEN}🎉 All tests passed! The application is working correctly.{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.YELLOW}⚠️  Some tests failed. Please review the errors above.{Style.RESET_ALL}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Tests interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Test suite error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
