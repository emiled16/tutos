"""Tests for data cleaning transformations."""

from __future__ import annotations

import pytest
from pyspark.sql import SparkSession
from pyspark.sql import types as T

from pyspark.transforms.cleaning import (
    cast_types,
    deduplicate,
    handle_nulls,
    remove_outliers,
)


@pytest.fixture
def df_with_duplicates(spark: SparkSession):
    """DataFrame with known duplicate rows."""
    data = [
        ("id_1", "user_1", "2024-01-01", 10.0),
        ("id_1", "user_1", "2024-01-01", 10.0),  # exact dup
        ("id_2", "user_1", "2024-01-02", 20.0),
        ("id_3", "user_2", "2024-01-01", 30.0),
    ]
    return spark.createDataFrame(data, ["id", "user_id", "date", "amount"])


@pytest.fixture
def df_with_nulls(spark: SparkSession):
    """DataFrame with null values."""
    data = [
        ("user_1", 25, "US"),
        ("user_2", None, "UK"),
        ("user_3", 30, None),
        ("user_4", None, None),
    ]
    return spark.createDataFrame(data, ["user_id", "age", "country"])


class TestDeduplicate:
    """Tests for deduplication."""

    def test_removes_exact_duplicates(self, df_with_duplicates) -> None:
        """Exact duplicate rows should be removed."""
        # TODO: Implement test
        # After dedup on ["id"], should have 3 rows
        pass

    def test_keeps_last_by_order_column(self, spark) -> None:
        """When keep='last', should retain the most recent row."""
        # TODO: Implement test
        pass

    def test_keeps_first_by_order_column(self, spark) -> None:
        """When keep='first', should retain the earliest row."""
        # TODO: Implement test
        pass


class TestHandleNulls:
    """Tests for null handling."""

    def test_drop_removes_rows_with_nulls(self, df_with_nulls) -> None:
        """Drop strategy should remove any row with a null."""
        # TODO: Implement test
        # Only user_1 has no nulls, so result should have 1 row
        pass

    def test_fill_replaces_nulls(self, df_with_nulls) -> None:
        """Fill strategy should replace nulls with provided values."""
        # TODO: Implement test
        pass

    def test_flag_adds_indicator_columns(self, df_with_nulls) -> None:
        """Flag strategy should add boolean _is_null columns."""
        # TODO: Implement test
        pass

    def test_subset_limits_null_handling(self, df_with_nulls) -> None:
        """Subset parameter should limit which columns are checked."""
        # TODO: Implement test
        pass


class TestCastTypes:
    """Tests for type casting."""

    def test_string_to_integer(self, spark) -> None:
        """Should cast string column to integer."""
        # TODO: Implement test
        pass

    def test_string_to_double(self, spark) -> None:
        """Should cast string column to double."""
        # TODO: Implement test
        pass


class TestRemoveOutliers:
    """Tests for outlier removal."""

    def test_iqr_removes_extreme_values(self, spark) -> None:
        """IQR method should remove values beyond Q1 - 1.5*IQR and Q3 + 1.5*IQR."""
        # TODO: Implement test
        pass

    def test_preserves_normal_values(self, spark) -> None:
        """Non-outlier values should be preserved."""
        # TODO: Implement test
        pass
