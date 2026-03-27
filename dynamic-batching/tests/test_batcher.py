"""Tests for the core DynamicBatcher logic."""

from __future__ import annotations

import asyncio

import pytest

from dynamic_batching.batcher import DynamicBatcher
from dynamic_batching.config import BatcherConfig
from dynamic_batching.executor import BatchExecutor
from dynamic_batching.metrics import MetricsCollector
from dynamic_batching.request import InferenceRequest


@pytest.fixture
def config() -> BatcherConfig:
    """Default batcher configuration for tests."""
    return BatcherConfig(
        max_batch_size=4,
        max_wait_ms=50,
        executor_latency_ms=5,
    )


@pytest.fixture
def executor(config: BatcherConfig) -> BatchExecutor:
    return BatchExecutor(config)


@pytest.fixture
def metrics() -> MetricsCollector:
    return MetricsCollector()


@pytest.fixture
def batcher(
    config: BatcherConfig,
    executor: BatchExecutor,
    metrics: MetricsCollector,
) -> DynamicBatcher:
    return DynamicBatcher(config=config, executor=executor, metrics=metrics)


class TestBatchFormation:
    """Tests for batch formation triggers."""

    async def test_batch_forms_when_max_size_reached(
        self, batcher: DynamicBatcher
    ) -> None:
        """Batch should dispatch immediately when max_batch_size requests arrive."""
        # TODO: Implement test:
        #   1. Start the batcher
        #   2. Submit max_batch_size requests concurrently
        #   3. Assert all responses are received
        #   4. Assert each response has batch_size == max_batch_size
        #   5. Stop the batcher
        pass

    async def test_batch_forms_on_timeout(
        self, batcher: DynamicBatcher, config: BatcherConfig
    ) -> None:
        """Partial batch should dispatch after timeout expires."""
        # TODO: Implement test:
        #   1. Start the batcher
        #   2. Submit fewer than max_batch_size requests
        #   3. Assert responses arrive within ~max_wait_ms + executor_latency_ms
        #   4. Assert batch_size < max_batch_size
        #   5. Stop the batcher
        pass

    async def test_empty_batch_not_dispatched(
        self, batcher: DynamicBatcher
    ) -> None:
        """No batch should be dispatched if no requests arrive."""
        # TODO: Implement test:
        #   1. Start the batcher
        #   2. Wait for 2× max_wait_ms
        #   3. Assert executor has processed 0 batches
        #   4. Stop the batcher
        pass

    async def test_single_request_batch(
        self, batcher: DynamicBatcher
    ) -> None:
        """A single request should form a batch of size 1 after timeout."""
        # TODO: Implement test:
        #   1. Start the batcher
        #   2. Submit exactly 1 request
        #   3. Assert response batch_size == 1
        #   4. Stop the batcher
        pass


class TestBatcherLifecycle:
    """Tests for batcher start/stop lifecycle."""

    async def test_submit_before_start_raises(
        self, batcher: DynamicBatcher
    ) -> None:
        """Submitting to a stopped batcher should raise RuntimeError."""
        # TODO: Implement test:
        #   1. Do NOT start the batcher
        #   2. Submit a request
        #   3. Assert RuntimeError is raised
        pass

    async def test_graceful_shutdown(
        self, batcher: DynamicBatcher
    ) -> None:
        """Shutdown should process or return pending requests."""
        # TODO: Implement test:
        #   1. Start the batcher
        #   2. Submit a few requests (don't await immediately)
        #   3. Stop the batcher
        #   4. Assert all futures are resolved or cancelled
        pass

    async def test_backpressure_rejects_when_full(self) -> None:
        """Requests should be rejected when queue depth exceeds limit."""
        # TODO: Implement test:
        #   1. Create config with max_queue_depth=5
        #   2. Start the batcher
        #   3. Submit more than 5 requests without allowing batch dispatch
        #   4. Assert later submissions raise an appropriate error
        pass


class TestResponseCorrectness:
    """Tests for response content and metadata."""

    async def test_response_contains_request_id(
        self, batcher: DynamicBatcher
    ) -> None:
        """Each response should carry the correct request_id."""
        # TODO: Implement test:
        #   1. Start the batcher
        #   2. Submit a request with a known request_id
        #   3. Assert response.request_id matches
        #   4. Stop the batcher
        pass

    async def test_wait_time_is_positive(
        self, batcher: DynamicBatcher
    ) -> None:
        """Response wait_time_ms should be > 0."""
        # TODO: Implement test
        pass

    async def test_multiple_batches_sequential(
        self, batcher: DynamicBatcher, config: BatcherConfig
    ) -> None:
        """Multiple batches should form sequentially under steady load."""
        # TODO: Implement test:
        #   1. Start the batcher
        #   2. Submit 2× max_batch_size requests in rapid succession
        #   3. Assert all responses received
        #   4. Assert at least 2 batches were executed
        #   5. Stop the batcher
        pass
