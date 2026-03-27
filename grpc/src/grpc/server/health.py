"""gRPC health checking service implementation."""

from __future__ import annotations

import logging
from enum import Enum
from threading import Lock

import grpc

logger = logging.getLogger(__name__)


class ServingStatus(str, Enum):
    """Health status of a service."""

    UNKNOWN = "UNKNOWN"
    SERVING = "SERVING"
    NOT_SERVING = "NOT_SERVING"
    SERVICE_UNKNOWN = "SERVICE_UNKNOWN"


class HealthServicer:
    """Implements the gRPC Health checking protocol.

    Tracks the health status of individual services and the overall server.
    Supports both Check (unary) and Watch (streaming) RPCs.
    """

    def __init__(self) -> None:
        self._status: dict[str, ServingStatus] = {}
        self._lock = Lock()
        self.set_status("", ServingStatus.SERVING)

    def set_status(self, service: str, status: ServingStatus) -> None:
        """Set the health status for a service.

        Args:
            service: Service name. Empty string for the overall server.
            status: The health status to set.
        """
        # TODO: Implement
        # - Acquire lock
        # - Set self._status[service] = status
        # - Log the status change
        raise NotImplementedError

    def get_status(self, service: str = "") -> ServingStatus:
        """Get the health status for a service.

        Args:
            service: Service name. Empty string for the overall server.

        Returns:
            Current ServingStatus, or SERVICE_UNKNOWN if not registered.
        """
        # TODO: Implement
        # - Acquire lock
        # - Return self._status.get(service, ServingStatus.SERVICE_UNKNOWN)
        raise NotImplementedError

    def Check(self, request, context: grpc.ServicerContext):
        """Handle a health check request (unary).

        Args:
            request: HealthCheckRequest with service name.
            context: gRPC servicer context.

        Returns:
            HealthCheckResponse with the current status.
        """
        # TODO: Implement
        # - Get status for request.service
        # - If SERVICE_UNKNOWN, abort with NOT_FOUND
        # - Return HealthCheckResponse with the status
        raise NotImplementedError

    def Watch(self, request, context: grpc.ServicerContext):
        """Stream health status changes for a service.

        Args:
            request: HealthCheckRequest with service name.
            context: gRPC servicer context.

        Yields:
            HealthCheckResponse whenever the status changes.
        """
        # TODO: Implement
        # - Get initial status and yield it
        # - Poll for status changes (or use an event-based approach)
        # - Yield new status when it changes
        # - Stop when context is cancelled
        raise NotImplementedError
