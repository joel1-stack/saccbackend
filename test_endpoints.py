#!/usr/bin/env python3
"""
Test script for SACCO Nova API endpoints
Run this to verify all endpoints are working
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_endpoint(method, url, data=None, headers=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        
        print(f"{method} {url}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print("🚀 Testing SACCO Nova API Endpoints\n")
    
    # 1. Test API Root
    print("1. API Root")
    test_endpoint('GET', f"{BASE_URL}/")
    
    # 2. Test Registration
    print("2. User Registration")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+254712345678",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    register_response = test_endpoint('POST', f"{BASE_URL}/auth/register/", register_data)
    
    # 3. Test Login
    print("3. User Login")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    login_response = test_endpoint('POST', f"{BASE_URL}/auth/login/", login_data)
    
    # Get token for authenticated requests
    token = None
    if login_response and login_response.status_code == 200:
        token = login_response.json().get('access')
    
    headers = {'Authorization': f'Bearer {token}'} if token else None
    
    # 4. Test Profile
    print("4. User Profile")
    test_endpoint('GET', f"{BASE_URL}/auth/profile/", headers=headers)
    
    # 5. Test Dashboard
    print("5. Dashboard")
    test_endpoint('GET', f"{BASE_URL}/dashboard/", headers=headers)
    
    # 6. Test Accounts
    print("6. Create Account")
    account_data = {
        "account_type": "savings",
        "interest_rate": "2.50"
    }
    test_endpoint('POST', f"{BASE_URL}/accounts/", account_data, headers)
    
    print("7. List Accounts")
    test_endpoint('GET', f"{BASE_URL}/accounts/", headers=headers)
    
    # 8. Test Member Registration
    print("8. Member Registration")
    member_data = {
        "username": "member1",
        "email": "member1@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+254712345679",
        "password": "memberpass123",
        "national_id": "12345678",
        "date_of_birth": "1990-01-01",
        "address": "123 Main St",
        "occupation": "Teacher",
        "employer": "ABC School",
        "monthly_income": "50000.00",
        "next_of_kin_name": "Jane Doe",
        "next_of_kin_phone": "+254712345680",
        "next_of_kin_relationship": "Spouse"
    }
    test_endpoint('POST', f"{BASE_URL}/members/register/", member_data)
    
    print("✅ All endpoint tests completed!")

if __name__ == "__main__":
    main()