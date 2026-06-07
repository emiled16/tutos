"""Data ingestion assets: raw_data and cleaned_data.

These are the first two stages of the ML pipeline, responsible for
loading raw data and producing a clean, typed DataFrame.
"""

import dagster as dg
import pandas as pd

from partitions import daily_partitions


@dg.asset(
    group_name="ingestion",
    partitions_def=daily_partitions,
    description="Raw dataset ingested from the source system.",
)
def raw_data(context: dg.AssetExecutionContext) -> pd.DataFrame:
    """Load raw data for the given partition date.

    In a real system this would read from a database, API, or file system.
    For this tutorial, it generates a synthetic dataset.

    Args:
        context: Dagster execution context with partition info.

    Returns:
        A DataFrame containing raw, unprocessed records.
    """
    partition_date = context.partition_key
    context.log.info(f"Loading raw data for partition: {partition_date}")

    # TODO: Implement data generation or loading:
    #   - Generate a synthetic dataset with columns:
    #     user_id, timestamp, feature_1, feature_2, feature_3, label
    #   - Include some missing values and outliers for the cleaning step
    #   - Use the partition_date to seed the random generator for reproducibility
    #   - Return ~1000 rows per partition
    raise NotImplementedError


@dg.asset(
    group_name="ingestion",
    partitions_def=daily_partitions,
    description="Cleaned dataset with missing values handled and outliers removed.",
)
def cleaned_data(context: dg.AssetExecutionContext, raw_data: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw dataset for downstream feature engineering.

    Handles missing values, removes outliers, casts types,
    and validates basic data quality constraints.

    Args:
        context: Dagster execution context.
        raw_data: The raw DataFrame from the ingestion step.

    Returns:
        A cleaned DataFrame ready for feature engineering.
    """
    context.log.info(f"Cleaning data: {len(raw_data)} rows input")

    # TODO: Implement data cleaning:
    #   1. Drop rows where the label column is null
    #   2. Fill missing feature values with the column median
    #   3. Remove outliers beyond 3 standard deviations
    #   4. Cast columns to appropriate dtypes
    #   5. Log the number of rows removed
    #   6. Add metadata about cleaning results via context.add_output_metadata()
    raise NotImplementedError
