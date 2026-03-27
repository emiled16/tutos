"""Tests for the hybrid recommender model."""

import numpy as np
import pytest
from scipy import sparse
from unittest.mock import MagicMock

from recsys.models.base import BaseRecommender
from recsys.models.hybrid import HybridRecommender, HybridWeights


def _make_mock_model(name: str, scores: dict[tuple[int, int], float]) -> MagicMock:
    """Create a mock recommender that returns predetermined scores."""
    model = MagicMock(spec=BaseRecommender)
    model.name = name
    model.is_fitted = True
    model.predict.side_effect = lambda u, i: scores.get((u, i), 0.0)
    model.recommend.return_value = [
        (item_id, score) for (u, item_id), score in scores.items()
    ]
    return model


class TestHybridWeights:
    def test_weights_normalize(self) -> None:
        """Weights that don't sum to 1 should be auto-normalized."""
        weights = HybridWeights(collaborative=2.0, content_based=2.0, neural=1.0)
        total = weights.collaborative + weights.content_based + weights.neural
        # TODO: Assert total ≈ 1.0

    def test_default_weights_sum_to_one(self) -> None:
        weights = HybridWeights()
        total = weights.collaborative + weights.content_based + weights.neural
        # TODO: Assert total ≈ 1.0


class TestHybridRecommender:
    def test_fit_requires_fitted_submodels(self) -> None:
        """Hybrid fit should fail if sub-models are not fitted."""
        unfitted = MagicMock(spec=BaseRecommender)
        unfitted.is_fitted = False

        hybrid = HybridRecommender(models={"collaborative": unfitted})
        matrix = sparse.csr_matrix((5, 5))

        # TODO: Assert that fit() raises an error when sub-models are not fitted

    def test_predict_combines_scores(self) -> None:
        """predict() should return a weighted combination of sub-model scores."""
        scores_cf = {(0, 1): 0.8, (0, 2): 0.6}
        scores_cb = {(0, 1): 0.5, (0, 2): 0.9}
        scores_nn = {(0, 1): 0.7, (0, 2): 0.4}

        models = {
            "collaborative": _make_mock_model("CF", scores_cf),
            "content_based": _make_mock_model("CB", scores_cb),
            "neural": _make_mock_model("NN", scores_nn),
        }
        weights = HybridWeights(collaborative=0.5, content_based=0.3, neural=0.2)
        hybrid = HybridRecommender(models=models, weights=weights)

        matrix = sparse.csr_matrix((5, 10))
        user_ids = np.arange(5)
        item_ids = np.arange(10)

        # TODO: Fit the hybrid model
        # TODO: Call predict(0, 1) and assert the result equals:
        #       0.5 * 0.8 + 0.3 * 0.5 + 0.2 * 0.7 = 0.69

    def test_recommend_returns_sorted_results(self) -> None:
        """recommend() should return items sorted by combined score descending."""
        # TODO: Set up mock models with known scores
        # TODO: Fit hybrid and call recommend()
        # TODO: Assert results are sorted by score descending

    def test_graceful_fallback_on_model_failure(self) -> None:
        """If one sub-model fails for a user, others should still produce results."""
        working = _make_mock_model("CF", {(0, 1): 0.8})
        failing = MagicMock(spec=BaseRecommender)
        failing.is_fitted = True
        failing.predict.side_effect = KeyError("Unknown user")

        models = {"collaborative": working, "content_based": failing}
        hybrid = HybridRecommender(models=models)

        # TODO: Fit the hybrid model
        # TODO: Assert predict(0, 1) still returns a score from the working model
        #       with re-normalized weights
