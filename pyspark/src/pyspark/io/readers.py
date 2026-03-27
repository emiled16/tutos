"""Data readers with schema enforcement."""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import types as T


def read_csv(
    spark: SparkSession,
    path: str,
    schema: T.StructType | None = None,
    header: bool = True,
    infer_schema: bool = False,
) -> DataFrame:
    """Read a CSV file into a DataFrame.

    Args:
        spark: Active SparkSession.
        path: Path to CSV file or directory.
        schema: Explicit schema. Preferred over inference for production.
        header: Whether CSV has a header row.
        infer_schema: Whether to infer types (slow, use schema instead).

    Returns:
        DataFrame with the CSV data.
    """
    # TODO: Implement CSV reader
    # 1. Build DataFrameReader with format("csv")
    # 2. Apply schema if provided, otherwise set inferSchema
    # 3. Set header option
    # 4. Load and return
    pass


def read_parquet(
    spark: SparkSession,
    path: str,
    columns: list[str] | None = None,
) -> DataFrame:
    """Read a Parquet file into a DataFrame.

    Args:
        spark: Active SparkSession.
        path: Path to Parquet file or directory.
        columns: Optional subset of columns to read (predicate pushdown).

    Returns:
        DataFrame with the Parquet data.
    """
    # TODO: Implement Parquet reader
    # 1. Read with spark.read.parquet(path)
    # 2. If columns specified, select only those columns
    pass


def read_delta(
    spark: SparkSession,
    path: str,
    version: int | None = None,
    timestamp: str | None = None,
) -> DataFrame:
    """Read a Delta table with optional time travel.

    Args:
        spark: Active SparkSession.
        path: Path to Delta table.
        version: Optional version number for time travel.
        timestamp: Optional timestamp string for time travel.

    Returns:
        DataFrame from the Delta table.
    """
    # TODO: Implement Delta reader with time travel support
    # 1. Build reader with format("delta")
    # 2. If version specified, set option("versionAsOf", version)
    # 3. If timestamp specified, set option("timestampAsOf", timestamp)
    # 4. Load and return
    pass
