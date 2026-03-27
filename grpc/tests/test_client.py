"""Client integration tests for the gRPC PredictClient."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from grpc.client.client import PredictClient
from grpc.client.load_balancer import RoundRobinBalancer


class TestPredictClient:
    """Tests for the PredictClient."""

    def test_metadata_includes_api_key(self) -> None:
        """Metadata should include x-api-key when configured."""
        # TODO: Implement
        # client = PredictClient(api_key="test-key")
        # metadata = client._get_metadata()
        # Assert ("x-api-key", "test-key") in metadata
        raise NotImplementedError

    def test_metadata_empty_without_api_key(self) -> None:
        """Metadata should be empty when no API key is set."""
        # TODO: Implement
        raise NotImplementedError

    def test_context_manager_connects_and_closes(self) -> None:
        """Using client as context manager should connect and close."""
        # TODO: Implement
        # Mock grpc.insecure_channel
        # Use `with PredictClient(...) as client:` and verify channel lifecycle
        raise NotImplementedError

    @patch("grpc.client.client.grpc.insecure_channel")
    def test_predict_retries_on_unavailable(
        self, mock_channel: MagicMock
    ) -> None:
        """Client should retry on UNAVAILABLE status."""
        # TODO: Implement
        # - Mock stub.Predict to raise UNAVAILABLE twice, then succeed
        # - Assert predict() eventually returns a result
        # - Assert stub.Predict was called 3 times
        raise NotImplementedError

    @patch("grpc.client.client.grpc.insecure_channel")
    def test_predict_raises_on_non_retryable_error(
        self, mock_channel: MagicMock
    ) -> None:
        """Client should raise immediately on non-retryable errors."""
        # TODO: Implement
        # - Mock stub.Predict to raise INVALID_ARGUMENT
        # - Assert grpc.RpcError is raised immediately (no retries)
        raise NotImplementedError

    def test_stream_predict_yields_results(self) -> None:
        """stream_predict should yield one array per streamed response."""
        # TODO: Implement
        raise NotImplementedError


class TestRoundRobinBalancer:
    """Tests for the round-robin load balancer."""

    def test_requires_at_least_one_address(self) -> None:
        """Should raise ValueError with empty address list."""
        # TODO: Implement
        # Assert ValueError is raised for RoundRobinBalancer([])
        raise NotImplementedError

    def test_rotates_through_servers(self) -> None:
        """Requests should rotate across servers."""
        # TODO: Implement
        # - Create balancer with 3 addresses
        # - Mock client.predict for each
        # - Make 6 predictions
        # - Assert each server received exactly 2 requests
        raise NotImplementedError

    def test_failover_to_next_server(self) -> None:
        """Should try the next server when one fails."""
        # TODO: Implement
        # - First server raises UNAVAILABLE (all retries exhausted)
        # - Second server succeeds
        # - Assert prediction result is returned
        raise NotImplementedError

    def test_n_servers_property(self) -> None:
        """n_servers should return the number of configured addresses."""
        # TODO: Implement
        raise NotImplementedError
