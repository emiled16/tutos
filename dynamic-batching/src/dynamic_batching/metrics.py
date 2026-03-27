"""Metrics collection for batch inference observability."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from dynamic_batching.request import Batch


@dataclass
class LatencyPercentiles:
    """Latency percentile summary.

    Attributes:
        p50: Median latency in milliseconds.
        p95: 95th percentile latency.
        p99: 99th percentile latency.
        mean: Mean latency.
        min: Minimum observed latency.
        max: Maximum observed latency.
    """

    p50: float = 0.0
    p95: float = 0.0
    p99: float = 0.0
    mean: float = 0.0
    min: float = 0.0
    max: float = 0.0


@dataclass
class MetricsSnapshot:
    """Point-in-time snapshot of all collected metrics.

    Attributes:
        total_requests: Total requests processed.
        total_batches: Total batches dispatched.
        avg_batch_size: Mean batch size.
        throughput_rps: Requests per second (measured over collection window).
        latency: Latency percentile summary.
        avg_padding_waste: Mean padding waste ratio.
        avg_queue_wait_ms: Mean time requests spent in the queue.
        gpu_utilization_estimate: Estimated fraction of time GPU is busy.
    """

    total_requests: int = 0
    total_batches: int = 0
    avg_batch_size: float = 0.0
    throughput_rps: float = 0.0
    latency: LatencyPercentiles = field(default_factory=LatencyPercentiles)
    avg_padding_waste: float = 0.0
    avg_queue_wait_ms: float = 0.0
    gpu_utilization_estimate: float = 0.0


class MetricsCollector:
    """Collects and aggregates serving metrics.

    Thread-safe within a single asyncio event loop (no locks needed for
    single-threaded async). Tracks per-request and per-batch statistics.

    Attributes:
        _batch_sizes: Recorded batch sizes.
        _wait_times_ms: Per-request queue wait times in milliseconds.
        _padding_wastes: Per-batch padding waste ratios.
        _latencies_ms: Per-request end-to-end latencies in milliseconds.
        _start_time: When this collector started recording.
        _total_requests: Running request count.
        _total_batches: Running batch count.
        _gpu_busy_ms: Estimated total GPU busy time.
    """

    def __init__(self) -> None:
        self._batch_sizes: list[int] = []
        self._wait_times_ms: list[float] = []
        self._padding_wastes: list[float] = []
        self._latencies_ms: list[float] = []
        self._start_time: float = time.monotonic()
        self._total_requests: int = 0
        self._total_batches: int = 0
        self._gpu_busy_ms: float = 0.0

    def record_batch(self, batch: Batch, results: list[Any]) -> None:
        """Record metrics for a completed batch.

        Args:
            batch: The completed batch.
            results: The inference results (used to confirm completion).
        """
        # TODO: Implement batch metric recording:
        #   1. Record batch.size in _batch_sizes
        #   2. Compute and record padding waste via batch.compute_padding_waste()
        #   3. For each request, compute wait_time = formed_at - request.created_at
        #   4. Append wait times to _wait_times_ms (converted to ms)
        #   5. Update _total_requests and _total_batches
        pass

    def record_latency(self, request_id: str, latency_ms: float) -> None:
        """Record end-to-end latency for a single request.

        Args:
            request_id: The request this latency measurement belongs to.
            latency_ms: Total time from submission to response, in milliseconds.
        """
        # TODO: Implement latency recording
        pass

    def record_gpu_time(self, duration_ms: float) -> None:
        """Record GPU execution time for utilization estimation.

        Args:
            duration_ms: How long the GPU was busy for this batch, in milliseconds.
        """
        # TODO: Implement GPU time recording
        pass

    def compute_percentiles(self, values: list[float]) -> LatencyPercentiles:
        """Compute latency percentiles from a list of values.

        Args:
            values: Raw latency measurements.

        Returns:
            LatencyPercentiles with p50, p95, p99, mean, min, max.
        """
        # TODO: Implement percentile computation:
        #   Use sorted list or numpy for percentile calculation
        #   Handle empty list edge case (return zeroed LatencyPercentiles)
        pass

    def snapshot(self) -> MetricsSnapshot:
        """Produce a point-in-time metrics snapshot.

        Returns:
            MetricsSnapshot with all aggregated metrics.
        """
        # TODO: Implement snapshot generation:
        #   1. Compute avg_batch_size from _batch_sizes
        #   2. Compute throughput_rps = _total_requests / elapsed_seconds
        #   3. Compute latency percentiles from _latencies_ms
        #   4. Compute avg_padding_waste and avg_queue_wait_ms
        #   5. Estimate GPU utilization = _gpu_busy_ms / total_elapsed_ms
        #   6. Return MetricsSnapshot
        pass

    def reset(self) -> None:
        """Reset all collected metrics."""
        # TODO: Implement reset — clear all lists and counters, reset _start_time
        pass
