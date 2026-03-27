"""Tests for ranking model training and prediction."""

from __future__ import annotations

import numpy as np
import pytest

from ranking.data.data_generator import GeneratorConfig, SyntheticDataGenerator
from ranking.models.lambdamart import LambdaMARTConfig, LambdaMARTRanker
from ranking.models.pairwise import PairwiseConfig, PairwiseRanker
from ranking.models.pointwise import PointwiseConfig, PointwiseRanker


@pytest.fixture
def synthetic_data():
    """Generate a small synthetic dataset for model testing."""
    config = GeneratorConfig(
        num_queries=20,
        docs_per_query=30,
        num_features=10,
        seed=42,
    )
    generator = SyntheticDataGenerator(config)
    return generator.generate()


class TestPointwiseRanker:
    def test_fit_and_predict_shape(self, synthetic_data) -> None:
        # TODO: Test that fit succeeds and predict returns correct shape
        config = PointwiseConfig(n_estimators=50, max_depth=3)
        ranker = PointwiseRanker(config)
        ranker.fit(synthetic_data.features, synthetic_data.labels, synthetic_data.query_ids)
        preds = ranker.predict(synthetic_data.features)
        assert preds.shape == (synthetic_data.num_samples,)

    def test_rank_returns_valid_indices(self, synthetic_data) -> None:
        # TODO: Test that rank returns a valid permutation of document indices
        config = PointwiseConfig(n_estimators=50, max_depth=3)
        ranker = PointwiseRanker(config)
        query_features, query_labels = synthetic_data.get_query(0)
        ranker.fit(synthetic_data.features, synthetic_data.labels, synthetic_data.query_ids)
        indices = ranker.rank(query_features)
        assert set(indices) == set(range(len(query_features)))

    def test_predict_without_fit_raises(self) -> None:
        # TODO: Test that predict raises RuntimeError before training
        ranker = PointwiseRanker()
        with pytest.raises(RuntimeError):
            ranker.predict(np.zeros((5, 10)))


class TestPairwiseRanker:
    def test_fit_and_predict_shape(self, synthetic_data) -> None:
        # TODO: Test that pairwise model trains and produces correct output shape
        config = PairwiseConfig(n_estimators=50, max_depth=3, max_pairs_per_query=100)
        ranker = PairwiseRanker(config)
        ranker.fit(synthetic_data.features, synthetic_data.labels, synthetic_data.query_ids)
        preds = ranker.predict(synthetic_data.features)
        assert preds.shape == (synthetic_data.num_samples,)

    def test_pair_generation_produces_valid_pairs(self, synthetic_data) -> None:
        # TODO: Test that _generate_pairs creates pairs only where labels differ
        config = PairwiseConfig(max_pairs_per_query=50)
        ranker = PairwiseRanker(config)
        pair_features, pair_labels = ranker._generate_pairs(
            synthetic_data.features, synthetic_data.labels, synthetic_data.query_ids
        )
        assert len(pair_features) == len(pair_labels)
        assert set(np.unique(pair_labels)).issubset({0, 1})

    def test_predict_without_fit_raises(self) -> None:
        # TODO: Test that predict raises before training
        ranker = PairwiseRanker()
        with pytest.raises(RuntimeError):
            ranker.predict(np.zeros((5, 10)))


class TestLambdaMARTRanker:
    def test_fit_and_predict_shape(self, synthetic_data) -> None:
        # TODO: Test that LambdaMART trains and produces correct output shape
        config = LambdaMARTConfig(n_estimators=50, num_leaves=15)
        ranker = LambdaMARTRanker(config)
        ranker.fit(synthetic_data.features, synthetic_data.labels, synthetic_data.query_ids)
        preds = ranker.predict(synthetic_data.features)
        assert preds.shape == (synthetic_data.num_samples,)

    def test_query_ids_to_groups(self) -> None:
        # TODO: Test that contiguous query IDs are correctly converted to group sizes
        query_ids = np.array([0, 0, 0, 1, 1, 2, 2, 2, 2])
        groups = LambdaMARTRanker._query_ids_to_groups(query_ids)
        assert groups == [3, 2, 4]

    def test_rank_returns_valid_indices(self, synthetic_data) -> None:
        # TODO: Test that rank returns valid permutation indices
        config = LambdaMARTConfig(n_estimators=50, num_leaves=15)
        ranker = LambdaMARTRanker(config)
        ranker.fit(synthetic_data.features, synthetic_data.labels, synthetic_data.query_ids)
        query_features, _ = synthetic_data.get_query(0)
        indices = ranker.rank(query_features)
        assert set(indices) == set(range(len(query_features)))

    def test_feature_importance_keys(self, synthetic_data) -> None:
        # TODO: Test that feature_importance returns a dict with expected keys
        config = LambdaMARTConfig(n_estimators=50, num_leaves=15)
        ranker = LambdaMARTRanker(config)
        ranker.fit(synthetic_data.features, synthetic_data.labels, synthetic_data.query_ids)
        importance = ranker.feature_importance()
        assert isinstance(importance, dict)
        assert len(importance) > 0

    def test_predict_without_fit_raises(self) -> None:
        # TODO: Test that predict raises before training
        ranker = LambdaMARTRanker()
        with pytest.raises(RuntimeError):
            ranker.predict(np.zeros((5, 10)))
