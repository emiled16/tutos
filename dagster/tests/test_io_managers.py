"""Tests for custom IO managers.

Tests ParquetIOManager and ModelIOManager with temporary directories
to verify serialization round-trips.
"""

from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier

from dagster.io_managers.model_io_manager import ModelIOManager
from dagster.io_managers.parquet_io_manager import ParquetIOManager


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """A simple DataFrame for testing Parquet IO."""
    return pd.DataFrame(
        {
            "feature_1": [1.0, 2.0, 3.0, 4.0, 5.0],
            "feature_2": [10.0, 20.0, 30.0, 40.0, 50.0],
            "label": [0, 1, 0, 1, 0],
        }
    )


@pytest.fixture
def fitted_model() -> RandomForestClassifier:
    """A fitted RandomForest model for testing Model IO."""
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([0, 1, 0, 1])
    model = RandomForestClassifier(n_estimators=5, random_state=42)
    model.fit(X, y)
    return model


def _mock_output_context(asset_key: str, partition_key: str = "2024-01-15") -> MagicMock:
    """Create a mock OutputContext for testing IO managers.

    Args:
        asset_key: The asset key name.
        partition_key: The partition key.

    Returns:
        A MagicMock configured as an OutputContext.
    """
    context = MagicMock()
    context.asset_key.path = ["test", asset_key]
    context.partition_key = partition_key
    context.has_partition_key = True
    context.add_output_metadata = MagicMock()
    context.log = MagicMock()
    return context


def _mock_input_context(asset_key: str, partition_key: str = "2024-01-15") -> MagicMock:
    """Create a mock InputContext for testing IO managers.

    Args:
        asset_key: The asset key name.
        partition_key: The partition key.

    Returns:
        A MagicMock configured as an InputContext.
    """
    context = MagicMock()
    context.asset_key.path = ["test", asset_key]
    context.partition_key = partition_key
    context.has_partition_key = True
    context.log = MagicMock()
    return context


class TestParquetIOManager:
    def test_write_and_read_roundtrip(
        self, tmp_path: Path, sample_dataframe: pd.DataFrame
    ) -> None:
        """Test that writing and reading a DataFrame preserves data."""
        # TODO: Implement — create ParquetIOManager with base_path=tmp_path,
        #       call handle_output with sample_dataframe,
        #       call load_input with the same context,
        #       assert the loaded DataFrame equals the original
        raise NotImplementedError

    def test_creates_directories(self, tmp_path: Path, sample_dataframe: pd.DataFrame) -> None:
        """Test that handle_output creates parent directories."""
        # TODO: Implement — use a nested path that doesn't exist,
        #       assert handle_output creates it and writes the file
        raise NotImplementedError

    def test_load_nonexistent_file_raises(self, tmp_path: Path) -> None:
        """Test that loading a non-existent file raises FileNotFoundError."""
        # TODO: Implement — call load_input for a path that doesn't exist,
        #       assert FileNotFoundError is raised
        raise NotImplementedError

    def test_partitioned_storage_path(self, tmp_path: Path, sample_dataframe: pd.DataFrame) -> None:
        """Test that different partitions write to different files."""
        # TODO: Implement — write two partitions (2024-01-15, 2024-01-16),
        #       assert two separate files are created
        raise NotImplementedError


class TestModelIOManager:
    def test_write_and_read_model_roundtrip(
        self, tmp_path: Path, fitted_model: RandomForestClassifier
    ) -> None:
        """Test that serializing and deserializing a model preserves it."""
        # TODO: Implement — create ModelIOManager with base_path=tmp_path,
        #       call handle_output with the fitted model,
        #       call load_input, assert the loaded model can predict
        raise NotImplementedError

    def test_model_predictions_match_after_roundtrip(
        self, tmp_path: Path, fitted_model: RandomForestClassifier
    ) -> None:
        """Test that model predictions are identical after serialization roundtrip."""
        # TODO: Implement — save and load the model,
        #       compare predictions on test data before and after
        raise NotImplementedError

    def test_load_nonexistent_model_raises(self, tmp_path: Path) -> None:
        """Test that loading a non-existent model file raises FileNotFoundError."""
        # TODO: Implement — call load_input for a model that doesn't exist,
        #       assert FileNotFoundError is raised
        raise NotImplementedError
