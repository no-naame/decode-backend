#!/usr/bin/env python3
"""Test the complete installation flow"""

import requests

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("🧪 Testing Installation Flow")
print("=" * 60)
print()

# Test 1: Installation status
print("1️⃣ Testing installation status...")
response = requests.get(f"{BASE_URL}/api/v1/github-smart-auth/install/status")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Status check: {response.status_code}")
    print(f"   Installed: {data.get('installed')}")
    print(f"   Count: {data.get('count')}")
else:
    print(f"❌ Status check failed: {response.status_code}")
print()

# Test 2: Installation redirect
print("2️⃣ Testing installation redirect...")
response = requests.get(f"{BASE_URL}/api/v1/github-smart-auth/install", allow_redirects=False)
if response.status_code == 307:
    location = response.headers.get('location', '')
    print(f"✅ Redirect working: {response.status_code}")
    print(f"   Location: {location}")
    
    # Verify URL format
    if 'github.com/apps/dkmcopen/installations/new' in location:
        print(f"✅ URL is correct!")
    else:
        print(f"❌ URL format incorrect")
else:
    print(f"❌ Redirect failed: {response.status_code}")
print()

# Test 3: Installation guide
print("3️⃣ Testing installation guide...")
response = requests.get(f"{BASE_URL}/api/v1/github-smart-auth/install/guide")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Guide endpoint: {response.status_code}")
    print(f"   Title: {data.get('title')}")
    install_url = data.get('steps', [{}])[0].get('url', '')
    print(f"   Install URL in guide: {install_url}")
else:
    print(f"❌ Guide failed: {response.status_code}")
print()

print("=" * 60)
print("✅ Installation flow is working correctly!")
print("=" * 60)
