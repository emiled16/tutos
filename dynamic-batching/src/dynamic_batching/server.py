"""FastAPI server integrating the dynamic batcher."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from dynamic_batching.batcher import DynamicBatcher
from dynamic_batching.config import BatcherConfig
from dynamic_batching.executor import BatchExecutor
from dynamic_batching.metrics import MetricsCollector
from dynamic_batching.request import InferenceRequest, InferenceResponse
from dynamic_batching.scheduler import RequestScheduler

logger = logging.getLogger(__name__)


class PredictRequest(BaseModel):
    """HTTP request body for the /predict endpoint.

    Attributes:
        payload: Input data for inference.
        model_name: Target model (defaults to configured model).
        priority: Request priority (0=high, 1=normal, 2=low).
    """

    payload: list[float]
    model_name: str | None = None
    priority: int = 1


class PredictResponse(BaseModel):
    """HTTP response body from the /predict endpoint.

    Attributes:
        request_id: Unique ID assigned to this request.
        result: Model output.
        batch_size: How many requests were in the batch.
        wait_time_ms: Time spent waiting for batch formation.
    """

    request_id: str
    result: list[float]
    batch_size: int = 0
    wait_time_ms: float = 0.0


class HealthResponse(BaseModel):
    """Response from the /health endpoint."""

    status: str = "ok"
    models: list[str] = []


scheduler: RequestScheduler | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler — starts and stops the batcher.

    Initializes the scheduler, registers the default model, and starts
    all batchers on startup. Stops everything on shutdown.
    """
    # TODO: Implement lifespan:
    #   Startup:
    #     1. Load BatcherConfig from environment
    #     2. Create RequestScheduler
    #     3. Create BatchExecutor and MetricsCollector
    #     4. Register the default model
    #     5. Start all batchers
    #     6. Assign to global `scheduler`
    #   Shutdown:
    #     7. Stop all batchers
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI app with all routes registered.
    """
    # TODO: Implement app creation:
    #   1. Create FastAPI with lifespan handler
    #   2. Register routes (predict, health, metrics)
    #   3. Return app
    pass


async def predict_endpoint(body: PredictRequest) -> PredictResponse:
    """Handle a prediction request.

    Converts the HTTP request into an InferenceRequest, submits it to the
    scheduler, and returns the result.

    Args:
        body: The HTTP request body.

    Returns:
        PredictResponse with model output and metadata.

    Raises:
        HTTPException: 503 if batcher is not available or overloaded.
    """
    # TODO: Implement predict endpoint:
    #   1. Check that scheduler is initialized (503 if not)
    #   2. Create InferenceRequest from body
    #   3. Submit to scheduler with appropriate model_name
    #   4. Convert InferenceResponse to PredictResponse
    #   5. Handle errors (queue full → 503, unknown model → 404)
    pass


async def health_endpoint() -> HealthResponse:
    """Health check endpoint.

    Returns:
        Health status and list of registered models.
    """
    # TODO: Implement health check:
    #   Return HealthResponse with status="ok" and list of registered models
    pass


async def metrics_endpoint() -> dict:
    """Metrics endpoint returning current metrics snapshot.

    Returns:
        Dictionary of metrics for all registered models.
    """
    # TODO: Implement metrics endpoint:
    #   1. For each registered model, get its MetricsCollector
    #   2. Call snapshot() and collect results
    #   3. Return as dict
    pass
