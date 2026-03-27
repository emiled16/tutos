"""Integration tests for the pipeline validation workflow."""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest

from great_expectations.pipeline_integration import (
    DataQualityError,
    PipelineStage,
    PipelineValidator,
    ValidationResult,
)


@pytest.fixture
def mock_context() -> MagicMock:
    """Create a mock GE Data Context."""
    return MagicMock()


@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Create sample data for pipeline tests."""
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {
            "id": range(100),
            "feature_1": rng.normal(0, 1, 100),
            "feature_2": rng.normal(5, 2, 100),
            "target": rng.integers(0, 2, 100),
        }
    )


class TestValidationResult:
    """Tests for the ValidationResult dataclass."""

    def test_n_expectations_from_statistics(self) -> None:
        """n_expectations should read from statistics dict."""
        # TODO: Implement
        # result = ValidationResult(
        #     stage=PipelineStage.RAW_DATA,
        #     success=True,
        #     statistics={"evaluated_expectations": 10, "unsuccessful_expectations": 0}
        # )
        # Assert result.n_expectations == 10
        raise NotImplementedError

    def test_n_failures_from_statistics(self) -> None:
        """n_failures should read from statistics dict."""
        # TODO: Implement
        raise NotImplementedError

    def test_defaults_to_zero_when_missing(self) -> None:
        """Properties should return 0 when statistics are empty."""
        # TODO: Implement
        raise NotImplementedError


class TestPipelineValidator:
    """Tests for the PipelineValidator class."""

    def test_validate_stage_appends_result(
        self, mock_context: MagicMock, sample_data: pd.DataFrame
    ) -> None:
        """validate_stage should append a result to self.results."""
        # TODO: Implement
        # validator = PipelineValidator(mock_context)
        # Mock the checkpoint run
        # Call validator.validate_stage(PipelineStage.RAW_DATA, sample_data)
        # Assert len(validator.results) == 1
        raise NotImplementedError

    def test_validate_stage_fail_fast_raises(
        self, mock_context: MagicMock, sample_data: pd.DataFrame
    ) -> None:
        """validate_stage with fail_fast should raise on failure."""
        # TODO: Implement
        # Mock checkpoint to return failure
        # Assert DataQualityError is raised
        raise NotImplementedError

    def test_validate_pipeline_runs_all_stages(
        self, mock_context: MagicMock, sample_data: pd.DataFrame
    ) -> None:
        """validate_pipeline should run validation at each stage."""
        # TODO: Implement
        # Provide transform_fn and predict_fn
        # Assert results for all three stages
        raise NotImplementedError

    def test_get_summary_aggregates_results(
        self, mock_context: MagicMock
    ) -> None:
        """get_summary should aggregate across all stages."""
        # TODO: Implement
        raise NotImplementedError


class TestDataQualityError:
    """Tests for the DataQualityError exception."""

    def test_error_message_includes_stage(self) -> None:
        """Error message should include the failing stage name."""
        # TODO: Implement
        # result = ValidationResult(stage=PipelineStage.FEATURES, success=False,
        #                           statistics={"evaluated_expectations": 5,
        #                                       "unsuccessful_expectations": 2})
        # err = DataQualityError(result)
        # Assert "features" in str(err)
        raise NotImplementedError

    def test_error_carries_result(self) -> None:
        """DataQualityError should carry the ValidationResult."""
        # TODO: Implement
        raise NotImplementedError
