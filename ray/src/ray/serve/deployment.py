"""Ray Serve model deployment."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
from ray import serve
from starlette.requests import Request


@dataclass
class DeploymentConfig:
    """Configuration for a Ray Serve model deployment.

    Attributes:
        model_path: Path to a saved model checkpoint.
        model_class: Fully-qualified class name or the class itself.
        model_kwargs: Constructor arguments for the model.
        num_replicas: Initial replica count.
        max_ongoing_requests: Max concurrent requests per replica.
        ray_actor_options: Resource dict (e.g. ``{"num_cpus": 1, "num_gpus": 0.5}``).
        route_prefix: HTTP route prefix for this deployment.
    """

    model_path: str | Path
    model_class: str | type = ""
    model_kwargs: dict[str, Any] | None = None
    num_replicas: int = 1
    max_ongoing_requests: int = 100
    ray_actor_options: dict[str, Any] | None = None
    route_prefix: str = "/predict"


@serve.deployment
class ModelDeployment:
    """A Ray Serve deployment that loads a PyTorch model and serves predictions.

    The deployment loads the model once in ``__init__`` and reuses it
    for every incoming request.
    """

    def __init__(self, config: DeploymentConfig) -> None:
        """
        Args:
            config: Deployment and model configuration.
        """
        self.config = config
        self.model: nn.Module | None = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # TODO: Load the model from config.model_path:
        #   1. Instantiate the model class with config.model_kwargs
        #   2. Load state_dict from config.model_path
        #   3. Move to self.device and set to eval mode
        #   4. Assign to self.model

    async def __call__(self, request: Request) -> dict[str, Any]:
        """Handle an HTTP prediction request.

        Expects a JSON body with a ``"data"`` key containing the input tensor
        as a nested list.

        Args:
            request: Incoming Starlette request.

        Returns:
            Dict with ``"predictions"`` key.
        """
        # TODO: Parse request JSON, convert data to tensor, run self.model
        #       in torch.no_grad(), return predictions as a JSON-serializable dict
        raise NotImplementedError

    def predict(self, data: list[list[float]]) -> list[float]:
        """Programmatic prediction (called via DeploymentHandle).

        Args:
            data: Input features as a 2-D list.

        Returns:
            Model predictions as a flat list.
        """
        # TODO: Convert data to tensor, run inference, return as list
        raise NotImplementedError


def deploy_model(config: DeploymentConfig) -> serve.DeploymentHandle:
    """Deploy a model to Ray Serve and return a handle.

    Args:
        config: Deployment configuration.

    Returns:
        A :class:`DeploymentHandle` for programmatic access.
    """
    # TODO: Bind ModelDeployment with config, set num_replicas and
    #       ray_actor_options from config, call serve.run(), return the handle
    raise NotImplementedError
