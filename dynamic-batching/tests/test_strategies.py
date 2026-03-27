"""Tests for batching strategies."""

from __future__ import annotations

import asyncio

import pytest

from dynamic_batching.config import BatcherConfig, BatchingStrategyName
from dynamic_batching.request import InferenceRequest, Priority
from dynamic_batching.strategies import (
    AdaptiveBatcher,
    NaiveBatcher,
    PaddingAwareBatcher,
    PriorityBatcher,
    create_strategy,
)


@pytest.fixture
def config() -> BatcherConfig:
    return BatcherConfig(
        max_batch_size=4,
        max_wait_ms=50,
        adaptive_alpha=0.3,
        adaptive_min_wait_ms=5,
        adaptive_max_wait_ms=100,
        bucket_boundaries=[8, 16, 32, 64],
    )


def make_request(
    seq_len: int = 10,
    priority: Priority = Priority.NORMAL,
) -> InferenceRequest:
    """Helper to create a test request with specified properties."""
    return InferenceRequest(
        payload=[1.0] * seq_len,
        sequence_length=seq_len,
        priority=priority,
    )


class TestNaiveBatcher:
    """Tests for NaiveBatcher strategy."""

    async def test_dispatches_on_max_size(self, config: BatcherConfig) -> None:
        """Batch dispatches immediately when max_batch_size reached."""
        # TODO: Implement test:
        #   1. Create NaiveBatcher
        #   2. Add max_batch_size requests
        #   3. Call wait_for_batch (should return immediately)
        #   4. Assert batch.size == max_batch_size
        pass

    async def test_dispatches_on_timeout(self, config: BatcherConfig) -> None:
        """Partial batch dispatches after timeout."""
        # TODO: Implement test:
        #   1. Create NaiveBatcher
        #   2. Add 2 requests (less than max_batch_size)
        #   3. Call wait_for_batch
        #   4. Assert it returns within ~max_wait_ms
        #   5. Assert batch.size == 2
        pass

    async def test_preserves_request_order(self, config: BatcherConfig) -> None:
        """Requests should appear in the batch in FIFO order."""
        # TODO: Implement test
        pass


class TestAdaptiveBatcher:
    """Tests for AdaptiveBatcher strategy."""

    async def test_timeout_shrinks_under_high_load(self, config: BatcherConfig) -> None:
        """Adaptive timeout should decrease when requests arrive rapidly."""
        # TODO: Implement test:
        #   1. Create AdaptiveBatcher
        #   2. Send requests in rapid succession (< 1ms apart)
        #   3. Assert _current_timeout has decreased from initial value
        pass

    async def test_timeout_grows_under_low_load(self, config: BatcherConfig) -> None:
        """Adaptive timeout should increase when requests arrive slowly."""
        # TODO: Implement test:
        #   1. Create AdaptiveBatcher with short initial timeout
        #   2. Send requests with long gaps (> max_wait_ms apart)
        #   3. Assert _current_timeout has increased
        pass

    async def test_ema_smoothing(self, config: BatcherConfig) -> None:
        """EMA should smooth out individual spikes in arrival rate."""
        # TODO: Implement test:
        #   1. Send requests at steady rate, then one outlier gap
        #   2. Assert timeout doesn't jump dramatically from one outlier
        pass


class TestPaddingAwareBatcher:
    """Tests for PaddingAwareBatcher strategy."""

    async def test_groups_similar_lengths(self, config: BatcherConfig) -> None:
        """Requests with similar sequence lengths should be batched together."""
        # TODO: Implement test:
        #   1. Add requests with lengths [5, 7, 6, 50, 55, 48]
        #   2. First batch should contain the short sequences (bucket ≤ 8)
        #   3. Assert all requests in the batch have similar lengths
        pass

    async def test_bucket_assignment(self, config: BatcherConfig) -> None:
        """Requests should be assigned to the correct length bucket."""
        # TODO: Implement test:
        #   1. Create PaddingAwareBatcher with boundaries [8, 16, 32]
        #   2. Test _find_bucket with various lengths
        #   3. Assert length=5 → bucket 8, length=12 → bucket 16, length=30 → bucket 32
        pass

    async def test_overflow_bucket(self, config: BatcherConfig) -> None:
        """Sequences longer than the largest bucket should still be batched."""
        # TODO: Implement test
        pass

    async def test_flushes_largest_bucket_on_timeout(
        self, config: BatcherConfig
    ) -> None:
        """On timeout, the bucket with the most pending requests should flush."""
        # TODO: Implement test
        pass


class TestPriorityBatcher:
    """Tests for PriorityBatcher strategy."""

    async def test_high_priority_dispatches_faster(self, config: BatcherConfig) -> None:
        """High-priority requests should trigger shorter effective timeout."""
        # TODO: Implement test:
        #   1. Create PriorityBatcher
        #   2. Add a HIGH priority request
        #   3. Assert _effective_timeout() is significantly less than max_wait_ms
        pass

    async def test_priority_ordering_in_batch(self, config: BatcherConfig) -> None:
        """Batch should contain requests ordered by priority (high first)."""
        # TODO: Implement test:
        #   1. Add requests with LOW, HIGH, NORMAL priorities
        #   2. Wait for batch
        #   3. Assert batch.requests[0].priority == HIGH
        pass

    async def test_low_priority_uses_full_timeout(self, config: BatcherConfig) -> None:
        """All-low-priority queue should use the full timeout."""
        # TODO: Implement test
        pass


class TestStrategyFactory:
    """Tests for the create_strategy factory function."""

    def test_creates_naive_strategy(self, config: BatcherConfig) -> None:
        """Factory should create NaiveBatcher for NAIVE config."""
        # TODO: Implement test
        pass

    def test_creates_adaptive_strategy(self, config: BatcherConfig) -> None:
        """Factory should create AdaptiveBatcher for ADAPTIVE config."""
        # TODO: Implement test
        pass

    def test_creates_padding_aware_strategy(self, config: BatcherConfig) -> None:
        """Factory should create PaddingAwareBatcher for PADDING_AWARE config."""
        # TODO: Implement test
        pass

    def test_creates_priority_strategy(self, config: BatcherConfig) -> None:
        """Factory should create PriorityBatcher for PRIORITY config."""
        # TODO: Implement test
        pass

    def test_unknown_strategy_raises(self, config: BatcherConfig) -> None:
        """Factory should raise ValueError for unknown strategy name."""
        # TODO: Implement test
        pass
