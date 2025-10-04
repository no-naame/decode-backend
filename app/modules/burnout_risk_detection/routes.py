from fastapi import APIRouter, HTTPException
from typing import List
from .schemas import BurnoutRiskRequest, BurnoutRiskResponse, BurnoutAlert
from .service import BurnoutRiskDetectionService

router = APIRouter()
service = BurnoutRiskDetectionService()


@router.post("/assess", response_model=BurnoutRiskResponse)
async def assess_burnout_risk(request: BurnoutRiskRequest):
    """
    Assess burnout risk for a maintainer.

    Analyzes activity patterns, workload, and other indicators
    to detect potential burnout risks.
    """
    try:
        result = await service.assess_risk(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts/{username}")
async def get_burnout_alerts(username: str) -> List[BurnoutAlert]:
    """
    Get active burnout alerts for a maintainer.
    """
    try:
        alerts = await service.get_alerts(username)
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{username}")
async def get_burnout_history(username: str, days: int = 90):
    """
    Get historical burnout risk scores.
    """
    try:
        history = await service.get_history(username, days)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/subscribe-alerts")
async def subscribe_to_alerts(username: str, email: str):
    """
    Subscribe to burnout risk alerts.
    """
    try:
        result = await service.subscribe_alerts(username, email)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
