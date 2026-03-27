"""Sequential testing using the Sequential Probability Ratio Test (SPRT)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import numpy as np


class SPRTDecision(str, Enum):
    """Decision states for the SPRT."""

    CONTINUE = "continue"
    REJECT_NULL = "reject_null"
    ACCEPT_NULL = "accept_null"


@dataclass(frozen=True)
class SPRTResult:
    """Result of an SPRT evaluation.

    Attributes:
        decision: Whether to continue, reject H0, or accept H0.
        log_likelihood_ratio: Current cumulative log-likelihood ratio.
        upper_boundary: Log of the upper decision boundary.
        lower_boundary: Log of the lower decision boundary.
        n_observations: Total number of observations processed.
        history: List of cumulative log-likelihood ratios over time.
    """

    decision: SPRTDecision
    log_likelihood_ratio: float
    upper_boundary: float
    lower_boundary: float
    n_observations: int
    history: list[float]


class SequentialTester:
    """Sequential Probability Ratio Test (SPRT) for A/B testing.

    SPRT allows testing after each observation (or batch of observations)
    while controlling both Type I and Type II error rates. It can
    detect large effects with substantially fewer samples than fixed-horizon tests.

    The test compares:
        H₀: p = p₀ (null hypothesis — no effect)
        H₁: p = p₁ (alternative — there is an effect of specified size)
    """

    def __init__(
        self,
        p0: float,
        p1: float,
        alpha: float = 0.05,
        beta: float = 0.20,
    ) -> None:
        """Initialize the sequential tester.

        Args:
            p0: Probability under the null hypothesis (baseline rate).
            p1: Probability under the alternative hypothesis (baseline + MDE).
            alpha: Type I error rate.
            beta: Type II error rate.

        Raises:
            ValueError: If p0, p1 not in (0, 1) or p0 == p1.
        """
        # TODO: Implement initialization.
        # - Validate parameters
        # - Store p0, p1, alpha, beta
        # - Compute decision boundaries:
        #   upper_boundary = log((1 - beta) / alpha)
        #   lower_boundary = log(beta / (1 - alpha))
        # - Initialize cumulative log-likelihood ratio to 0
        # - Initialize observation counter and history list
        raise NotImplementedError

    @property
    def upper_boundary(self) -> float:
        """Upper decision boundary (log scale). Crossing → reject H₀."""
        # TODO: Return the upper boundary.
        raise NotImplementedError

    @property
    def lower_boundary(self) -> float:
        """Lower decision boundary (log scale). Crossing → accept H₀."""
        # TODO: Return the lower boundary.
        raise NotImplementedError

    def update(self, observation: float) -> SPRTDecision:
        """Process a single binary observation and update the test.

        For a binary outcome (0 or 1), the log-likelihood ratio increment is:
            if observation == 1: log(p1 / p0)
            if observation == 0: log((1 - p1) / (1 - p0))

        Args:
            observation: A binary outcome (0 or 1).

        Returns:
            Current decision (CONTINUE, REJECT_NULL, or ACCEPT_NULL).
        """
        # TODO: Implement single observation update.
        # 1. Compute log-likelihood ratio increment
        # 2. Add to cumulative log-likelihood ratio
        # 3. Increment observation counter
        # 4. Append current cumulative LLR to history
        # 5. Check against boundaries and return decision
        raise NotImplementedError

    def update_batch(self, observations: np.ndarray) -> SPRTDecision:
        """Process a batch of observations, stopping early if a boundary is crossed.

        Args:
            observations: Array of binary outcomes (0s and 1s).

        Returns:
            Final decision after processing all observations (or early stop).
        """
        # TODO: Implement batch update.
        # Iterate through observations, calling self.update() for each.
        # Stop early if decision is not CONTINUE.
        raise NotImplementedError

    def get_result(self) -> SPRTResult:
        """Return the current state of the sequential test.

        Returns:
            SPRTResult with current log-likelihood ratio, boundaries,
            observation count, and full history.
        """
        # TODO: Implement result generation.
        raise NotImplementedError

    def reset(self) -> None:
        """Reset the tester to its initial state for a new test run."""
        # TODO: Implement reset.
        # Reset cumulative LLR to 0, counter to 0, clear history.
        raise NotImplementedError
