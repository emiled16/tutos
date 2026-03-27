"""Hybrid model combining collaborative and content-based signals."""

from dataclasses import dataclass, field

import numpy as np
from scipy import sparse

from recsys.models.base import BaseRecommender


@dataclass
class HybridWeights:
    """Weights for combining different recommender scores."""

    collaborative: float = 0.5
    content_based: float = 0.3
    neural: float = 0.2

    def __post_init__(self) -> None:
        total = self.collaborative + self.content_based + self.neural
        if abs(total - 1.0) > 1e-6:
            self.collaborative /= total
            self.content_based /= total
            self.neural /= total


class HybridRecommender(BaseRecommender):
    """Weighted hybrid recommender combining multiple sub-models.

    Computes a weighted average of scores from collaborative, content-based,
    and neural collaborative filtering models. Falls back gracefully when
    a sub-model cannot score a user-item pair (e.g., cold-start).
    """

    def __init__(
        self,
        models: dict[str, BaseRecommender],
        weights: HybridWeights | None = None,
    ) -> None:
        """Initialize the hybrid recommender.

        Args:
            models: Dict mapping model names to fitted BaseRecommender instances.
                    Expected keys: "collaborative", "content_based", "neural".
            weights: Relative weights for each model. Defaults to equal weighting.
        """
        super().__init__(name="Hybrid")
        self.models = models
        self.weights = weights or HybridWeights()
        self.interaction_matrix: sparse.csr_matrix | None = None
        self._user_ids: np.ndarray | None = None
        self._item_ids: np.ndarray | None = None

    def fit(
        self,
        interaction_matrix: sparse.csr_matrix,
        user_ids: np.ndarray,
        item_ids: np.ndarray,
    ) -> "HybridRecommender":
        """Store interaction data. Sub-models should already be fitted.

        Args:
            interaction_matrix: Sparse CSR matrix of shape (n_users, n_items).
            user_ids: Array of original user IDs.
            item_ids: Array of original item IDs.

        Returns:
            self
        """
        self.interaction_matrix = interaction_matrix
        self._user_ids = user_ids
        self._item_ids = item_ids

        # TODO: Verify all sub-models are fitted (check is_fitted flag)
        # TODO: Set self.is_fitted = True

        raise NotImplementedError

    def _get_weight(self, model_name: str) -> float:
        """Get the weight for a named model."""
        return getattr(self.weights, model_name, 0.0)

    def predict(self, user_id: int, item_id: int) -> float:
        self._check_is_fitted()

        # TODO: For each sub-model, attempt to predict(user_id, item_id)
        #       Catch exceptions for models that can't score this pair (cold-start)
        # TODO: Compute weighted average of available scores
        #       Re-normalize weights if some models failed
        raise NotImplementedError

    def recommend(
        self,
        user_id: int,
        n: int = 10,
        exclude_seen: bool = True,
    ) -> list[tuple[int, float]]:
        self._check_is_fitted()

        # TODO: Collect recommendation lists from each sub-model
        # TODO: Merge scores using weighted combination
        #       For each item, combine scores across models that produced it
        #       Re-normalize weights for items only scored by a subset of models
        # TODO: Sort by combined score, optionally exclude seen items
        # TODO: Return top-n (item_id, combined_score) tuples
        raise NotImplementedError

    def recommend_with_explanation(
        self,
        user_id: int,
        n: int = 10,
    ) -> list[dict]:
        """Recommend with per-model score breakdown for explainability.

        Returns:
            List of dicts with keys: item_id, combined_score, model_scores.
        """
        self._check_is_fitted()

        # TODO: For each recommended item, include the individual model scores
        #       alongside the combined score for transparency
        raise NotImplementedError
