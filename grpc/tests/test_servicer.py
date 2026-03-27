"""Tests for the PredictServicer implementation."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from grpc.server.model_manager import ModelManager
from grpc.server.servicer import PredictServicer


@pytest.fixture
def mock_model_manager() -> MagicMock:
    """Create a mock ModelManager with a loaded model."""
    manager = MagicMock(spec=ModelManager)
    mock_predictor = MagicMock()
    mock_predictor.predict.return_value = np.array([0.85, 0.12])
    manager.get_model.return_value = mock_predictor
    return manager


@pytest.fixture
def servicer(mock_model_manager: MagicMock) -> PredictServicer:
    """Create a PredictServicer with a mock model manager."""
    return PredictServicer(mock_model_manager)


@pytest.fixture
def mock_context() -> MagicMock:
    """Create a mock gRPC ServicerContext."""
    ctx = MagicMock()
    ctx.is_active.return_value = True
    return ctx


class TestUnaryPredict:
    """Tests for the Predict unary RPC."""

    def test_predict_returns_response(
        self, servicer: PredictServicer, mock_context: MagicMock
    ) -> None:
        """Predict should return a PredictResponse with predictions."""
        # TODO: Implement
        # - Create a mock PredictRequest with model_name and NDArray features
        # - Call servicer.Predict(request, mock_context)
        # - Assert response contains predictions
        raise NotImplementedError

    def test_predict_model_not_found_aborts(
        self, servicer: PredictServicer, mock_context: MagicMock
    ) -> None:
        """Predict should abort with NOT_FOUND for unknown models."""
        # TODO: Implement
        # - Set mock_model_manager.get_model.return_value = None
        # - Call servicer.Predict with an unknown model name
        # - Assert context.abort was called with NOT_FOUND status
        raise NotImplementedError

    def test_predict_includes_latency(
        self, servicer: PredictServicer, mock_context: MagicMock
    ) -> None:
        """Response should include server-side latency in milliseconds."""
        # TODO: Implement
        raise NotImplementedError


class TestStreamPredict:
    """Tests for the StreamPredict server-streaming RPC."""

    def test_stream_yields_per_sample(
        self, servicer: PredictServicer, mock_context: MagicMock
    ) -> None:
        """StreamPredict should yield one response per input sample."""
        # TODO: Implement
        # - Create request with batch features of shape (5, 3)
        # - Call servicer.StreamPredict(request, mock_context)
        # - Collect all yielded responses
        # - Assert len(responses) == 5
        raise NotImplementedError

    def test_stream_stops_on_cancelled_context(
        self, servicer: PredictServicer, mock_context: MagicMock
    ) -> None:
        """StreamPredict should stop yielding when context is cancelled."""
        # TODO: Implement
        # - Set mock_context.is_active to return False after 2 calls
        # - Assert fewer than batch_size responses are yielded
        raise NotImplementedError


class TestListModels:
    """Tests for the ListModels RPC."""

    def test_list_returns_loaded_models(
        self, servicer: PredictServicer, mock_context: MagicMock
    ) -> None:
        """ListModels should return info about all loaded models."""
        # TODO: Implement
        raise NotImplementedError


class TestReloadModel:
    """Tests for the ReloadModel RPC."""

    def test_reload_success(
        self, servicer: PredictServicer, mock_context: MagicMock
    ) -> None:
        """ReloadModel should return success on valid reload."""
        # TODO: Implement
        raise NotImplementedError

    def test_reload_failure_returns_error(
        self, servicer: PredictServicer, mock_context: MagicMock
    ) -> None:
        """ReloadModel should handle reload failures gracefully."""
        # TODO: Implement
        # - Make model_manager.reload raise RuntimeError
        # - Assert response.success is False
        raise NotImplementedError
