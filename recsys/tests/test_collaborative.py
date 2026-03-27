"""Tests for collaborative filtering models (ALS and SVD)."""

import numpy as np
import pytest
from scipy import sparse

from recsys.models.collaborative import ALSRecommender, SVDRecommender


@pytest.fixture
def small_interaction_matrix() -> sparse.csr_matrix:
    """Create a small dense-ish interaction matrix for testing."""
    rng = np.random.default_rng(42)
    n_users, n_items = 20, 15
    density = 0.3
    data = rng.choice([0.0, 1.0], size=(n_users, n_items), p=[1 - density, density])
    return sparse.csr_matrix(data)


@pytest.fixture
def user_ids() -> np.ndarray:
    return np.arange(20)


@pytest.fixture
def item_ids() -> np.ndarray:
    return np.arange(15)


class TestALSRecommender:
    def test_fit_stores_factors(
        self, small_interaction_matrix, user_ids, item_ids
    ) -> None:
        """ALS fit should produce user and item factor matrices of the correct shape."""
        model = ALSRecommender(n_factors=8, n_iterations=3)

        # TODO: Fit the model on small_interaction_matrix
        # TODO: Assert user_factors shape is (n_users, n_factors)
        # TODO: Assert item_factors shape is (n_items, n_factors)
        # TODO: Assert model.is_fitted is True

    def test_recommend_returns_correct_count(
        self, small_interaction_matrix, user_ids, item_ids
    ) -> None:
        """recommend() should return exactly n items."""
        model = ALSRecommender(n_factors=8, n_iterations=3)

        # TODO: Fit the model
        # TODO: Call recommend(user_id=0, n=5)
        # TODO: Assert exactly 5 (item_id, score) tuples are returned
        # TODO: Assert scores are in descending order

    def test_recommend_excludes_seen_items(
        self, small_interaction_matrix, user_ids, item_ids
    ) -> None:
        """With exclude_seen=True, recommended items should not include training items."""
        model = ALSRecommender(n_factors=8, n_iterations=3)

        # TODO: Fit the model
        # TODO: Get user 0's seen items from the interaction matrix
        # TODO: Call recommend(user_id=0, n=5, exclude_seen=True)
        # TODO: Assert none of the recommended items are in the seen set

    def test_predict_returns_float(
        self, small_interaction_matrix, user_ids, item_ids
    ) -> None:
        """predict() should return a scalar float score."""
        model = ALSRecommender(n_factors=8, n_iterations=3)

        # TODO: Fit and call predict(user_id=0, item_id=0)
        # TODO: Assert the result is a float

    def test_unfitted_model_raises(self) -> None:
        """Calling recommend or predict before fit should raise RuntimeError."""
        model = ALSRecommender()

        with pytest.raises(RuntimeError):
            model.recommend(user_id=0)

        with pytest.raises(RuntimeError):
            model.predict(user_id=0, item_id=0)


class TestSVDRecommender:
    def test_fit_stores_factors(
        self, small_interaction_matrix, user_ids, item_ids
    ) -> None:
        """SVD fit should produce user and item factor matrices."""
        model = SVDRecommender(n_components=8)

        # TODO: Fit the model on small_interaction_matrix
        # TODO: Assert user_factors and item_factors are not None
        # TODO: Assert shapes are consistent (n_users x n_components, n_items x n_components)

    def test_recommend_returns_sorted_scores(
        self, small_interaction_matrix, user_ids, item_ids
    ) -> None:
        """Recommendations should be sorted by descending score."""
        model = SVDRecommender(n_components=8)

        # TODO: Fit and call recommend(user_id=0, n=5)
        # TODO: Extract scores and assert they are monotonically non-increasing

    def test_svd_captures_structure(self) -> None:
        """SVD should recover structure from a low-rank matrix."""
        # TODO: Create a rank-2 matrix (outer product of two vectors)
        # TODO: Fit SVD with n_components=2
        # TODO: Assert that predictions approximately recover the original matrix
        #       (mean absolute error < threshold)
