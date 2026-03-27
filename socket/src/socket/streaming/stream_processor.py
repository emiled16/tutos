"""Stream processing pipeline with windowed statistics and aggregation."""

from __future__ import annotations

import asyncio
from collections import deque
from dataclasses import dataclass, field
from typing import AsyncIterator

import numpy as np

from socket_project.models.messages import DataPoint


@dataclass
class WindowStats:
    """Aggregated statistics for a sliding window of data points."""

    count: int
    mean: float
    std: float
    min_val: float
    max_val: float
    latest_value: float
    metric_name: str


@dataclass
class ProcessorConfig:
    """Configuration for the stream processor."""

    window_size: int = 100
    emit_interval: int = 1


class StreamProcessor:
    """Applies sliding-window statistics over incoming data points.

    Maintains a fixed-size window per metric and computes running statistics
    that downstream detectors can use.
    """

    def __init__(self, config: ProcessorConfig | None = None) -> None:
        self.config = config or ProcessorConfig()
        self._windows: dict[str, deque[float]] = {}

    def _ensure_window(self, metric_name: str) -> deque[float]:
        """Get or create the sliding window for a metric."""
        if metric_name not in self._windows:
            self._windows[metric_name] = deque(maxlen=self.config.window_size)
        return self._windows[metric_name]

    def process(self, point: DataPoint) -> WindowStats | None:
        """Add a data point to its metric window and compute stats.

        Returns:
            WindowStats if enough data has been collected, None otherwise.
        """
        # TODO: Implement — append the value to the metric's deque,
        # then compute count, mean, std, min, max from the window.
        # Return None if the window has fewer than 2 points (can't compute std).
        raise NotImplementedError

    async def process_stream(
        self,
        source: AsyncIterator[DataPoint],
    ) -> AsyncIterator[tuple[DataPoint, WindowStats]]:
        """Consume an async stream of DataPoints, yielding (point, stats) pairs.

        Only yields when ``process()`` returns non-None stats.
        """
        # TODO: Implement — async for over source, call self.process(),
        # yield the pair when stats are available.
        raise NotImplementedError

    def reset(self, metric_name: str | None = None) -> None:
        """Clear the window for a metric, or all metrics if None."""
        if metric_name is None:
            self._windows.clear()
        else:
            self._windows.pop(metric_name, None)
