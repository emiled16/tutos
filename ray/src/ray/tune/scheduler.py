"""Trial scheduler configuration for Ray Tune (ASHA, PBT, HyperBand)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from ray.tune.schedulers import (
    ASHAScheduler,
    HyperBandScheduler,
    PopulationBasedTraining,
    TrialScheduler,
)


class SchedulerType(Enum):
    """Supported trial scheduler types."""

    ASHA = "asha"
    PBT = "pbt"
    HYPERBAND = "hyperband"


@dataclass
class ASHAConfig:
    """Configuration for the ASHA (Async Successive Halving) scheduler.

    Attributes:
        max_t: Maximum number of training iterations per trial.
        grace_period: Minimum iterations before a trial can be stopped.
        reduction_factor: Factor by which to reduce the number of trials at each rung.
        brackets: Number of brackets (higher = more exploration).
    """

    max_t: int = 100
    grace_period: int = 10
    reduction_factor: int = 3
    brackets: int = 1


@dataclass
class PBTConfig:
    """Configuration for Population-Based Training.

    Attributes:
        perturbation_interval: Number of training iterations between perturbations.
        hyperparam_mutations: Dict of parameter name → mutation spec
            (e.g. ``{"lr": tune.uniform(1e-5, 1e-1)}``).
        quantile_fraction: Fraction defining the exploit boundary.
        resample_probability: Probability of resampling (vs. perturbing) a parameter.
    """

    perturbation_interval: int = 10
    hyperparam_mutations: dict[str, Any] | None = None
    quantile_fraction: float = 0.25
    resample_probability: float = 0.25


@dataclass
class HyperBandConfig:
    """Configuration for the HyperBand scheduler.

    Attributes:
        max_t: Maximum training iterations.
        reduction_factor: Successive halving reduction factor.
    """

    max_t: int = 100
    reduction_factor: int = 3


def create_scheduler(
    scheduler_type: SchedulerType,
    metric: str,
    mode: str,
    **kwargs: Any,
) -> TrialScheduler:
    """Factory function to create a trial scheduler.

    Args:
        scheduler_type: Which scheduler algorithm to use.
        metric: Name of the metric to optimize (e.g. ``"val_loss"``).
        mode: ``"min"`` or ``"max"``.
        **kwargs: Forwarded to the scheduler's config dataclass.

    Returns:
        A configured :class:`TrialScheduler` instance.

    Raises:
        ValueError: If *scheduler_type* is not recognized.
    """
    # TODO: Dispatch on scheduler_type to build the appropriate config
    #       dataclass, then instantiate and return the corresponding scheduler
    #       (ASHAScheduler, PopulationBasedTraining, or HyperBandScheduler)
    #       with metric and mode
    raise NotImplementedError
