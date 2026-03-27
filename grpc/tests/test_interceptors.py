"""Tests for gRPC server interceptors."""

from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest

from grpc.server.interceptors import (
    AuthenticationInterceptor,
    LoggingInterceptor,
    RateLimitInterceptor,
)


@pytest.fixture
def mock_continuation() -> MagicMock:
    """Create a mock continuation (next handler in chain)."""
    return MagicMock()


@pytest.fixture
def mock_handler_details() -> MagicMock:
    """Create mock handler call details."""
    details = MagicMock()
    details.method = "/PredictService/Predict"
    details.invocation_metadata = []
    return details


class TestLoggingInterceptor:
    """Tests for the LoggingInterceptor."""

    def test_passes_through_to_continuation(
        self,
        mock_continuation: MagicMock,
        mock_handler_details: MagicMock,
    ) -> None:
        """Logging interceptor should call the continuation."""
        # TODO: Implement
        # interceptor = LoggingInterceptor()
        # interceptor.intercept_service(mock_continuation, mock_handler_details)
        # Assert mock_continuation was called once
        raise NotImplementedError

    def test_logs_request_method(
        self,
        mock_continuation: MagicMock,
        mock_handler_details: MagicMock,
    ) -> None:
        """Should log the RPC method name."""
        # TODO: Implement
        # Use patch on logger to capture log calls
        # Assert the method name appears in a log message
        raise NotImplementedError


class TestAuthenticationInterceptor:
    """Tests for the AuthenticationInterceptor."""

    def test_valid_key_passes_through(
        self,
        mock_continuation: MagicMock,
        mock_handler_details: MagicMock,
    ) -> None:
        """Valid API key should allow the request through."""
        # TODO: Implement
        # Set metadata to [("x-api-key", "valid-key")]
        # interceptor = AuthenticationInterceptor("valid-key")
        # result = interceptor.intercept_service(mock_continuation, mock_handler_details)
        # Assert continuation was called
        raise NotImplementedError

    def test_missing_key_rejects(
        self,
        mock_continuation: MagicMock,
        mock_handler_details: MagicMock,
    ) -> None:
        """Missing API key should reject the request."""
        # TODO: Implement
        # Set metadata to [] (no key)
        # Assert the returned handler aborts with UNAUTHENTICATED
        raise NotImplementedError

    def test_wrong_key_rejects(
        self,
        mock_continuation: MagicMock,
        mock_handler_details: MagicMock,
    ) -> None:
        """Wrong API key should reject the request."""
        # TODO: Implement
        # Set metadata with wrong key
        # Assert rejection
        raise NotImplementedError


class TestRateLimitInterceptor:
    """Tests for the RateLimitInterceptor."""

    def test_allows_requests_within_limit(
        self,
        mock_continuation: MagicMock,
        mock_handler_details: MagicMock,
    ) -> None:
        """Requests within the token budget should pass through."""
        # TODO: Implement
        # interceptor = RateLimitInterceptor(max_tokens=10)
        # Make 5 requests → all should pass
        raise NotImplementedError

    def test_rejects_when_tokens_exhausted(
        self,
        mock_continuation: MagicMock,
        mock_handler_details: MagicMock,
    ) -> None:
        """Requests exceeding the token budget should be rejected."""
        # TODO: Implement
        # interceptor = RateLimitInterceptor(max_tokens=2, refill_rate=0)
        # Make 3 requests → third should be rejected with RESOURCE_EXHAUSTED
        raise NotImplementedError

    def test_tokens_refill_over_time(
        self,
        mock_continuation: MagicMock,
        mock_handler_details: MagicMock,
    ) -> None:
        """Tokens should refill over time at the configured rate."""
        # TODO: Implement
        # interceptor = RateLimitInterceptor(max_tokens=1, refill_rate=100)
        # Consume token, wait briefly, try again → should pass
        raise NotImplementedError
