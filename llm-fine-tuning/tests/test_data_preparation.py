"""Tests for the data preparation pipeline."""

import json
import tempfile
from pathlib import Path

import pytest

from llm_fine_tuning.data.dataset_preparation import (
    apply_chat_template,
    clean_conversation,
    format_as_instruction_pair,
    load_raw_data,
    prepare_dataset,
)


@pytest.fixture
def sample_conversation() -> dict:
    """Create a sample conversation for testing."""
    return {
        "messages": [
            {"role": "user", "content": "My laptop won't connect to WiFi."},
            {
                "role": "assistant",
                "content": "Let's troubleshoot. First, check if WiFi is enabled "
                "in your system settings. Go to Settings > Network > WiFi.",
            },
        ]
    }


@pytest.fixture
def sample_data_file(tmp_path: Path, sample_conversation: dict) -> Path:
    """Create a temporary JSONL data file."""
    file_path = tmp_path / "test_data.jsonl"
    with open(file_path, "w") as f:
        for _ in range(5):
            f.write(json.dumps(sample_conversation) + "\n")
    return file_path


class TestLoadRawData:
    """Tests for loading raw data files."""

    def test_load_valid_jsonl(self, sample_data_file: Path) -> None:
        """Valid JSONL file should load all records."""
        # TODO: Implement
        raise NotImplementedError

    def test_load_nonexistent_file_raises(self) -> None:
        """Loading a missing file should raise FileNotFoundError."""
        # TODO: Implement
        raise NotImplementedError

    def test_load_empty_file(self, tmp_path: Path) -> None:
        """An empty file should return an empty list."""
        # TODO: Implement
        raise NotImplementedError


class TestCleanConversation:
    """Tests for conversation cleaning."""

    def test_clean_valid_conversation(self, sample_conversation: dict) -> None:
        """A valid conversation should pass through cleaning."""
        # TODO: Implement
        raise NotImplementedError

    def test_strips_whitespace(self) -> None:
        """Extra whitespace in messages should be stripped."""
        # TODO: Implement
        raise NotImplementedError

    def test_removes_pii(self) -> None:
        """Email addresses and phone numbers should be removed."""
        # TODO: Implement
        raise NotImplementedError

    def test_filters_too_short(self) -> None:
        """Conversations with too few turns should return None."""
        # TODO: Implement
        raise NotImplementedError


class TestFormatAsInstructionPair:
    """Tests for instruction/response formatting."""

    def test_format_basic_conversation(self, sample_conversation: dict) -> None:
        """A conversation should be formatted as instruction/input/response."""
        # TODO: Implement
        raise NotImplementedError

    def test_output_has_required_keys(self, sample_conversation: dict) -> None:
        """Output should have instruction, input, and response keys."""
        # TODO: Implement
        raise NotImplementedError


class TestPrepareDataset:
    """Tests for the full data preparation pipeline."""

    def test_produces_train_val_test_splits(self, sample_data_file: Path) -> None:
        """prepare_dataset should return train, validation, test splits."""
        # TODO: Implement
        raise NotImplementedError

    def test_splits_are_non_overlapping(self, sample_data_file: Path) -> None:
        """No examples should appear in multiple splits."""
        # TODO: Implement
        raise NotImplementedError
