"""Ray cluster configuration and initialization."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

import ray


@dataclass
class ClusterConfig:
    """Configuration for a Ray cluster connection.

    Attributes:
        address: Ray cluster address (e.g. "auto", "ray://<head>:10001").
        num_cpus: Override detected CPU count (local mode only).
        num_gpus: Override detected GPU count (local mode only).
        object_store_memory: Bytes allocated to the plasma object store.
        dashboard_host: Bind address for the Ray dashboard.
        dashboard_port: Port for the Ray dashboard.
        custom_resources: Additional logical resources (e.g. {"special_hw": 2}).
        runtime_env: Runtime environment specification (pip, conda, env vars, etc.).
        logging_level: Python logging level name for Ray internals.
    """

    address: str | None = field(default_factory=lambda: os.getenv("RAY_ADDRESS"))
    num_cpus: int | None = field(
        default_factory=lambda: int(v) if (v := os.getenv("RAY_NUM_CPUS")) else None
    )
    num_gpus: int | None = field(
        default_factory=lambda: int(v) if (v := os.getenv("RAY_NUM_GPUS")) else None
    )
    object_store_memory: int | None = field(
        default_factory=lambda: int(v)
        if (v := os.getenv("RAY_OBJECT_STORE_MEMORY"))
        else None
    )
    dashboard_host: str = field(
        default_factory=lambda: os.getenv("RAY_DASHBOARD_HOST", "127.0.0.1")
    )
    dashboard_port: int = field(
        default_factory=lambda: int(os.getenv("RAY_DASHBOARD_PORT", "8265"))
    )
    custom_resources: dict[str, float] = field(default_factory=dict)
    runtime_env: dict[str, Any] | None = None
    logging_level: str = "INFO"


def init_cluster(config: ClusterConfig) -> ray.runtime_context.RuntimeContext:
    """Initialize or connect to a Ray cluster.

    If Ray is already initialized the existing context is returned without
    re-initializing.  Otherwise ``ray.init`` is called with the provided
    *config*.

    Args:
        config: Cluster configuration dataclass.

    Returns:
        The Ray runtime context for the active session.
    """
    # TODO: Initialize Ray cluster with the given configuration, handling
    #       existing connections (ray.is_initialized). Pass through address,
    #       num_cpus, num_gpus, object_store_memory, dashboard settings,
    #       custom_resources, runtime_env, and logging_level.
    raise NotImplementedError


def shutdown_cluster(graceful: bool = True) -> None:
    """Shutdown the Ray cluster connection.

    Args:
        graceful: If True, wait for pending tasks to complete before shutting down.
    """
    # TODO: Shut down Ray cleanly, respecting the graceful flag
    raise NotImplementedError


def get_cluster_resources() -> dict[str, float]:
    """Return the total resources available in the connected cluster.

    Returns:
        Mapping of resource name to total quantity (e.g. {"CPU": 8, "GPU": 2}).
    """
    # TODO: Query ray.cluster_resources() and return the result
    raise NotImplementedError


def get_available_resources() -> dict[str, float]:
    """Return the currently *available* (unused) resources.

    Returns:
        Mapping of resource name to available quantity.
    """
    # TODO: Query ray.available_resources() and return the result
    raise NotImplementedError
