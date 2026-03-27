"""Tests for frequentist statistical tests."""

from __future__ import annotations

import numpy as np
import pytest

from ab_testing.statistics import (
    TestResult,
    apply_bonferroni_correction,
    chi_squared_test,
    cohens_d,
    confidence_interval_difference,
    mann_whitney_u_test,
    welch_ttest,
)


class TestCohensD:
    """Tests for Cohen's d effect size calculation."""

    def test_identical_groups_returns_zero(self) -> None:
        """Cohen's d should be 0 when both groups have the same distribution."""
        # TODO: Implement test with two identical arrays.
        raise NotImplementedError

    def test_known_effect_size(self) -> None:
        """Cohen's d should match a hand-calculated value for known data."""
        # TODO: Implement test with groups that have a known d ≈ 0.5.
        raise NotImplementedError

    def test_positive_when_treatment_higher(self) -> None:
        """Cohen's d should be positive when treatment mean > control mean."""
        # TODO: Implement test.
        raise NotImplementedError

    def test_raises_on_small_group(self) -> None:
        """Should raise ValueError when a group has fewer than 2 observations."""
        # TODO: Implement test.
        raise NotImplementedError


class TestConfidenceInterval:
    """Tests for confidence interval of the difference in means."""

    def test_ci_contains_true_difference(self) -> None:
        """95% CI should contain the true difference most of the time."""
        # TODO: Implement test by generating data with known difference
        # and checking that the CI contains it.
        raise NotImplementedError

    def test_ci_width_decreases_with_sample_size(self) -> None:
        """Larger samples should produce narrower confidence intervals."""
        # TODO: Implement test comparing CI widths for n=100 vs n=10000.
        raise NotImplementedError

    def test_ci_centered_at_zero_for_identical_distributions(self) -> None:
        """CI should be approximately centered at 0 for same-distribution groups."""
        # TODO: Implement test.
        raise NotImplementedError


class TestWelchTTest:
    """Tests for Welch's t-test."""

    def test_significant_difference(self) -> None:
        """Should detect a significant difference between groups with different means."""
        # TODO: Implement test with clearly different groups (e.g., N(0,1) vs N(1,1)).
        raise NotImplementedError

    def test_no_significant_difference(self) -> None:
        """Should not find significance when groups are drawn from the same distribution."""
        # TODO: Implement test with two N(0,1) samples.
        raise NotImplementedError

    def test_returns_test_result_type(self) -> None:
        """Should return a TestResult dataclass with all fields populated."""
        # TODO: Implement test checking return type and field presence.
        raise NotImplementedError

    def test_effect_size_included(self) -> None:
        """TestResult should include a non-zero effect size for different groups."""
        # TODO: Implement test.
        raise NotImplementedError


class TestChiSquaredTest:
    """Tests for chi-squared test on proportions."""

    def test_significant_proportion_difference(self) -> None:
        """Should detect significance for clearly different conversion rates."""
        # TODO: Implement test, e.g., 100/1000 vs 150/1000.
        raise NotImplementedError

    def test_no_significant_difference(self) -> None:
        """Should not find significance for similar conversion rates."""
        # TODO: Implement test, e.g., 100/1000 vs 105/1000.
        raise NotImplementedError

    def test_raises_on_low_expected_counts(self) -> None:
        """Should raise ValueError when expected cell counts are below 5."""
        # TODO: Implement test with very small sample sizes.
        raise NotImplementedError


class TestMannWhitneyU:
    """Tests for Mann-Whitney U test."""

    def test_detects_shifted_distribution(self) -> None:
        """Should detect a significant difference for shifted distributions."""
        # TODO: Implement test.
        raise NotImplementedError

    def test_no_difference_same_distribution(self) -> None:
        """Should not find significance for samples from the same distribution."""
        # TODO: Implement test.
        raise NotImplementedError

    def test_handles_ties(self) -> None:
        """Should handle data with tied values correctly."""
        # TODO: Implement test with data containing many ties.
        raise NotImplementedError


class TestBonferroniCorrection:
    """Tests for Bonferroni multiple testing correction."""

    def test_single_test_unchanged(self) -> None:
        """A single p-value should be unchanged by Bonferroni correction."""
        # TODO: Implement test.
        raise NotImplementedError

    def test_adjusts_multiple_pvalues(self) -> None:
        """Multiple p-values should be multiplied by the number of tests."""
        # TODO: Implement test, e.g., [0.01, 0.03, 0.04] with 3 tests.
        raise NotImplementedError

    def test_adjusted_pvalue_capped_at_one(self) -> None:
        """Adjusted p-values should never exceed 1.0."""
        # TODO: Implement test with p-values that would exceed 1.0 after correction.
        raise NotImplementedError
