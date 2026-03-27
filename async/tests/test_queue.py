"""Tests for the priority async queue."""

from __future__ import annotations

import asyncio

import numpy as np
import pytest

from async_engine.inference import InferenceRequest
from async_engine.queue import Priority, PriorityInferenceQueue


def _make_request(request_id: str = "test-1") -> InferenceRequest:
    """Helper to create a test InferenceRequest."""
    return InferenceRequest(
        request_id=request_id,
        input_data=np.zeros(128),
    )


class TestEnqueue:
    """Tests for enqueue behavior."""

    async def test_enqueue_single_request(self) -> None:
        """Should successfully enqueue a request."""
        # TODO: Implement test.
        # q = PriorityInferenceQueue(max_size=10)
        # await q.enqueue(_make_request())
        # assert q.size == 1
        raise NotImplementedError

    async def test_enqueue_raises_when_full(self) -> None:
        """Should raise QueueFull when at max capacity."""
        # TODO: Implement test.
        # q = PriorityInferenceQueue(max_size=2)
        # Fill the queue, then verify the next enqueue raises QueueFull
        raise NotImplementedError

    async def test_enqueue_tracks_count(self) -> None:
        """Stats should reflect total enqueued count."""
        # TODO: Implement test.
        raise NotImplementedError


class TestDequeue:
    """Tests for dequeue behavior."""

    async def test_dequeue_returns_request(self) -> None:
        """Should return the enqueued request."""
        # TODO: Implement test.
        raise NotImplementedError

    async def test_dequeue_blocks_when_empty(self) -> None:
        """Dequeue should block until a request is available."""
        # TODO: Implement test.
        # 1. Create empty queue
        # 2. Start dequeue in a task
        # 3. Verify it hasn't completed after short sleep
        # 4. Enqueue a request
        # 5. Verify dequeue completes
        raise NotImplementedError

    async def test_dequeue_nowait_returns_none(self) -> None:
        """Non-blocking dequeue should return None on empty queue."""
        # TODO: Implement test.
        raise NotImplementedError


class TestPriority:
    """Tests for priority ordering."""

    async def test_high_priority_first(self) -> None:
        """HIGH priority requests should be dequeued before NORMAL."""
        # TODO: Implement test.
        # 1. Enqueue a NORMAL request
        # 2. Enqueue a HIGH request
        # 3. Dequeue and verify the HIGH request comes first
        raise NotImplementedError

    async def test_fifo_within_same_priority(self) -> None:
        """Requests with the same priority should be dequeued in FIFO order."""
        # TODO: Implement test.
        # 1. Enqueue request "a", then "b", then "c", all NORMAL
        # 2. Dequeue and verify order is a, b, c
        raise NotImplementedError

    async def test_all_priority_levels(self) -> None:
        """Should correctly order across all priority levels."""
        # TODO: Implement test.
        # Enqueue LOW, NORMAL, HIGH in mixed order
        # Verify dequeue order is HIGH, NORMAL, LOW
        raise NotImplementedError


class TestBackpressure:
    """Tests for backpressure behavior."""

    async def test_rejects_when_full(self) -> None:
        """Queue should reject new requests when at capacity."""
        # TODO: Implement test.
        raise NotImplementedError

    async def test_rejected_count_in_stats(self) -> None:
        """Stats should track the number of rejected requests."""
        # TODO: Implement test.
        raise NotImplementedError

    async def test_accepts_after_dequeue(self) -> None:
        """Queue should accept requests again after items are dequeued."""
        # TODO: Implement test.
        raise NotImplementedError


class TestQueueStats:
    """Tests for queue statistics."""

    async def test_initial_stats(self) -> None:
        """Fresh queue should have zero counts."""
        # TODO: Implement test.
        raise NotImplementedError

    async def test_stats_after_operations(self) -> None:
        """Stats should accurately reflect enqueue/dequeue operations."""
        # TODO: Implement test.
        raise NotImplementedError
