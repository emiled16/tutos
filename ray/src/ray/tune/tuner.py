"""Tuner setup and execution for Ray Tune experiments."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ray import tune
from ray.tune import ResultGrid
from ray.tune.schedulers import TrialScheduler


@dataclass
class TunerConfig:
    """High-level configuration for a Tune experiment.

    Attributes:
        metric: Metric name to optimize.
        mode: ``"min"`` or ``"max"``.
        num_samples: Number of trials to run.
        max_concurrent_trials: Limit on parallel trials (None = unlimited).
        storage_path: Directory for experiment results and checkpoints.
        experiment_name: Human-readable experiment name.
        resources_per_trial: Resource dict (e.g. ``{"cpu": 2, "gpu": 0.5}``).
        stop_conditions: Early-stop conditions
            (e.g. ``{"val_loss": 0.01, "training_iteration": 100}``).
    """

    metric: str = "val_loss"
    mode: str = "min"
    num_samples: int = 50
    max_concurrent_trials: int | None = None
    storage_path: str | Path = "./ray_results"
    experiment_name: str = "tune_experiment"
    resources_per_trial: dict[str, float] = field(
        default_factory=lambda: {"cpu": 1, "gpu": 0}
    )
    stop_conditions: dict[str, Any] = field(default_factory=dict)


def create_tuner(
    trainable: Any,
    param_space: dict[str, Any],
    tuner_config: TunerConfig,
    scheduler: TrialScheduler | None = None,
) -> tune.Tuner:
    """Build a :class:`tune.Tuner` from configuration objects.

    Args:
        trainable: A trainable function or class.
        param_space: Search space dict (from ``build_search_space``).
        tuner_config: Experiment-level settings.
        scheduler: Optional trial scheduler (from ``create_scheduler``).

    Returns:
        A configured ``Tuner`` ready to call ``.fit()``.
    """
    # TODO: Construct a tune.TuneConfig with metric, mode, num_samples,
    #       max_concurrent_trials, and scheduler. Construct a
    #       tune.RunConfig with storage_path, name, and stop conditions.
    #       Merge resources_per_trial into param_space. Return tune.Tuner(…).
    raise NotImplementedError


def run_tuning(tuner: tune.Tuner) -> ResultGrid:
    """Execute a tuning experiment.

    Args:
        tuner: A configured ``Tuner`` instance.

    Returns:
        The :class:`ResultGrid` with all trial results.
    """
    # TODO: Call tuner.fit() and return the ResultGrid
    raise NotImplementedError


def get_best_config(results: ResultGrid) -> dict[str, Any]:
    """Extract the best hyperparameter configuration from results.

    Args:
        results: Completed experiment results.

    Returns:
        The config dict of the best trial.
    """
    # TODO: Use results.get_best_result() to retrieve the best trial,
    #       then return its config
    raise NotImplementedError


def get_results_df(results: ResultGrid) -> Any:
    """Convert experiment results to a Pandas DataFrame for analysis.

    Args:
        results: Completed experiment results.

    Returns:
        A DataFrame with one row per trial.
    """
    # TODO: Call results.get_dataframe() and return it
    raise NotImplementedError
