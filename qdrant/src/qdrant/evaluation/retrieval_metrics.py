"""Retrieval evaluation metrics: precision, recall, MRR, NDCG."""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def precision_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    """Compute precision@k: fraction of top-k results that are relevant.

    Args:
        retrieved_ids: Ordered list of retrieved document IDs.
        relevant_ids: Set of ground-truth relevant document IDs.
        k: Cutoff rank.

    Returns:
        Precision@k score (0.0 to 1.0).
    """
    # TODO: Implement precision@k
    # Count how many of the top-k retrieved IDs are in relevant_ids
    # Return count / k
    pass


def recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    """Compute recall@k: fraction of relevant docs found in top-k.

    Args:
        retrieved_ids: Ordered list of retrieved document IDs.
        relevant_ids: Set of ground-truth relevant document IDs.
        k: Cutoff rank.

    Returns:
        Recall@k score (0.0 to 1.0).
    """
    # TODO: Implement recall@k
    # Count how many relevant IDs appear in top-k
    # Return count / len(relevant_ids)
    pass


def mean_reciprocal_rank(
    retrieved_ids: list[str],
    relevant_ids: set[str],
) -> float:
    """Compute Mean Reciprocal Rank (MRR).

    The reciprocal of the rank of the first relevant result.

    Args:
        retrieved_ids: Ordered list of retrieved document IDs.
        relevant_ids: Set of ground-truth relevant document IDs.

    Returns:
        MRR score (0.0 to 1.0). Returns 0 if no relevant doc is found.
    """
    # TODO: Implement MRR
    # Find the rank (1-indexed) of the first relevant document
    # Return 1 / rank, or 0 if none found
    pass


def ndcg_at_k(
    retrieved_ids: list[str],
    relevance_scores: dict[str, float],
    k: int,
) -> float:
    """Compute Normalized Discounted Cumulative Gain at k (NDCG@k).

    Uses graded relevance scores rather than binary relevance.

    Args:
        retrieved_ids: Ordered list of retrieved document IDs.
        relevance_scores: Mapping of doc ID to relevance grade (e.g., 0-3).
        k: Cutoff rank.

    Returns:
        NDCG@k score (0.0 to 1.0).
    """
    # TODO: Implement NDCG@k
    # 1. Compute DCG@k = Σ (2^rel_i - 1) / log2(i + 1) for i in 1..k
    # 2. Compute ideal DCG@k (sort relevance scores descending)
    # 3. Return DCG@k / IDCG@k (handle IDCG = 0)
    pass


def average_precision(
    retrieved_ids: list[str],
    relevant_ids: set[str],
) -> float:
    """Compute Average Precision (AP) for a single query.

    AP = (1/|relevant|) * Σ P(k) * rel(k) for k=1..n

    Args:
        retrieved_ids: Ordered list of retrieved document IDs.
        relevant_ids: Set of ground-truth relevant document IDs.

    Returns:
        Average precision score (0.0 to 1.0).
    """
    # TODO: Implement average precision
    # For each position k where the result is relevant:
    #   Add precision_at_k(retrieved, relevant, k) to running sum
    # Divide by total number of relevant documents
    pass


def evaluate_retrieval(
    queries: list[dict[str, Any]],
    search_fn: callable,
    k_values: list[int] | None = None,
) -> dict[str, float]:
    """Run full retrieval evaluation over a set of queries.

    Args:
        queries: List of {"query": str, "relevant_ids": set[str]} dicts.
        search_fn: Function that takes a query string and returns list of IDs.
        k_values: K values to evaluate at. Defaults to [1, 3, 5, 10].

    Returns:
        Dictionary of metric_name -> average score.
    """
    # TODO: Implement batch evaluation
    # 1. For each query, run search_fn and get retrieved IDs
    # 2. Compute all metrics at each k value
    # 3. Average across queries
    # 4. Return as {"precision@1": X, "recall@5": Y, "mrr": Z, ...}
    pass
