"""Abstract base class for all recommender models."""

from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from scipy import sparse


class BaseRecommender(ABC):
    """Abstract base recommender providing the interface all models must implement."""

    def __init__(self, name: str = "BaseRecommender") -> None:
        self.name = name
        self.is_fitted: bool = False

    @abstractmethod
    def fit(
        self,
        interaction_matrix: sparse.csr_matrix,
        user_ids: np.ndarray,
        item_ids: np.ndarray,
    ) -> "BaseRecommender":
        """Train the model on a user-item interaction matrix.

        Args:
            interaction_matrix: Sparse CSR matrix of shape (n_users, n_items).
            user_ids: Array of original user IDs corresponding to matrix rows.
            item_ids: Array of original item IDs corresponding to matrix columns.

        Returns:
            self
        """
        ...

    @abstractmethod
    def recommend(
        self,
        user_id: int,
        n: int = 10,
        exclude_seen: bool = True,
    ) -> list[tuple[int, float]]:
        """Generate top-N recommendations for a user.

        Args:
            user_id: The original user ID.
            n: Number of items to recommend.
            exclude_seen: Whether to filter out items the user already interacted with.

        Returns:
            List of (item_id, score) tuples sorted by descending score.
        """
        ...

    @abstractmethod
    def predict(self, user_id: int, item_id: int) -> float:
        """Predict the score for a specific user-item pair.

        Args:
            user_id: The original user ID.
            item_id: The original item ID.

        Returns:
            Predicted score.
        """
        ...

    def _check_is_fitted(self) -> None:
        if not self.is_fitted:
            raise RuntimeError(f"{self.name} has not been fitted. Call fit() first.")
