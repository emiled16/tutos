"""Client-side round-robin load balancing for gRPC."""

from __future__ import annotations

import logging
from itertools import cycle
from threading import Lock
from typing import Any

import numpy as np

from grpc.client.client import PredictClient

logger = logging.getLogger(__name__)


class RoundRobinBalancer:
    """Client-side load balancer that distributes requests round-robin.

    Maintains a pool of PredictClient instances, one per server address,
    and rotates through them for each request.
    """

    def __init__(
        self,
        server_addresses: list[str],
        api_key: str | None = None,
        timeout: float = 10.0,
        max_retries: int = 3,
    ) -> None:
        """Initialize the load balancer with server addresses.

        Args:
            server_addresses: List of server addresses (host:port).
            api_key: API key shared by all servers.
            timeout: Default RPC deadline.
            max_retries: Retry attempts per server.
        """
        if not server_addresses:
            raise ValueError("At least one server address is required")
        self.server_addresses = server_addresses
        self._clients: list[PredictClient] = []
        self._api_key = api_key
        self._timeout = timeout
        self._max_retries = max_retries
        self._cycle: cycle | None = None
        self._lock = Lock()

    def connect_all(self) -> None:
        """Establish connections to all servers.

        Creates a PredictClient for each server address and connects.
        """
        # TODO: Implement
        # - For each address in server_addresses:
        #   - Create PredictClient(address, api_key, timeout, max_retries)
        #   - Call client.connect()
        #   - Append to self._clients
        # - Create self._cycle = cycle(range(len(self._clients)))
        raise NotImplementedError

    def close_all(self) -> None:
        """Close all client connections."""
        # TODO: Implement
        # - For each client, call close()
        # - Clear self._clients
        raise NotImplementedError

    def __enter__(self) -> RoundRobinBalancer:
        self.connect_all()
        return self

    def __exit__(self, *args: Any) -> None:
        self.close_all()

    def _next_client(self) -> PredictClient:
        """Get the next client in the round-robin rotation.

        Returns:
            The next PredictClient.

        Raises:
            RuntimeError: If no clients are connected.
        """
        # TODO: Implement
        # - Lock, get next index from self._cycle
        # - Return self._clients[index]
        raise NotImplementedError

    def predict(
        self,
        features: np.ndarray,
        model_name: str = "default",
        **kwargs: Any,
    ) -> np.ndarray:
        """Send a prediction request to the next server in rotation.

        If the selected server fails with a transient error and retries
        are exhausted, tries the next server.

        Args:
            features: Input feature array.
            model_name: Name of the model.
            **kwargs: Additional arguments passed to PredictClient.predict.

        Returns:
            Prediction result as numpy array.

        Raises:
            grpc.RpcError: If all servers fail.
        """
        # TODO: Implement
        # - Try _next_client().predict(features, model_name, **kwargs)
        # - On failure, try next client (up to len(clients) attempts)
        # - If all fail, raise the last exception
        raise NotImplementedError

    @property
    def n_servers(self) -> int:
        """Number of servers in the pool."""
        return len(self.server_addresses)
