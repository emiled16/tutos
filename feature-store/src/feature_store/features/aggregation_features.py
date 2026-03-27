"""Time-windowed aggregation features for fraud detection."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

import numpy as np
import pandas as pd


@dataclass
class AggregationWindow:
    """Configuration for a time-based aggregation window."""

    name: str
    duration: timedelta

    @property
    def hours(self) -> float:
        return self.duration.total_seconds() / 3600


STANDARD_WINDOWS = [
    AggregationWindow("1h", timedelta(hours=1)),
    AggregationWindow("24h", timedelta(hours=24)),
    AggregationWindow("7d", timedelta(days=7)),
]


def compute_rolling_transaction_count(
    transactions: pd.DataFrame,
    user_id_col: str = "user_id",
    windows: list[AggregationWindow] | None = None,
) -> pd.DataFrame:
    """Compute rolling transaction count per user for each time window.

    For each user's latest timestamp, count transactions in the preceding window.

    Args:
        transactions: DataFrame with columns [user_id, amount, timestamp].
        user_id_col: Name of the user ID column.
        windows: List of aggregation windows. Defaults to STANDARD_WINDOWS.

    Returns:
        DataFrame with columns [user_id, txn_count_{window}, ..., timestamp].
    """
    # TODO: Implement
    # - For each window in windows (default STANDARD_WINDOWS)
    # - For each user, count transactions within [latest - window, latest]
    # - Create column txn_count_{window.name} for each window
    # - Use the latest timestamp per user as the feature timestamp
    raise NotImplementedError


def compute_rolling_amount_stats(
    transactions: pd.DataFrame,
    user_id_col: str = "user_id",
    windows: list[AggregationWindow] | None = None,
) -> pd.DataFrame:
    """Compute rolling amount statistics per user for each time window.

    For each window, computes sum, mean, and max of transaction amounts.

    Args:
        transactions: DataFrame with columns [user_id, amount, timestamp].
        user_id_col: Name of the user ID column.
        windows: List of aggregation windows. Defaults to STANDARD_WINDOWS.

    Returns:
        DataFrame with columns [user_id, txn_amount_sum_{window},
        txn_amount_mean_{window}, txn_amount_max_{window}, ..., timestamp].
    """
    # TODO: Implement
    # - For each window in windows (default STANDARD_WINDOWS)
    # - For each user, compute sum/mean/max of amount within the window
    # - Create appropriately named columns
    # - Use the latest timestamp per user
    raise NotImplementedError


def build_aggregation_feature_table(
    transactions: pd.DataFrame,
    user_id_col: str = "user_id",
    windows: list[AggregationWindow] | None = None,
) -> pd.DataFrame:
    """Build the complete aggregation feature table.

    Combines rolling counts and amount statistics into a single DataFrame.

    Args:
        transactions: DataFrame with columns [user_id, amount, timestamp].
        user_id_col: Name of the user ID column.
        windows: List of aggregation windows.

    Returns:
        Combined aggregation feature DataFrame keyed by user_id.
    """
    # TODO: Implement
    # - Call compute_rolling_transaction_count and compute_rolling_amount_stats
    # - Merge on user_id
    # - Ensure no duplicate timestamp columns
    raise NotImplementedError
