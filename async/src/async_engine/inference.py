"""Async model inference wrapper."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class InferenceRequest:
    """A single inference request.

    Attributes:
        request_id: Unique identifier for the request.
        input_data: Input feature vector as a numpy array.
        future: asyncio.Future that will hold the prediction result.
        priority: Request priority (lower = higher).
        created_at: Monotonic timestamp when the request was created.
    """

    request_id: str
    input_data: np.ndarray
    future: asyncio.Future = field(default_factory=lambda: asyncio.get_event_loop().create_future())
    priority: int = 1
    created_at: float = field(default_factory=lambda: asyncio.get_event_loop().time())


@dataclass
class InferenceResult:
    """Result of a model inference.

    Attributes:
        request_id: The request this result corresponds to.
        prediction: The model's prediction output.
        latency_ms: Time taken for inference in milliseconds.
        model_version: Version of the model used.
    """

    request_id: str
    prediction: np.ndarray
    latency_ms: float
    model_version: str = "v1.0"


class InferenceEngine:
    """Async wrapper for ML model inference.

    Provides both single and batch inference methods. The engine
    simulates model inference with configurable latency to allow
    testing the async infrastructure without a real model.

    Attributes:
        model_name: Name of the model being served.
        model_version: Version identifier.
        simulate_latency_ms: Simulated inference latency in milliseconds.
    """

    def __init__(
        self,
        model_name: str = "recommendation_model",
        model_version: str = "v1.0",
        simulate_latency_ms: float = 10.0,
        input_dim: int = 128,
        output_dim: int = 10,
    ) -> None:
        self.model_name = model_name
        self.model_version = model_version
        self.simulate_latency_ms = simulate_latency_ms
        self.input_dim = input_dim
        self.output_dim = output_dim
        self._is_ready = False

    async def load_model(self) -> None:
        """Load the model (simulated).

        In a real implementation, this would load model weights from disk
        or a model registry.
        """
        # TODO: Implement model loading.
        # - Simulate loading delay with asyncio.sleep
        # - Set self._is_ready = True
        # - Log that the model is loaded
        raise NotImplementedError

    async def predict(self, input_data: np.ndarray) -> InferenceResult:
        """Run inference on a single input.

        Args:
            input_data: Input feature vector of shape (input_dim,).

        Returns:
            InferenceResult with the prediction.

        Raises:
            RuntimeError: If the model has not been loaded.
            ValueError: If input shape doesn't match expected dimensions.
        """
        # TODO: Implement single inference.
        # 1. Validate model is ready
        # 2. Validate input shape
        # 3. Simulate inference latency with asyncio.sleep
        # 4. Generate a simulated prediction (e.g., softmax-like random output)
        # 5. Return InferenceResult
        raise NotImplementedError

    async def predict_batch(
        self, inputs: np.ndarray
    ) -> list[InferenceResult]:
        """Run inference on a batch of inputs.

        Batch inference is more efficient than individual predictions
        because it amortizes model overhead across multiple inputs.

        Args:
            inputs: Batch of input vectors, shape (batch_size, input_dim).

        Returns:
            List of InferenceResult objects, one per input.

        Raises:
            RuntimeError: If the model has not been loaded.
        """
        # TODO: Implement batch inference.
        # 1. Validate model is ready
        # 2. Validate input shape
        # 3. Simulate batch inference latency (slightly more than single, less than N * single)
        # 4. Generate predictions for all inputs
        # 5. Return list of InferenceResult objects
        raise NotImplementedError

    @property
    def is_ready(self) -> bool:
        """Whether the model is loaded and ready for inference."""
        return self._is_ready

    def get_info(self) -> dict[str, Any]:
        """Return model metadata.

        Returns:
            Dictionary with model_name, model_version, input_dim,
            output_dim, and is_ready status.
        """
        # TODO: Implement model info.
        raise NotImplementedError
