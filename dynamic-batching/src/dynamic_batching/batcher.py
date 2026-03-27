"""Core DynamicBatcher that accumulates requests and dispatches batches."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from dynamic_batching.config import BatcherConfig
from dynamic_batching.executor import BatchExecutor
from dynamic_batching.metrics import MetricsCollector
from dynamic_batching.request import Batch, InferenceRequest, InferenceResponse
from dynamic_batching.strategies import BatchingStrategy, create_strategy

logger = logging.getLogger(__name__)


class DynamicBatcher:
    """Orchestrates request batching, execution, and response routing.

    The batcher runs as an asyncio background task. Callers submit requests
    via `submit()` and receive a Future that resolves when the batch containing
    their request completes inference.

    Attributes:
        config: Batcher configuration.
        strategy: The batching strategy in use.
        executor: The batch executor for running inference.
        metrics: Metrics collector for observability.
        _futures: Mapping of request_id → asyncio.Future for response delivery.
        _batch_loop_task: Background task running the batch formation loop.
        _running: Flag to control the batch loop lifecycle.
    """

    def __init__(
        self,
        config: BatcherConfig,
        executor: BatchExecutor,
        metrics: MetricsCollector,
        strategy: BatchingStrategy | None = None,
    ) -> None:
        self.config = config
        self.executor = executor
        self.metrics = metrics
        self.strategy = strategy or create_strategy(config)
        self._futures: dict[str, asyncio.Future[InferenceResponse]] = {}
        self._batch_loop_task: asyncio.Task[None] | None = None
        self._running = False

    async def start(self) -> None:
        """Start the background batch formation loop.

        Creates an asyncio task that continuously waits for batches from the
        strategy, executes them, and resolves the corresponding futures.
        """
        # TODO: Implement startup:
        #   1. Set _running = True
        #   2. Create _batch_loop_task = asyncio.create_task(self._batch_loop())
        #   3. Log that the batcher has started
        pass

    async def stop(self) -> None:
        """Gracefully stop the batcher.

        Signals the batch loop to stop, cancels the task, and resolves
        any remaining futures with an error or processes remaining requests.
        """
        # TODO: Implement graceful shutdown:
        #   1. Set _running = False
        #   2. Cancel _batch_loop_task and await it (handle CancelledError)
        #   3. Get remaining requests from strategy.shutdown()
        #   4. Cancel or resolve remaining futures
        #   5. Log shutdown completion
        pass

    async def submit(self, request: InferenceRequest) -> InferenceResponse:
        """Submit a request for batched inference.

        Creates a Future for the request, adds it to the strategy, and awaits
        the result. The future is resolved by the batch loop when the request's
        batch completes execution.

        Args:
            request: The inference request to process.

        Returns:
            The inference response after batch execution completes.

        Raises:
            RuntimeError: If the batcher is not running.
            asyncio.QueueFull: If the queue depth exceeds max_queue_depth (backpressure).
        """
        # TODO: Implement request submission:
        #   1. Check that _running is True, raise RuntimeError otherwise
        #   2. Check queue depth against max_queue_depth for backpressure
        #   3. Create a Future for this request_id
        #   4. Store it in _futures
        #   5. Add request to the strategy
        #   6. Await and return the Future's result
        pass

    async def _batch_loop(self) -> None:
        """Background loop: wait for batches and execute them.

        Runs continuously while _running is True. Each iteration:
        1. Waits for the strategy to produce a batch
        2. Executes the batch via the executor
        3. Resolves futures for each request in the batch
        4. Records metrics
        """
        # TODO: Implement the batch processing loop:
        #   while self._running:
        #       batch = await self.strategy.wait_for_batch()
        #       if batch.size == 0: continue
        #       results = await self.executor.execute(batch)
        #       self._resolve_futures(batch, results)
        #       self.metrics.record_batch(batch, results)
        pass

    def _resolve_futures(
        self, batch: Batch, results: list[Any]
    ) -> None:
        """Resolve the Future for each request in a completed batch.

        Args:
            batch: The completed batch.
            results: Model outputs, one per request in the batch.
        """
        # TODO: Implement future resolution:
        #   For each (request, result) in zip(batch.requests, results):
        #       Build InferenceResponse with timing info
        #       Set the result on _futures[request.request_id]
        #       Remove the future from _futures
        pass
