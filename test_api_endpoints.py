#!/usr/bin/env python3
"""
SACCO Nova API Endpoint Tester
Tests all core API endpoints to ensure frontend-backend compatibility
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_endpoint(method, url, data=None, headers=None, description=""):
    """Test an API endpoint and return the result"""
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers)
        
        print(f"\n{description}")
        print(f"{method.upper()} {url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code < 400:
            print("✅ SUCCESS")
            if response.content:
                try:
                    result = response.json()
                    if isinstance(result, dict) and len(result) > 3:
                        # Show only first few keys for large responses
                        keys = list(result.keys())[:3]
                        print(f"Response keys: {keys}...")
                    else:
                        print(f"Response: {result}")
                except:
                    print(f"Response: {response.text[:200]}...")
        else:
            print("❌ ERROR")
            print(f"Error: {response.text}")
        
        return response
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        return None

def main():
    print("🚀 SACCO Nova API Endpoint Testing")
    print("=" * 50)
    
    # Test API Root
    test_endpoint('GET', f"{BASE_URL}/", description="1. API Root - System Information")
    
    # Test Authentication Endpoints
    test_endpoint('GET', f"{BASE_URL}/auth/login/", description="2. Login Endpoint Documentation")
    test_endpoint('GET', f"{BASE_URL}/auth/register/", description="3. Register Endpoint Documentation")
    
    # Test Core Endpoints (Documentation)
    test_endpoint('GET', f"{BASE_URL}/dashboard/", description="4. Dashboard (requires auth)")
    test_endpoint('GET', f"{BASE_URL}/accounts/", description="5. Accounts (requires auth)")
    test_endpoint('GET', f"{BASE_URL}/loans/", description="6. Loans (requires auth)")
    test_endpoint('GET', f"{BASE_URL}/transactions/", description="7. Transactions (requires auth)")
    test_endpoint('GET', f"{BASE_URL}/members/", description="8. Members (requires auth)")
    
    # Test Member Registration Documentation
    test_endpoint('GET', f"{BASE_URL}/members/register/", description="9. Member Registration Documentation")
    
    # Test Transaction Endpoints Documentation
    test_endpoint('GET', f"{BASE_URL}/transactions/deposit/", description="10. Deposit Documentation")
    test_endpoint('GET', f"{BASE_URL}/transactions/withdraw/", description="11. Withdrawal Documentation")
    test_endpoint('GET', f"{BASE_URL}/transactions/transfer/", description="12. Transfer Documentation")
    
    # Test Loan Application Documentation
    test_endpoint('GET', f"{BASE_URL}/loans/apply/", description="13. Loan Application Documentation")
    
    # Test Ecosystem Endpoints
    test_endpoint('GET', f"{BASE_URL}/guarantors/", description="14. Guarantors System")
    test_endpoint('GET', f"{BASE_URL}/shares/", description="15. Shares System")
    test_endpoint('GET', f"{BASE_URL}/notifications/", description="16. Notifications System")
    test_endpoint('GET', f"{BASE_URL}/reporting/", description="17. Reporting System")
    test_endpoint('GET', f"{BASE_URL}/integrations/", description="18. Integrations System")
    
    print("\n" + "=" * 50)
    print("✅ API Endpoint Testing Complete!")
    print("\nNext Steps:")
    print("1. All endpoints should return 200 OK for documentation")
    print("2. Authenticated endpoints will return 401/403 without token")
    print("3. Use these endpoints in your Angular frontend")
    print("4. Test actual operations after implementing authentication")

if __name__ == "__main__":
    main()