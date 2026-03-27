"""Tests for IR evaluation metrics."""

from __future__ import annotations

import numpy as np
import pytest

from ranking.evaluation.metrics import (
    average_precision,
    dcg_at_k,
    mean_reciprocal_rank,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)


class TestDCG:
    def test_perfect_ranking(self) -> None:
        # TODO: Test DCG with ideal ordering [3, 2, 1, 0]
        relevances = np.array([3, 2, 1, 0])
        result = dcg_at_k(relevances, k=4)
        expected = (2**3 - 1) / np.log2(2) + (2**2 - 1) / np.log2(3) + (2**1 - 1) / np.log2(4)
        assert result == pytest.approx(expected, rel=1e-6)

    def test_all_irrelevant(self) -> None:
        # TODO: Test that DCG is 0 when all documents have relevance 0
        relevances = np.array([0, 0, 0, 0])
        assert dcg_at_k(relevances, k=4) == pytest.approx(0.0)

    def test_k_greater_than_list_length(self) -> None:
        # TODO: Test that DCG handles k larger than the list gracefully
        relevances = np.array([3, 1])
        result = dcg_at_k(relevances, k=5)
        expected = dcg_at_k(relevances, k=2)
        assert result == pytest.approx(expected)


class TestNDCG:
    def test_perfect_ranking_gives_one(self) -> None:
        # TODO: Test that a perfectly sorted list yields NDCG = 1.0
        relevances = np.array([3, 2, 1, 0])
        assert ndcg_at_k(relevances, k=4) == pytest.approx(1.0)

    def test_reversed_ranking(self) -> None:
        # TODO: Test that a reversed ranking gives NDCG < 1.0
        relevances = np.array([0, 1, 2, 3])
        assert ndcg_at_k(relevances, k=4) < 1.0

    def test_all_irrelevant_gives_zero(self) -> None:
        # TODO: Test that NDCG is 0 when no relevant documents exist
        relevances = np.array([0, 0, 0])
        assert ndcg_at_k(relevances, k=3) == pytest.approx(0.0)

    def test_single_relevant_at_top(self) -> None:
        # TODO: Test NDCG when only one relevant doc exists and it's at position 1
        relevances = np.array([1, 0, 0, 0])
        assert ndcg_at_k(relevances, k=4) == pytest.approx(1.0)

    def test_ndcg_at_1(self) -> None:
        # TODO: Test NDCG@1 is 1.0 when the top document is the most relevant
        relevances = np.array([3, 1, 0])
        assert ndcg_at_k(relevances, k=1) == pytest.approx(1.0)


class TestMRR:
    def test_first_result_relevant(self) -> None:
        # TODO: Test MRR = 1.0 when the first result is relevant
        relevances = np.array([1, 0, 0])
        assert mean_reciprocal_rank(relevances) == pytest.approx(1.0)

    def test_second_result_relevant(self) -> None:
        # TODO: Test MRR = 0.5 when the first relevant result is at position 2
        relevances = np.array([0, 1, 0])
        assert mean_reciprocal_rank(relevances) == pytest.approx(0.5)

    def test_no_relevant_results(self) -> None:
        # TODO: Test MRR = 0 when no results are relevant
        relevances = np.array([0, 0, 0])
        assert mean_reciprocal_rank(relevances) == pytest.approx(0.0)


class TestAveragePrecision:
    def test_all_relevant_at_top(self) -> None:
        # TODO: Test AP = 1.0 when all relevant docs are ranked first
        relevances = np.array([1, 1, 0, 0])
        assert average_precision(relevances) == pytest.approx(1.0)

    def test_relevant_docs_scattered(self) -> None:
        # TODO: Test AP with relevant docs at positions 1, 3, 5
        # AP = (1/3) * (1/1 + 2/3 + 3/5) = (1/3) * (1.0 + 0.667 + 0.6) = 0.7556
        relevances = np.array([1, 0, 1, 0, 1])
        expected = (1 / 3) * (1.0 + 2 / 3 + 3 / 5)
        assert average_precision(relevances) == pytest.approx(expected, rel=1e-4)

    def test_no_relevant_docs(self) -> None:
        # TODO: Test AP = 0 when no documents are relevant
        relevances = np.array([0, 0, 0])
        assert average_precision(relevances) == pytest.approx(0.0)


class TestPrecisionAtK:
    def test_all_relevant(self) -> None:
        # TODO: Test P@3 = 1.0 when all top 3 are relevant
        relevances = np.array([1, 1, 1, 0, 0])
        assert precision_at_k(relevances, k=3) == pytest.approx(1.0)

    def test_none_relevant(self) -> None:
        # TODO: Test P@3 = 0 when no top 3 are relevant
        relevances = np.array([0, 0, 0, 1, 1])
        assert precision_at_k(relevances, k=3) == pytest.approx(0.0)

    def test_partial_relevant(self) -> None:
        # TODO: Test P@4 = 0.5 when 2 of top 4 are relevant
        relevances = np.array([1, 0, 1, 0, 0])
        assert precision_at_k(relevances, k=4) == pytest.approx(0.5)


class TestRecallAtK:
    def test_all_relevant_retrieved(self) -> None:
        # TODO: Test R@3 = 1.0 when all relevant docs are in top 3
        relevances = np.array([1, 1, 0, 0])
        assert recall_at_k(relevances, k=3) == pytest.approx(1.0)

    def test_partial_recall(self) -> None:
        # TODO: Test R@2 = 0.5 when 1 of 2 relevant docs is in top 2
        relevances = np.array([1, 0, 1, 0])
        assert recall_at_k(relevances, k=2) == pytest.approx(0.5)

    def test_no_relevant_docs(self) -> None:
        # TODO: Test R@k = 0 when no relevant documents exist
        relevances = np.array([0, 0, 0])
        assert recall_at_k(relevances, k=2) == pytest.approx(0.0)
