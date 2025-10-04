#!/usr/bin/env python3
"""
Test script for GitHub Smart Authentication

This script tests the GitHub smart authentication implementation.
Run this after setting up your environment variables.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.modules.github_smart_auth.service import github_smart_auth_service


async def test_github_smart_auth():
    """Test the GitHub smart authentication service"""
    
    print("🔧 Testing GitHub Smart Authentication...")
    print("=" * 50)
    
    # Check if environment variables are set
    github_app_id = os.getenv("GITHUB_APP_ID")
    github_private_key = os.getenv("GITHUB_PRIVATE_KEY")
    
    if not github_app_id or not github_private_key:
        print("❌ Environment variables not set!")
        print("Please set the following environment variables:")
        print("  GITHUB_APP_ID=your-app-id")
        print("  GITHUB_PRIVATE_KEY=your-private-key")
        return False
    
    print(f"✅ GitHub App ID: {github_app_id}")
    print(f"✅ Private Key: {'*' * 20}...{github_private_key[-10:] if github_private_key else 'Not set'}")
    print()
    
    try:
        # Test 1: App-level authentication
        print("🧪 Test 1: App-level authentication")
        app_info = github_smart_auth_service.get_app_info()
        if app_info.get("success"):
            print("✅ App-level authentication successful!")
            print(f"   App Name: {app_info.get('app_info', {}).get('name', 'Unknown')}")
        else:
            print(f"❌ App-level authentication failed: {app_info.get('error', 'Unknown error')}")
            return False
        print()
        
        # Test 2: Get installations
        print("🧪 Test 2: Get all installations")
        installations = github_smart_auth_service.get_all_installations()
        if installations.get("success"):
            print(f"✅ Found {installations.get('count', 0)} installations")
            for i, installation in enumerate(installations.get('installations', [])[:3]):  # Show first 3
                account = installation.get('account', {})
                print(f"   {i+1}. {account.get('login', 'Unknown')} ({account.get('type', 'Unknown')})")
        else:
            print(f"❌ Failed to get installations: {installations.get('error', 'Unknown error')}")
        print()
        
        # Test 3: Get repositories (smart)
        print("🧪 Test 3: Get repositories (smart)")
        repositories = github_smart_auth_service.get_repositories()
        if repositories.get("success"):
            print(f"✅ Found {repositories.get('count', 0)} repositories")
            for i, repo in enumerate(repositories.get('repositories', [])[:3]):  # Show first 3
                print(f"   {i+1}. {repo.get('full_name', 'Unknown')} - {repo.get('description', 'No description')[:50]}...")
        else:
            print(f"❌ Failed to get repositories: {repositories.get('error', 'Unknown error')}")
        print()
        
        print("🎉 All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False


def main():
    """Main function"""
    print("GitHub Smart Authentication Test")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Please run this script from the decode-backend root directory")
        return
    
    # Run the test
    success = asyncio.run(test_github_smart_auth())
    
    if success:
        print("\n✅ GitHub Smart Authentication is working correctly!")
        print("\nNext steps:")
        print("1. Set up your GitHub App with the required permissions")
        print("2. Install the app on your repositories")
        print("3. Test the API endpoints using the FastAPI docs at http://localhost:8000/docs")
    else:
        print("\n❌ GitHub Smart Authentication test failed!")
        print("Please check your environment variables and GitHub App configuration.")


if __name__ == "__main__":
    main()
