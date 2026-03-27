"""FastAPI serving endpoint for recommendations."""

from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException

from recsys.models.base import BaseRecommender


class RecommendationItem(BaseModel):
    """A single recommended item with its score."""

    item_id: int
    score: float
    rank: int


class RecommendationResponse(BaseModel):
    """Response payload for a recommendation request."""

    user_id: int
    recommendations: list[RecommendationItem]
    model_name: str
    n_requested: int


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    model_loaded: bool


app = FastAPI(title="Hybrid Recommendation Engine", version="0.1.0")

_model: BaseRecommender | None = None


def set_model(model: BaseRecommender) -> None:
    """Register a fitted model for serving."""
    global _model
    model._check_is_fitted()
    _model = model


def _get_model() -> BaseRecommender:
    if _model is None:
        raise HTTPException(status_code=503, detail="No model loaded")
    return _model


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model_loaded=_model is not None,
    )


@app.get("/recommend/{user_id}", response_model=RecommendationResponse)
async def recommend(user_id: int, n: int = 10) -> RecommendationResponse:
    """Generate top-N recommendations for a user.

    Args:
        user_id: The user to generate recommendations for.
        n: Number of recommendations to return (default 10, max 100).
    """
    # TODO: Validate n (clamp to 1..100)
    # TODO: Call model.recommend(user_id, n)
    # TODO: Handle unknown users gracefully (return popular items or 404)
    # TODO: Format as RecommendationResponse with ranked items
    raise NotImplementedError


@app.get("/predict/{user_id}/{item_id}")
async def predict_score(user_id: int, item_id: int) -> dict:
    """Predict the score for a specific user-item pair.

    Args:
        user_id: The user ID.
        item_id: The item ID.
    """
    # TODO: Call model.predict(user_id, item_id)
    # TODO: Return {"user_id": ..., "item_id": ..., "score": ...}
    raise NotImplementedError
