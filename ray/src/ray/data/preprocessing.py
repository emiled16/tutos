"""Data preprocessing with Ray actors for stateful transforms."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd
import ray


@dataclass
class NormalizationStats:
    """Stores per-column mean and standard deviation for normalization."""

    mean: dict[str, float] = field(default_factory=dict)
    std: dict[str, float] = field(default_factory=dict)


@ray.remote
class PreprocessingActor:
    """A stateful Ray actor that fits and applies preprocessing transforms.

    The actor maintains fitted statistics (e.g., mean/std for normalization,
    category mappings for encoding) so that the same transform can be applied
    consistently to train and validation data.
    """

    def __init__(self) -> None:
        self.normalization_stats: NormalizationStats | None = None
        self.category_mappings: dict[str, dict[str, int]] = {}

    def fit_normalizer(
        self, df: pd.DataFrame, columns: list[str]
    ) -> NormalizationStats:
        """Compute mean and std from the given DataFrame columns.

        Args:
            df: Training data as a Pandas DataFrame.
            columns: Column names to compute statistics for.

        Returns:
            The fitted :class:`NormalizationStats`.
        """
        # TODO: Compute mean and std for each column, store in
        #       self.normalization_stats, and return the stats object
        raise NotImplementedError

    def transform_normalize(self, batch: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
        """Apply z-score normalization to a batch using fitted statistics.

        Args:
            batch: Column-name → numpy array mapping (a Ray Data batch).

        Returns:
            The batch with normalized columns.

        Raises:
            RuntimeError: If ``fit_normalizer`` has not been called.
        """
        # TODO: Normalize each column in batch using self.normalization_stats.
        #       Raise RuntimeError if stats are not fitted yet.
        raise NotImplementedError

    def fit_encoder(
        self, df: pd.DataFrame, columns: list[str]
    ) -> dict[str, dict[str, int]]:
        """Build category-to-integer mappings for the given columns.

        Args:
            df: Training data.
            columns: Categorical column names.

        Returns:
            A dict mapping column name → {category_value: int_code}.
        """
        # TODO: For each column, build a mapping from unique values to integer
        #       codes, store in self.category_mappings, and return it
        raise NotImplementedError

    def transform_encode(self, batch: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
        """Apply label encoding to a batch using fitted category mappings.

        Args:
            batch: Column-name → numpy array mapping.

        Returns:
            The batch with categorical columns replaced by integer codes.
        """
        # TODO: Replace values in categorical columns using
        #       self.category_mappings. Unknown categories should map to -1.
        raise NotImplementedError


def create_preprocessing_pipeline(
    ds: ray.data.Dataset,
    normalize_columns: list[str],
    categorical_columns: list[str],
    fit_df: pd.DataFrame,
) -> ray.data.Dataset:
    """Build and apply a preprocessing pipeline backed by a PreprocessingActor.

    Steps:
      1. Create a ``PreprocessingActor``.
      2. Fit normalizer and encoder on *fit_df* (typically a sample of training data).
      3. Apply transforms to the full dataset using ``ds.map_batches``.

    Args:
        ds: Input Ray Dataset.
        normalize_columns: Columns to z-score normalize.
        categorical_columns: Columns to label-encode.
        fit_df: DataFrame used for fitting statistics.

    Returns:
        The fully preprocessed Ray Dataset.
    """
    # TODO: Instantiate PreprocessingActor, call fit_normalizer and
    #       fit_encoder remotely, then chain map_batches calls for normalize
    #       and encode transforms on ds
    raise NotImplementedError
