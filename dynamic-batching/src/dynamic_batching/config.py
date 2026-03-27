"""Configuration via pydantic-settings with environment variable support."""

from __future__ import annotations

from enum import StrEnum

from pydantic_settings import BaseSettings


class PaddingStrategy(StrEnum):
    """Available padding strategies."""

    NONE = "none"
    PAD_TO_MAX = "pad_to_max"
    BUCKET = "bucket"
    SORT_AND_PAD = "sort_and_pad"


class BatchingStrategyName(StrEnum):
    """Available batching strategy names."""

    NAIVE = "naive"
    ADAPTIVE = "adaptive"
    PADDING_AWARE = "padding_aware"
    PRIORITY = "priority"


class BatcherConfig(BaseSettings):
    """Configuration for the dynamic batcher.

    All values can be overridden via environment variables (case-insensitive).

    Attributes:
        max_batch_size: Maximum number of requests per batch.
        max_wait_ms: Maximum time (ms) to wait before dispatching an incomplete batch.
        model_name: Name/identifier of the model being served.
        log_level: Logging level.
        batching_strategy: Which batching strategy to use.
        padding_strategy: Which padding strategy to use.
        adaptive_alpha: EMA smoothing factor for adaptive timeout (0 < α ≤ 1).
        adaptive_min_wait_ms: Floor for adaptive timeout.
        adaptive_max_wait_ms: Ceiling for adaptive timeout.
        bucket_boundaries: Sequence length boundaries for bucket-based padding.
        executor_latency_ms: Simulated GPU inference latency per batch (ms).
        max_queue_depth: Maximum pending requests before rejecting new ones (backpressure).
        server_host: Host to bind the FastAPI server.
        server_port: Port to bind the FastAPI server.
    """

    max_batch_size: int = 32
    max_wait_ms: float = 50.0
    model_name: str = "mock-bert-base"
    log_level: str = "INFO"
    batching_strategy: BatchingStrategyName = BatchingStrategyName.NAIVE
    padding_strategy: PaddingStrategy = PaddingStrategy.PAD_TO_MAX
    adaptive_alpha: float = 0.3
    adaptive_min_wait_ms: float = 5.0
    adaptive_max_wait_ms: float = 100.0
    bucket_boundaries: list[int] = [16, 32, 64, 128, 256]
    executor_latency_ms: float = 10.0
    max_queue_depth: int = 1000
    server_host: str = "0.0.0.0"
    server_port: int = 8000

    model_config = {"env_prefix": "", "case_sensitive": False}
