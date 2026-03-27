"""ML model wrapper for inference via gRPC."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


class ModelPredictor:
    """Wraps an sklearn-compatible model for use with the gRPC server.

    Handles model loading, input validation, and inference.
    """

    def __init__(self) -> None:
        self._model: Any = None
        self._model_path: str = ""

    @property
    def is_loaded(self) -> bool:
        """Check if a model is currently loaded."""
        return self._model is not None

    def load(self, model_path: str | Path) -> None:
        """Load a model from a file.

        Supports joblib (.joblib) and pickle (.pkl) formats.

        Args:
            model_path: Path to the serialized model file.

        Raises:
            FileNotFoundError: If model_path doesn't exist.
            ValueError: If file extension is not supported.
            RuntimeError: If model loading fails.
        """
        # TODO: Implement
        # - Validate path exists
        # - Determine format from extension (.joblib → joblib.load, .pkl → pickle.load)
        # - Load the model
        # - Store as self._model
        # - Store path as self._model_path
        raise NotImplementedError

    def predict(self, features: np.ndarray) -> np.ndarray:
        """Run inference on input features.

        Args:
            features: Input array of shape (n_samples, n_features)
                      or (n_features,) for a single sample.

        Returns:
            Prediction array.

        Raises:
            RuntimeError: If no model is loaded.
            ValueError: If input shape is invalid.
        """
        # TODO: Implement
        # - Check self.is_loaded, raise RuntimeError if not
        # - If features is 1D, reshape to (1, -1)
        # - Call self._model.predict(features)
        # - Return predictions as numpy array
        raise NotImplementedError

    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        """Run inference and return class probabilities.

        Args:
            features: Input array of shape (n_samples, n_features).

        Returns:
            Probability array of shape (n_samples, n_classes).

        Raises:
            RuntimeError: If no model is loaded.
            AttributeError: If model doesn't support predict_proba.
        """
        # TODO: Implement
        # - Check model is loaded
        # - Reshape if needed
        # - Call self._model.predict_proba(features)
        # - Return probabilities
        raise NotImplementedError

    def get_input_shape(self) -> tuple[int, ...] | None:
        """Get the expected input shape from the model if available.

        Returns:
            Expected input shape tuple, or None if not determinable.
        """
        # TODO: Implement
        # - Try to extract n_features_in_ from the model
        # - Return (n_features_in_,) or None
        raise NotImplementedError
