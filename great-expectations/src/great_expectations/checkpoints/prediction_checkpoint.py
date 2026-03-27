"""Checkpoint for prediction output validation."""

from __future__ import annotations

from typing import Any

import great_expectations as gx
from great_expectations.checkpoint import Checkpoint
from great_expectations.data_context import FileDataContext


def create_prediction_checkpoint(
    context: FileDataContext,
    checkpoint_name: str = "prediction_checkpoint",
    expectation_suite_name: str = "prediction_suite",
    datasource_name: str = "pandas_datasource",
    asset_name: str = "predictions",
) -> Checkpoint:
    """Create a checkpoint for validating model prediction outputs.

    Validates that prediction outputs have the correct format, probability
    ranges, and reasonable class distributions.

    Args:
        context: Great Expectations Data Context.
        checkpoint_name: Name for the checkpoint.
        expectation_suite_name: Suite to validate against.
        datasource_name: Name of the data source.
        asset_name: Name of the data asset.

    Returns:
        Configured Checkpoint.
    """
    # TODO: Implement
    # - Build batch request from datasource and asset
    # - Create checkpoint with prediction-specific suite
    # - Include actions for storing results and updating Data Docs
    raise NotImplementedError


def build_prediction_suite(
    context: FileDataContext,
    suite_name: str = "prediction_suite",
    prediction_column: str = "prediction",
    probability_column: str = "probability",
) -> None:
    """Build expectation suite for prediction outputs.

    Expectations:
    - prediction column exists and has no nulls
    - probability column exists, has no nulls, values in [0, 1]
    - prediction values are in the expected label set
    - row count is within expected range

    Args:
        context: Great Expectations Data Context.
        suite_name: Name for the expectation suite.
        prediction_column: Name of the prediction label column.
        probability_column: Name of the probability column.
    """
    # TODO: Implement
    # - Create or get the expectation suite
    # - Add expectations for column existence, null checks
    # - Add expect_column_values_to_be_between for probability [0, 1]
    # - Add expect_column_values_to_be_in_set for prediction labels
    # - Save the suite
    raise NotImplementedError
