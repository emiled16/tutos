"""Sample size calculation for A/B test experiment design."""

from __future__ import annotations

import math

from scipy import stats


def sample_size_for_means(
    mde: float,
    std_dev: float,
    alpha: float = 0.05,
    power: float = 0.80,
    ratio: float = 1.0,
) -> int:
    """Calculate the required sample size per group for comparing means.

    Uses the formula for a two-sample t-test:
    n = (z_{α/2} + z_β)² × (1 + 1/ratio) × σ² / δ²

    Args:
        mde: Minimum detectable effect (absolute difference in means).
        std_dev: Estimated standard deviation of the metric.
        alpha: Significance level (two-sided).
        power: Desired statistical power (1 - β).
        ratio: Ratio of treatment to control group size (n_b / n_a).

    Returns:
        Required sample size for the control group (ceiling).

    Raises:
        ValueError: If mde <= 0, std_dev <= 0, alpha not in (0, 1), or power not in (0, 1).
    """
    # TODO: Implement sample size calculation for means.
    # 1. Validate inputs
    # 2. Compute z-scores: z_alpha = stats.norm.ppf(1 - alpha/2), z_beta = stats.norm.ppf(power)
    # 3. n_a = (z_alpha + z_beta)² × (1 + 1/ratio) × std_dev² / mde²
    # 4. Return math.ceil(n_a)
    raise NotImplementedError


def sample_size_for_proportions(
    baseline_rate: float,
    mde: float,
    alpha: float = 0.05,
    power: float = 0.80,
    ratio: float = 1.0,
) -> int:
    """Calculate sample size per group for comparing proportions.

    Uses the normal approximation to the binomial.

    Args:
        baseline_rate: Expected conversion rate of the control group.
        mde: Minimum detectable effect (absolute difference in proportions).
        alpha: Significance level (two-sided).
        power: Desired statistical power.
        ratio: Ratio of treatment to control group size.

    Returns:
        Required sample size for the control group.

    Raises:
        ValueError: If baseline_rate not in (0, 1) or baseline_rate + mde not in (0, 1).
    """
    # TODO: Implement sample size calculation for proportions.
    # p1 = baseline_rate, p2 = baseline_rate + mde
    # p_bar = (p1 + ratio * p2) / (1 + ratio)
    # n = ((z_alpha * sqrt((1+1/ratio) * p_bar * (1-p_bar)) +
    #        z_beta * sqrt(p1*(1-p1) + p2*(1-p2)/ratio)) / mde)²
    raise NotImplementedError


def required_duration_days(
    sample_size_per_group: int,
    daily_traffic: int,
    traffic_fraction: float = 1.0,
    n_groups: int = 2,
) -> int:
    """Estimate the number of days required to collect enough data.

    Args:
        sample_size_per_group: Required sample size per variant group.
        daily_traffic: Average number of users/events per day.
        traffic_fraction: Fraction of total traffic allocated to the experiment.
        n_groups: Number of groups in the experiment (default 2).

    Returns:
        Number of days needed (ceiling).

    Raises:
        ValueError: If daily_traffic <= 0 or traffic_fraction not in (0, 1].
    """
    # TODO: Implement duration estimation.
    # total_needed = sample_size_per_group * n_groups
    # daily_per_experiment = daily_traffic * traffic_fraction
    # Return math.ceil(total_needed / daily_per_experiment)
    raise NotImplementedError


def power_analysis(
    sample_size: int,
    mde: float,
    std_dev: float,
    alpha: float = 0.05,
    ratio: float = 1.0,
) -> float:
    """Calculate the statistical power given a fixed sample size.

    This is the inverse problem: given n, what power do we achieve?

    Args:
        sample_size: Available sample size per group (control).
        mde: Minimum detectable effect.
        std_dev: Estimated standard deviation.
        alpha: Significance level.
        ratio: Ratio of treatment to control.

    Returns:
        Statistical power (probability of detecting the effect).
    """
    # TODO: Implement power calculation.
    # se = std_dev * sqrt(1/sample_size + 1/(sample_size * ratio))
    # z_alpha = stats.norm.ppf(1 - alpha/2)
    # z_beta = mde / se - z_alpha
    # power = stats.norm.cdf(z_beta)
    raise NotImplementedError
