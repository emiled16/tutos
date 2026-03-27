"""Frequentist statistical tests for A/B testing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from scipy import stats


@dataclass(frozen=True)
class TestResult:
    """Result of a statistical test.

    Attributes:
        test_name: Name of the statistical test performed.
        statistic: The test statistic value.
        p_value: The p-value for the test.
        significant: Whether the result is significant at the given alpha.
        alpha: Significance level used.
        confidence_interval: Tuple of (lower, upper) bounds for the
            difference in means/proportions.
        effect_size: Standardized effect size (Cohen's d or equivalent).
        interpretation: Human-readable interpretation of the result.
    """

    test_name: str
    statistic: float
    p_value: float
    significant: bool
    alpha: float
    confidence_interval: tuple[float, float]
    effect_size: float
    interpretation: str


def cohens_d(group_a: np.ndarray, group_b: np.ndarray) -> float:
    """Compute Cohen's d effect size between two groups.

    Uses the pooled standard deviation as the denominator.

    Args:
        group_a: Observations from group A (control).
        group_b: Observations from group B (treatment).

    Returns:
        Cohen's d effect size. Positive values indicate group_b > group_a.

    Raises:
        ValueError: If either group has fewer than 2 observations.
    """
    # TODO: Implement Cohen's d calculation.
    # d = (mean_b - mean_a) / pooled_std
    # pooled_std = sqrt(((n_a-1)*var_a + (n_b-1)*var_b) / (n_a + n_b - 2))
    raise NotImplementedError


def confidence_interval_difference(
    group_a: np.ndarray,
    group_b: np.ndarray,
    alpha: float = 0.05,
) -> tuple[float, float]:
    """Compute confidence interval for the difference in means (B - A).

    Uses Welch's approximation for the degrees of freedom.

    Args:
        group_a: Observations from group A.
        group_b: Observations from group B.
        alpha: Significance level (default 0.05 for 95% CI).

    Returns:
        Tuple of (lower_bound, upper_bound) for the difference.
    """
    # TODO: Implement confidence interval for the difference in means.
    # diff = mean_b - mean_a
    # se = sqrt(var_a/n_a + var_b/n_b)
    # Use t-distribution with Welch-Satterthwaite degrees of freedom
    raise NotImplementedError


def welch_ttest(
    group_a: np.ndarray,
    group_b: np.ndarray,
    alpha: float = 0.05,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
) -> TestResult:
    """Perform Welch's t-test comparing two independent samples.

    Welch's t-test does not assume equal variances between groups.

    Args:
        group_a: Observations from the control group.
        group_b: Observations from the treatment group.
        alpha: Significance level.
        alternative: Direction of the test.

    Returns:
        TestResult with t-statistic, p-value, CI, and effect size.

    Raises:
        ValueError: If either group has fewer than 2 observations.
    """
    # TODO: Implement Welch's t-test.
    # - Validate input sizes
    # - Compute t-statistic and p-value using scipy.stats.ttest_ind (equal_var=False)
    # - Compute confidence interval via confidence_interval_difference()
    # - Compute effect size via cohens_d()
    # - Build interpretation string
    # - Return TestResult
    raise NotImplementedError


def chi_squared_test(
    conversions_a: int,
    total_a: int,
    conversions_b: int,
    total_b: int,
    alpha: float = 0.05,
) -> TestResult:
    """Perform chi-squared test for comparing two proportions.

    Uses a 2x2 contingency table of conversions/non-conversions.

    Args:
        conversions_a: Number of conversions in group A.
        total_a: Total observations in group A.
        conversions_b: Number of conversions in group B.
        total_b: Total observations in group B.
        alpha: Significance level.

    Returns:
        TestResult with chi-squared statistic, p-value, and effect size.

    Raises:
        ValueError: If any expected cell count is less than 5.
    """
    # TODO: Implement chi-squared test for proportions.
    # - Build the 2x2 contingency table
    # - Use scipy.stats.chi2_contingency
    # - Compute confidence interval for difference in proportions
    # - Compute effect size (Cramér's V or difference in proportions)
    # - Check expected cell counts >= 5
    raise NotImplementedError


def mann_whitney_u_test(
    group_a: np.ndarray,
    group_b: np.ndarray,
    alpha: float = 0.05,
    alternative: Literal["two-sided", "greater", "less"] = "two-sided",
) -> TestResult:
    """Perform Mann-Whitney U test (non-parametric alternative to t-test).

    Compares the distributions of two independent samples using ranks.

    Args:
        group_a: Observations from the control group.
        group_b: Observations from the treatment group.
        alpha: Significance level.
        alternative: Direction of the test.

    Returns:
        TestResult with U-statistic, p-value, and rank-biserial effect size.

    Raises:
        ValueError: If either group is empty.
    """
    # TODO: Implement Mann-Whitney U test.
    # - Use scipy.stats.mannwhitneyu
    # - Compute rank-biserial correlation as effect size: r = 1 - (2U)/(n_a * n_b)
    # - Build interpretation string
    raise NotImplementedError


def apply_bonferroni_correction(
    p_values: list[float], alpha: float = 0.05
) -> list[tuple[float, bool]]:
    """Apply Bonferroni correction for multiple testing.

    Args:
        p_values: List of p-values from individual tests.
        alpha: Family-wise significance level.

    Returns:
        List of (adjusted_p_value, significant) tuples.
    """
    # TODO: Implement Bonferroni correction.
    # adjusted_p = min(p * n_tests, 1.0) for each p-value
    raise NotImplementedError
