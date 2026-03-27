"""Priority async queue with backpressure for inference requests."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any

from async_engine.inference import InferenceRequest


class Priority(IntEnum):
    """Request priority levels. Lower value = higher priority."""

    HIGH = 0
    NORMAL = 1
    LOW = 2


@dataclass(order=True)
class PrioritizedRequest:
    """Wrapper that makes InferenceRequest comparable for priority queue ordering.

    Attributes:
        priority: Request priority (lower = higher priority).
        sequence: Insertion order for FIFO within same priority.
        request: The actual inference request (excluded from comparison).
    """

    priority: int
    sequence: int
    request: InferenceRequest = field(compare=False)


class PriorityInferenceQueue:
    """Async priority queue with bounded capacity and backpressure.

    Requests are dequeued in priority order (highest first), with FIFO
    ordering within the same priority level. When the queue reaches
    max_size, new requests are rejected (backpressure).

    Attributes:
        max_size: Maximum number of requests in the queue.
    """

    def __init__(self, max_size: int = 1000) -> None:
        """Initialize the priority queue.

        Args:
            max_size: Maximum queue capacity. When full, enqueue raises QueueFull.
        """
        # TODO: Implement initialization.
        # - Store max_size
        # - Create an asyncio.PriorityQueue(maxsize=max_size)
        # - Initialize a sequence counter for FIFO ordering
        # - Initialize tracking counters (enqueued, dequeued, rejected)
        raise NotImplementedError

    async def enqueue(
        self,
        request: InferenceRequest,
        priority: Priority = Priority.NORMAL,
    ) -> None:
        """Add a request to the queue.

        Args:
            request: The inference request to enqueue.
            priority: Priority level for the request.

        Raises:
            asyncio.QueueFull: If the queue is at maximum capacity.
        """
        # TODO: Implement enqueue with backpressure.
        # 1. Create a PrioritizedRequest with the current sequence number
        # 2. Increment the sequence counter
        # 3. Try put_nowait on the priority queue
        # 4. If QueueFull, increment rejected counter and re-raise
        # 5. Increment enqueued counter
        raise NotImplementedError

    async def dequeue(self) -> InferenceRequest:
        """Remove and return the highest-priority request.

        Blocks until a request is available.

        Returns:
            The next InferenceRequest to process.
        """
        # TODO: Implement dequeue.
        # 1. await self._queue.get()
        # 2. Unwrap the PrioritizedRequest to get the InferenceRequest
        # 3. Increment dequeued counter
        # 4. Return the request
        raise NotImplementedError

    def dequeue_nowait(self) -> InferenceRequest | None:
        """Non-blocking dequeue. Returns None if queue is empty.

        Returns:
            The next InferenceRequest, or None if queue is empty.
        """
        # TODO: Implement non-blocking dequeue.
        raise NotImplementedError

    @property
    def size(self) -> int:
        """Current number of requests in the queue."""
        # TODO: Return current queue size.
        raise NotImplementedError

    @property
    def is_full(self) -> bool:
        """Whether the queue is at maximum capacity."""
        # TODO: Implement full check.
        raise NotImplementedError

    @property
    def is_empty(self) -> bool:
        """Whether the queue is empty."""
        # TODO: Implement empty check.
        raise NotImplementedError

    def stats(self) -> dict[str, int]:
        """Return queue statistics.

        Returns:
            Dictionary with current_size, max_size, total_enqueued,
            total_dequeued, total_rejected.
        """
        # TODO: Implement stats collection.
        raise NotImplementedError
