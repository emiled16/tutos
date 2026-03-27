"""Tests for Great Expectations checkpoints."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from great_expectations.checkpoints.data_checkpoint import (
    create_data_checkpoint,
    run_data_checkpoint,
)
from great_expectations.checkpoints.feature_checkpoint import (
    create_feature_checkpoint,
    run_feature_checkpoint,
)
from great_expectations.checkpoints.prediction_checkpoint import (
    build_prediction_suite,
    create_prediction_checkpoint,
)


@pytest.fixture
def mock_context() -> MagicMock:
    """Create a mock GE Data Context."""
    return MagicMock()


class TestDataCheckpoint:
    """Tests for the raw data checkpoint."""

    def test_create_checkpoint_returns_checkpoint(
        self, mock_context: MagicMock
    ) -> None:
        """create_data_checkpoint should return a Checkpoint object."""
        # TODO: Implement
        # Mock the context methods
        # Call create_data_checkpoint(mock_context)
        # Assert a checkpoint is returned
        raise NotImplementedError

    def test_run_checkpoint_returns_results(
        self, mock_context: MagicMock
    ) -> None:
        """run_data_checkpoint should return a results dictionary."""
        # TODO: Implement
        # Mock checkpoint.run() to return a mock result
        # Assert the return dict has "success" and "results" keys
        raise NotImplementedError


class TestFeatureCheckpoint:
    """Tests for the feature data checkpoint."""

    def test_create_feature_checkpoint(
        self, mock_context: MagicMock
    ) -> None:
        """create_feature_checkpoint should return a Checkpoint."""
        # TODO: Implement
        raise NotImplementedError

    def test_run_feature_checkpoint(
        self, mock_context: MagicMock
    ) -> None:
        """run_feature_checkpoint should return structured results."""
        # TODO: Implement
        raise NotImplementedError


class TestPredictionCheckpoint:
    """Tests for the prediction output checkpoint."""

    def test_create_prediction_checkpoint(
        self, mock_context: MagicMock
    ) -> None:
        """create_prediction_checkpoint should return a Checkpoint."""
        # TODO: Implement
        raise NotImplementedError

    def test_build_prediction_suite_adds_expectations(
        self, mock_context: MagicMock
    ) -> None:
        """build_prediction_suite should add probability range expectations."""
        # TODO: Implement
        # Verify that the suite includes expect_column_values_to_be_between
        # for the probability column with min=0, max=1
        raise NotImplementedError
