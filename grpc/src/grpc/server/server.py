"""gRPC server setup and lifecycle management."""

from __future__ import annotations

import logging
import os
import signal
from concurrent import futures

import grpc

from grpc.server.health import HealthServicer
from grpc.server.interceptors import (
    AuthenticationInterceptor,
    LoggingInterceptor,
    RateLimitInterceptor,
)
from grpc.server.model_manager import ModelManager
from grpc.server.servicer import PredictServicer

logger = logging.getLogger(__name__)


def create_server(
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 4,
    api_key: str | None = None,
    model_dir: str = "models/",
    enable_reflection: bool = True,
) -> grpc.Server:
    """Create and configure a gRPC server with all services and interceptors.

    Args:
        host: Server bind address.
        port: Server bind port.
        max_workers: Maximum thread pool workers.
        api_key: API key for authentication. If None, auth is disabled.
        model_dir: Directory containing model files.
        enable_reflection: Enable gRPC server reflection for debugging.

    Returns:
        Configured but not-yet-started gRPC Server.
    """
    # TODO: Implement
    # - Create interceptors list: [LoggingInterceptor()]
    # - If api_key, add AuthenticationInterceptor(api_key)
    # - Add RateLimitInterceptor()
    # - Create server with grpc.server(futures.ThreadPoolExecutor, interceptors)
    # - Initialize ModelManager and load models from model_dir
    # - Create PredictServicer(model_manager) and register with server
    # - Create HealthServicer and register with server
    # - If enable_reflection, enable server reflection
    # - Add insecure port f"{host}:{port}"
    # - Return the server
    raise NotImplementedError


def serve(
    host: str | None = None,
    port: int | None = None,
) -> None:
    """Start the gRPC server and block until shutdown.

    Reads configuration from environment variables with fallbacks.
    Sets up graceful shutdown on SIGINT/SIGTERM.

    Args:
        host: Override for server host.
        port: Override for server port.
    """
    # TODO: Implement
    # - Read host from arg → GRPC_SERVER_HOST env → "localhost"
    # - Read port from arg → GRPC_SERVER_PORT env → 50051
    # - Read api_key from GRPC_API_KEY env
    # - Read model_dir from MODEL_DIR env → "models/"
    # - Read max_workers from MAX_WORKERS env → 4
    # - Create server with create_server(...)
    # - Start server
    # - Register signal handlers for graceful shutdown:
    #   signal.signal(SIGINT, handler) → server.stop(grace=5)
    # - server.wait_for_termination()
    raise NotImplementedError


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
