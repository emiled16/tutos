"""Shared test fixtures for PySpark tests."""

from __future__ import annotations

import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark() -> SparkSession:
    """Create a SparkSession for testing.

    Uses local mode with minimal config for fast test execution.
    Session is shared across all tests in the session.
    """
    session = (
        SparkSession.builder
        .master("local[2]")
        .appName("FeatureFactoryTests")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse-test")
        .getOrCreate()
    )
    yield session
    session.stop()
