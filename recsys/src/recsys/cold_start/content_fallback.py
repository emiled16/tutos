"""Content-based fallback for new items without interaction history."""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from recsys.models.base import BaseRecommender


class ContentFallbackRecommender(BaseRecommender):
    """Handles cold-start for new items by using content similarity.

    For a new item with no interactions, finds the most similar existing items
    based on content features and transfers their collaborative scores.
    """

    def __init__(
        self,
        n_neighbors: int = 10,
        primary_model: BaseRecommender | None = None,
    ) -> None:
        """Initialize content fallback.

        Args:
            n_neighbors: Number of similar items to use for score transfer.
            primary_model: The main recommender to borrow scores from for warm items.
        """
        super().__init__(name="ContentFallback")
        self.n_neighbors = n_neighbors
        self.primary_model = primary_model
        self.item_feature_matrix: np.ndarray | None = None
        self.item_similarity: np.ndarray | None = None
        self._known_item_ids: set[int] | None = None
        self._user_ids: np.ndarray | None = None
        self._item_ids: np.ndarray | None = None

    def fit(
        self,
        interaction_matrix=None,
        user_ids: np.ndarray | None = None,
        item_ids: np.ndarray | None = None,
        item_features: np.ndarray | None = None,
    ) -> "ContentFallbackRecommender":
        """Fit the content fallback using item feature vectors.

        Args:
            interaction_matrix: Not used directly, accepted for API compatibility.
            user_ids: Array of known user IDs.
            item_ids: Array of known item IDs.
            item_features: Dense feature matrix of shape (n_items, n_features).

        Returns:
            self
        """
        self._user_ids = user_ids
        self._item_ids = item_ids

        # TODO: Store the item feature matrix
        # TODO: Precompute pairwise cosine similarity between all items
        # TODO: Record the set of known item IDs (items with interactions)
        # TODO: Set self.is_fitted = True

        raise NotImplementedError

    def recommend_for_new_item(
        self,
        new_item_features: np.ndarray,
        user_id: int,
        n: int = 10,
    ) -> list[tuple[int, float]]:
        """Recommend users who might like a new (cold-start) item.

        Finds existing items similar to the new item, then identifies users
        who liked those similar items.

        Args:
            new_item_features: Feature vector for the new item, shape (n_features,).
            user_id: Target user ID.
            n: Number of recommendations.

        Returns:
            List of (item_id, estimated_score) tuples.
        """
        self._check_is_fitted()

        # TODO: Compute cosine similarity between new_item_features and all known items
        # TODO: Find the top-n_neighbors most similar known items
        # TODO: If primary_model is available, compute a weighted average of its scores
        #       for the user across the similar items (weighted by similarity)
        # TODO: Return the new item with the transferred score estimate
        raise NotImplementedError

    def recommend(
        self,
        user_id: int,
        n: int = 10,
        exclude_seen: bool = True,
    ) -> list[tuple[int, float]]:
        self._check_is_fitted()

        # TODO: If primary_model is available and can handle this user, delegate to it
        # TODO: Otherwise fall back to content-similarity-based recommendations
        raise NotImplementedError

    def predict(self, user_id: int, item_id: int) -> float:
        self._check_is_fitted()

        # TODO: If item_id is known and primary_model available, delegate
        # TODO: Otherwise estimate via content similarity to known items
        raise NotImplementedError
