"""Model loading, versioning, and hot-reload management."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from typing import Any

import numpy as np

from grpc.models.predictor import ModelPredictor

logger = logging.getLogger(__name__)


@dataclass
class ModelEntry:
    """Metadata and reference for a loaded model."""

    name: str
    version: str
    predictor: ModelPredictor
    loaded_at: float = field(default_factory=time.time)
    status: str = "loaded"
    path: str = ""


class ModelManager:
    """Manages loading, serving, and hot-reloading of ML models.

    Thread-safe model registry that supports versioning and zero-downtime
    model updates.
    """

    def __init__(self, model_dir: str | Path = "models/") -> None:
        """Initialize the model manager.

        Args:
            model_dir: Directory containing model files.
        """
        self.model_dir = Path(model_dir)
        self._models: dict[str, ModelEntry] = {}
        self._lock = Lock()

    def load_model(
        self, name: str, path: str | Path, version: str = "1"
    ) -> ModelEntry:
        """Load a model from disk and register it.

        Args:
            name: Unique model name.
            path: Path to the model file (e.g., joblib/pickle).
            version: Version string for this model.

        Returns:
            ModelEntry for the loaded model.

        Raises:
            FileNotFoundError: If the model file doesn't exist.
            RuntimeError: If model loading fails.
        """
        # TODO: Implement
        # - Validate the path exists
        # - Create a ModelPredictor and load the model from path
        # - Create a ModelEntry with metadata
        # - Register in self._models under the name (thread-safe)
        # - Log the successful load
        # - Return the ModelEntry
        raise NotImplementedError

    def get_model(
        self, name: str, version: str | None = None
    ) -> ModelPredictor | None:
        """Get a loaded model by name and optional version.

        Args:
            name: Model name.
            version: Specific version to retrieve. None returns the latest.

        Returns:
            The ModelPredictor if found, None otherwise.
        """
        # TODO: Implement
        # - Lock and look up name in self._models
        # - If version specified, check it matches
        # - Return the predictor or None
        raise NotImplementedError

    def list_models(self) -> list[ModelEntry]:
        """List all loaded models.

        Returns:
            List of ModelEntry objects.
        """
        # TODO: Implement
        # - Return a copy of all model entries (thread-safe)
        raise NotImplementedError

    def reload(self, name: str, path: str | None = None) -> ModelEntry:
        """Hot-reload a model without downtime.

        Loads the new model first, then swaps the reference atomically.
        If loading fails, the old model remains active.

        Args:
            name: Model name to reload.
            path: New path for the model. If None, reloads from same path.

        Returns:
            Updated ModelEntry.

        Raises:
            KeyError: If the model name is not registered.
            RuntimeError: If the new model fails to load.
        """
        # TODO: Implement
        # - Get the existing model entry (raise KeyError if missing)
        # - Determine path (use new path or existing entry's path)
        # - Load the new model into a temporary predictor
        # - Atomically swap the model entry (lock)
        # - Increment the version string
        # - Log the reload
        # - Return the updated ModelEntry
        raise NotImplementedError

    def load_all_from_directory(self) -> list[ModelEntry]:
        """Scan model_dir and load all model files found.

        Looks for .joblib and .pkl files.

        Returns:
            List of loaded ModelEntry objects.
        """
        # TODO: Implement
        # - Scan self.model_dir for .joblib and .pkl files
        # - Load each one with name = stem of filename
        # - Return list of ModelEntry
        raise NotImplementedError
