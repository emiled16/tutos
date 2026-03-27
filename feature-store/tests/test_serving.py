"""Tests for the online feature serving endpoint."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from feature_store.serving import PredictionRequest, app


@pytest.fixture
def client() -> TestClient:
    """Create a FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_features() -> dict:
    """Sample feature dictionary as returned by the online store."""
    return {
        "amount_mean": 45.0,
        "amount_std": 20.0,
        "amount_max": 200.0,
        "transaction_count": 150,
        "account_age_days": 365,
        "txn_count_1h": 2,
        "txn_count_24h": 5,
        "txn_amount_sum_1h": 80.0,
    }


class TestHealthCheck:
    """Tests for the health check endpoint."""

    def test_health_returns_ok(self, client: TestClient) -> None:
        """Health endpoint should return 200 with status healthy."""
        # TODO: Implement
        # response = client.get("/health")
        # Assert status_code == 200
        # Assert response body contains {"status": "healthy"}
        raise NotImplementedError


class TestGetFeatures:
    """Tests for the feature retrieval endpoint."""

    @patch("feature_store.serving.get_online_features")
    def test_get_features_returns_feature_values(
        self,
        mock_get_features: MagicMock,
        client: TestClient,
        sample_features: dict,
    ) -> None:
        """GET /features/{user_id} should return feature values."""
        # TODO: Implement
        # Mock get_online_features to return sample_features
        # Call client.get("/features/user_001")
        # Assert response contains expected features
        raise NotImplementedError

    @patch("feature_store.serving.get_online_features")
    def test_get_features_user_not_found(
        self,
        mock_get_features: MagicMock,
        client: TestClient,
    ) -> None:
        """GET /features/{user_id} should return 404 for unknown users."""
        # TODO: Implement
        # Mock get_online_features to raise HTTPException(404)
        # Assert response status is 404
        raise NotImplementedError


class TestPredict:
    """Tests for the prediction endpoint."""

    @patch("feature_store.serving.predict_fraud")
    @patch("feature_store.serving.get_online_features")
    def test_predict_returns_probability(
        self,
        mock_get_features: MagicMock,
        mock_predict: MagicMock,
        client: TestClient,
        sample_features: dict,
    ) -> None:
        """POST /predict should return fraud probability."""
        # TODO: Implement
        # Mock get_online_features → sample_features
        # Mock predict_fraud → 0.85
        # POST to /predict with PredictionRequest body
        # Assert response has fraud_probability and is_fraud fields
        raise NotImplementedError

    @patch("feature_store.serving.predict_fraud")
    @patch("feature_store.serving.get_online_features")
    def test_predict_is_fraud_threshold(
        self,
        mock_get_features: MagicMock,
        mock_predict: MagicMock,
        client: TestClient,
        sample_features: dict,
    ) -> None:
        """is_fraud should be True when probability > 0.5."""
        # TODO: Implement
        # Test with probability 0.3 → is_fraud=False
        # Test with probability 0.8 → is_fraud=True
        raise NotImplementedError

    def test_predict_rejects_negative_amount(self, client: TestClient) -> None:
        """POST /predict should reject negative transaction amounts."""
        # TODO: Implement
        # POST with amount=-10 → expect 422 validation error
        raise NotImplementedError
