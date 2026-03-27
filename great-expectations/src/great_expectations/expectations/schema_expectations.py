"""Custom expectations for schema validation."""

from __future__ import annotations

from typing import Any

import pandas as pd
from great_expectations.core import ExpectationConfiguration
from great_expectations.expectations.expectation import (
    ColumnAggregateExpectation,
    ExpectationValidationResult,
)


class ExpectColumnTypeToBe(ColumnAggregateExpectation):
    """Expect a column to have a specific pandas dtype.

    Validates that a column's dtype matches the expected type string
    (e.g., "int64", "float64", "object", "datetime64[ns]").

    Args:
        column: The column name.
        expected_type: The expected pandas dtype string.
    """

    metric_dependencies = ("column.dtype",)
    success_keys = ("expected_type",)
    default_kwarg_values = {
        "expected_type": None,
    }

    def _validate(
        self,
        metrics: dict[str, Any],
        runtime_configuration: dict | None = None,
        result_format: str = "BASIC",
    ) -> ExpectationValidationResult:
        """Validate that the column dtype matches expected_type.

        Args:
            metrics: Dictionary of computed metrics.
            runtime_configuration: Optional runtime settings.
            result_format: Level of detail in the result.

        Returns:
            ExpectationValidationResult with success and observed value.
        """
        # TODO: Implement
        # - Get the actual dtype from metrics["column.dtype"]
        # - Compare with self.configuration.kwargs["expected_type"]
        # - Return ExpectationValidationResult with:
        #   success=True/False, result={"observed_value": str(actual_dtype)}
        raise NotImplementedError


class ExpectRequiredColumnsToExist(ColumnAggregateExpectation):
    """Expect that a set of required columns all exist in the dataset.

    This is a table-level check that verifies schema completeness.

    Args:
        required_columns: List of column names that must be present.
    """

    metric_dependencies = ()
    success_keys = ("required_columns",)
    default_kwarg_values = {
        "required_columns": [],
    }

    def _validate(
        self,
        metrics: dict[str, Any],
        runtime_configuration: dict | None = None,
        result_format: str = "BASIC",
    ) -> ExpectationValidationResult:
        """Validate that all required columns exist.

        Returns:
            ExpectationValidationResult with missing columns listed.
        """
        # TODO: Implement
        # - Get the DataFrame columns from the batch
        # - Find which required_columns are missing
        # - Return success=True if none missing, False otherwise
        # - Include missing_columns in the result details
        raise NotImplementedError


def validate_schema(
    df: pd.DataFrame,
    expected_columns: dict[str, str],
) -> dict[str, list[str]]:
    """Validate DataFrame schema against expected column types.

    Args:
        df: DataFrame to validate.
        expected_columns: Mapping of column_name → expected_dtype_string.

    Returns:
        Dictionary with "missing_columns", "type_mismatches", and
        "extra_columns" lists.
    """
    # TODO: Implement
    # - Check which expected columns are missing from df
    # - Check which present columns have wrong types
    # - Identify extra columns not in expected_columns
    # - Return {"missing_columns": [...], "type_mismatches": [...],
    #           "extra_columns": [...]}
    raise NotImplementedError
