"""Recommendation evaluation metrics."""

import numpy as np


def precision_at_k(recommended: list[int], relevant: set[int], k: int) -> float:
    """Precision@K: fraction of top-K recommendations that are relevant.

    Args:
        recommended: Ordered list of recommended item IDs.
        relevant: Set of ground-truth relevant item IDs.
        k: Cutoff rank.

    Returns:
        Precision@K score in [0, 1].
    """
    # TODO: Take the top-k recommendations
    # TODO: Count how many are in the relevant set
    # TODO: Return count / k
    raise NotImplementedError


def recall_at_k(recommended: list[int], relevant: set[int], k: int) -> float:
    """Recall@K: fraction of relevant items that appear in top-K recommendations.

    Args:
        recommended: Ordered list of recommended item IDs.
        relevant: Set of ground-truth relevant item IDs.
        k: Cutoff rank.

    Returns:
        Recall@K score in [0, 1]. Returns 0.0 if relevant set is empty.
    """
    # TODO: Take the top-k recommendations
    # TODO: Count how many relevant items are captured
    # TODO: Return count / |relevant| (handle empty relevant set)
    raise NotImplementedError


def ndcg_at_k(recommended: list[int], relevant: set[int], k: int) -> float:
    """Normalized Discounted Cumulative Gain at K.

    Uses binary relevance: 1 if item is in relevant set, 0 otherwise.
    DCG@K = Σ (rel_i / log2(i+2)) for i in 0..K-1
    IDCG@K = best possible DCG@K with |relevant| items.

    Args:
        recommended: Ordered list of recommended item IDs.
        relevant: Set of ground-truth relevant item IDs.
        k: Cutoff rank.

    Returns:
        NDCG@K score in [0, 1]. Returns 0.0 if relevant set is empty.
    """
    # TODO: Compute DCG@K using binary relevance and log2 discount
    # TODO: Compute IDCG@K (ideal DCG with min(k, |relevant|) hits at top positions)
    # TODO: Return DCG / IDCG (handle IDCG = 0)
    raise NotImplementedError


def hit_rate_at_k(recommended: list[int], relevant: set[int], k: int) -> float:
    """Hit Rate@K: 1 if at least one relevant item is in top-K, else 0.

    Args:
        recommended: Ordered list of recommended item IDs.
        relevant: Set of ground-truth relevant item IDs.
        k: Cutoff rank.

    Returns:
        1.0 or 0.0.
    """
    # TODO: Check if any of the top-k recommendations are in the relevant set
    raise NotImplementedError


def mean_reciprocal_rank(recommended: list[int], relevant: set[int]) -> float:
    """Mean Reciprocal Rank: 1 / rank of the first relevant item.

    Args:
        recommended: Ordered list of recommended item IDs.
        relevant: Set of ground-truth relevant item IDs.

    Returns:
        MRR score in (0, 1]. Returns 0.0 if no relevant item is found.
    """
    # TODO: Find the rank (1-indexed) of the first relevant item in the list
    # TODO: Return 1 / rank, or 0.0 if none found
    raise NotImplementedError


def catalog_coverage(
    all_recommendations: list[list[int]],
    catalog_size: int,
) -> float:
    """Coverage: fraction of the item catalog recommended to at least one user.

    Args:
        all_recommendations: List of recommendation lists (one per user).
        catalog_size: Total number of items in the catalog.

    Returns:
        Coverage in [0, 1].
    """
    # TODO: Collect all unique item IDs across all users' recommendations
    # TODO: Return |unique items| / catalog_size
    raise NotImplementedError


def intra_list_diversity(
    recommended: list[int],
    item_features: np.ndarray,
) -> float:
    """Average pairwise distance between recommended items.

    Uses cosine distance (1 - cosine_similarity) between item feature vectors.

    Args:
        recommended: List of recommended item indices.
        item_features: Feature matrix of shape (n_items, n_features).

    Returns:
        Average pairwise cosine distance. Returns 0.0 for single-item lists.
    """
    # TODO: Extract feature vectors for the recommended items
    # TODO: Compute pairwise cosine distances
    # TODO: Return the mean of the upper triangle of the distance matrix
    raise NotImplementedError


def novelty_at_k(
    recommended: list[int],
    item_popularity: np.ndarray,
    k: int,
) -> float:
    """Novelty@K: average self-information of recommended items.

    Novelty = mean(-log2(popularity)) for top-K items.
    Less popular items contribute higher novelty.

    Args:
        recommended: Ordered list of recommended item IDs.
        item_popularity: Array of item popularity scores (fraction of users who interacted).
        k: Cutoff rank.

    Returns:
        Average novelty score. Higher = more novel.
    """
    # TODO: Take the top-k recommended items
    # TODO: Look up each item's popularity, clip to avoid log(0)
    # TODO: Compute mean(-log2(popularity)) across the k items
    raise NotImplementedError
