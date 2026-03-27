"""Tests for sample size calculation functions."""

from __future__ import annotations

import pytest

from ab_testing.sample_size import (
    power_analysis,
    required_duration_days,
    sample_size_for_means,
    sample_size_for_proportions,
)


class TestSampleSizeForMeans:
    """Tests for sample size calculation with continuous metrics."""

    def test_known_sample_size(self) -> None:
        """Verify against a known analytical result.

        For mde=0.5, std_dev=1.0, alpha=0.05, power=0.80:
        n ≈ 63 per group (two-sample t-test).
        """
        # TODO: Implement test and verify result is approximately 63.
        raise NotImplementedError

    def test_larger_effect_needs_fewer_samples(self) -> None:
        """Larger MDE should require fewer samples."""
        # TODO: Implement test comparing sample sizes for mde=0.2 vs mde=0.5.
        raise NotImplementedError

    def test_higher_power_needs_more_samples(self) -> None:
        """Higher power should require more samples."""
        # TODO: Implement test comparing power=0.80 vs power=0.95.
        raise NotImplementedError

    def test_raises_on_invalid_inputs(self) -> None:
        """Should raise ValueError for mde<=0, std_dev<=0, etc."""
        # TODO: Implement test with various invalid inputs.
        raise NotImplementedError


class TestSampleSizeForProportions:
    """Tests for sample size calculation with binary metrics."""

    def test_known_proportion_sample_size(self) -> None:
        """Verify against a known result for proportion test."""
        # TODO: Implement test, e.g., baseline=0.10, mde=0.02.
        raise NotImplementedError

    def test_higher_baseline_affects_sample_size(self) -> None:
        """Different baseline rates should produce different sample sizes."""
        # TODO: Implement test comparing baseline=0.05 vs baseline=0.50.
        raise NotImplementedError

    def test_raises_on_invalid_baseline(self) -> None:
        """Should raise ValueError for baseline_rate outside (0, 1)."""
        # TODO: Implement test.
        raise NotImplementedError


class TestRequiredDuration:
    """Tests for experiment duration estimation."""

    def test_basic_duration(self) -> None:
        """Verify duration calculation for straightforward inputs."""
        # TODO: Implement test, e.g., 1000 per group, 500 daily traffic.
        raise NotImplementedError

    def test_partial_traffic_increases_duration(self) -> None:
        """Using only a fraction of traffic should increase duration."""
        # TODO: Implement test comparing traffic_fraction=1.0 vs 0.5.
        raise NotImplementedError

    def test_raises_on_zero_traffic(self) -> None:
        """Should raise ValueError for daily_traffic <= 0."""
        # TODO: Implement test.
        raise NotImplementedError


class TestPowerAnalysis:
    """Tests for power calculation given fixed sample size."""

    def test_power_at_design_sample_size(self) -> None:
        """Power should be approximately 0.80 at the designed sample size."""
        # TODO: Implement test using the sample size from sample_size_for_means.
        raise NotImplementedError

    def test_power_increases_with_sample_size(self) -> None:
        """Power should increase as sample size increases."""
        # TODO: Implement test comparing power at n=50 vs n=500.
        raise NotImplementedError

    def test_power_between_zero_and_one(self) -> None:
        """Power should always be in (0, 1)."""
        # TODO: Implement test.
        raise NotImplementedError
