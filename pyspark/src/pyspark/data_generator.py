"""Generate synthetic e-commerce data for the feature engineering pipeline."""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Any

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import types as T


USER_SCHEMA = T.StructType([
    T.StructField("user_id", T.StringType(), False),
    T.StructField("signup_date", T.DateType(), False),
    T.StructField("country", T.StringType(), True),
    T.StructField("age", T.IntegerType(), True),
    T.StructField("gender", T.StringType(), True),
])

PRODUCT_SCHEMA = T.StructType([
    T.StructField("product_id", T.StringType(), False),
    T.StructField("category", T.StringType(), False),
    T.StructField("subcategory", T.StringType(), True),
    T.StructField("price", T.DoubleType(), False),
    T.StructField("brand", T.StringType(), True),
])

TRANSACTION_SCHEMA = T.StructType([
    T.StructField("transaction_id", T.StringType(), False),
    T.StructField("user_id", T.StringType(), False),
    T.StructField("product_id", T.StringType(), False),
    T.StructField("timestamp", T.TimestampType(), False),
    T.StructField("quantity", T.IntegerType(), False),
    T.StructField("amount", T.DoubleType(), False),
])

CLICKSTREAM_SCHEMA = T.StructType([
    T.StructField("event_id", T.StringType(), False),
    T.StructField("user_id", T.StringType(), False),
    T.StructField("product_id", T.StringType(), False),
    T.StructField("event_type", T.StringType(), False),  # view, click, add_to_cart
    T.StructField("timestamp", T.TimestampType(), False),
    T.StructField("dwell_seconds", T.IntegerType(), True),
])


def generate_users(spark: SparkSession, n_users: int = 10_000) -> DataFrame:
    """Generate a DataFrame of synthetic user profiles.

    Args:
        spark: Active SparkSession.
        n_users: Number of users to generate.

    Returns:
        DataFrame conforming to USER_SCHEMA.
    """
    # TODO: Implement user data generation
    # Generate random user profiles with realistic distributions
    # for country, age, gender, and signup dates spanning 3 years
    pass


def generate_products(spark: SparkSession, n_products: int = 5_000) -> DataFrame:
    """Generate a DataFrame of synthetic product listings.

    Args:
        spark: Active SparkSession.
        n_products: Number of products to generate.

    Returns:
        DataFrame conforming to PRODUCT_SCHEMA.
    """
    # TODO: Implement product data generation
    # Generate products across categories (Electronics, Clothing, Home, etc.)
    # with realistic price distributions per category
    pass


def generate_transactions(
    spark: SparkSession,
    user_ids: list[str],
    product_ids: list[str],
    n_transactions: int = 100_000,
) -> DataFrame:
    """Generate a DataFrame of synthetic purchase transactions.

    Args:
        spark: Active SparkSession.
        user_ids: Valid user IDs to sample from.
        product_ids: Valid product IDs to sample from.
        n_transactions: Number of transactions to generate.

    Returns:
        DataFrame conforming to TRANSACTION_SCHEMA.
    """
    # TODO: Implement transaction data generation
    # Generate transactions with power-law distribution (some users buy more)
    # Include some duplicates for testing deduplication
    pass


def generate_clickstream(
    spark: SparkSession,
    user_ids: list[str],
    product_ids: list[str],
    n_events: int = 500_000,
) -> DataFrame:
    """Generate a DataFrame of synthetic clickstream events.

    Args:
        spark: Active SparkSession.
        user_ids: Valid user IDs to sample from.
        product_ids: Valid product IDs to sample from.
        n_events: Number of events to generate.

    Returns:
        DataFrame conforming to CLICKSTREAM_SCHEMA.
    """
    # TODO: Implement clickstream data generation
    # Generate view/click/add_to_cart events with realistic funnel ratios
    # (many views, fewer clicks, even fewer add_to_cart)
    pass
