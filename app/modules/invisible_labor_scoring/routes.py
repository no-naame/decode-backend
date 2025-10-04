from fastapi import APIRouter, HTTPException
from typing import List
from .schemas import InvisibleLaborScoreRequest, InvisibleLaborScoreResponse
from .service import InvisibleLaborScoringService

router = APIRouter()
service = InvisibleLaborScoringService()


@router.post("/calculate", response_model=InvisibleLaborScoreResponse)
async def calculate_invisible_labor_score(request: InvisibleLaborScoreRequest):
    """
    Calculate invisible labor score for a maintainer.

    This endpoint analyzes various contribution metrics to score
    non-code contributions like code reviews, issue triaging, etc.
    """
    try:
        result = await service.calculate_score(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/{username}")
async def get_invisible_labor_metrics(username: str):
    """
    Get detailed invisible labor metrics for a specific maintainer.
    """
    try:
        metrics = await service.get_metrics(username)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
