"""Custom Airflow operator for data validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from airflow.exceptions import AirflowFailException
from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context


@dataclass
class ValidationRule:
    """A single data validation rule.

    Attributes:
        name: Human-readable rule name.
        column: Column to validate (None for table-level checks).
        check_type: Type of check (e.g., "not_null", "range", "unique", "regex").
        parameters: Check-specific parameters (e.g., {"min": 0, "max": 100}).
        severity: "error" (fails the task) or "warning" (logs but continues).
    """

    name: str
    column: str | None
    check_type: str
    parameters: dict[str, Any]
    severity: str = "error"


@dataclass
class ValidationResult:
    """Result of running a validation rule.

    Attributes:
        rule: The validation rule that was checked.
        passed: Whether the check passed.
        details: Description of what was found.
        failing_rows: Number of rows that failed the check.
    """

    rule: ValidationRule
    passed: bool
    details: str
    failing_rows: int = 0


class DataValidationOperator(BaseOperator):
    """Custom operator that validates a dataset against a set of rules.

    Runs configurable data quality checks and fails the task if any
    error-severity rules are violated. Warning-severity rules are
    logged but do not block the pipeline.

    Attributes:
        data_path: Path to the dataset to validate.
        validation_rules: List of ValidationRule objects to check.
        fail_on_warning: If True, warnings also cause task failure.
    """

    template_fields = ("data_path",)

    def __init__(
        self,
        data_path: str,
        validation_rules: list[ValidationRule] | None = None,
        fail_on_warning: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.data_path = data_path
        self.validation_rules = validation_rules or []
        self.fail_on_warning = fail_on_warning

    def execute(self, context: Context) -> dict[str, Any]:
        """Execute data validation.

        Steps:
        1. Load the dataset
        2. Run each validation rule
        3. Collect results
        4. Fail if any error-severity rules failed
        5. Return validation report

        Args:
            context: Airflow context dictionary.

        Returns:
            Validation report dictionary with pass/fail status and details.

        Raises:
            AirflowFailException: If any error-severity validation rule fails.
        """
        # TODO: Implement data validation execution.
        # self.log.info("Validating data at %s", self.data_path)
        # 1. Load data with pandas
        # 2. Iterate through self.validation_rules
        # 3. Call _run_check() for each rule
        # 4. Collect ValidationResult objects
        # 5. If any error-severity checks failed, raise AirflowFailException
        # 6. Return validation report dict
        raise NotImplementedError

    def _run_check(self, df: Any, rule: ValidationRule) -> ValidationResult:
        """Run a single validation check on the dataframe.

        Args:
            df: Pandas DataFrame to validate.
            rule: The validation rule to apply.

        Returns:
            ValidationResult with pass/fail status and details.
        """
        # TODO: Implement individual check execution.
        # Dispatch based on rule.check_type:
        # - "not_null": Check that column has no null values
        # - "range": Check that column values are within min/max
        # - "unique": Check that column has no duplicates
        # - "regex": Check that column values match a pattern
        # - "row_count": Check that table has min/max number of rows
        raise NotImplementedError
