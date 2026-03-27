"""Dataset loading and temporal train/test splitting."""

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class InteractionDataset:
    """Container for user-item interaction data with metadata."""

    interactions: pd.DataFrame
    user_features: pd.DataFrame | None = None
    item_features: pd.DataFrame | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def n_users(self) -> int:
        return self.interactions["user_id"].nunique()

    @property
    def n_items(self) -> int:
        return self.interactions["item_id"].nunique()

    @property
    def n_interactions(self) -> int:
        return len(self.interactions)

    @property
    def sparsity(self) -> float:
        """Fraction of the user-item matrix that is empty."""
        return 1.0 - self.n_interactions / (self.n_users * self.n_items)


@dataclass
class TrainTestSplit:
    """Result of a temporal train/test split."""

    train: pd.DataFrame
    test: pd.DataFrame
    split_timestamp: float | None = None


def load_dataset(path: Path) -> InteractionDataset:
    """Load an interaction dataset from a directory.

    Expects at minimum an `interactions.csv` file with columns:
    user_id, item_id, rating, timestamp.

    Optionally loads `user_features.csv` and `item_features.csv`.

    Args:
        path: Directory containing dataset CSV files.

    Returns:
        Loaded InteractionDataset.
    """
    # TODO: Load interactions.csv and parse the timestamp column
    # TODO: Optionally load user_features.csv and item_features.csv if they exist
    # TODO: Populate metadata (n_users, n_items, date range, etc.)
    raise NotImplementedError


def temporal_train_test_split(
    interactions: pd.DataFrame,
    test_ratio: float = 0.2,
    timestamp_col: str = "timestamp",
) -> TrainTestSplit:
    """Split interactions by time — all test interactions occur after all training interactions.

    Uses a global timestamp cutoff so that the split simulates a realistic scenario
    where the model is trained on past data and evaluated on future data.

    Args:
        interactions: DataFrame with at least user_id, item_id, and a timestamp column.
        test_ratio: Approximate fraction of interactions to use as test set.
        timestamp_col: Name of the timestamp column.

    Returns:
        TrainTestSplit with train and test DataFrames.
    """
    # TODO: Sort interactions by timestamp
    # TODO: Find the cutoff timestamp at the (1 - test_ratio) quantile
    # TODO: Split into train (before cutoff) and test (at or after cutoff)
    # TODO: Filter test to only include users and items seen in training
    raise NotImplementedError


def per_user_temporal_split(
    interactions: pd.DataFrame,
    n_test_per_user: int = 1,
    timestamp_col: str = "timestamp",
) -> TrainTestSplit:
    """Split by holding out the last N interactions per user.

    Args:
        interactions: DataFrame with user_id, item_id, and timestamp.
        n_test_per_user: Number of most recent interactions per user to hold out.
        timestamp_col: Name of the timestamp column.

    Returns:
        TrainTestSplit with train and test DataFrames.
    """
    # TODO: For each user, sort their interactions by timestamp
    # TODO: Hold out the last n_test_per_user interactions as test
    # TODO: Use the remaining interactions as training data
    raise NotImplementedError
