"""Integration tests for the FastAPI server."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from dynamic_batching.server import create_app


@pytest.fixture
def app():
    """Create a fresh app instance for testing."""
    # TODO: Implement fixture:
    #   Return create_app() (lifespan will handle setup/teardown)
    pass


@pytest.fixture
async def client(app) -> AsyncClient:
    """Async HTTP client bound to the test app."""
    # TODO: Implement fixture:
    #   Use httpx.AsyncClient with ASGITransport to test without a real server
    #   async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    #       yield c
    pass


class TestPredictEndpoint:
    """Tests for the /predict endpoint."""

    async def test_predict_returns_result(self, client: AsyncClient) -> None:
        """POST /predict should return a valid prediction response."""
        # TODO: Implement test:
        #   1. POST to /predict with payload=[1.0, 2.0, 3.0]
        #   2. Assert status 200
        #   3. Assert response has request_id and result fields
        pass

    async def test_predict_assigns_request_id(self, client: AsyncClient) -> None:
        """Each prediction should get a unique request_id."""
        # TODO: Implement test:
        #   Send 2 requests, assert they have different request_ids
        pass

    async def test_predict_with_priority(self, client: AsyncClient) -> None:
        """Priority field should be accepted and respected."""
        # TODO: Implement test:
        #   POST with priority=0 (HIGH), assert 200
        pass

    async def test_predict_with_model_name(self, client: AsyncClient) -> None:
        """Custom model_name should route to the correct batcher."""
        # TODO: Implement test:
        #   POST with model_name=configured model, assert 200
        pass

    async def test_predict_empty_payload(self, client: AsyncClient) -> None:
        """Empty payload should still be handled (edge case)."""
        # TODO: Implement test
        pass

    async def test_predict_concurrent_requests(self, client: AsyncClient) -> None:
        """Multiple concurrent requests should all receive responses."""
        # TODO: Implement test:
        #   1. Send 10 requests concurrently using asyncio.gather
        #   2. Assert all return 200
        #   3. Assert all have unique request_ids
        pass


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    async def test_health_check(self, client: AsyncClient) -> None:
        """GET /health should return status=ok."""
        # TODO: Implement test:
        #   GET /health, assert 200, assert body contains status="ok"
        pass

    async def test_health_lists_models(self, client: AsyncClient) -> None:
        """Health response should list registered models."""
        # TODO: Implement test
        pass


class TestMetricsEndpoint:
    """Tests for the /metrics endpoint."""

    async def test_metrics_endpoint(self, client: AsyncClient) -> None:
        """GET /metrics should return metrics data."""
        # TODO: Implement test:
        #   1. Send a few predict requests first
        #   2. GET /metrics
        #   3. Assert 200
        #   4. Assert response contains expected metric fields
        pass

    async def test_metrics_reflect_requests(self, client: AsyncClient) -> None:
        """Metrics should reflect the number of requests processed."""
        # TODO: Implement test:
        #   1. Send N predict requests
        #   2. GET /metrics
        #   3. Assert total_requests >= N
        pass
