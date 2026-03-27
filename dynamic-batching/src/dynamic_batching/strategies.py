"""Batching strategies that determine when and how to form batches."""

from __future__ import annotations

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Protocol

from dynamic_batching.config import BatcherConfig
from dynamic_batching.request import Batch, InferenceRequest


class BatchingStrategy(Protocol):
    """Protocol defining the interface for all batching strategies.

    A strategy decides when a batch is ready to dispatch and may transform
    how requests are grouped.
    """

    async def add_request(self, request: InferenceRequest) -> None:
        """Add a request to the pending pool."""
        ...

    async def wait_for_batch(self) -> Batch:
        """Block until a batch is ready, then return it."""
        ...

    async def shutdown(self) -> list[InferenceRequest]:
        """Gracefully shut down, returning any undispatched requests."""
        ...


class NaiveBatcher(ABC):
    """Fixed-timeout batching strategy.

    Waits up to `max_wait_ms` for requests to accumulate, dispatching
    when either the timeout expires or `max_batch_size` is reached.

    Attributes:
        config: Batcher configuration.
        _queue: Internal buffer of pending requests.
        _batch_event: Asyncio event signalling that a batch threshold was hit.
    """

    def __init__(self, config: BatcherConfig) -> None:
        self.config = config
        self._queue: list[InferenceRequest] = []
        self._batch_event = asyncio.Event()

    async def add_request(self, request: InferenceRequest) -> None:
        """Add a request and signal if max_batch_size is reached.

        Args:
            request: The incoming inference request.
        """
        # TODO: Implement request addition:
        #   1. Append request to _queue
        #   2. If len(_queue) >= config.max_batch_size, set _batch_event
        pass

    async def wait_for_batch(self) -> Batch:
        """Wait for a batch to be ready (timeout or full) and return it.

        Uses asyncio.wait_for to implement the timeout. When triggered by either
        condition, drains up to max_batch_size requests from the queue into a Batch.

        Returns:
            A Batch containing the accumulated requests.
        """
        # TODO: Implement batch formation:
        #   1. Wait for _batch_event with timeout = max_wait_ms / 1000
        #   2. On timeout (asyncio.TimeoutError), proceed anyway (dispatch partial batch)
        #   3. Drain min(len(_queue), max_batch_size) requests from _queue
        #   4. Clear _batch_event
        #   5. Compute max_sequence_length across the batch
        #   6. Return a Batch with the drained requests
        pass

    async def shutdown(self) -> list[InferenceRequest]:
        """Return all undispatched requests for graceful shutdown."""
        # TODO: Implement shutdown — drain and return remaining requests
        pass


class AdaptiveBatcher:
    """Adaptive-timeout batching strategy.

    Adjusts the wait timeout based on an exponential moving average (EMA) of
    inter-arrival times. Under high load, the timeout shrinks (batches fill fast).
    Under low load, it grows (to accumulate more requests).

    Attributes:
        config: Batcher configuration.
        _queue: Internal buffer of pending requests.
        _batch_event: Asyncio event for batch threshold signalling.
        _last_arrival: Timestamp of the most recent request arrival.
        _ema_interval: Smoothed inter-arrival interval (seconds).
        _current_timeout: Dynamically computed timeout (seconds).
    """

    def __init__(self, config: BatcherConfig) -> None:
        self.config = config
        self._queue: list[InferenceRequest] = []
        self._batch_event = asyncio.Event()
        self._last_arrival: float | None = None
        self._ema_interval: float = config.max_wait_ms / 1000.0
        self._current_timeout: float = config.max_wait_ms / 1000.0

    async def add_request(self, request: InferenceRequest) -> None:
        """Add a request and update the adaptive timeout estimate.

        Args:
            request: The incoming inference request.
        """
        # TODO: Implement adaptive request addition:
        #   1. Compute inter-arrival interval since _last_arrival
        #   2. Update _ema_interval = alpha * interval + (1 - alpha) * _ema_interval
        #   3. Recompute _current_timeout = clamp(_ema_interval * some_factor, min_wait, max_wait)
        #   4. Update _last_arrival timestamp
        #   5. Append request to _queue
        #   6. Signal _batch_event if max_batch_size reached
        pass

    async def wait_for_batch(self) -> Batch:
        """Wait using the adaptive timeout and return the formed batch.

        Returns:
            A Batch with accumulated requests.
        """
        # TODO: Implement batch formation using _current_timeout instead of fixed timeout
        #   Same flow as NaiveBatcher.wait_for_batch but with dynamic timeout
        pass

    async def shutdown(self) -> list[InferenceRequest]:
        """Return all undispatched requests."""
        # TODO: Implement shutdown
        pass


