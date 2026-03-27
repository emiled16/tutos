"""FastAPI endpoint for serving search rankings.

Exposes a REST API that accepts queries and candidate documents,
computes features, runs the ranking model, and returns ordered results.
"""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Search Ranking API",
    description="Learning-to-rank service using LambdaMART",
    version="0.1.0",
)


class CandidateDocument(BaseModel):
    """A candidate document to be ranked."""

    doc_id: str
    title: str
    body: str
    url: str
    pagerank: float = 0.0


class RankRequest(BaseModel):
    """Request to rank candidate documents for a query."""

    query: str
    candidates: list[CandidateDocument] = Field(..., min_length=1)
    top_k: int = Field(default=10, ge=1, le=100)


class RankedDocument(BaseModel):
    """A document with its ranking score."""

    doc_id: str
    title: str
    score: float
    rank: int


class RankResponse(BaseModel):
    """Response containing ranked documents."""

    query: str
    results: list[RankedDocument]
    total_candidates: int


_ranker = None


def get_ranker():
    """Lazy-load the ranking service singleton."""
    global _ranker
    if _ranker is None:
        from ranking.serving.ranker import OnlineRanker

        model_path = Path(os.getenv("MODEL_PATH", "models/lambdamart.txt"))
        # TODO: Initialize OnlineRanker with appropriate corpus stats and model
        raise NotImplementedError("Ranker initialization not configured")
    return _ranker


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/rank", response_model=RankResponse)
async def rank_documents(request: RankRequest) -> RankResponse:
    """Rank candidate documents for a query.

    Accepts a query and a list of candidate documents, computes ranking
    features, applies the trained model, and returns top-k results.

    Args:
        request: Ranking request with query and candidates.

    Returns:
        Ranked results ordered by predicted relevance.
    """
    # TODO: Implement the ranking endpoint
    # 1. Get the ranker via get_ranker()
    # 2. Convert CandidateDocument models to Document objects
    # 3. Call ranker.rank(query, documents, top_k)
    # 4. Build and return RankResponse with ranked documents
    raise NotImplementedError


@app.post("/rank/batch", response_model=list[RankResponse])
async def rank_batch(requests: list[RankRequest]) -> list[RankResponse]:
    """Rank documents for multiple queries in a single call.

    Args:
        requests: List of ranking requests.

    Returns:
        List of ranking responses, one per query.
    """
    # TODO: Implement batch ranking by iterating over requests
    raise NotImplementedError
