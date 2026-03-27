"""Synthetic ranking data generation.

Generates realistic-looking ranking datasets with controlled properties
for testing and development without needing real labeled data.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ranking.data.data_loader import RankingDataset


@dataclass
class GeneratorConfig:
    """Configuration for synthetic data generation."""

    num_queries: int = 100
    docs_per_query: int = 50
    num_features: int = 35
    relevance_levels: int = 5
    noise_level: float = 0.3
    relevant_doc_ratio: float = 0.3
    seed: int = 42


class SyntheticDataGenerator:
    """Generates synthetic ranking datasets for testing.

    Creates feature matrices where a known linear combination of features
    correlates with relevance labels, with controllable noise. This allows
    validating that models can learn the signal.
    """

    def __init__(self, config: GeneratorConfig | None = None) -> None:
        self.config = config or GeneratorConfig()
        self.rng = np.random.default_rng(self.config.seed)
        self._true_weights: np.ndarray | None = None

    def generate(self) -> RankingDataset:
        """Generate a complete synthetic ranking dataset.

        The generation process:
        1. Sample random feature vectors for each query-document pair
        2. Compute a "true" relevance signal from a hidden linear model
        3. Add noise and discretize into relevance grades
        4. Ensure each query has a mix of relevant and non-relevant documents

        Returns:
            RankingDataset with synthetic features, labels, and query IDs.
        """
        # TODO: Implement synthetic data generation
        # 1. Generate self._true_weights as the hidden scoring function
        # 2. For each query, generate docs_per_query feature vectors
        # 3. Compute true scores as features @ weights + noise
        # 4. Discretize scores into integer relevance labels (0 to relevance_levels-1)
        # 5. Assemble into contiguous arrays with query IDs
        raise NotImplementedError

    def generate_query_documents(
        self, query_id: int
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Generate synthetic documents for a single query.

        Args:
            query_id: Integer query identifier.

        Returns:
            Tuple of (features, labels, query_ids) for this query's documents.
        """
        # TODO: Implement per-query document generation
        # 1. Sample feature vectors from a distribution centered on a query-specific mean
        # 2. Compute scores and discretize to labels
        # 3. Return arrays with constant query_id
        raise NotImplementedError

    @property
    def true_weights(self) -> np.ndarray:
        """The hidden feature weights used for generating relevance labels.

        Useful for validating that a trained model recovers the correct
        feature importance ordering.
        """
        if self._true_weights is None:
            self._true_weights = self.rng.standard_normal(self.config.num_features)
        return self._true_weights
