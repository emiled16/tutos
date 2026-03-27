"""Data loading for ranking datasets.

Supports MSLR-WEB format (Microsoft Learning to Rank) and a simpler
custom CSV format for loading query-document feature matrices.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class RankingDataset:
    """Loaded ranking dataset ready for model training."""

    features: np.ndarray
    labels: np.ndarray
    query_ids: np.ndarray
    feature_names: list[str] | None = None

    @property
    def num_queries(self) -> int:
        return len(np.unique(self.query_ids))

    @property
    def num_samples(self) -> int:
        return len(self.labels)

    @property
    def num_features(self) -> int:
        return self.features.shape[1]

    def get_query(self, query_id: int) -> tuple[np.ndarray, np.ndarray]:
        """Get features and labels for a single query.

        Args:
            query_id: The query identifier.

        Returns:
            Tuple of (features, labels) for documents in this query.
        """
        mask = self.query_ids == query_id
        return self.features[mask], self.labels[mask]

    def split_by_query(
        self, train_ratio: float = 0.8, seed: int = 42
    ) -> tuple[RankingDataset, RankingDataset]:
        """Split dataset by query into train and test sets.

        Ensures all documents for a query stay in the same split.

        Args:
            train_ratio: Fraction of queries for training.
            seed: Random seed for reproducibility.

        Returns:
            Tuple of (train_dataset, test_dataset).
        """
        # TODO: Implement query-level train/test split
        # 1. Get unique query IDs
        # 2. Shuffle and split query IDs by train_ratio
        # 3. Create boolean masks for train/test samples
        # 4. Return two RankingDataset instances
        raise NotImplementedError


def load_mslr(path: Path, num_features: int = 136) -> RankingDataset:
    """Load a dataset in MSLR-WEB format (SVM-light style).

    Format: label qid:value 1:value 2:value ... n:value
    Example: 2 qid:10 1:0.5 2:1.0 3:0.3

    Args:
        path: Path to the data file.
        num_features: Number of features per sample (136 for MSLR-WEB10K).

    Returns:
        RankingDataset with parsed features, labels, and query IDs.
    """
    # TODO: Implement MSLR-WEB format parser
    # 1. Read file line by line
    # 2. Parse label (first token), qid (second token after "qid:"), features (remaining tokens)
    # 3. Handle missing features by filling with zeros
    # 4. Return RankingDataset with numpy arrays
    raise NotImplementedError


def load_csv(
    path: Path,
    label_col: str = "relevance",
    query_col: str = "query_id",
    feature_cols: list[str] | None = None,
) -> RankingDataset:
    """Load a ranking dataset from CSV format.

    Args:
        path: Path to the CSV file.
        label_col: Column name for relevance labels.
        query_col: Column name for query identifiers.
        feature_cols: Feature column names. If None, uses all columns
            except label_col and query_col.

    Returns:
        RankingDataset with parsed data.
    """
    # TODO: Implement CSV loader
    # 1. Read CSV with pandas
    # 2. Extract labels, query_ids, and features
    # 3. If feature_cols is None, infer from remaining columns
    # 4. Sort by query_id to ensure contiguous grouping
    raise NotImplementedError
