"""Pointwise ranking model.

Treats ranking as a regression problem: predict each document's relevance
score independently, then sort by predicted score.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor


class RankingModel(Protocol):
    """Interface that all ranking models must implement."""

    def fit(self, features: np.ndarray, labels: np.ndarray, query_ids: np.ndarray) -> None: ...
    def predict(self, features: np.ndarray) -> np.ndarray: ...
    def save(self, path: Path) -> None: ...
    def load(self, path: Path) -> None: ...


@dataclass
class PointwiseConfig:
    """Configuration for the pointwise ranking model."""

    n_estimators: int = 200
    max_depth: int = 6
    learning_rate: float = 0.1
    min_samples_leaf: int = 10
    subsample: float = 0.8
    random_state: int = 42


class PointwiseRanker:
    """Pointwise learning-to-rank model using gradient boosted regression.

    Trains a GBM regressor to predict relevance labels directly. Documents
    are ranked by sorting on predicted scores.
    """

    def __init__(self, config: PointwiseConfig | None = None) -> None:
        self.config = config or PointwiseConfig()
        self.model: GradientBoostingRegressor | None = None

    def fit(
        self,
        features: np.ndarray,
        labels: np.ndarray,
        query_ids: np.ndarray,
    ) -> None:
        """Train the pointwise model.

        Note: query_ids are accepted for API compatibility but not used
        in pointwise training (each sample is independent).

        Args:
            features: Feature matrix of shape (n_samples, n_features).
            labels: Relevance labels of shape (n_samples,).
            query_ids: Query group identifiers of shape (n_samples,).
        """
        # TODO: Implement pointwise training
        # 1. Initialize GradientBoostingRegressor with self.config parameters
        # 2. Fit on features/labels (ignoring query_ids since pointwise is independent)
        # 3. Store the trained model in self.model
        raise NotImplementedError

    def predict(self, features: np.ndarray) -> np.ndarray:
        """Predict relevance scores for documents.

        Args:
            features: Feature matrix of shape (n_samples, n_features).

        Returns:
            Predicted scores of shape (n_samples,).

        Raises:
            RuntimeError: If the model has not been trained.
        """
        # TODO: Implement prediction using self.model
        raise NotImplementedError

    def rank(self, features: np.ndarray) -> np.ndarray:
        """Return document indices sorted by predicted relevance (descending).

        Args:
            features: Feature matrix of shape (n_docs, n_features).

        Returns:
            Array of indices that would sort documents by score descending.
        """
        # TODO: Implement ranking by calling predict and sorting by score descending
        raise NotImplementedError

    def save(self, path: Path) -> None:
        """Persist the trained model to disk.

        Args:
            path: File path to save to (pickle format).
        """
        # TODO: Implement model serialization using joblib or pickle
        raise NotImplementedError

    def load(self, path: Path) -> None:
        """Load a trained model from disk.

        Args:
            path: File path to load from.
        """
        # TODO: Implement model deserialization
        raise NotImplementedError
