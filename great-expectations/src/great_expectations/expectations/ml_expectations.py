"""ML-specific expectations: feature correlation, target leakage, class balance."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def detect_target_leakage(
    df: pd.DataFrame,
    target_column: str,
    correlation_threshold: float = 0.95,
) -> list[dict[str, Any]]:
    """Detect features that may be leaking the target variable.

    A feature with very high correlation to the target is suspicious
    because it may contain information derived from the target that
    wouldn't be available at prediction time.

    Args:
        df: DataFrame with features and target column.
        target_column: Name of the target/label column.
        correlation_threshold: Absolute correlation above which a feature
                               is flagged as potential leakage.

    Returns:
        List of dicts with keys: feature, correlation, is_leakage.
    """
    # TODO: Implement
    # - Compute correlation of each numeric column with target_column
    # - Flag columns where |correlation| > correlation_threshold
    # - Exclude the target column itself
    # - Return list of {feature, correlation, is_leakage} dicts
    raise NotImplementedError


def check_class_balance(
    df: pd.DataFrame,
    target_column: str,
    min_minority_ratio: float = 0.01,
    max_majority_ratio: float = 0.99,
) -> dict[str, Any]:
    """Check the class distribution of a target variable.

    Flags if the minority class proportion is below min_minority_ratio
    or the majority class exceeds max_majority_ratio.

    Args:
        df: DataFrame with the target column.
        target_column: Name of the target/label column.
        min_minority_ratio: Minimum acceptable proportion for minority class.
        max_majority_ratio: Maximum acceptable proportion for majority class.

    Returns:
        Dictionary with class_counts, class_ratios, is_balanced, and details.
    """
    # TODO: Implement
    # - Compute value counts and proportions for target_column
    # - Check if minority class ratio >= min_minority_ratio
    # - Check if majority class ratio <= max_majority_ratio
    # - Return results dict with class_counts, class_ratios, is_balanced
    raise NotImplementedError


def check_feature_correlations(
    df: pd.DataFrame,
    high_correlation_threshold: float = 0.95,
    expected_correlations: dict[tuple[str, str], float] | None = None,
    correlation_tolerance: float = 0.1,
) -> dict[str, Any]:
    """Check feature-feature correlations for issues.

    Detects:
    - Highly correlated feature pairs (potential redundancy)
    - Correlation deviations from expected values (potential data issues)

    Args:
        df: DataFrame with feature columns.
        high_correlation_threshold: Threshold for flagging high correlations.
        expected_correlations: Optional dict of (col_a, col_b) → expected_corr.
        correlation_tolerance: Acceptable deviation from expected correlations.

    Returns:
        Dictionary with highly_correlated_pairs, correlation_deviations,
        and correlation_matrix.
    """
    # TODO: Implement
    # - Compute correlation matrix for numeric columns
    # - Find pairs with |correlation| > high_correlation_threshold (exclude diagonal)
    # - If expected_correlations provided, check deviations beyond tolerance
    # - Return results dict
    raise NotImplementedError


class MLDataValidator:
    """Combines ML-specific validation checks into a single interface.

    Runs target leakage, class balance, and correlation checks,
    then returns a comprehensive validation report.
    """

    def __init__(
        self,
        target_column: str,
        leakage_threshold: float = 0.95,
        min_minority_ratio: float = 0.01,
        correlation_threshold: float = 0.95,
    ) -> None:
        self.target_column = target_column
        self.leakage_threshold = leakage_threshold
        self.min_minority_ratio = min_minority_ratio
        self.correlation_threshold = correlation_threshold

    def validate(self, df: pd.DataFrame) -> dict[str, Any]:
        """Run all ML-specific validation checks.

        Args:
            df: DataFrame to validate.

        Returns:
            Dictionary with leakage_results, balance_results,
            correlation_results, and overall_pass.
        """
        # TODO: Implement
        # - Call detect_target_leakage
        # - Call check_class_balance
        # - Call check_feature_correlations
        # - Set overall_pass = True only if no leakage, balanced, and no issues
        # - Return combined results
        raise NotImplementedError
