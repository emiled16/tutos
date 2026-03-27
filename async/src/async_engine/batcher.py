"""Dynamic request batcher for efficient model inference."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from async_engine.inference import InferenceEngine, InferenceRequest


class DynamicBatcher:
    """Batches individual inference requests for efficient processing.

    The batcher runs a continuous loop that collects requests from a queue
    and groups them into batches. A batch is dispatched when either:
    - The batch reaches max_batch_size, OR
    - The batch_timeout_ms has elapsed since the first request in the batch

    This balances throughput (larger batches) with latency (shorter wait).

    Attributes:
        max_batch_size: Maximum number of requests per batch.
        batch_timeout_ms: Maximum wait time (ms) before processing a partial batch.
        inference_engine: The engine that processes batched requests.
    """

    def __init__(
        self,
        inference_engine: InferenceEngine,
        max_batch_size: int = 32,
        batch_timeout_ms: int = 50,
    ) -> None:
        self.inference_engine = inference_engine
        self.max_batch_size = max_batch_size
        self.batch_timeout_ms = batch_timeout_ms
        self._running = False
        self._queue: asyncio.Queue[InferenceRequest] | None = None

    async def start(self, queue: asyncio.Queue[InferenceRequest]) -> None:
        """Start the batching loop.

        Continuously pulls requests from the queue, forms batches,
        and dispatches them to the inference engine.

        Args:
            queue: The async queue to pull requests from.
        """
        # TODO: Implement the main batching loop.
        # self._running = True
        # self._queue = queue
        # while self._running:
        #     batch = await self._collect_batch()
        #     if batch:
        #         await self._dispatch_batch(batch)
        raise NotImplementedError

    async def stop(self) -> None:
        """Stop the batching loop gracefully.

        Processes any remaining items in the queue before stopping.
        """
        # TODO: Implement graceful stop.
        # - Set self._running = False
        # - Drain remaining items from the queue
        raise NotImplementedError

    async def _collect_batch(self) -> list[InferenceRequest]:
        """Collect requests into a batch.

        Waits for the first request (blocking), then collects additional
        requests until max_batch_size or batch_timeout_ms is reached.

        Returns:
            List of InferenceRequest objects forming the batch.
        """
        # TODO: Implement batch collection.
        # 1. Wait for the first request (blocking get)
        # 2. Record the start time
        # 3. While batch size < max and time < timeout:
        #    - Try to get another request with remaining timeout
        #    - Add to batch if available
        # 4. Return the batch
        raise NotImplementedError

    async def _dispatch_batch(
        self, batch: list[InferenceRequest]
    ) -> None:
        """Send a batch to the inference engine and resolve futures.

        Args:
            batch: List of InferenceRequest objects to process.
        """
        # TODO: Implement batch dispatch.
        # 1. Extract input arrays from all requests
        # 2. Stack into a single numpy array
        # 3. Call inference_engine.predict_batch()
        # 4. Split results and set each request's Future result
        # 5. Handle errors: set exception on all futures in the batch
        raise NotImplementedError

    @property
    def is_running(self) -> bool:
        """Whether the batcher is currently running."""
        return self._running
