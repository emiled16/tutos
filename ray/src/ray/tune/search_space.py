"""Hyperparameter search space definitions for Ray Tune."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ray import tune


@dataclass
class SearchSpaceConfig:
    """Describes a hyperparameter search space.

    Attributes:
        learning_rate: Continuous range for learning rate (log-uniform).
        batch_size: Discrete choices for batch size.
        num_layers: Integer range for network depth.
        hidden_size: Discrete choices for hidden layer width.
        dropout: Uniform range for dropout probability.
        optimizer: Categorical choice of optimizer name.
        weight_decay: Continuous range for L2 regularization.
        extra: Arbitrary additional parameters.
    """

    learning_rate: tuple[float, float] = (1e-5, 1e-1)
    batch_size: list[int] = field(default_factory=lambda: [32, 64, 128, 256])
    num_layers: tuple[int, int] = (1, 5)
    hidden_size: list[int] = field(default_factory=lambda: [64, 128, 256, 512])
    dropout: tuple[float, float] = (0.0, 0.5)
    optimizer: list[str] = field(default_factory=lambda: ["adam", "sgd", "adamw"])
    weight_decay: tuple[float, float] = (1e-6, 1e-2)
    extra: dict[str, Any] = field(default_factory=dict)


def build_search_space(config: SearchSpaceConfig) -> dict[str, Any]:
    """Convert a :class:`SearchSpaceConfig` into a Ray Tune search space dict.

    The returned dict maps parameter names to ``tune.*`` samplers
    (e.g. ``tune.loguniform``, ``tune.choice``).

    Args:
        config: High-level search space specification.

    Returns:
        A dict suitable for passing as ``param_space`` to ``tune.Tuner``.
    """
    # TODO: Map each SearchSpaceConfig field to the appropriate tune sampler:
    #   - learning_rate  → tune.loguniform(*config.learning_rate)
    #   - batch_size     → tune.choice(config.batch_size)
    #   - num_layers     → tune.randint(*config.num_layers)
    #   - hidden_size    → tune.choice(config.hidden_size)
    #   - dropout        → tune.uniform(*config.dropout)
    #   - optimizer      → tune.choice(config.optimizer)
    #   - weight_decay   → tune.loguniform(*config.weight_decay)
    #   - extra          → merge in as-is
    raise NotImplementedError


def build_conditional_space(
    base_space: dict[str, Any],
    conditions: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Extend a search space with conditional parameters.

    Conditional parameters only apply when a parent parameter takes a
    specific value (e.g., momentum only matters when optimizer == "sgd").

    Args:
        base_space: The base search space dict.
        conditions: Mapping of ``parent_param_value`` →
            dict of child parameter samplers.

    Returns:
        The augmented search space dict with conditional entries.
    """
    # TODO: Merge conditional parameters into the search space. Use
    #       tune.sample_from with a lambda that checks the parent value
    #       to implement conditionality.
    raise NotImplementedError
