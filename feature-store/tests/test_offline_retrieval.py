"""Tests for point-in-time correct offline feature retrieval."""

from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pytest

from feature_store.offline_retrieval import (
    create_entity_dataframe,
    validate_no_temporal_leakage,
)


@pytest.fixture
def sample_transactions() -> pd.DataFrame:
    """Create sample transaction data for testing."""
    return pd.DataFrame(
        {
            "user_id": ["u1", "u1", "u2", "u2", "u3"],
            "amount": [100.0, 50.0, 200.0, 75.0, 30.0],
            "timestamp": pd.to_datetime(
                [
                    "2024-03-01 10:00:00",
                    "2024-03-02 14:00:00",
                    "2024-03-01 09:00:00",
                    "2024-03-03 11:00:00",
                    "2024-03-02 16:00:00",
                ]
            ),
            "is_fraud": [0, 0, 1, 0, 0],
        }
    )


class TestCreateEntityDataframe:
    """Tests for entity DataFrame creation."""

    def test_creates_correct_columns(
        self, sample_transactions: pd.DataFrame
    ) -> None:
        """Entity DataFrame should have user_id, event_timestamp, is_fraud."""
        # TODO: Implement
        # Call create_entity_dataframe(sample_transactions)
        # Assert columns are ["user_id", "event_timestamp", "is_fraud"]
        raise NotImplementedError

    def test_renames_timestamp_column(
        self, sample_transactions: pd.DataFrame
    ) -> None:
        """Timestamp column should be renamed to event_timestamp."""
        # TODO: Implement
        raise NotImplementedError

    def test_drops_rows_with_missing_timestamps(self) -> None:
        """Rows with NaT timestamps should be dropped."""
        # TODO: Implement
        # Create DataFrame with some NaT timestamps
        # Assert they are removed
        raise NotImplementedError

    def test_preserves_all_rows(
        self, sample_transactions: pd.DataFrame
    ) -> None:
        """All valid rows should be preserved."""
        # TODO: Implement
        raise NotImplementedError


class TestValidateNoTemporalLeakage:
    """Tests for temporal leakage validation."""

    def test_valid_data_returns_true(self) -> None:
        """Data with all feature timestamps <= event timestamps passes."""
        # TODO: Implement
        # Create DataFrame where all feature timestamps are before event times
        # Assert validate_no_temporal_leakage returns True
        raise NotImplementedError

    def test_detects_future_leak(self) -> None:
        """Data with feature timestamp after event timestamp fails."""
        # TODO: Implement
        # Create DataFrame where some feature timestamps are after event times
        # Assert validate_no_temporal_leakage returns False
        raise NotImplementedError

    def test_equal_timestamps_are_valid(self) -> None:
        """Feature timestamp exactly equal to event timestamp is valid."""
        # TODO: Implement
        raise NotImplementedError
