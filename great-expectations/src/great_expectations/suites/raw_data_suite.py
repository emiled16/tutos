"""Expectation suite for raw data validation."""

from __future__ import annotations

from typing import Any

import great_expectations as gx
from great_expectations.data_context import FileDataContext


def build_raw_data_suite(
    context: FileDataContext,
    suite_name: str = "raw_data_suite",
    expected_columns: list[str] | None = None,
    row_count_range: tuple[int, int] = (100, 1_000_000),
) -> None:
    """Build an expectation suite for validating raw/incoming data.

    Creates expectations for:
    - Table-level: row count within range
    - Schema: required columns exist
    - Completeness: critical columns have no nulls
    - Ranges: numeric columns within expected bounds
    - Categorical: categorical columns have values from expected sets

    Args:
        context: Great Expectations Data Context.
        suite_name: Name for the suite.
        expected_columns: List of required column names.
        row_count_range: (min, max) expected row count.
    """
    # TODO: Implement
    # - Create or get suite from context
    # - Add expect_table_row_count_to_be_between
    # - Add expect_column_to_exist for each expected column
    # - Add expect_column_values_to_not_be_null for critical columns
    # - Add expect_column_values_to_be_between for numeric columns
    # - Add expect_column_values_to_be_in_set for categorical columns
    # - Save the suite to the context
    raise NotImplementedError


def get_default_raw_data_expectations() -> list[dict[str, Any]]:
    """Return a list of default expectation configurations for raw data.

    Provides a template that can be customized per dataset.

    Returns:
        List of expectation config dictionaries.
    """
    # TODO: Implement
    # Return a list of dicts like:
    # [
    #   {"expectation_type": "expect_table_row_count_to_be_between",
    #    "kwargs": {"min_value": 1}},
    #   {"expectation_type": "expect_column_values_to_not_be_null",
    #    "kwargs": {"column": "id"}},
    #   ...
    # ]
    raise NotImplementedError
