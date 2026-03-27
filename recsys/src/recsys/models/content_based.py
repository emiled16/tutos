"""Content-based filtering with item features and TF-IDF."""

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from recsys.models.base import BaseRecommender


class ContentBasedRecommender(BaseRecommender):
    """Content-based recommender using TF-IDF item representations.

    Builds user profiles by aggregating the feature vectors of items
    they have interacted with, then recommends items most similar
    to the user profile.
    """

    def __init__(self, max_features: int = 5000) -> None:
        super().__init__(name="ContentBased")
        self.max_features = max_features
        self.tfidf: TfidfVectorizer | None = None
        self.item_tfidf_matrix: sparse.csr_matrix | None = None
        self.user_profiles: np.ndarray | None = None
        self.interaction_matrix: sparse.csr_matrix | None = None
        self._user_ids: np.ndarray | None = None
        self._item_ids: np.ndarray | None = None
        self._item_features_df: pd.DataFrame | None = None

    def fit(
        self,
        interaction_matrix: sparse.csr_matrix,
        user_ids: np.ndarray,
        item_ids: np.ndarray,
        item_features: pd.DataFrame | None = None,
    ) -> "ContentBasedRecommender":
        """Fit the content-based model.

        Args:
            interaction_matrix: Sparse CSR matrix of shape (n_users, n_items).
            user_ids: Array of original user IDs.
            item_ids: Array of original item IDs.
            item_features: DataFrame with item_id, title, description, genre columns.

        Returns:
            self
        """
        self.interaction_matrix = interaction_matrix
        self._user_ids = user_ids
        self._item_ids = item_ids
        self._item_features_df = item_features

        # TODO: Combine item text fields (title, description, genre) into a single text column
        # TODO: Fit TfidfVectorizer on the combined text and transform to get item_tfidf_matrix
        # TODO: Build user profiles by averaging the TF-IDF vectors of items each user interacted with
        #       user_profiles = normalize(interaction_matrix @ item_tfidf_matrix)
        # TODO: Set self.is_fitted = True

        raise NotImplementedError

    def recommend(
        self,
        user_id: int,
        n: int = 10,
        exclude_seen: bool = True,
    ) -> list[tuple[int, float]]:
        self._check_is_fitted()

        # TODO: Compute cosine similarity between the user profile and all item TF-IDF vectors
        # TODO: Optionally exclude seen items
        # TODO: Return top-n (item_id, score) tuples
        raise NotImplementedError

    def predict(self, user_id: int, item_id: int) -> float:
        self._check_is_fitted()

        # TODO: Compute cosine similarity between user profile and item TF-IDF vector
        raise NotImplementedError

    def get_similar_items(
        self,
        item_id: int,
        n: int = 10,
    ) -> list[tuple[int, float]]:
        """Find items most similar to the given item based on content features.

        Args:
            item_id: The original item ID.
            n: Number of similar items to return.

        Returns:
            List of (item_id, similarity) tuples.
        """
        self._check_is_fitted()

        # TODO: Compute cosine similarity between the target item's TF-IDF vector and all others
        # TODO: Exclude the item itself
        # TODO: Return top-n (item_id, similarity) tuples
        raise NotImplementedError
