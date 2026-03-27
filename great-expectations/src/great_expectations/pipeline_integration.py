"""Integration helpers for running Great Expectations in an ML pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import pandas as pd
from great_expectations.data_context import FileDataContext


class PipelineStage(str, Enum):
    """Stages in the ML pipeline where validation occurs."""

    RAW_DATA = "raw_data"
    FEATURES = "features"
    PREDICTIONS = "predictions"


@dataclass
class ValidationResult:
    """Result of a validation run at a pipeline stage."""

    stage: PipelineStage
    success: bool
    statistics: dict[str, Any] = field(default_factory=dict)
    failed_expectations: list[dict[str, Any]] = field(default_factory=list)
    run_id: str = ""

    @property
    def n_expectations(self) -> int:
        """Total number of expectations evaluated."""
        return self.statistics.get("evaluated_expectations", 0)

    @property
    def n_failures(self) -> int:
        """Number of failed expectations."""
        return self.statistics.get("unsuccessful_expectations", 0)


class PipelineValidator:
    """Orchestrates data quality validation across pipeline stages.

    Runs the appropriate checkpoint at each stage and collects results
    for reporting.
    """

    def __init__(self, context: FileDataContext) -> None:
        """Initialize with a GE Data Context.

        Args:
            context: Configured Great Expectations Data Context.
        """
        self.context = context
        self.results: list[ValidationResult] = []

    def validate_stage(
        self,
        stage: PipelineStage,
        data: pd.DataFrame,
        checkpoint_name: str | None = None,
        fail_fast: bool = False,
    ) -> ValidationResult:
        """Validate data at a specific pipeline stage.

        Args:
            stage: The pipeline stage being validated.
            data: DataFrame to validate.
            checkpoint_name: Override the default checkpoint name for this stage.
            fail_fast: If True, raise an exception on validation failure.

        Returns:
            ValidationResult with success status and details.

        Raises:
            DataQualityError: If fail_fast is True and validation fails.
        """
        # TODO: Implement
        # - Determine checkpoint_name from stage if not provided
        # - Run the checkpoint with the provided data
        # - Parse the GE result into a ValidationResult
        # - Append to self.results
        # - If fail_fast and not success, raise DataQualityError
        # - Return the result
        raise NotImplementedError

    def validate_pipeline(
        self,
        raw_data: pd.DataFrame,
        transform_fn: Any = None,
        predict_fn: Any = None,
        fail_fast: bool = True,
    ) -> list[ValidationResult]:
        """Run validation across all pipeline stages.

        Args:
            raw_data: Raw input data.
            transform_fn: Function to transform raw data into features.
            predict_fn: Function to generate predictions from features.
            fail_fast: Stop pipeline on first validation failure.

        Returns:
            List of ValidationResult for each stage.
        """
        # TODO: Implement
        # 1. Validate raw_data at RAW_DATA stage
        # 2. If transform_fn, apply it and validate at FEATURES stage
        # 3. If predict_fn, apply it and validate at PREDICTIONS stage
        # - Return all results
        raise NotImplementedError

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of all validation results.

        Returns:
            Dictionary with overall_success, stage results, and statistics.
        """
        # TODO: Implement
        # - Aggregate results across all stages
        # - Return overall pass/fail and per-stage summaries
        raise NotImplementedError


class DataQualityError(Exception):
    """Raised when data quality validation fails in fail_fast mode."""

    def __init__(self, result: ValidationResult) -> None:
        self.result = result
        super().__init__(
            f"Data quality check failed at stage {result.stage.value}: "
            f"{result.n_failures}/{result.n_expectations} expectations failed"
        )
