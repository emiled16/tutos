"""Data simulator for testing the A/B testing framework."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class SimulationConfig:
    """Configuration for simulating A/B test data.

    Attributes:
        n_control: Number of observations for the control group.
        n_treatment: Number of observations for the treatment group.
        control_rate: Baseline conversion rate (for binary metrics).
        treatment_rate: Treatment conversion rate (for binary metrics).
        control_mean: Baseline mean (for continuous metrics).
        treatment_mean: Treatment mean (for continuous metrics).
        std_dev: Standard deviation for continuous metrics.
        random_seed: Seed for reproducibility.
    """

    n_control: int = 1000
    n_treatment: int = 1000
    control_rate: float = 0.10
    treatment_rate: float = 0.12
    control_mean: float = 50.0
    treatment_mean: float = 52.0
    std_dev: float = 10.0
    random_seed: int | None = 42


def simulate_binary_experiment(
    config: SimulationConfig,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate binary outcome data (e.g., conversions) for an A/B test.

    Args:
        config: Simulation configuration.

    Returns:
        Tuple of (control_conversions, treatment_conversions) as binary arrays.
    """
    # TODO: Implement binary data simulation.
    # Use np.random.Generator.binomial or .random to generate binary outcomes
    # with the specified conversion rates.
    raise NotImplementedError


def simulate_continuous_experiment(
    config: SimulationConfig,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate continuous outcome data (e.g., revenue) for an A/B test.

    Args:
        config: Simulation configuration.

    Returns:
        Tuple of (control_values, treatment_values) as float arrays.
    """
    # TODO: Implement continuous data simulation.
    # Use np.random.Generator.normal to generate values with specified means and std_dev.
    raise NotImplementedError


def simulate_time_series_experiment(
    config: SimulationConfig,
    n_days: int = 14,
) -> pd.DataFrame:
    """Simulate daily A/B test data over time.

    Creates a DataFrame with daily observations, allowing
    analysis of time trends and sequential testing.

    Args:
        config: Simulation configuration.
        n_days: Number of days to simulate.

    Returns:
        DataFrame with columns: day, variant, user_id, converted, value.
    """
    # TODO: Implement time series simulation.
    # - Distribute observations across days (roughly equal per day)
    # - Add realistic daily variation (e.g., weekday/weekend effects)
    # - Include user_id, variant label, binary conversion, and continuous value
    raise NotImplementedError


def simulate_with_novelty_effect(
    config: SimulationConfig,
    novelty_boost: float = 0.05,
    novelty_decay_days: int = 7,
    n_days: int = 30,
) -> pd.DataFrame:
    """Simulate data where the treatment has a decaying novelty effect.

    The treatment group initially shows a higher effect that decays
    over time, simulating user novelty/primacy bias.

    Args:
        config: Simulation configuration.
        novelty_boost: Additional lift during the novelty period.
        novelty_decay_days: Number of days for the novelty effect to decay.
        n_days: Total simulation duration.

    Returns:
        DataFrame with daily observations including novelty-affected metrics.
    """
    # TODO: Implement novelty effect simulation.
    # The treatment rate on day d should be:
    # effective_rate = treatment_rate + novelty_boost * exp(-d / novelty_decay_days)
    raise NotImplementedError
