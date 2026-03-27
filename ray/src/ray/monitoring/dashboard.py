"""Ray dashboard integration and custom metrics."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

import ray


@dataclass
class MetricDefinition:
    """Defines a custom metric to expose via Ray's metrics system.

    Attributes:
        name: Metric name (Prometheus-compatible, e.g. ``"my_app_requests_total"``).
        description: Human-readable description.
        tag_keys: Label keys attached to each observation.
        metric_type: One of ``"counter"``, ``"gauge"``, ``"histogram"``.
    """

    name: str
    description: str = ""
    tag_keys: list[str] = field(default_factory=list)
    metric_type: str = "gauge"


class MetricsCollector:
    """Creates and manages custom Ray metrics (Counter, Gauge, Histogram).

    Metrics are automatically exported to Prometheus when Ray's metrics
    endpoint is enabled (``/metrics`` on the dashboard port).
    """

    def __init__(self) -> None:
        self.metrics: dict[str, Any] = {}

    def register(self, definition: MetricDefinition) -> None:
        """Register a new metric.

        Args:
            definition: The metric specification.

        Raises:
            ValueError: If a metric with the same name is already registered.
        """
        # TODO: Use ray.util.metrics (Counter, Gauge, or Histogram) to create
        #       the metric based on definition.metric_type, store it in
        #       self.metrics keyed by definition.name. Raise ValueError on
        #       duplicate registration.
        raise NotImplementedError

    def increment(self, name: str, value: float = 1.0, tags: dict[str, str] | None = None) -> None:
        """Increment a counter or gauge metric.

        Args:
            name: Registered metric name.
            value: Amount to increment by.
            tags: Label values for this observation.

        Raises:
            KeyError: If the metric is not registered.
        """
        # TODO: Look up the metric by name, call .inc(value, tags)
        raise NotImplementedError

    def set_gauge(self, name: str, value: float, tags: dict[str, str] | None = None) -> None:
        """Set a gauge metric to an absolute value.

        Args:
            name: Registered metric name.
            value: The value to set.
            tags: Label values.
        """
        # TODO: Look up the gauge metric, call .set(value, tags)
        raise NotImplementedError

    def observe_histogram(self, name: str, value: float, tags: dict[str, str] | None = None) -> None:
        """Record an observation in a histogram metric.

        Args:
            name: Registered metric name.
            value: The observed value.
            tags: Label values.
        """
        # TODO: Look up the histogram metric, call .observe(value, tags)
        raise NotImplementedError


def get_dashboard_url() -> str | None:
    """Return the URL of the Ray dashboard, or None if unavailable.

    Returns:
        Dashboard URL string (e.g. ``"http://127.0.0.1:8265"``), or None.
    """
    # TODO: Use ray.get_dashboard_url() if Ray is initialized, else return None
    raise NotImplementedError


def get_node_stats() -> list[dict[str, Any]]:
    """Collect resource usage statistics for every node in the cluster.

    Returns:
        A list of dicts, one per node, with keys:
        ``"node_id"``, ``"address"``, ``"cpu_usage"``, ``"gpu_usage"``,
        ``"memory_used"``, ``"memory_total"``, ``"object_store_used"``,
        ``"object_store_total"``.
    """
    # TODO: Use ray.nodes() and ray.cluster_resources() /
    #       ray.available_resources() to build per-node resource stats
    raise NotImplementedError


@ray.remote
class MonitoringActor:
    """A long-running actor that periodically collects and records cluster metrics.

    Deploy this actor to continuously track cluster health and push
    metrics to the Prometheus endpoint.
    """

    def __init__(self, interval_s: float = 30.0) -> None:
        """
        Args:
            interval_s: Seconds between metric collection cycles.
        """
        self.interval_s = interval_s
        self.collector = MetricsCollector()
        self.running = False
        # TODO: Register default cluster health metrics (e.g. cpu_utilization,
        #       gpu_utilization, object_store_usage)

    async def start(self) -> None:
        """Begin the periodic collection loop.

        Runs until ``stop()`` is called.
        """
        # TODO: Set self.running = True, loop with asyncio.sleep(self.interval_s),
        #       collect node stats, and update gauge metrics each cycle
        raise NotImplementedError

    def stop(self) -> None:
        """Signal the collection loop to stop."""
        # TODO: Set self.running = False so the loop exits on next iteration
        raise NotImplementedError

    def get_latest_stats(self) -> list[dict[str, Any]]:
        """Return the most recent node stats snapshot.

        Returns:
            Per-node resource statistics.
        """
        # TODO: Call get_node_stats() and return the result
        raise NotImplementedError
