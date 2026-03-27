"""Collaborative filtering: ALS matrix factorization and SVD."""

import numpy as np
from scipy import sparse
from sklearn.decomposition import TruncatedSVD

from recsys.models.base import BaseRecommender


class ALSRecommender(BaseRecommender):
    """Alternating Least Squares matrix factorization for implicit feedback.

    Implements the weighted matrix factorization approach from
    Hu, Koren & Volinsky (2008).
    """

    def __init__(
        self,
        n_factors: int = 32,
        n_iterations: int = 15,
        regularization: float = 0.1,
        alpha: float = 40.0,
    ) -> None:
        super().__init__(name="ALS")
        self.n_factors = n_factors
        self.n_iterations = n_iterations
        self.regularization = regularization
        self.alpha = alpha  # confidence scaling factor

        self.user_factors: np.ndarray | None = None
        self.item_factors: np.ndarray | None = None
        self.interaction_matrix: sparse.csr_matrix | None = None
        self._user_ids: np.ndarray | None = None
        self._item_ids: np.ndarray | None = None

    def fit(
        self,
        interaction_matrix: sparse.csr_matrix,
        user_ids: np.ndarray,
        item_ids: np.ndarray,
    ) -> "ALSRecommender":
        """Train ALS on implicit feedback.

        The confidence matrix is C = 1 + alpha * R, where R is the interaction matrix.
        Binary preference is P = (R > 0).

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

        n_users, n_items = interaction_matrix.shape

        # TODO: Initialize user_factors and item_factors randomly (n_users x n_factors, n_items x n_factors)
        # TODO: Compute confidence matrix C = 1 + alpha * interaction_matrix
        # TODO: Compute binary preference matrix P = (interaction_matrix > 0)
        # TODO: Alternate for n_iterations:
        #   1. Fix item_factors, solve for each user vector:
        #      u_u = (V^T C_u V + λI)^{-1} V^T C_u p_u
        #   2. Fix user_factors, solve for each item vector:
        #      v_i = (U^T C_i U + λI)^{-1} U^T C_i p_i
        # TODO: Set self.is_fitted = True

        raise NotImplementedError

    def recommend(
        self,
        user_id: int,
        n: int = 10,
        exclude_seen: bool = True,
    ) -> list[tuple[int, float]]:
        self._check_is_fitted()

        # TODO: Find the user's matrix index from user_id
        # TODO: Compute scores = user_factors[user_idx] @ item_factors.T
        # TODO: If exclude_seen, set scores of already-interacted items to -inf
        # TODO: Return top-n (item_id, score) tuples sorted by descending score
        raise NotImplementedError

    def predict(self, user_id: int, item_id: int) -> float:
        self._check_is_fitted()

        # TODO: Compute dot product of user and item factor vectors
        raise NotImplementedError


class SVDRecommender(BaseRecommender):
    """Truncated SVD-based collaborative filtering.

    Uses scikit-learn's TruncatedSVD on the sparse interaction matrix
    to learn latent factors.
    """

    def __init__(self, n_components: int = 32) -> None:
        super().__init__(name="SVD")
        self.n_components = n_components
        self.svd: TruncatedSVD | None = None
        self.user_factors: np.ndarray | None = None
        self.item_factors: np.ndarray | None = None
        self.interaction_matrix: sparse.csr_matrix | None = None
        self._user_ids: np.ndarray | None = None
        self._item_ids: np.ndarray | None = None

    def fit(
        self,
        interaction_matrix: sparse.csr_matrix,
        user_ids: np.ndarray,
        item_ids: np.ndarray,
    ) -> "SVDRecommender":
        """Fit truncated SVD to the interaction matrix.

        Decomposes R ≈ U_k Σ_k V_k^T and stores user factors (U_k Σ_k)
        and item factors (V_k^T transposed).

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

        # TODO: Fit TruncatedSVD with n_components on the interaction matrix
        # TODO: Store user_factors = svd.transform(interaction_matrix)  (U_k Σ_k)
        # TODO: Store item_factors = svd.components_.T  (V_k)
        # TODO: Set self.is_fitted = True

        raise NotImplementedError

    def recommend(
        self,
        user_id: int,
        n: int = 10,
        exclude_seen: bool = True,
    ) -> list[tuple[int, float]]:
        self._check_is_fitted()

        # TODO: Compute scores as user_factors[user_idx] @ item_factors.T
        # TODO: Optionally exclude seen items
        # TODO: Return top-n (item_id, score) tuples
        raise NotImplementedError

    def predict(self, user_id: int, item_id: int) -> float:
        self._check_is_fitted()

        # TODO: Compute dot product of user and item factor vectors
        raise NotImplementedError
