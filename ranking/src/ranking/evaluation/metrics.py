"""Information retrieval evaluation metrics.

Implements standard IR ranking metrics: NDCG@k, MRR, MAP, Precision@k,
and Recall@k. All metrics operate on arrays of relevance labels sorted
by predicted rank (position 0 = highest ranked).
"""

from __future__ import annotations

import math

import numpy as np


def dcg_at_k(relevances: np.ndarray, k: int) -> float:
    """Compute Discounted Cumulative Gain at cutoff k.

    DCG@k = Σ_{i=1}^{k} (2^{rel_i} - 1) / log2(i + 1)

    Args:
        relevances: Array of relevance labels in rank order.
        k: Cutoff position (1-based).

    Returns:
        DCG value.
    """
    # TODO: Implement DCG@k using the standard exponential gain formula
    raise NotImplementedError


def ndcg_at_k(relevances: np.ndarray, k: int) -> float:
    """Compute Normalized Discounted Cumulative Gain at cutoff k.

    NDCG@k = DCG@k / IDCG@k where IDCG is the DCG of the ideal ranking.
    Returns 0.0 when no relevant documents exist.

    Args:
        relevances: Array of relevance labels in predicted rank order.
        k: Cutoff position.

    Returns:
        NDCG value in [0, 1].
    """
    # TODO: Implement NDCG@k
    # 1. Compute DCG@k for the given ordering
    # 2. Compute IDCG@k by sorting relevances descending and computing DCG
    # 3. Return DCG / IDCG, handling the case where IDCG = 0
    raise NotImplementedError


def mean_reciprocal_rank(relevances: np.ndarray, threshold: float = 1.0) -> float:
    """Compute Reciprocal Rank for a single query.

    RR = 1 / rank_of_first_relevant_document.
    A document is relevant if its label >= threshold.

    Args:
        relevances: Array of relevance labels in predicted rank order.
        threshold: Minimum relevance label to be considered relevant.

    Returns:
        Reciprocal rank, or 0.0 if no relevant documents.
    """
    # TODO: Implement reciprocal rank by finding the first relevant document
    raise NotImplementedError


def average_precision(relevances: np.ndarray, threshold: float = 1.0) -> float:
    """Compute Average Precision for a single query.

    AP = (1/R) Σ_{k=1}^{n} P(k) · rel(k)
    where R is total relevant documents and P(k) is precision at position k.

    Args:
        relevances: Array of relevance labels in predicted rank order.
        threshold: Minimum relevance label to be considered relevant.

    Returns:
        Average precision, or 0.0 if no relevant documents.
    """
    # TODO: Implement AP by accumulating precision at each relevant position
    # 1. Iterate through ranked positions
    # 2. At each relevant position, compute precision (relevant_so_far / position)
    # 3. Average the precision values over total relevant documents
    raise NotImplementedError


def precision_at_k(relevances: np.ndarray, k: int, threshold: float = 1.0) -> float:
    """Compute Precision at cutoff k.

    P@k = |relevant in top k| / k

    Args:
        relevances: Array of relevance labels in predicted rank order.
        k: Cutoff position.
        threshold: Minimum relevance label to be considered relevant.

    Returns:
        Precision value in [0, 1].
    """
    # TODO: Implement P@k by counting relevant documents in the top k
    raise NotImplementedError


def recall_at_k(relevances: np.ndarray, k: int, threshold: float = 1.0) -> float:
    """Compute Recall at cutoff k.

    R@k = |relevant in top k| / |total relevant|

    Args:
        relevances: Array of relevance labels in predicted rank order.
        k: Cutoff position.
        threshold: Minimum relevance label to be considered relevant.

    Returns:
        Recall value in [0, 1], or 0.0 if no relevant documents exist.
    """
    # TODO: Implement R@k by counting relevant documents in top k vs total relevant
    raise NotImplementedError
