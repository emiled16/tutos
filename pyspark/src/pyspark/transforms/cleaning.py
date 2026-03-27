"""Data cleaning transformations."""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T


def deduplicate(
    df: DataFrame,
    key_columns: list[str],
    order_column: str | None = None,
    keep: str = "last",
) -> DataFrame:
    """Remove duplicate rows, keeping first or last occurrence.

    Args:
        df: Input DataFrame.
        key_columns: Columns that define uniqueness.
        order_column: Column to determine ordering (for first/last).
        keep: Which duplicate to keep — "first" or "last".

    Returns:
        Deduplicated DataFrame.
    """
    # TODO: Implement deduplication
    # 1. If no order_column, use dropDuplicates(key_columns)
    # 2. If order_column provided:
    #    - Window partitioned by key_columns, ordered by order_column
    #    - row_number() to identify first/last
    #    - Filter to keep the desired occurrence
    pass


def handle_nulls(
    df: DataFrame,
    strategy: str = "drop",
    fill_values: dict[str, object] | None = None,
    subset: list[str] | None = None,
) -> DataFrame:
    """Handle null values using the specified strategy.

    Args:
        df: Input DataFrame.
        strategy: One of "drop", "fill", "flag".
            - "drop": remove rows with nulls
            - "fill": fill nulls with provided values
            - "flag": add boolean columns indicating null presence
        fill_values: Column-to-value mapping for "fill" strategy.
        subset: Columns to apply the strategy to (default: all).

    Returns:
        DataFrame with nulls handled.
    """
    # TODO: Implement null handling
    # For "drop": df.dropna(subset=subset)
    # For "fill": df.fillna(fill_values) for specified columns
    # For "flag": add {col}_is_null boolean columns, then fill nulls
    pass


def cast_types(
    df: DataFrame,
    type_mapping: dict[str, T.DataType],
) -> DataFrame:
    """Cast columns to specified data types.

    Args:
        df: Input DataFrame.
        type_mapping: Column name to target DataType mapping.

    Returns:
        DataFrame with columns cast to specified types.
    """
    # TODO: Implement type casting
    # For each column in type_mapping, apply .cast(target_type)
    pass


def remove_outliers(
    df: DataFrame,
    column: str,
    method: str = "iqr",
    factor: float = 1.5,
) -> DataFrame:
    """Remove outliers from a numeric column.

    Args:
        df: Input DataFrame.
        column: Numeric column to check for outliers.
        method: Detection method — "iqr" or "zscore".
        factor: Multiplier for IQR method (default 1.5) or
                z-score threshold (default 3.0 if method is "zscore").

    Returns:
        DataFrame with outlier rows removed.
    """
    # TODO: Implement outlier removal
    # For IQR:
    #   1. Compute Q1, Q3 using approxQuantile
    #   2. IQR = Q3 - Q1
    #   3. Filter: Q1 - factor*IQR <= value <= Q3 + factor*IQR
    # For zscore:
    #   1. Compute mean and stddev
    #   2. Filter: abs(value - mean) / stddev <= factor
    pass