class PaddingAwareBatcher:
    """Padding-aware batching strategy.

    Groups requests into buckets by sequence length, maintaining a separate
    batch queue per bucket. This minimizes padding waste at the cost of
    potentially higher latency for uncommon lengths.

    Attributes:
        config: Batcher configuration.
        _buckets: Mapping of bucket boundary → list of queued requests.
        _bucket_events: Per-bucket asyncio events.
    """

    def __init__(self, config: BatcherConfig) -> None:
        self.config = config
        boundaries = sorted(config.bucket_boundaries)
        self._buckets: dict[int, list[InferenceRequest]] = {b: [] for b in boundaries}
        self._bucket_events: dict[int, asyncio.Event] = {b: asyncio.Event() for b in boundaries}
        self._global_event = asyncio.Event()

    def _find_bucket(self, sequence_length: int) -> int:
        """Find the appropriate bucket for a given sequence length.

        Args:
            sequence_length: Length of the input sequence.

        Returns:
            The bucket boundary to assign this request to.
        """
        # TODO: Implement bucket lookup — find smallest boundary >= sequence_length,
        #   use the largest boundary for overflow
        pass

    async def add_request(self, request: InferenceRequest) -> None:
        """Add a request to the appropriate length bucket.

        Args:
            request: The incoming inference request.
        """
        # TODO: Implement bucketed request addition:
        #   1. Find the right bucket via _find_bucket
        #   2. Append to that bucket's queue
        #   3. Signal bucket event if bucket reaches max_batch_size
        #   4. Signal _global_event so wait_for_batch wakes up
        pass

    async def wait_for_batch(self) -> Batch:
        """Wait for any bucket to be ready and return its batch.

        Checks all buckets for fullness. Uses a global timeout to flush
        the largest partial bucket if no bucket fills in time.

        Returns:
            A Batch from the first ready bucket.
        """
        # TODO: Implement multi-bucket batch formation:
        #   1. Check if any bucket has >= max_batch_size requests, drain it immediately
        #   2. Otherwise wait on _global_event with timeout
        #   3. On timeout, flush the bucket with the most pending requests
        #   4. Return the formed Batch
        pass

    async def shutdown(self) -> list[InferenceRequest]:
        """Return all undispatched requests across all buckets."""
        # TODO: Implement shutdown — collect remaining requests from all buckets
        pass


class PriorityBatcher:
    """Priority-aware batching strategy.

    Maintains a priority queue of requests. High-priority requests trigger
    faster batch dispatch (shorter effective timeout). The batch is formed
    from the highest-priority requests first.

    Attributes:
        config: Batcher configuration.
        _queue: Priority-sorted request buffer.
        _batch_event: Asyncio event for signalling.
    """

    def __init__(self, config: BatcherConfig) -> None:
        self.config = config
        self._queue: list[InferenceRequest] = []
        self._batch_event = asyncio.Event()

    def _effective_timeout(self) -> float:
        """Compute timeout based on the highest-priority request in the queue.

        High-priority requests reduce the timeout to ensure faster dispatch.

        Returns:
            Timeout in seconds.
        """
        # TODO: Implement priority-based timeout calculation:
        #   HIGH priority → max_wait_ms * 0.25
        #   NORMAL priority → max_wait_ms * 0.5
        #   LOW priority → max_wait_ms * 1.0
        #   Use the highest priority (lowest value) in the queue
        pass

    async def add_request(self, request: InferenceRequest) -> None:
        """Add a request maintaining priority order.

        Args:
            request: The incoming inference request.
        """
        # TODO: Implement priority-ordered insertion:
        #   1. Insert request into _queue maintaining sort by priority (ascending)
        #   2. Signal _batch_event if max_batch_size reached
        pass

    async def wait_for_batch(self) -> Batch:
        """Wait using priority-adjusted timeout and return the batch.

        Returns:
            A Batch with requests ordered by priority.
        """
        # TODO: Implement priority-aware batch formation:
        #   1. Compute effective timeout via _effective_timeout()
        #   2. Wait for _batch_event with the effective timeout
        #   3. Drain up to max_batch_size requests (already priority-sorted)
        #   4. Return Batch
        pass

    async def shutdown(self) -> list[InferenceRequest]:
        """Return all undispatched requests."""
        # TODO: Implement shutdown
        pass


def create_strategy(config: BatcherConfig) -> BatchingStrategy:
    """Factory function to instantiate the configured batching strategy.

    Args:
        config: Batcher configuration specifying which strategy to use.

    Returns:
        An instance implementing the BatchingStrategy protocol.

    Raises:
        ValueError: If the configured strategy name is unknown.
    """
    # TODO: Implement strategy factory using match statement:
    #   match config.batching_strategy:
    #       case BatchingStrategyName.NAIVE: return NaiveBatcher(config)
    #       case BatchingStrategyName.ADAPTIVE: return AdaptiveBatcher(config)
    #       case BatchingStrategyName.PADDING_AWARE: return PaddingAwareBatcher(config)
    #       case BatchingStrategyName.PRIORITY: return PriorityBatcher(config)
    #       case _: raise ValueError(...)
    pass
