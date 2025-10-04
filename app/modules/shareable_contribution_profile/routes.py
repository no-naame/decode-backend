from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional
from .schemas import ProfileRequest, ProfileResponse, ProfileUpdateRequest
from .service import ShareableProfileService

router = APIRouter()
service = ShareableProfileService()


@router.post("/generate", response_model=ProfileResponse)
async def generate_profile(request: ProfileRequest):
    """
    Generate a shareable contribution profile.

    Creates a comprehensive profile showcasing visible and invisible
    contributions, suitable for sharing with employers or community.
    """
    try:
        result = await service.generate_profile(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{username}")
async def get_profile(username: str):
    """
    Get existing shareable profile.
    """
    try:
        profile = await service.get_profile(username)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{username}")
async def update_profile(username: str, request: ProfileUpdateRequest):
    """
    Update shareable profile.
    """
    try:
        profile = await service.update_profile(username, request)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{username}/public", response_class=HTMLResponse)
async def get_public_profile(username: str):
    """
    Get public HTML version of profile (shareable link).
    """
    try:
        html = await service.get_public_html(username)
        return html
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{username}/export/{format}")
async def export_profile(username: str, format: str):
    """
    Export profile in various formats (PDF, JSON, Markdown).
    """
    try:
        if format not in ["pdf", "json", "markdown"]:
            raise HTTPException(status_code=400, detail="Invalid format")

        result = await service.export_profile(username, format)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{username}")
async def delete_profile(username: str):
    """
    Delete shareable profile.
    """
    try:
        result = await service.delete_profile(username)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
