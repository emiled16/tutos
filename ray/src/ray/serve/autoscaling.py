"""Autoscaling configuration for Ray Serve deployments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ray import serve


@dataclass
class AutoscalingConfig:
    """Autoscaling policy for a Ray Serve deployment.

    Attributes:
        min_replicas: Minimum number of replicas (never scales below this).
        max_replicas: Maximum number of replicas.
        initial_replicas: Replica count at deployment start.
        target_ongoing_requests: Target in-flight requests per replica;
            the controller scales up when the actual value exceeds this.
        upscale_delay_s: Seconds to wait before adding replicas.
        downscale_delay_s: Seconds of low load before removing replicas.
        smoothing_factor: Exponential smoothing factor for load metrics.
        metrics_interval_s: How often the controller samples load metrics.
    """

    min_replicas: int = 1
    max_replicas: int = 10
    initial_replicas: int | None = None
    target_ongoing_requests: float = 5.0
    upscale_delay_s: float = 30.0
    downscale_delay_s: float = 300.0
    smoothing_factor: float = 1.0
    metrics_interval_s: float = 10.0


def build_autoscaling_options(config: AutoscalingConfig) -> dict[str, Any]:
    """Convert an :class:`AutoscalingConfig` to a dict for ``@serve.deployment``.

    The returned dict is suitable for passing as the ``autoscaling_config``
    parameter of ``@serve.deployment``.

    Args:
        config: Autoscaling policy dataclass.

    Returns:
        Dict matching Ray Serve's autoscaling_config schema.
    """
    # TODO: Build and return a dict with keys matching Ray Serve's
    #       autoscaling_config: min_replicas, max_replicas, initial_replicas,
    #       target_ongoing_requests, upscale_delay_s, downscale_delay_s,
    #       smoothing_factor, metrics_interval_s
    raise NotImplementedError


def apply_autoscaling(
    deployment: Any,
    config: AutoscalingConfig,
) -> Any:
    """Apply autoscaling configuration to a Ray Serve deployment.

    This replaces a static ``num_replicas`` with a dynamic autoscaling policy.

    Args:
        deployment: A Serve deployment (class decorated with ``@serve.deployment``).
        config: Autoscaling settings.

    Returns:
        The deployment with autoscaling options applied.
    """
    # TODO: Use deployment.options(autoscaling_config=...) to attach the
    #       autoscaling configuration to the deployment, and return it
    raise NotImplementedError


def get_deployment_status(name: str) -> dict[str, Any]:
    """Query the current status of a named deployment.

    Args:
        name: The registered deployment name.

    Returns:
        Dict with ``"name"``, ``"status"``, ``"num_replicas"``, and
        ``"message"`` keys.
    """
    # TODO: Use serve.status() to query the deployment controller and
    #       extract status information for the named deployment
    raise NotImplementedError
