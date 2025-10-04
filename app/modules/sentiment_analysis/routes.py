from fastapi import APIRouter, HTTPException
from typing import List
from .schemas import SentimentAnalysisRequest, SentimentAnalysisResponse
from .service import SentimentAnalysisService

router = APIRouter()
service = SentimentAnalysisService()


@router.post("/analyze", response_model=SentimentAnalysisResponse)
async def analyze_sentiment(request: SentimentAnalysisRequest):
    """
    Analyze sentiment from repository interactions.

    Analyzes comments, issues, and PR discussions to gauge
    community sentiment and maintainer stress levels.
    """
    try:
        result = await service.analyze(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends/{repository}")
async def get_sentiment_trends(repository: str, days: int = 30):
    """
    Get sentiment trends over time for a repository.
    """
    try:
        trends = await service.get_trends(repository, days)
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch-analyze")
async def batch_analyze_sentiment(repositories: List[str]):
    """
    Analyze sentiment for multiple repositories.
    """
    try:
        results = await service.batch_analyze(repositories)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
