"""User profile feature computation for fraud detection."""

from __future__ import annotations

from datetime import datetime

import numpy as np
import pandas as pd


def compute_account_age(
    users: pd.DataFrame, reference_date: datetime | None = None
) -> pd.DataFrame:
    """Compute account age in days for each user.

    Args:
        users: DataFrame with columns [user_id, account_created_at].
        reference_date: Date to compute age relative to. Defaults to now.

    Returns:
        DataFrame with columns [user_id, account_age_days, timestamp].
    """
    # TODO: Implement
    # - Calculate days between account_created_at and reference_date
    # - Handle timezone-naive vs timezone-aware datetimes
    # - Set timestamp to reference_date for the feature row
    raise NotImplementedError


def compute_historical_spending_patterns(
    transactions: pd.DataFrame, user_id_col: str = "user_id"
) -> pd.DataFrame:
    """Compute historical spending pattern features per user.

    Features include average daily spend, spend variance, and the ratio
    of the largest transaction to average transaction.

    Args:
        transactions: DataFrame with columns [user_id, amount, timestamp].
        user_id_col: Name of the user ID column.

    Returns:
        DataFrame with columns [user_id, avg_daily_spend, spend_variance,
        max_to_avg_ratio, timestamp].
    """
    # TODO: Implement
    # - Group transactions by user and date to get daily totals
    # - Compute mean and variance of daily spend across all days
    # - Compute max_to_avg_ratio = max(amount) / mean(amount)
    # - Use latest transaction timestamp per user
    raise NotImplementedError


def compute_days_since_last_transaction(
    transactions: pd.DataFrame,
    user_id_col: str = "user_id",
    reference_date: datetime | None = None,
) -> pd.DataFrame:
    """Compute days since each user's most recent transaction.

    Args:
        transactions: DataFrame with columns [user_id, timestamp].
        user_id_col: Name of the user ID column.
        reference_date: Date to compute recency from. Defaults to now.

    Returns:
        DataFrame with columns [user_id, days_since_last_transaction, timestamp].
    """
    # TODO: Implement
    # - Find the max timestamp per user
    # - Compute difference in days from reference_date
    # - Set timestamp to reference_date
    raise NotImplementedError


def build_user_feature_table(
    users: pd.DataFrame,
    transactions: pd.DataFrame,
    reference_date: datetime | None = None,
) -> pd.DataFrame:
    """Combine all user-level features into a single feature table.

    Merges account age, spending patterns, and recency features.

    Args:
        users: User profiles DataFrame.
        transactions: Transactions DataFrame.
        reference_date: Reference date for time-dependent features.

    Returns:
        Combined feature DataFrame keyed by user_id.
    """
    # TODO: Implement
    # - Call compute_account_age, compute_historical_spending_patterns,
    #   compute_days_since_last_transaction
    # - Merge results on user_id
    # - Fill missing values for users with no transactions
    raise NotImplementedError
