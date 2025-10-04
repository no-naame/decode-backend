"""
GitHub App Installation Routes

This module provides routes for GitHub App installation flow.
"""

from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import RedirectResponse
from typing import Dict, Any
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/install")
async def install_github_app():
    """Redirect to GitHub App installation page"""
    if not settings.GITHUB_APP_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GitHub App ID is not configured"
        )
    
    # Use app slug if available, otherwise use settings URL
    if settings.GITHUB_APP_SLUG:
        install_url = f"https://github.com/apps/{settings.GITHUB_APP_SLUG}/installations/new"
    else:
        # Fallback to settings URL
        install_url = f"https://github.com/settings/apps/{settings.GITHUB_APP_ID}/installations/new"
    
    return RedirectResponse(url=install_url)


@router.get("/install/callback")
async def installation_callback(
    installation_id: str = Query(..., description="Installation ID from GitHub"),
    setup_action: str = Query("install", description="Setup action from GitHub")
):
    """Handle GitHub App installation callback"""
    
    return {
        "success": True,
        "message": "GitHub App installed successfully!",
        "installation_id": installation_id,
        "setup_action": setup_action,
        "next_steps": [
            "Your GitHub App is now installed",
            "You can now access repositories through the API",
            "Test your authentication using the Smart GitHub Auth endpoints"
        ]
    }


@router.get("/install/status")
async def installation_status():
    """Check installation status and provide installation link if needed"""
    try:
        from app.shared.smart_github_auth import smart_github_auth_service
        
        # Get all installations
        installations = smart_github_auth_service.get_all_installations()
        
        if installations:
            return {
                "success": True,
                "installed": True,
                "count": len(installations),
                "installations": installations,
                "message": "GitHub App is installed and ready to use!"
            }
        else:
            return {
                "success": False,
                "installed": False,
                "count": 0,
                "installations": [],
                "message": "GitHub App is not installed yet",
                "install_url": f"/api/v1/github-smart-auth/install/install"
            }
    except Exception as e:
        logger.error(f"Failed to check installation status: {e}")
        return {
            "success": False,
            "installed": False,
            "error": str(e),
            "message": "Failed to check installation status"
        }


@router.get("/install/guide")
async def installation_guide():
    """Provide installation guide and instructions"""
    
    return {
        "title": "GitHub App Installation Guide",
        "steps": [
            {
                "step": 1,
                "title": "Install the GitHub App",
                "description": "Click the install button to install the GitHub App on your account or organization",
                "action": "install",
                "url": f"https://github.com/apps/{settings.GITHUB_APP_SLUG or settings.GITHUB_APP_ID}/installations/new"
            },
            {
                "step": 2,
                "title": "Grant Permissions",
                "description": "Grant the required permissions to the GitHub App",
                "permissions": [
                    "Contents: Read",
                    "Issues: Read & Write", 
                    "Metadata: Read",
                    "Pull requests: Read"
                ]
            },
            {
                "step": 3,
                "title": "Select Repositories",
                "description": "Choose which repositories the GitHub App can access",
                "options": [
                    "All repositories",
                    "Selected repositories only"
                ]
            },
            {
                "step": 4,
                "title": "Test Authentication",
                "description": "Use the Smart GitHub Auth endpoints to test your authentication",
                "endpoints": [
                    "/api/v1/github-smart-auth/app/info",
                    "/api/v1/github-smart-auth/app/installations",
                    "/api/v1/github-smart-auth/repositories"
                ]
            }
        ],
        "troubleshooting": {
            "common_issues": [
                {
                    "issue": "401 Unauthorized Error",
                    "solution": "Make sure the GitHub App is installed on the repository you're trying to access"
                },
                {
                    "issue": "No installations found",
                    "solution": "Install the GitHub App first using the install link"
                },
                {
                    "issue": "Permission denied",
                    "solution": "Check that the GitHub App has the required permissions"
                }
            ]
        }
    }
