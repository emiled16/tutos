"""Tests for the new data sensor."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from dagster.sensors.new_data_sensor import new_data_sensor


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    """Create a temporary data directory with sample files."""
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    return incoming


def _create_data_file(data_dir: Path, filename: str, content: str = "data") -> Path:
    """Helper to create a data file in the incoming directory.

    Args:
        data_dir: The directory to create the file in.
        filename: The file name to create.
        content: File content.

    Returns:
        Path to the created file.
    """
    file_path = data_dir / filename
    file_path.write_text(content)
    return file_path


class TestNewDataSensor:
    def test_no_new_files_returns_empty(self, data_dir: Path) -> None:
        """Test that an empty directory produces no run requests."""
        # TODO: Implement — build a sensor context with no cursor,
        #       evaluate the sensor with an empty data directory,
        #       assert no RunRequests are generated
        raise NotImplementedError

    def test_new_file_triggers_run_request(self, data_dir: Path) -> None:
        """Test that a new data file triggers a RunRequest."""
        # TODO: Implement — create a CSV file in data_dir,
        #       evaluate the sensor,
        #       assert one RunRequest is generated with the file as run_key
        raise NotImplementedError

    def test_cursor_prevents_duplicate_runs(self, data_dir: Path) -> None:
        """Test that the cursor prevents re-triggering for processed files."""
        # TODO: Implement — create a file, evaluate sensor (gets run request),
        #       evaluate sensor again with the updated cursor,
        #       assert no new RunRequests on second evaluation
        raise NotImplementedError

    def test_multiple_new_files(self, data_dir: Path) -> None:
        """Test that multiple new files each generate a RunRequest."""
        # TODO: Implement — create 3 CSV files,
        #       evaluate sensor, assert 3 RunRequests are generated,
        #       each with a unique run_key
        raise NotImplementedError

    def test_only_csv_and_parquet_files_trigger(self, data_dir: Path) -> None:
        """Test that non-data files (e.g., .txt, .log) are ignored."""
        # TODO: Implement — create a .txt file and a .csv file,
        #       evaluate sensor, assert only 1 RunRequest (for the .csv)
        raise NotImplementedError
