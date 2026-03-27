"""Window function-based feature engineering."""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def compute_rolling_averages(
    transactions: DataFrame,
    windows: list[int] | None = None,
) -> DataFrame:
    """Compute rolling average purchase amount over different time windows.

    Args:
        transactions: DataFrame with columns [user_id, timestamp, amount].
        windows: List of window sizes in number of preceding transactions.
            Defaults to [3, 7, 30].

    Returns:
        DataFrame with rolling average columns for each window size.
    """
    # TODO: Implement rolling averages
    # 1. Define window spec partitioned by user_id, ordered by timestamp
    # 2. For each window size, compute avg(amount) over rowsBetween(-size, 0)
    # 3. Name columns as rolling_avg_{size}
    pass


def compute_lag_features(
    transactions: DataFrame,
    lag_periods: list[int] | None = None,
) -> DataFrame:
    """Compute lag features for purchase amount and time between purchases.

    Args:
        transactions: DataFrame with columns [user_id, timestamp, amount].
        lag_periods: Lag periods to compute. Defaults to [1, 2, 3].

    Returns:
        DataFrame with lag columns for amount and inter-purchase time.
    """
    # TODO: Implement lag features
    # 1. Define window spec partitioned by user_id, ordered by timestamp
    # 2. For each lag period:
    #    - lag(amount, n) as amount_lag_{n}
    #    - lag(timestamp, n) to compute days_since_lag_{n}
    # 3. Compute amount_change_{n} = amount - amount_lag_{n}
    pass


def compute_rank_within_category(
    transactions: DataFrame,
    products: DataFrame,
) -> DataFrame:
    """Rank users by spending within each product category.

    Args:
        transactions: DataFrame with columns [user_id, product_id, amount].
        products: DataFrame with columns [product_id, category].

    Returns:
        DataFrame with columns [user_id, category, category_spend,
        spend_rank, spend_percentile].
    """
    # TODO: Implement within-category ranking
    # 1. Join transactions with products on product_id
    # 2. Group by (user_id, category), sum amount as category_spend
    # 3. Window partitioned by category, ordered by category_spend desc
    # 4. Compute dense_rank() and percent_rank()
    pass


def compute_session_features(
    clickstream: DataFrame,
    session_gap_minutes: int = 30,
) -> DataFrame:
    """Compute session-level features from clickstream data.

    A new session starts when the gap between events exceeds session_gap_minutes.

    Args:
        clickstream: DataFrame with columns [user_id, timestamp, event_type].
        session_gap_minutes: Minutes of inactivity before a new session starts.

    Returns:
        DataFrame with columns [user_id, session_id, session_duration,
        events_per_session, session_count].
    """
    # TODO: Implement session detection and features
    # 1. Window by user_id, ordered by timestamp
    # 2. Compute time gap from previous event using lag()
    # 3. Flag new sessions where gap > session_gap_minutes
    # 4. Assign session_id using cumulative sum of session flags
    # 5. Aggregate session-level metrics
    pass
