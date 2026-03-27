"""Popularity-based fallback for cold-start users."""

import numpy as np
from scipy import sparse

from recsys.models.base import BaseRecommender


class PopularityRecommender(BaseRecommender):
    """Recommends the most popular items globally.

    Serves as a non-personalized baseline and a cold-start fallback
    when no user interaction history is available.
    """

    def __init__(self, time_decay: float = 0.0) -> None:
        """Initialize the popularity recommender.

        Args:
            time_decay: Exponential decay factor for older interactions.
                        0.0 = no decay (raw counts), higher = more recency bias.
        """
        super().__init__(name="Popularity")
        self.time_decay = time_decay
        self.item_scores: np.ndarray | None = None
        self.item_ranking: np.ndarray | None = None
        self.interaction_matrix: sparse.csr_matrix | None = None
        self._user_ids: np.ndarray | None = None
        self._item_ids: np.ndarray | None = None

    def fit(
        self,
        interaction_matrix: sparse.csr_matrix,
        user_ids: np.ndarray,
        item_ids: np.ndarray,
        timestamps: np.ndarray | None = None,
    ) -> "PopularityRecommender":
        """Compute item popularity scores from the interaction matrix.

        Args:
            interaction_matrix: Sparse CSR matrix of shape (n_users, n_items).
            user_ids: Array of original user IDs.
            item_ids: Array of original item IDs.
            timestamps: Optional array of interaction timestamps for time-decayed popularity.

        Returns:
            self
        """
        self.interaction_matrix = interaction_matrix
        self._user_ids = user_ids
        self._item_ids = item_ids

        # TODO: If no time_decay, compute popularity as column sums of the interaction matrix
        # TODO: If time_decay > 0 and timestamps provided, weight each interaction by
        #       exp(-time_decay * (max_timestamp - interaction_timestamp))
        #       then sum per item
        # TODO: Store item_scores and the argsort ranking (item_ranking)
        # TODO: Set self.is_fitted = True

        raise NotImplementedError

    def recommend(
        self,
        user_id: int,
        n: int = 10,
        exclude_seen: bool = True,
    ) -> list[tuple[int, float]]:
        self._check_is_fitted()

        # TODO: Return the top-n most popular items by score
        # TODO: If exclude_seen and user_id is known, filter out seen items
        # TODO: Handle unknown user_id gracefully (just return popular items)
        raise NotImplementedError

    def predict(self, user_id: int, item_id: int) -> float:
        self._check_is_fitted()

        # TODO: Return the popularity score of the item (user-independent)
        raise NotImplementedError
