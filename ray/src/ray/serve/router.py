"""Request routing and model composition (ensemble) for Ray Serve."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
from ray import serve
from starlette.requests import Request


class AggregationStrategy:
    """Strategies for combining predictions from multiple models."""

    @staticmethod
    def mean(predictions: list[list[float]]) -> list[float]:
        """Average predictions across models.

        Args:
            predictions: List of per-model prediction lists.

        Returns:
            Element-wise mean predictions.
        """
        # TODO: Compute element-wise mean of all prediction lists using numpy
        raise NotImplementedError

    @staticmethod
    def weighted_mean(
        predictions: list[list[float]], weights: list[float]
    ) -> list[float]:
        """Weighted average of predictions.

        Args:
            predictions: Per-model prediction lists.
            weights: Per-model weights (must sum to 1).

        Returns:
            Weighted mean predictions.
        """
        # TODO: Compute weighted element-wise mean, validate that weights sum to ~1
        raise NotImplementedError

    @staticmethod
    def majority_vote(predictions: list[list[int]]) -> list[int]:
        """Majority vote for classification ensembles.

        Args:
            predictions: Per-model class predictions.

        Returns:
            Per-sample majority class.
        """
        # TODO: For each sample position, pick the class with the most votes
        raise NotImplementedError


@dataclass
class EnsembleConfig:
    """Configuration for an ensemble deployment.

    Attributes:
        model_handles: Named mapping of deployment handles.
        aggregation: Aggregation strategy name ("mean", "weighted_mean", "majority_vote").
        weights: Per-model weights (only used with "weighted_mean").
        route_prefix: HTTP route for the ensemble endpoint.
    """

    model_handles: dict[str, Any] = field(default_factory=dict)
    aggregation: str = "mean"
    weights: list[float] = field(default_factory=list)
    route_prefix: str = "/ensemble"


@serve.deployment
class EnsembleRouter:
    """Routes requests to multiple model deployments and aggregates results.

    This deployment demonstrates Ray Serve's composition pattern: one
    deployment calling others via handles.
    """

    def __init__(self, config: EnsembleConfig) -> None:
        """
        Args:
            config: Ensemble configuration with handles and aggregation strategy.
        """
        self.config = config
        self.handles = config.model_handles
        self.aggregation_fn = self._resolve_aggregation(config.aggregation)

    def _resolve_aggregation(self, name: str) -> Any:
        """Map an aggregation name to a callable.

        Args:
            name: One of "mean", "weighted_mean", "majority_vote".

        Returns:
            The corresponding static method from :class:`AggregationStrategy`.
        """
        # TODO: Return the appropriate AggregationStrategy method, raising
        #       ValueError for unknown names
        raise NotImplementedError

    async def __call__(self, request: Request) -> dict[str, Any]:
        """Handle an HTTP request by fanning out to sub-models.

        Args:
            request: Incoming request with JSON body containing ``"data"``.

        Returns:
            Dict with ``"predictions"`` and ``"model_predictions"`` keys.
        """
        # TODO: Parse request, fan out to all handles concurrently using
        #       asyncio.gather, aggregate predictions, and return result
        raise NotImplementedError


def create_ensemble(config: EnsembleConfig) -> serve.DeploymentHandle:
    """Deploy an ensemble router to Ray Serve.

    Args:
        config: Ensemble configuration.

    Returns:
        A handle to the deployed ensemble.
    """
    # TODO: Bind EnsembleRouter with config, deploy via serve.run, return handle
    raise NotImplementedError
