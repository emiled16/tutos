"""Tests for user feature computations."""

from __future__ import annotations

from datetime import date, datetime

import pytest
from pyspark.sql import SparkSession

from pyspark.features.user_features import (
    compute_lifetime_value,
    compute_purchase_frequency,
    compute_recency,
    compute_user_segments,
)


@pytest.fixture
def sample_transactions(spark: SparkSession):
    """Create a small transactions DataFrame for testing."""
    data = [
        ("tx1", "user_1", "prod_1", datetime(2024, 1, 10), 1, 50.0),
        ("tx2", "user_1", "prod_2", datetime(2024, 2, 15), 2, 100.0),
        ("tx3", "user_1", "prod_3", datetime(2024, 3, 20), 1, 75.0),
        ("tx4", "user_2", "prod_1", datetime(2024, 1, 5), 1, 200.0),
        ("tx5", "user_2", "prod_4", datetime(2024, 6, 1), 3, 300.0),
    ]
    return spark.createDataFrame(
        data,
        ["transaction_id", "user_id", "product_id", "timestamp", "quantity", "amount"],
    )


class TestLifetimeValue:
    """Tests for lifetime value computation."""

    def test_total_spend_per_user(self, spark, sample_transactions) -> None:
        """LTV should equal total amount spent by each user."""
        # TODO: Implement test
        # user_1: 50 + 100 + 75 = 225
        # user_2: 200 + 300 = 500
        pass

    def test_tenure_days(self, spark, sample_transactions) -> None:
        """Tenure should be the days between first and last purchase."""
        # TODO: Implement test
        pass

    def test_single_purchase_user(self, spark) -> None:
        """User with one purchase should have tenure_days = 0."""
        # TODO: Implement test
        pass


class TestPurchaseFrequency:
    """Tests for purchase frequency computation."""

    def test_total_purchases(self, spark, sample_transactions) -> None:
        """Total purchases should match transaction count per user."""
        # TODO: Implement test
        pass

    def test_avg_days_between_purchases(self, spark, sample_transactions) -> None:
        """Average interval should be computed correctly."""
        # TODO: Implement test
        pass


class TestRecency:
    """Tests for recency computation."""

    def test_days_since_last_purchase(self, spark, sample_transactions) -> None:
        """Should compute correct days from reference date to last purchase."""
        # TODO: Implement test
        pass

    def test_recency_score_range(self, spark, sample_transactions) -> None:
        """Recency score should be between 0 and 1."""
        # TODO: Implement test
        pass


class TestUserSegments:
    """Tests for RFM segmentation."""

    def test_segments_include_all_users(self, spark, sample_transactions) -> None:
        """Every user should receive a segment label."""
        # TODO: Implement test
        pass
