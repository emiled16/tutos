"""Generate test datasets with known quality issues for testing validation."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class DatasetConfig:
    """Configuration for test data generation."""

    n_rows: int = 1000
    n_features: int = 10
    target_column: str = "target"
    random_seed: int = 42


def generate_clean_dataset(config: DatasetConfig | None = None) -> pd.DataFrame:
    """Generate a clean dataset that should pass all quality checks.

    Features are normally distributed with no nulls, no duplicates,
    and a balanced binary target.

    Args:
        config: Data generation configuration.

    Returns:
        Clean DataFrame.
    """
    # TODO: Implement
    # - Generate n_features normally distributed columns
    # - Add an ID column with unique values
    # - Add a balanced binary target column
    # - Add a timestamp column
    # - Ensure no nulls, no duplicates
    raise NotImplementedError


def inject_null_values(
    df: pd.DataFrame,
    columns: list[str],
    null_fraction: float = 0.1,
    seed: int = 42,
) -> pd.DataFrame:
    """Inject null values into specified columns.

    Args:
        df: Clean DataFrame.
        columns: Columns to inject nulls into.
        null_fraction: Fraction of values to set to null.
        seed: Random seed.

    Returns:
        DataFrame with injected nulls.
    """
    # TODO: Implement
    # - For each column, randomly set null_fraction of values to NaN
    # - Return a copy of the DataFrame (don't modify in place)
    raise NotImplementedError


def inject_distribution_drift(
    df: pd.DataFrame,
    columns: list[str],
    shift_magnitude: float = 3.0,
    seed: int = 42,
) -> pd.DataFrame:
    """Inject distribution drift by shifting column values.

    Args:
        df: Clean DataFrame.
        columns: Columns to shift.
        shift_magnitude: Standard deviations to shift the mean by.
        seed: Random seed.

    Returns:
        DataFrame with shifted distributions.
    """
    # TODO: Implement
    # - For each column, add shift_magnitude * column_std to all values
    # - Return a copy
    raise NotImplementedError


def inject_target_leakage(
    df: pd.DataFrame,
    target_column: str = "target",
    leaky_column_name: str = "leaky_feature",
) -> pd.DataFrame:
    """Inject a feature that leaks the target variable.

    Creates a column that is a near-perfect copy of the target with
    small noise, simulating target leakage.

    Args:
        df: DataFrame with target column.
        target_column: Name of the target column.
        leaky_column_name: Name for the leaky feature.

    Returns:
        DataFrame with added leaky feature.
    """
    # TODO: Implement
    # - Create leaky_column = target + small_noise
    # - Correlation with target should be > 0.95
    # - Return a copy with the new column
    raise NotImplementedError


def inject_class_imbalance(
    df: pd.DataFrame,
    target_column: str = "target",
    minority_ratio: float = 0.01,
    seed: int = 42,
) -> pd.DataFrame:
    """Inject severe class imbalance into the target column.

    Args:
        df: DataFrame with target column.
        target_column: Name of the target column.
        minority_ratio: Desired fraction of minority class.
        seed: Random seed.

    Returns:
        DataFrame with imbalanced target.
    """
    # TODO: Implement
    # - Resample the target column so that one class has minority_ratio
    # - Return a copy
    raise NotImplementedError


def generate_dataset_with_issues(
    config: DatasetConfig | None = None,
    issues: list[str] | None = None,
) -> pd.DataFrame:
    """Generate a dataset with specific quality issues for testing.

    Args:
        config: Data generation configuration.
        issues: List of issues to inject. Options:
                "nulls", "drift", "leakage", "imbalance", "duplicates".

    Returns:
        DataFrame with injected quality issues.
    """
    # TODO: Implement
    # - Generate a clean dataset
    # - For each issue in issues, apply the corresponding injection function
    # - Return the corrupted dataset
    raise NotImplementedError
