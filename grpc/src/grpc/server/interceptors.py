"""Server interceptors: logging, authentication, rate limiting."""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from threading import Lock
from typing import Any, Callable

import grpc

logger = logging.getLogger(__name__)


class LoggingInterceptor(grpc.ServerInterceptor):
    """Interceptor that logs request method, duration, and status."""

    def intercept_service(
        self, continuation: Callable, handler_call_details: grpc.HandlerCallDetails
    ) -> Any:
        """Log incoming RPC details and response time.

        Args:
            continuation: The next handler in the chain.
            handler_call_details: Metadata about the incoming call.

        Returns:
            The RPC handler (possibly wrapped).
        """
        # TODO: Implement
        # - Extract the method name from handler_call_details.method
        # - Log the incoming request method
        # - Record the start time
        # - Call continuation(handler_call_details) to get the handler
        # - Wrap the handler to log duration after completion
        # - Return the (possibly wrapped) handler
        raise NotImplementedError


class AuthenticationInterceptor(grpc.ServerInterceptor):
    """Interceptor that validates API key from request metadata.

    Expects the API key in the "x-api-key" metadata field.
    """

    def __init__(self, api_key: str) -> None:
        """Initialize with the expected API key.

        Args:
            api_key: The valid API key to check against.
        """
        self._api_key = api_key

    def intercept_service(
        self, continuation: Callable, handler_call_details: grpc.HandlerCallDetails
    ) -> Any:
        """Validate the API key from request metadata.

        Args:
            continuation: The next handler in the chain.
            handler_call_details: Metadata about the incoming call.

        Returns:
            The handler if authenticated, or an abort handler if not.
        """
        # TODO: Implement
        # - Extract metadata from handler_call_details.invocation_metadata
        # - Look for the "x-api-key" key
        # - If missing or wrong, return a handler that aborts with
        #   UNAUTHENTICATED status
        # - If valid, call continuation(handler_call_details)
        raise NotImplementedError


class RateLimitInterceptor(grpc.ServerInterceptor):
    """Interceptor that rate-limits requests using a token bucket algorithm.

    Each client (identified by peer address) gets its own bucket.
    """

    def __init__(
        self,
        max_tokens: int = 100,
        refill_rate: float = 10.0,
    ) -> None:
        """Initialize the rate limiter.

        Args:
            max_tokens: Maximum tokens in the bucket.
            refill_rate: Tokens added per second.
        """
        self._max_tokens = max_tokens
        self._refill_rate = refill_rate
        self._buckets: dict[str, float] = defaultdict(lambda: float(max_tokens))
        self._last_refill: dict[str, float] = {}
        self._lock = Lock()

    def _get_tokens(self, client_id: str) -> float:
        """Get the current token count for a client, refilling as needed.

        Args:
            client_id: Identifier for the client (e.g., peer address).

        Returns:
            Current number of available tokens.
        """
        # TODO: Implement
        # - Calculate elapsed time since last refill
        # - Add elapsed * refill_rate tokens (capped at max_tokens)
        # - Update last_refill time
        # - Return current token count
        raise NotImplementedError

    def _consume_token(self, client_id: str) -> bool:
        """Try to consume one token from the client's bucket.

        Args:
            client_id: Identifier for the client.

        Returns:
            True if a token was consumed, False if bucket is empty.
        """
        # TODO: Implement
        # - Lock, get tokens, if >= 1 decrement and return True, else False
        raise NotImplementedError

    def intercept_service(
        self, continuation: Callable, handler_call_details: grpc.HandlerCallDetails
    ) -> Any:
        """Rate-limit the request based on client identity.

        Args:
            continuation: The next handler in the chain.
            handler_call_details: Metadata about the incoming call.

        Returns:
            The handler if within rate limit, abort handler if exceeded.
        """
        # TODO: Implement
        # - Extract client identity from metadata or peer info
        # - Call _consume_token
        # - If rate limited, return handler that aborts with RESOURCE_EXHAUSTED
        # - Otherwise, call continuation(handler_call_details)
        raise NotImplementedError
