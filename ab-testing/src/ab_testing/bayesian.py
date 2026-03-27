"""Bayesian A/B testing using the Beta-Binomial conjugate model."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats as sp_stats


@dataclass(frozen=True)
class BayesianResult:
    """Result of a Bayesian A/B test.

    Attributes:
        prob_b_beats_a: Probability that treatment is better than control.
        expected_loss_a: Expected loss from choosing control.
        expected_loss_b: Expected loss from choosing treatment.
        credible_interval_a: 95% credible interval for control rate.
        credible_interval_b: 95% credible interval for treatment rate.
        posterior_a: Tuple of (alpha, beta) for control posterior.
        posterior_b: Tuple of (alpha, beta) for treatment posterior.
        risk_threshold: Maximum acceptable expected loss.
        decision: Recommended decision string.
    """

    prob_b_beats_a: float
    expected_loss_a: float
    expected_loss_b: float
    credible_interval_a: tuple[float, float]
    credible_interval_b: tuple[float, float]
    posterior_a: tuple[float, float]
    posterior_b: tuple[float, float]
    risk_threshold: float
    decision: str


class BetaBinomialModel:
    """Bayesian A/B testing using Beta-Binomial conjugate model.

    The Beta distribution is the conjugate prior for the Binomial
    likelihood, meaning the posterior is also a Beta distribution
    with updated parameters.

    Prior: Beta(prior_alpha, prior_beta)
    Posterior: Beta(prior_alpha + successes, prior_beta + failures)
    """

    def __init__(
        self,
        prior_alpha: float = 1.0,
        prior_beta: float = 1.0,
    ) -> None:
        """Initialize the model with a prior.

        Args:
            prior_alpha: Alpha parameter of the Beta prior (default: 1.0 = uniform).
            prior_beta: Beta parameter of the Beta prior (default: 1.0 = uniform).
        """
        self.prior_alpha = prior_alpha
        self.prior_beta = prior_beta

    def compute_posterior(
        self, successes: int, trials: int
    ) -> tuple[float, float]:
        """Compute the posterior Beta distribution parameters.

        Args:
            successes: Number of successes (e.g., conversions).
            trials: Total number of trials.

        Returns:
            Tuple of (posterior_alpha, posterior_beta).

        Raises:
            ValueError: If successes > trials or either is negative.
        """
        # TODO: Implement posterior computation.
        # posterior_alpha = prior_alpha + successes
        # posterior_beta = prior_beta + (trials - successes)
        raise NotImplementedError

    def probability_b_beats_a(
        self,
        successes_a: int,
        trials_a: int,
        successes_b: int,
        trials_b: int,
        n_samples: int = 100_000,
    ) -> float:
        """Compute P(p_B > p_A) via Monte Carlo sampling.

        Draws samples from both posterior distributions and computes
        the fraction where treatment samples exceed control samples.

        Args:
            successes_a: Conversions in control group.
            trials_a: Total users in control group.
            successes_b: Conversions in treatment group.
            trials_b: Total users in treatment group.
            n_samples: Number of Monte Carlo samples to draw.

        Returns:
            Probability that treatment rate exceeds control rate.
        """
        # TODO: Implement Monte Carlo probability computation.
        # 1. Compute posteriors for both variants
        # 2. Draw n_samples from each posterior (scipy.stats.beta.rvs)
        # 3. Return the fraction where samples_b > samples_a
        raise NotImplementedError

    def expected_loss(
        self,
        successes_a: int,
        trials_a: int,
        successes_b: int,
        trials_b: int,
        n_samples: int = 100_000,
    ) -> tuple[float, float]:
        """Compute expected loss for choosing each variant.

        Expected loss of choosing A = E[max(p_B - p_A, 0)]
        Expected loss of choosing B = E[max(p_A - p_B, 0)]

        Args:
            successes_a: Conversions in control.
            trials_a: Total in control.
            successes_b: Conversions in treatment.
            trials_b: Total in treatment.
            n_samples: Number of Monte Carlo samples.

        Returns:
            Tuple of (expected_loss_a, expected_loss_b).
        """
        # TODO: Implement expected loss computation.
        # 1. Draw samples from both posteriors
        # 2. loss_a = mean(max(samples_b - samples_a, 0))
        # 3. loss_b = mean(max(samples_a - samples_b, 0))
        raise NotImplementedError

    def credible_interval(
        self,
        successes: int,
        trials: int,
        credibility: float = 0.95,
    ) -> tuple[float, float]:
        """Compute the credible interval for the conversion rate.

        Args:
            successes: Number of successes.
            trials: Total number of trials.
            credibility: Credibility level (default 0.95).

        Returns:
            Tuple of (lower_bound, upper_bound).
        """
        # TODO: Implement credible interval using scipy.stats.beta.ppf.
        # Compute the posterior, then find the (1-credibility)/2 and
        # (1+credibility)/2 quantiles.
        raise NotImplementedError

    def run_test(
        self,
        successes_a: int,
        trials_a: int,
        successes_b: int,
        trials_b: int,
        risk_threshold: float = 0.01,
        n_samples: int = 100_000,
    ) -> BayesianResult:
        """Run a complete Bayesian A/B test.

        Args:
            successes_a: Conversions in control.
            trials_a: Total in control.
            successes_b: Conversions in treatment.
            trials_b: Total in treatment.
            risk_threshold: Maximum acceptable expected loss to declare a winner.
            n_samples: Number of Monte Carlo samples.

        Returns:
            BayesianResult with all computed metrics and a decision.
        """
        # TODO: Implement full Bayesian test.
        # 1. Compute prob_b_beats_a
        # 2. Compute expected losses
        # 3. Compute credible intervals for both variants
        # 4. Compute posteriors for both variants
        # 5. Make a decision:
        #    - If expected_loss_b < risk_threshold → "Choose treatment"
        #    - If expected_loss_a < risk_threshold → "Choose control"
        #    - Otherwise → "Continue testing"
        raise NotImplementedError
