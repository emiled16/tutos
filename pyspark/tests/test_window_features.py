"""Tests for window function features."""

from __future__ import annotations

from datetime import datetime

import pytest
from pyspark.sql import SparkSession

from pyspark.features.window_features import (
    compute_lag_features,
    compute_rank_within_category,
    compute_rolling_averages,
    compute_session_features,
)


@pytest.fixture
def ordered_transactions(spark: SparkSession):
    """Create transactions with known ordering for window function tests."""
    data = [
        ("user_1", datetime(2024, 1, 1), 10.0),
        ("user_1", datetime(2024, 1, 5), 20.0),
        ("user_1", datetime(2024, 1, 10), 30.0),
        ("user_1", datetime(2024, 1, 15), 40.0),
        ("user_1", datetime(2024, 1, 20), 50.0),
        ("user_2", datetime(2024, 1, 1), 100.0),
        ("user_2", datetime(2024, 1, 10), 200.0),
    ]
    return spark.createDataFrame(data, ["user_id", "timestamp", "amount"])


class TestRollingAverages:
    """Tests for rolling average computation."""

    def test_rolling_avg_3(self, spark, ordered_transactions) -> None:
        """3-period rolling average should average the last 3 transactions."""
        # TODO: Implement test
        # For user_1 at row 3 (amount=30): avg(10, 20, 30) = 20.0
        pass

    def test_rolling_avg_handles_insufficient_data(
        self, spark, ordered_transactions
    ) -> None:
        """Rolling average at start should use available rows only."""
        # TODO: Implement test
        pass

    def test_rolling_avg_respects_partition(
        self, spark, ordered_transactions
    ) -> None:
        """Rolling average should not cross user boundaries."""
        # TODO: Implement test
        pass


class TestLagFeatures:
    """Tests for lag feature computation."""

    def test_lag_1_amount(self, spark, ordered_transactions) -> None:
        """Lag 1 should return the previous transaction's amount."""
        # TODO: Implement test
        pass

    def test_lag_null_for_first_row(self, spark, ordered_transactions) -> None:
        """First row in partition should have null lag values."""
        # TODO: Implement test
        pass

    def test_amount_change(self, spark, ordered_transactions) -> None:
        """Amount change should be current amount minus lagged amount."""
        # TODO: Implement test
        pass


class TestRankWithinCategory:
    """Tests for within-category ranking."""

    def test_rank_ordering(self, spark) -> None:
        """Higher spend should get lower (better) rank."""
        # TODO: Implement test
        pass

    def test_rank_partitioned_by_category(self, spark) -> None:
        """Rankings should reset per category."""
        # TODO: Implement test
        pass


class TestSessionFeatures:
    """Tests for session detection and features."""

    def test_session_boundary_detection(self, spark) -> None:
        """A gap > session_gap_minutes should start a new session."""
        # TODO: Implement test
        pass

    def test_session_count_per_user(self, spark) -> None:
        """Session count should reflect number of detected sessions."""
        # TODO: Implement test
        pass
