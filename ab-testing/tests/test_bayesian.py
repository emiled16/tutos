"""Tests for Bayesian A/B testing methods."""

from __future__ import annotations

import numpy as np
import pytest

from ab_testing.bayesian import BayesianResult, BetaBinomialModel


class TestBetaBinomialPosterior:
    """Tests for posterior computation."""

    def test_posterior_with_uniform_prior(self) -> None:
        """Posterior with Beta(1,1) prior and 50 successes in 100 trials."""
        # TODO: Implement test.
        # Posterior should be Beta(51, 51).
        raise NotImplementedError

    def test_posterior_with_informative_prior(self) -> None:
        """Posterior with Beta(10, 10) prior should incorporate prior information."""
        # TODO: Implement test.
        # Beta(10,10) + 30 successes in 50 trials → Beta(40, 30).
        raise NotImplementedError

    def test_raises_on_invalid_input(self) -> None:
        """Should raise ValueError for successes > trials or negative values."""
        # TODO: Implement test.
        raise NotImplementedError


class TestProbabilityBBeatsA:
    """Tests for Monte Carlo probability computation."""

    def test_clear_winner(self) -> None:
        """When B has much higher conversion, P(B > A) should be close to 1."""
        # TODO: Implement test with e.g. A: 50/1000, B: 150/1000.
        raise NotImplementedError

    def test_tied_variants(self) -> None:
        """When A and B have identical data, P(B > A) should be close to 0.5."""
        # TODO: Implement test with identical data for both variants.
        raise NotImplementedError

    def test_probability_between_zero_and_one(self) -> None:
        """P(B > A) should always be in [0, 1]."""
        # TODO: Implement test.
        raise NotImplementedError


class TestExpectedLoss:
    """Tests for expected loss computation."""

    def test_losses_sum_to_mean_difference(self) -> None:
        """Expected loss of A + expected loss of B ≈ |E[p_B] - E[p_A]|."""
        # TODO: Implement test.
        raise NotImplementedError

    def test_winner_has_lower_loss(self) -> None:
        """The clearly better variant should have lower expected loss."""
        # TODO: Implement test.
        raise NotImplementedError

    def test_losses_are_non_negative(self) -> None:
        """Expected losses should always be >= 0."""
        # TODO: Implement test.
        raise NotImplementedError


class TestCredibleInterval:
    """Tests for credible interval computation."""

    def test_95_ci_contains_true_rate(self) -> None:
        """95% credible interval should contain the true rate (with high probability)."""
        # TODO: Implement test by simulating data with known rate.
        raise NotImplementedError

    def test_wider_ci_with_less_data(self) -> None:
        """Credible interval should be wider with fewer observations."""
        # TODO: Implement test comparing CI widths for n=100 vs n=10000.
        raise NotImplementedError

    def test_ci_bounds_between_zero_and_one(self) -> None:
        """Credible interval bounds should be in [0, 1] for proportions."""
        # TODO: Implement test.
        raise NotImplementedError


class TestRunTest:
    """Tests for the full Bayesian A/B test."""

    def test_recommends_treatment_when_clearly_better(self) -> None:
        """Should recommend treatment when it clearly outperforms control."""
        # TODO: Implement test.
        raise NotImplementedError

    def test_recommends_continue_when_inconclusive(self) -> None:
        """Should recommend continuing when results are not yet decisive."""
        # TODO: Implement test with very small sample sizes.
        raise NotImplementedError

    def test_returns_bayesian_result(self) -> None:
        """Should return a BayesianResult with all fields populated."""
        # TODO: Implement test checking return type and fields.
        raise NotImplementedError
