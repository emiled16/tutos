"""Tests for the FastAPI recommendation serving endpoint."""

import numpy as np
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from recsys.models.base import BaseRecommender
from recsys.serving.api import app, set_model


@pytest.fixture
def mock_model() -> MagicMock:
    """Create a mock fitted recommender model."""
    model = MagicMock(spec=BaseRecommender)
    model.name = "MockModel"
    model.is_fitted = True
    model._check_is_fitted = MagicMock()
    model.recommend.return_value = [
        (101, 0.95),
        (202, 0.87),
        (303, 0.76),
    ]
    model.predict.return_value = 0.82
    return model


@pytest.fixture
def client(mock_model: MagicMock) -> TestClient:
    """Create a test client with a loaded mock model."""
    set_model(mock_model)
    return TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self, client: TestClient) -> None:
        """GET /health should return status and model_loaded flag."""
        # TODO: Send GET /health
        # TODO: Assert status code 200
        # TODO: Assert response contains {"status": "healthy", "model_loaded": true}

    def test_health_no_model(self) -> None:
        """Health check should report model_loaded=false when no model is set."""
        # TODO: Create a client without setting a model
        # TODO: Assert model_loaded is False


class TestRecommendEndpoint:
    def test_recommend_returns_items(self, client: TestClient) -> None:
        """GET /recommend/{user_id} should return a list of recommendations."""
        # TODO: Send GET /recommend/1?n=3
        # TODO: Assert status code 200
        # TODO: Assert response has user_id, recommendations list
        # TODO: Assert each recommendation has item_id, score, rank

    def test_recommend_default_n(self, client: TestClient) -> None:
        """Default n should be 10."""
        # TODO: Send GET /recommend/1 without n parameter
        # TODO: Assert model.recommend was called with n=10

    def test_recommend_clamps_n(self, client: TestClient) -> None:
        """n should be clamped to [1, 100]."""
        # TODO: Send GET /recommend/1?n=200
        # TODO: Assert model.recommend was called with n <= 100

    def test_recommend_unknown_user(
        self, client: TestClient, mock_model: MagicMock
    ) -> None:
        """Unknown users should be handled gracefully."""
        mock_model.recommend.side_effect = KeyError("Unknown user")

        # TODO: Send GET /recommend/99999
        # TODO: Assert appropriate error response (404 or fallback recommendations)


class TestPredictEndpoint:
    def test_predict_score(self, client: TestClient) -> None:
        """GET /predict/{user_id}/{item_id} should return a score."""
        # TODO: Send GET /predict/1/101
        # TODO: Assert status code 200
        # TODO: Assert response contains user_id, item_id, and score fields

    def test_predict_unknown_pair(
        self, client: TestClient, mock_model: MagicMock
    ) -> None:
        """Unknown user-item pair should be handled gracefully."""
        mock_model.predict.side_effect = KeyError("Unknown pair")

        # TODO: Send GET /predict/99999/99999
        # TODO: Assert appropriate error response
