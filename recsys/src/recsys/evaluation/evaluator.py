"""Evaluation pipeline with proper negative sampling for recommendation models."""

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy import sparse

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
from recsys.models.base import BaseRecommender


@dataclass
class EvaluationConfig:
    """Configuration for the evaluation pipeline."""

    k_values: list[int] = field(default_factory=lambda: [5, 10, 20])
    n_negative_samples: int = 100
    random_seed: int = 42


@dataclass
class EvaluationResults:
    """Container for evaluation results across metrics and K values."""

    metrics: dict[str, dict[int, float]] = field(default_factory=dict)
    per_user_metrics: pd.DataFrame | None = None

    def summary(self) -> pd.DataFrame:
        """Return a summary DataFrame of all metrics."""
        rows = []
        for metric_name, k_values in self.metrics.items():
            for k, value in k_values.items():
                rows.append({"metric": metric_name, "k": k, "value": value})
        return pd.DataFrame(rows)


class RecommenderEvaluator:
    """Evaluates a recommender model on held-out test interactions.

    Implements the sampled metrics protocol: for each test user, the relevant item(s)
    are mixed with N randomly sampled negative items, and the model is asked to rank
    them. Metrics are computed on this ranking.
    """

    def __init__(self, config: EvaluationConfig | None = None) -> None:
        self.config = config or EvaluationConfig()
        self.rng = np.random.default_rng(self.config.random_seed)

    def evaluate(
        self,
        model: BaseRecommender,
        train_interactions: sparse.csr_matrix,
        test_interactions: pd.DataFrame,
        item_features: np.ndarray | None = None,
    ) -> EvaluationResults:
        """Run full evaluation of a recommender model.

        Args:
            model: Fitted recommender model.
            train_interactions: Sparse training interaction matrix.
            test_interactions: DataFrame of test interactions (user_id, item_id).
            item_features: Optional item feature matrix for diversity computation.

        Returns:
            EvaluationResults with per-metric, per-K results.
        """
        # TODO: Group test interactions by user
        # TODO: For each test user:
        #   1. Get their relevant (test) items
        #   2. Sample n_negative_samples items not in train or test for this user
        #   3. Ask the model to rank relevant + negative items
        #   4. Compute per-user metrics at each K value
        # TODO: Aggregate per-user metrics into macro-averages
        # TODO: Compute system-level metrics (coverage, diversity, novelty)
        # TODO: Return EvaluationResults
        raise NotImplementedError

    def _sample_negatives_for_user(
        self,
        user_idx: int,
        train_matrix: sparse.csr_matrix,
        test_items: set[int],
        n_items: int,
    ) -> np.ndarray:
        """Sample negative items for evaluation of a single user.

        Items in the user's training set and test set are excluded.

        Args:
            user_idx: Matrix index of the user.
            train_matrix: Sparse training interaction matrix.
            test_items: Set of test item indices for this user.
            n_items: Total number of items.

        Returns:
            Array of sampled negative item indices.
        """
        # TODO: Get items the user interacted with in training
        # TODO: Exclude those and the test items from the candidate pool
        # TODO: Sample min(n_negative_samples, |candidates|) items uniformly
        raise NotImplementedError

    def compare_models(
        self,
        models: dict[str, BaseRecommender],
        train_interactions: sparse.csr_matrix,
        test_interactions: pd.DataFrame,
    ) -> pd.DataFrame:
        """Evaluate and compare multiple models side by side.

        Args:
            models: Dict mapping model names to fitted models.
            train_interactions: Sparse training interaction matrix.
            test_interactions: Test interactions DataFrame.

        Returns:
            DataFrame with model names as rows and metrics as columns.
        """
        # TODO: Evaluate each model using self.evaluate()
        # TODO: Combine results into a comparison DataFrame
        raise NotImplementedError
