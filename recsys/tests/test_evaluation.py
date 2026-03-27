"""Tests for recommendation evaluation metrics."""

import numpy as np
import pytest

from recsys.evaluation.metrics import (
    catalog_coverage,
    hit_rate_at_k,
    intra_list_diversity,
    mean_reciprocal_rank,
    ndcg_at_k,
    novelty_at_k,
    precision_at_k,
    recall_at_k,
)


class TestPrecisionAtK:
    def test_perfect_precision(self) -> None:
        """All recommended items are relevant."""
        recommended = [1, 2, 3, 4, 5]
        relevant = {1, 2, 3, 4, 5}
        # TODO: Assert precision_at_k(recommended, relevant, k=5) == 1.0

    def test_zero_precision(self) -> None:
        """No recommended items are relevant."""
        recommended = [10, 11, 12, 13, 14]
        relevant = {1, 2, 3}
        # TODO: Assert precision_at_k(recommended, relevant, k=5) == 0.0

    def test_partial_precision(self) -> None:
        """Some recommended items are relevant."""
        recommended = [1, 10, 2, 11, 3]
        relevant = {1, 2, 3}
        # TODO: Assert precision_at_k(recommended, relevant, k=5) == 3/5

    def test_k_less_than_list_length(self) -> None:
        """Only top-k items should be considered."""
        recommended = [1, 2, 10, 11, 12]
        relevant = {1, 2, 3}
        # TODO: Assert precision_at_k(recommended, relevant, k=2) == 1.0


class TestRecallAtK:
    def test_full_recall(self) -> None:
        """All relevant items are in the recommendations."""
        recommended = [1, 2, 3, 10, 11]
        relevant = {1, 2, 3}
        # TODO: Assert recall_at_k(recommended, relevant, k=5) == 1.0

    def test_partial_recall(self) -> None:
        recommended = [1, 10, 11, 12, 13]
        relevant = {1, 2, 3}
        # TODO: Assert recall_at_k(recommended, relevant, k=5) ≈ 1/3

    def test_empty_relevant_set(self) -> None:
        recommended = [1, 2, 3]
        relevant: set[int] = set()
        # TODO: Assert recall_at_k returns 0.0 (not division by zero)


class TestNDCGAtK:
    def test_perfect_ranking(self) -> None:
        """All relevant items at the top positions."""
        recommended = [1, 2, 3, 10, 11]
        relevant = {1, 2, 3}
        # TODO: Assert ndcg_at_k(recommended, relevant, k=5) == 1.0

    def test_worst_ranking(self) -> None:
        """Relevant items at the bottom positions."""
        recommended = [10, 11, 1, 2, 3]
        relevant = {1, 2, 3}
        # TODO: Assert ndcg_at_k(recommended, relevant, k=5) < 1.0

    def test_single_relevant_item(self) -> None:
        """NDCG with one relevant item at different positions."""
        relevant = {1}
        at_top = ndcg_at_k([1, 2, 3, 4, 5], relevant, k=5)
        at_bottom = ndcg_at_k([2, 3, 4, 5, 1], relevant, k=5)
        # TODO: Assert at_top > at_bottom (higher rank = better NDCG)

    def test_empty_relevant_set(self) -> None:
        recommended = [1, 2, 3]
        relevant: set[int] = set()
        # TODO: Assert ndcg_at_k returns 0.0


class TestHitRateAtK:
    def test_hit(self) -> None:
        recommended = [1, 2, 3]
        relevant = {2}
        # TODO: Assert hit_rate_at_k(recommended, relevant, k=3) == 1.0

    def test_miss(self) -> None:
        recommended = [1, 2, 3]
        relevant = {5}
        # TODO: Assert hit_rate_at_k(recommended, relevant, k=3) == 0.0


class TestMRR:
    def test_first_position(self) -> None:
        """Relevant item at rank 1."""
        recommended = [1, 2, 3]
        relevant = {1}
        # TODO: Assert mean_reciprocal_rank(recommended, relevant) == 1.0

    def test_third_position(self) -> None:
        """Relevant item at rank 3."""
        recommended = [10, 11, 1, 12, 13]
        relevant = {1}
        # TODO: Assert mean_reciprocal_rank(recommended, relevant) ≈ 1/3

    def test_no_relevant(self) -> None:
        recommended = [10, 11, 12]
        relevant = {1}
        # TODO: Assert mean_reciprocal_rank(recommended, relevant) == 0.0


class TestCoverage:
    def test_full_coverage(self) -> None:
        all_recs = [[1, 2], [3, 4], [5]]
        # TODO: Assert catalog_coverage(all_recs, catalog_size=5) == 1.0

    def test_partial_coverage(self) -> None:
        all_recs = [[1, 2], [1, 3]]
        # TODO: Assert catalog_coverage(all_recs, catalog_size=10) == 0.3


class TestDiversity:
    def test_identical_items_zero_diversity(self) -> None:
        """Recommending identical feature vectors should give zero diversity."""
        features = np.array([[1.0, 0.0], [1.0, 0.0], [1.0, 0.0]])
        recommended = [0, 1, 2]
        # TODO: Assert intra_list_diversity(recommended, features) ≈ 0.0

    def test_orthogonal_items_max_diversity(self) -> None:
        """Orthogonal feature vectors should give maximum diversity."""
        features = np.eye(3)
        recommended = [0, 1, 2]
        # TODO: Assert intra_list_diversity(recommended, features) == 1.0


class TestNovelty:
    def test_popular_items_low_novelty(self) -> None:
        """Very popular items should have low novelty."""
        popularity = np.array([0.9, 0.8, 0.7, 0.01, 0.01])
        recommended = [0, 1, 2]
        # TODO: Compute novelty_at_k and assert it is relatively low

    def test_niche_items_high_novelty(self) -> None:
        """Rare items should have high novelty."""
        popularity = np.array([0.9, 0.8, 0.7, 0.01, 0.01])
        recommended = [3, 4, 0]
        # TODO: Compute novelty_at_k and assert it is higher than for popular items
