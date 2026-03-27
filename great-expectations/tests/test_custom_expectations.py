"""Tests for custom expectations."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from great_expectations.expectations.distribution_expectations import (
    DistributionValidator,
    compute_ks_statistic,
    compute_psi,
)
from great_expectations.expectations.ml_expectations import (
    check_class_balance,
    check_feature_correlations,
    detect_target_leakage,
)


@pytest.fixture
def reference_data() -> pd.DataFrame:
    """Reference dataset with known distributions."""
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {
            "feature_a": rng.normal(0, 1, 1000),
            "feature_b": rng.normal(5, 2, 1000),
            "feature_c": rng.uniform(0, 10, 1000),
        }
    )


@pytest.fixture
def balanced_data() -> pd.DataFrame:
    """Dataset with balanced classes and no leakage."""
    rng = np.random.default_rng(42)
    n = 500
    target = np.concatenate([np.zeros(n), np.ones(n)])
    return pd.DataFrame(
        {
            "feat_1": rng.normal(0, 1, 2 * n),
            "feat_2": rng.normal(0, 1, 2 * n),
            "target": target,
        }
    )


class TestKSStatistic:
    """Tests for the KS test computation."""

    def test_identical_distributions_high_p_value(
        self, reference_data: pd.DataFrame
    ) -> None:
        """KS test on identical data should yield a high p-value."""
        # TODO: Implement
        # stat, p = compute_ks_statistic(reference_data["feature_a"],
        #                                 reference_data["feature_a"])
        # Assert p > 0.05
        raise NotImplementedError

    def test_different_distributions_low_p_value(self) -> None:
        """KS test on data from different distributions should yield low p-value."""
        # TODO: Implement
        # Compare N(0,1) vs N(5,1) → p should be very small
        raise NotImplementedError

    def test_returns_statistic_and_p_value(
        self, reference_data: pd.DataFrame
    ) -> None:
        """compute_ks_statistic should return a (statistic, p_value) tuple."""
        # TODO: Implement
        raise NotImplementedError


class TestPSI:
    """Tests for the Population Stability Index computation."""

    def test_identical_distributions_low_psi(
        self, reference_data: pd.DataFrame
    ) -> None:
        """PSI of identical data should be near zero."""
        # TODO: Implement
        # psi = compute_psi(reference_data["feature_a"], reference_data["feature_a"])
        # Assert psi < 0.1
        raise NotImplementedError

    def test_shifted_distribution_high_psi(self) -> None:
        """PSI of shifted distribution should exceed threshold."""
        # TODO: Implement
        # Compare N(0,1) vs N(3,1) → PSI > 0.2
        raise NotImplementedError

    def test_psi_is_non_negative(self, reference_data: pd.DataFrame) -> None:
        """PSI should always be non-negative."""
        # TODO: Implement
        raise NotImplementedError


class TestDistributionValidator:
    """Tests for the DistributionValidator class."""

    def test_no_drift_on_same_data(
        self, reference_data: pd.DataFrame
    ) -> None:
        """No drift should be detected when current = reference."""
        # TODO: Implement
        # validator = DistributionValidator(reference_data)
        # drifted = validator.get_drifted_columns(reference_data)
        # Assert drifted is empty
        raise NotImplementedError

    def test_detects_drift_on_shifted_data(
        self, reference_data: pd.DataFrame
    ) -> None:
        """Drift should be detected when a column is shifted."""
        # TODO: Implement
        # Shift feature_a by +5 and check that it appears in drifted columns
        raise NotImplementedError


class TestTargetLeakage:
    """Tests for target leakage detection."""

    def test_no_leakage_on_clean_data(
        self, balanced_data: pd.DataFrame
    ) -> None:
        """No leakage should be detected on independent features."""
        # TODO: Implement
        # results = detect_target_leakage(balanced_data, "target")
        # Assert no features flagged as leakage
        raise NotImplementedError

    def test_detects_leaky_feature(
        self, balanced_data: pd.DataFrame
    ) -> None:
        """Should detect a feature that is nearly identical to target."""
        # TODO: Implement
        # Add a column that's target + small noise
        # Assert it's flagged as leakage
        raise NotImplementedError


class TestClassBalance:
    """Tests for class balance checking."""

    def test_balanced_data_passes(self, balanced_data: pd.DataFrame) -> None:
        """Balanced data should pass the class balance check."""
        # TODO: Implement
        # result = check_class_balance(balanced_data, "target")
        # Assert result["is_balanced"] is True
        raise NotImplementedError

    def test_imbalanced_data_fails(self) -> None:
        """Severely imbalanced data should fail."""
        # TODO: Implement
        # Create data with 99% class 0, 1% class 1
        # Assert result["is_balanced"] is False
        raise NotImplementedError


class TestFeatureCorrelations:
    """Tests for feature correlation checks."""

    def test_independent_features_no_issues(self) -> None:
        """Independent features should have no high correlations."""
        # TODO: Implement
        raise NotImplementedError

    def test_detects_highly_correlated_pair(self) -> None:
        """Should detect when two features are nearly identical."""
        # TODO: Implement
        # Create two columns where col_b = col_a + small noise
        # Assert the pair is flagged
        raise NotImplementedError
