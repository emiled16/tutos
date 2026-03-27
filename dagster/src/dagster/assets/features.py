"""Feature engineering assets: feature_table and feature_stats.

Derives ML features from cleaned data and computes statistics
about the feature distributions.
"""

import dagster as dg
import pandas as pd

from dagster.partitions import daily_partitions


@dg.asset(
    group_name="features",
    partitions_def=daily_partitions,
    description="Engineered feature table derived from cleaned data.",
)
def feature_table(context: dg.AssetExecutionContext, cleaned_data: pd.DataFrame) -> pd.DataFrame:
    """Compute ML features from the cleaned dataset.

    Creates derived features including interactions, ratios,
    and polynomial features suitable for model training.

    Args:
        context: Dagster execution context.
        cleaned_data: The cleaned DataFrame.

    Returns:
        A DataFrame with original and derived feature columns.
    """
    context.log.info(f"Engineering features from {len(cleaned_data)} rows")

    # TODO: Implement feature engineering:
    #   1. Create interaction features: feature_1 * feature_2
    #   2. Create ratio features: feature_1 / (feature_2 + 1)
    #   3. Create polynomial features: feature_1 ** 2, feature_2 ** 2
    #   4. Normalize numeric features to zero mean and unit variance
    #   5. Keep the label column and user_id for downstream use
    #   6. Add output metadata with feature count via context.add_output_metadata()
    raise NotImplementedError


@dg.asset(
    group_name="features",
    partitions_def=daily_partitions,
    description="Statistical summary of feature distributions.",
)
def feature_stats(context: dg.AssetExecutionContext, feature_table: pd.DataFrame) -> pd.DataFrame:
    """Compute descriptive statistics for each feature.

    Tracks feature distributions over time to detect data drift.

    Args:
        context: Dagster execution context.
        feature_table: The engineered feature table.

    Returns:
        A DataFrame with per-feature statistics (mean, std, min, max, etc.).
    """
    context.log.info(f"Computing feature statistics for {feature_table.shape[1]} features")

    # TODO: Implement statistics computation:
    #   1. Compute describe() for all numeric columns
    #   2. Add skewness and kurtosis
    #   3. Add null counts per column
    #   4. Add correlation matrix summary (top correlated pairs)
    #   5. Return as a DataFrame indexed by feature name
    raise NotImplementedError
