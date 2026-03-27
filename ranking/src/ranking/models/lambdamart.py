"""LambdaMART ranking model using LightGBM.

LambdaMART combines lambda gradients (from LambdaRank) with gradient boosted
trees. It directly optimizes NDCG by using lambda gradients that weight
pairwise losses by the NDCG change from swapping each pair.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import lightgbm as lgb
import numpy as np


@dataclass
class LambdaMARTConfig:
    """Configuration for the LambdaMART model."""

    objective: str = "lambdarank"
    metric: str = "ndcg"
    ndcg_eval_at: list[int] | None = None
    n_estimators: int = 300
    num_leaves: int = 63
    learning_rate: float = 0.05
    min_child_samples: int = 20
    subsample: float = 0.8
    colsample_bytree: float = 0.8
    reg_lambda: float = 1.0
    random_state: int = 42
    verbose: int = -1

    def __post_init__(self) -> None:
        if self.ndcg_eval_at is None:
            self.ndcg_eval_at = [5, 10]


class LambdaMARTRanker:
    """LambdaMART model wrapping LightGBM's built-in lambdarank objective.

    LightGBM implements LambdaMART natively through its "lambdarank" objective,
    handling lambda gradient computation and NDCG-aware pair weighting internally.
    """

    def __init__(self, config: LambdaMARTConfig | None = None) -> None:
        self.config = config or LambdaMARTConfig()
        self.model: lgb.Booster | None = None

    def fit(
        self,
        features: np.ndarray,
        labels: np.ndarray,
        query_ids: np.ndarray,
        val_features: np.ndarray | None = None,
        val_labels: np.ndarray | None = None,
        val_query_ids: np.ndarray | None = None,
    ) -> dict[str, list[float]]:
        """Train the LambdaMART model.

        Args:
            features: Training feature matrix of shape (n_samples, n_features).
            labels: Relevance labels of shape (n_samples,) with integer grades.
            query_ids: Query group identifiers of shape (n_samples,).
            val_features: Optional validation features.
            val_labels: Optional validation labels.
            val_query_ids: Optional validation query IDs.

        Returns:
            Dictionary of evaluation metric histories (e.g., {"ndcg@5": [...]}).
        """
        # TODO: Implement LambdaMART training
        # 1. Convert query_ids to group sizes using _query_ids_to_groups
        # 2. Create lgb.Dataset with features, labels, and group parameter
        # 3. If validation data provided, create a validation Dataset
        # 4. Build LightGBM params from self.config
        # 5. Train with lgb.train(), storing the booster in self.model
        # 6. Return the evaluation log
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
        # TODO: Implement prediction using self.model.predict()
        raise NotImplementedError

    def rank(self, features: np.ndarray) -> np.ndarray:
        """Return document indices sorted by predicted relevance (descending).

        Args:
            features: Feature matrix of shape (n_docs, n_features).

        Returns:
            Array of indices that would sort documents by score descending.
        """
        # TODO: Implement ranking by calling predict and argsort descending
        raise NotImplementedError

    def feature_importance(self, importance_type: str = "gain") -> dict[str, float]:
        """Get feature importance scores from the trained model.

        Args:
            importance_type: One of "gain", "split", or "cover".

        Returns:
            Dict mapping feature index (as string) to importance value.

        Raises:
            RuntimeError: If the model has not been trained.
        """
        # TODO: Implement feature importance extraction from LightGBM booster
        raise NotImplementedError

    def save(self, path: Path) -> None:
        """Save the model in LightGBM text format.

        Args:
            path: File path to save to.
        """
        # TODO: Implement using self.model.save_model()
        raise NotImplementedError

    def load(self, path: Path) -> None:
        """Load a model from LightGBM text format.

        Args:
            path: File path to load from.
        """
        # TODO: Implement using lgb.Booster(model_file=...)
        raise NotImplementedError

    @staticmethod
    def _query_ids_to_groups(query_ids: np.ndarray) -> list[int]:
        """Convert per-sample query IDs to LightGBM group sizes.

        Assumes query_ids are contiguous (all samples for a query are
        adjacent in the array).

        Args:
            query_ids: Array of query identifiers, one per sample.

        Returns:
            List of group sizes, where each entry is the number of
            documents for that query.
        """
        # TODO: Implement conversion from query ID array to group size list
        # e.g., [0, 0, 0, 1, 1] → [3, 2]
        raise NotImplementedError
