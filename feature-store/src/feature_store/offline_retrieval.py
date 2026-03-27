"""Offline feature retrieval with point-in-time correct joins."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from feast import FeatureStore

from feature_store.materialization import get_feature_store


def create_entity_dataframe(
    transactions: pd.DataFrame,
    user_id_col: str = "user_id",
    timestamp_col: str = "timestamp",
    label_col: str = "is_fraud",
) -> pd.DataFrame:
    """Create an entity DataFrame for point-in-time feature retrieval.

    The entity DataFrame contains the entity keys, event timestamps, and
    labels needed for historical feature retrieval.

    Args:
        transactions: Raw transaction DataFrame.
        user_id_col: Column name for user ID.
        timestamp_col: Column name for event timestamp.
        label_col: Column name for the fraud label.

    Returns:
        DataFrame with columns [user_id, event_timestamp, is_fraud].
    """
    # TODO: Implement
    # - Select user_id_col, timestamp_col, and label_col columns
    # - Rename timestamp_col to "event_timestamp" (Feast convention)
    # - Ensure event_timestamp is datetime type
    # - Drop rows with missing timestamps
    raise NotImplementedError


def get_training_data(
    entity_df: pd.DataFrame,
    feature_service_name: str = "fraud_detection",
    store: FeatureStore | None = None,
) -> pd.DataFrame:
    """Retrieve historical features using point-in-time joins.

    Performs a temporal join between the entity DataFrame and the feature
    store, ensuring no future data leaks into the training set.

    Args:
        entity_df: Entity DataFrame with [user_id, event_timestamp, is_fraud].
        feature_service_name: Name of the Feast feature service.
        store: Optional FeatureStore instance. Creates one if None.

    Returns:
        Training DataFrame with entity keys, features, and labels.
    """
    # TODO: Implement
    # - Initialize store if None
    # - Get the feature service by name from store.get_feature_service()
    # - Call store.get_historical_features(entity_df, features=feature_service)
    # - Convert to DataFrame with .to_df()
    # - Drop rows with all-null features (entities not in the store)
    raise NotImplementedError


def validate_no_temporal_leakage(
    training_df: pd.DataFrame,
    entity_timestamp_col: str = "event_timestamp",
    feature_timestamp_col: str = "timestamp",
) -> bool:
    """Validate that no feature timestamps are after the event timestamp.

    Args:
        training_df: Training DataFrame from get_training_data.
        entity_timestamp_col: Column with the event timestamp.
        feature_timestamp_col: Column with the feature computation timestamp.

    Returns:
        True if no leakage is detected, False otherwise.
    """
    # TODO: Implement
    # - Compare feature_timestamp_col <= entity_timestamp_col for all rows
    # - Return True if all feature timestamps are <= event timestamps
    # - Log any violating rows for debugging
    raise NotImplementedError


def generate_training_dataset(
    transactions_path: str | Path,
    output_path: str | Path,
    store: FeatureStore | None = None,
) -> pd.DataFrame:
    """End-to-end training dataset generation.

    Reads raw transactions, creates entity DataFrame, retrieves historical
    features, validates temporal correctness, and saves the result.

    Args:
        transactions_path: Path to raw transactions parquet file.
        output_path: Path to save the training dataset.
        store: Optional FeatureStore instance.

    Returns:
        Training DataFrame.
    """
    # TODO: Implement
    # - Read transactions from parquet
    # - Create entity DataFrame
    # - Get training data with point-in-time joins
    # - Validate no temporal leakage
    # - Save to output_path as parquet
    # - Return the training DataFrame
    raise NotImplementedError
