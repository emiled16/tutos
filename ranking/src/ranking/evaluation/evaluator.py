"""Evaluation pipeline for ranking models.

Evaluates a ranking model across multiple queries using configurable
metrics and cutoffs, producing per-query and aggregate results.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd

from ranking.evaluation.metrics import (
    average_precision,
    mean_reciprocal_rank,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)


@dataclass
class EvaluationConfig:
    """Configuration for the evaluation pipeline."""

    cutoffs: list[int] = field(default_factory=lambda: [1, 3, 5, 10, 20])
    relevance_threshold: float = 1.0
    metrics: list[str] = field(
        default_factory=lambda: ["ndcg", "mrr", "map", "precision", "recall"]
    )


@dataclass
class QueryResult:
    """Evaluation results for a single query."""

    query_id: str
    metrics: dict[str, float]
    num_docs: int
    num_relevant: int


@dataclass
class EvaluationReport:
    """Aggregate evaluation report across all queries."""

    per_query: list[QueryResult]
    aggregate: dict[str, float]
    config: EvaluationConfig


METRIC_FUNCTIONS: dict[str, Callable] = {
    "ndcg": ndcg_at_k,
    "precision": precision_at_k,
    "recall": recall_at_k,
}


class RankingEvaluator:
    """Evaluates ranking quality across multiple queries and metrics.

    Computes per-query metrics at each configured cutoff, then aggregates
    across queries using macro-averaging.
    """

    def __init__(self, config: EvaluationConfig | None = None) -> None:
        self.config = config or EvaluationConfig()

    def evaluate(
        self,
        predictions: dict[str, np.ndarray],
        relevances: dict[str, np.ndarray],
    ) -> EvaluationReport:
        """Evaluate a ranker's output across all queries.

        Args:
            predictions: Mapping from query_id to predicted scores
                (higher = more relevant).
            relevances: Mapping from query_id to ground-truth relevance labels,
                aligned with the same document ordering as predictions.

        Returns:
            EvaluationReport with per-query and aggregate results.
        """
        # TODO: Implement full evaluation pipeline
        # 1. For each query, sort documents by predicted score descending
        # 2. Reorder relevance labels to match the predicted ranking
        # 3. Compute each configured metric at each cutoff via _evaluate_query
        # 4. Aggregate per-query metrics via _aggregate
        raise NotImplementedError

    def _evaluate_query(
        self,
        query_id: str,
        ranked_relevances: np.ndarray,
    ) -> QueryResult:
        """Compute all configured metrics for a single query.

        Args:
            query_id: Query identifier.
            ranked_relevances: Relevance labels sorted by predicted rank.

        Returns:
            QueryResult with all metric values.
        """
        # TODO: Implement per-query evaluation
        # 1. For each metric in self.config.metrics:
        #    - If metric has a cutoff variant (ndcg, precision, recall),
        #      compute at each cutoff in self.config.cutoffs
        #    - If metric is mrr or map, compute once (no cutoff)
        # 2. Count relevant documents using self.config.relevance_threshold
        raise NotImplementedError

    def _aggregate(self, query_results: list[QueryResult]) -> dict[str, float]:
        """Macro-average metrics across all queries.

        Args:
            query_results: Per-query evaluation results.

        Returns:
            Dict mapping metric names to their mean values across queries.
        """
        # TODO: Implement macro-averaging across queries
        raise NotImplementedError

    def to_dataframe(self, report: EvaluationReport) -> pd.DataFrame:
        """Convert per-query results to a DataFrame for analysis.

        Args:
            report: Evaluation report.

        Returns:
            DataFrame with one row per query and one column per metric.
        """
        # TODO: Implement DataFrame conversion from report.per_query
        raise NotImplementedError
