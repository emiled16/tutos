"""Transaction-based feature computation for fraud detection."""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_amount_statistics(
    transactions: pd.DataFrame, user_id_col: str = "user_id"
) -> pd.DataFrame:
    """Compute per-user transaction amount statistics.

    Computes mean, standard deviation, max, and min of transaction amounts
    grouped by user.

    Args:
        transactions: DataFrame with columns [user_id, amount, timestamp].
        user_id_col: Name of the user ID column.

    Returns:
        DataFrame with columns [user_id, amount_mean, amount_std, amount_max,
        amount_min, timestamp] where timestamp is the latest transaction time.
    """
    # TODO: Implement
    # - Group by user_id_col
    # - Compute mean, std, max, min of the "amount" column
    # - Use the latest timestamp per user as the feature timestamp
    # - Fill NaN std with 0.0 (users with single transaction)
    raise NotImplementedError


def compute_transaction_frequency(
    transactions: pd.DataFrame, user_id_col: str = "user_id"
) -> pd.DataFrame:
    """Compute per-user transaction frequency features.

    Args:
        transactions: DataFrame with columns [user_id, amount, timestamp].
        user_id_col: Name of the user ID column.

    Returns:
        DataFrame with columns [user_id, transaction_count,
        avg_time_between_transactions, timestamp].
    """
    # TODO: Implement
    # - Group by user_id_col
    # - Count transactions per user
    # - Compute average time between consecutive transactions (in hours)
    #   For users with a single transaction, set avg_time to 0.0
    # - Use the latest timestamp per user
    raise NotImplementedError


def compute_transaction_velocity(
    transactions: pd.DataFrame,
    user_id_col: str = "user_id",
    window_hours: int = 1,
) -> pd.DataFrame:
    """Compute transaction velocity: number of transactions within a time window.

    For each transaction, count how many other transactions by the same user
    occurred within the preceding `window_hours`.

    Args:
        transactions: DataFrame with columns [user_id, amount, timestamp].
        user_id_col: Name of the user ID column.
        window_hours: Size of the lookback window in hours.

    Returns:
        DataFrame with original columns plus a `velocity_{window_hours}h` column.
    """
    # TODO: Implement
    # - Sort by timestamp
    # - For each transaction, count transactions by same user in [t - window, t)
    # - This is an expensive operation; consider using rolling joins or
    #   merge_asof for efficiency
    raise NotImplementedError
