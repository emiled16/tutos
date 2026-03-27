"""RequestScheduler that routes requests to appropriate batcher instances."""

from __future__ import annotations

import logging

from dynamic_batching.batcher import DynamicBatcher
from dynamic_batching.config import BatcherConfig
from dynamic_batching.executor import BatchExecutor
from dynamic_batching.metrics import MetricsCollector
from dynamic_batching.request import InferenceRequest, InferenceResponse

logger = logging.getLogger(__name__)


class RequestScheduler:
    """Routes incoming requests to the correct DynamicBatcher instance.

    Supports multiple models/endpoints, each with its own batcher configuration.
    New models can be registered dynamically.

    Attributes:
        _batchers: Mapping of model name → DynamicBatcher instance.
        _configs: Mapping of model name → BatcherConfig.
        _metrics: Shared or per-model MetricsCollector instances.
    """

    def __init__(self) -> None:
        self._batchers: dict[str, DynamicBatcher] = {}
        self._configs: dict[str, BatcherConfig] = {}
        self._metrics: dict[str, MetricsCollector] = {}

    def register_model(
        self,
        model_name: str,
        config: BatcherConfig,
        executor: BatchExecutor | None = None,
        metrics: MetricsCollector | None = None,
    ) -> None:
        """Register a new model with its own batcher.

        Args:
            model_name: Unique identifier for the model/endpoint.
            config: Batcher configuration for this model.
            executor: Optional custom executor. Created from config if not provided.
            metrics: Optional custom metrics collector.

        Raises:
            ValueError: If a model with this name is already registered.
        """
        # TODO: Implement model registration:
        #   1. Check for duplicate model_name
        #   2. Create executor and metrics if not provided
        #   3. Create DynamicBatcher with the config, executor, and metrics
        #   4. Store in _batchers, _configs, _metrics
        pass

    async def submit(
        self,
        model_name: str,
        request: InferenceRequest,
    ) -> InferenceResponse:
        """Route a request to the appropriate batcher.

        Args:
            model_name: Which model/endpoint to target.
            request: The inference request.

        Returns:
            The inference response.

        Raises:
            KeyError: If the model_name is not registered.
        """
        # TODO: Implement request routing:
        #   1. Look up batcher by model_name (raise KeyError if missing)
        #   2. Submit request to the batcher
        #   3. Return the response
        pass

    async def start_all(self) -> None:
        """Start all registered batchers."""
        # TODO: Implement — call start() on each batcher
        pass

    async def stop_all(self) -> None:
        """Gracefully stop all registered batchers."""
        # TODO: Implement — call stop() on each batcher
        pass

    def list_models(self) -> list[str]:
        """Return names of all registered models."""
        return list(self._batchers.keys())

    def get_metrics(self, model_name: str) -> MetricsCollector:
        """Get the metrics collector for a specific model.

        Args:
            model_name: The model to get metrics for.

        Returns:
            The MetricsCollector for the specified model.

        Raises:
            KeyError: If the model is not registered.
        """
        # TODO: Implement metrics lookup
        pass
