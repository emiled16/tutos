"""Complex aggregation transformations with groupBy and window specs."""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def compute_time_bucketed_aggregations(
    df: DataFrame,
    group_columns: list[str],
    agg_column: str,
    timestamp_column: str = "timestamp",
    buckets: list[str] | None = None,
) -> DataFrame:
    """Compute aggregations over time buckets (daily, weekly, monthly).

    Args:
        df: Input DataFrame.
        group_columns: Columns to group by in addition to time bucket.
        agg_column: Numeric column to aggregate.
        timestamp_column: Timestamp column for bucketing.
        buckets: Time bucket granularities. Defaults to ["day", "week", "month"].

    Returns:
        DataFrame with sum, avg, count, min, max for each time bucket.
    """
    # TODO: Implement time-bucketed aggregations
    # 1. For each bucket granularity, truncate timestamp to that level
    # 2. Group by group_columns + time_bucket
    # 3. Compute sum, avg, count, min, max of agg_column
    # 4. Union results across bucket granularities
    pass


def compute_running_totals(
    df: DataFrame,
    partition_columns: list[str],
    order_column: str,
    value_column: str,
) -> DataFrame:
    """Compute running (cumulative) totals partitioned by given columns.

    Args:
        df: Input DataFrame.
        partition_columns: Columns to partition the window by.
        order_column: Column to order by within each partition.
        value_column: Numeric column to accumulate.

    Returns:
        DataFrame with {value_column}_running_total column added.
    """
    # TODO: Implement running totals
    # 1. Define window: partitioned by partition_columns, ordered by order_column
    # 2. Use rowsBetween(Window.unboundedPreceding, Window.currentRow)
    # 3. Compute sum(value_column) over window
    pass


def compute_pivot_aggregation(
    df: DataFrame,
    group_column: str,
    pivot_column: str,
    value_column: str,
    agg_func: str = "sum",
) -> DataFrame:
    """Pivot a DataFrame with aggregation.

    Args:
        df: Input DataFrame.
        group_column: Column to group by (becomes rows).
        pivot_column: Column to pivot (values become columns).
        value_column: Column to aggregate.
        agg_func: Aggregation function ("sum", "avg", "count", "max", "min").

    Returns:
        Pivoted DataFrame with one column per pivot value.
    """
    # TODO: Implement pivot aggregation
    # 1. Group by group_column
    # 2. Pivot on pivot_column
    # 3. Apply the specified aggregation function on value_column
    pass
