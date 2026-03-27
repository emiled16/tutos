"""Tests for the stream processing pipeline."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import AsyncIterator

import numpy as np
import pytest

from socket_project.models.messages import DataPoint
from socket_project.streaming.stream_processor import ProcessorConfig, StreamProcessor


def _make_point(value: float, metric: str = "test_metric") -> DataPoint:
    return DataPoint(timestamp=datetime.utcnow(), metric_name=metric, value=value)


async def _async_points(values: list[float], metric: str = "test_metric") -> AsyncIterator[DataPoint]:
    for v in values:
        yield _make_point(v, metric)


class TestStreamProcessor:
    """Tests for sliding window statistics computation."""

    @pytest.fixture
    def processor(self) -> StreamProcessor:
        return StreamProcessor(ProcessorConfig(window_size=10))

    def test_returns_none_with_single_point(self, processor: StreamProcessor) -> None:
        # TODO: Implement — process a single point, assert None is returned
        # (need at least 2 points to compute std).
        pass

    def test_returns_stats_with_enough_points(self, processor: StreamProcessor) -> None:
        # TODO: Implement — process 5 points, assert WindowStats is returned
        # with correct count, mean, and std.
        pass

    def test_window_respects_max_size(self, processor: StreamProcessor) -> None:
        # TODO: Implement — process 20 points with window_size=10,
        # assert the stats reflect only the last 10 values.
        pass

    def test_stats_accuracy(self, processor: StreamProcessor) -> None:
        # TODO: Implement — process known values [10, 20, 30, 40, 50],
        # assert mean == 30.0 and std matches np.std([10,20,30,40,50], ddof=1).
        pass

    def test_multiple_metrics_tracked_independently(self, processor: StreamProcessor) -> None:
        # TODO: Implement — process points for "cpu" and "memory",
        # assert each metric has its own window and stats.
        pass

    def test_reset_clears_metric_window(self, processor: StreamProcessor) -> None:
        # TODO: Implement — process points, reset("test_metric"),
        # assert next process returns None (window is empty).
        pass

    def test_reset_all_clears_everything(self, processor: StreamProcessor) -> None:
        # TODO: Implement — process points for multiple metrics,
        # reset(None), assert all windows are empty.
        pass

    async def test_process_stream_yields_pairs(self, processor: StreamProcessor) -> None:
        # TODO: Implement — create an async iterator of 10 points,
        # pass to process_stream, collect results, assert each result
        # is a (DataPoint, WindowStats) tuple.
        pass
