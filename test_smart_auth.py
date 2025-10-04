#!/usr/bin/env python3
"""
Comprehensive Smart Auth Test for decode-backend
"""

import requests
import json

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1/github-smart-auth"

def test_endpoint(name, endpoint, expected_status=200):
    """Test a single endpoint"""
    url = f"{BASE_URL}{API_PREFIX}{endpoint}"
    try:
        response = requests.get(url)
        success = response.status_code == expected_status
        status_icon = "✅" if success else "❌"
        print(f"{status_icon} {name}: {response.status_code}")
        
        if not success:
            print(f"   Expected: {expected_status}, Got: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
        else:
            # Print brief response info
            try:
                data = response.json()
                if isinstance(data, dict):
                    if 'success' in data:
                        print(f"   Success: {data.get('success')}")
                    if 'count' in data:
                        print(f"   Count: {data.get('count')}")
                    if 'installed' in data:
                        print(f"   Installed: {data.get('installed')}")
            except:
                pass
        
        return success
    except Exception as e:
        print(f"❌ {name}: ERROR - {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 decode-backend Smart Auth Verification")
    print("=" * 60)
    print()
    
    tests = [
        ("Health Check", "/health", 200, ""),
        ("App Info", "/app/info", 200, API_PREFIX),
        ("App Installations", "/app/installations", 200, API_PREFIX),
        ("Installation Status", "/install/status", 200, API_PREFIX),
        ("Installation Guide", "/install/guide", 200, API_PREFIX),
        ("Get Repositories", "/repositories", 200, API_PREFIX),
    ]
    
    results = []
    for name, endpoint, expected_status, prefix in tests:
        full_endpoint = endpoint if not prefix else endpoint
        url = f"{BASE_URL}{prefix}{endpoint}" if prefix else f"{BASE_URL}{endpoint}"
        
        try:
            response = requests.get(url)
            success = response.status_code == expected_status
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {name}")
            print(f"   URL: {url}")
            print(f"   Status: {response.status_code}")
            
            if success and response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        # Show relevant info
                        if 'success' in data:
                            print(f"   Result: {data.get('success')}")
                        if 'count' in data:
                            print(f"   Count: {data.get('count')}")
                        if 'installed' in data:
                            print(f"   Installed: {data.get('installed')}")
                        if 'repositories' in data and isinstance(data['repositories'], list):
                            print(f"   Repositories: {len(data['repositories'])} found")
                except:
                    pass
            
            results.append(success)
            print()
            
        except Exception as e:
            print(f"❌ {name}: ERROR - {str(e)}")
            print()
            results.append(False)
    
    print("=" * 60)
    print(f"📊 Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("✅ All tests passed! Smart Auth is working correctly.")
    else:
        print("❌ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
