"""Serving configuration for the LLM inference server.

Defines operational parameters like batch sizes, timeouts, and
rate limiting.
"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class ServingConfig(BaseSettings):
    """Configuration for the serving layer.

    Attributes:
        host: Host address to bind the server to.
        port: Port number for the server.
        max_num_seqs: Maximum number of sequences in a batch.
        max_num_batched_tokens: Maximum tokens across all sequences in a batch.
        max_concurrent_requests: Maximum concurrent requests to accept.
        request_timeout: Timeout for a single request in seconds.
        enable_prefix_caching: Enable KV-cache sharing for common prefixes.
        enable_metrics: Enable Prometheus metrics endpoint.
        metrics_port: Port for the Prometheus metrics server.
        log_level: Logging level.
    """

    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)
    max_num_seqs: int = Field(default=256, ge=1)
    max_num_batched_tokens: int = Field(default=8192, ge=1)
    max_concurrent_requests: int = Field(default=100, ge=1)
    request_timeout: float = Field(default=60.0, ge=1.0, le=600.0)
    enable_prefix_caching: bool = False
    enable_metrics: bool = True
    metrics_port: int = Field(default=9090, ge=1, le=65535)
    log_level: str = "info"

    model_config = {"env_prefix": "SERVING_", "env_file": ".env"}

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level string."""
        # TODO: Implement
        # Allowed values: "debug", "info", "warning", "error", "critical"
        raise NotImplementedError

    @field_validator("max_num_batched_tokens")
    @classmethod
    def validate_batched_tokens(cls, v: int) -> int:
        """Validate max_num_batched_tokens is reasonable."""
        # TODO: Implement
        # Should be >= max_num_seqs (at least 1 token per sequence)
        raise NotImplementedError

    def to_uvicorn_kwargs(self) -> dict:
        """Convert to keyword arguments for uvicorn.run().

        Returns:
            Dict of uvicorn configuration.
        """
        # TODO: Implement
        # Map host, port, log_level to uvicorn kwargs
        raise NotImplementedError
