"""User-level feature engineering."""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def compute_lifetime_value(
    transactions: DataFrame,
) -> DataFrame:
    """Compute customer lifetime value as total spend per user.

    Args:
        transactions: DataFrame with columns [user_id, amount, timestamp].

    Returns:
        DataFrame with columns [user_id, lifetime_value, first_purchase,
        last_purchase, tenure_days].
    """
    # TODO: Implement lifetime value computation
    # 1. Group by user_id
    # 2. Sum amount as lifetime_value
    # 3. Min/max timestamp as first_purchase/last_purchase
    # 4. Compute tenure_days as datediff(last_purchase, first_purchase)
    pass


def compute_purchase_frequency(
    transactions: DataFrame,
) -> DataFrame:
    """Compute purchase frequency metrics per user.

    Args:
        transactions: DataFrame with columns [user_id, transaction_id, timestamp].

    Returns:
        DataFrame with columns [user_id, total_purchases, avg_days_between_purchases,
        purchase_regularity].
    """
    # TODO: Implement purchase frequency computation
    # 1. Count transactions per user
    # 2. Use window function with lag() to compute inter-purchase intervals
    # 3. Calculate average and std of intervals
    # 4. purchase_regularity = 1 / (1 + std_interval)
    pass


def compute_recency(
    transactions: DataFrame,
    reference_date: str | None = None,
) -> DataFrame:
    """Compute recency features — how recently each user made a purchase.

    Args:
        transactions: DataFrame with columns [user_id, timestamp].
        reference_date: Date to compute recency from (default: max date in data).

    Returns:
        DataFrame with columns [user_id, days_since_last_purchase, recency_score].
    """
    # TODO: Implement recency computation
    # 1. Find most recent purchase per user
    # 2. Compute days_since_last_purchase from reference_date
    # 3. recency_score = 1 / (1 + days_since_last_purchase)
    pass


def compute_user_segments(
    lifetime_value: DataFrame,
    frequency: DataFrame,
    recency: DataFrame,
) -> DataFrame:
    """Combine LTV, frequency, and recency into user segments (RFM).

    Args:
        lifetime_value: Output of compute_lifetime_value.
        frequency: Output of compute_purchase_frequency.
        recency: Output of compute_recency.

    Returns:
        DataFrame with RFM scores and segment labels.
    """
    # TODO: Implement RFM segmentation
    # 1. Join the three feature DataFrames on user_id
    # 2. Assign R, F, M quartile scores (1-4) using ntile window function
    # 3. Combine into segment labels (e.g., "Champions", "At Risk", etc.)
    pass
