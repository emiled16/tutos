"""Tests for metrics collection."""

from __future__ import annotations

import time

import pytest

from dynamic_batching.metrics import LatencyPercentiles, MetricsCollector, MetricsSnapshot
from dynamic_batching.request import Batch, InferenceRequest


@pytest.fixture
def collector() -> MetricsCollector:
    return MetricsCollector()


def make_batch(size: int, sequence_lengths: list[int] | None = None) -> Batch:
    """Create a Batch with the given number of requests."""
    if sequence_lengths is None:
        sequence_lengths = [10] * size
    requests = [
        InferenceRequest(
            payload=[1.0] * sl,
            sequence_length=sl,
        )
        for sl in sequence_lengths
    ]
    return Batch(
        requests=requests,
        max_sequence_length=max(sequence_lengths) if sequence_lengths else 0,
    )


class TestMetricsRecording:
    """Tests for recording individual metrics."""

    def test_record_batch_updates_counts(self, collector: MetricsCollector) -> None:
        """Recording a batch should increment total_requests and total_batches."""
        # TODO: Implement test:
        #   1. Record a batch of size 5
        #   2. Assert _total_requests == 5
        #   3. Assert _total_batches == 1
        pass

    def test_record_multiple_batches(self, collector: MetricsCollector) -> None:
        """Multiple batch recordings should accumulate correctly."""
        # TODO: Implement test:
        #   Record batches of sizes [3, 5, 2]
        #   Assert _total_requests == 10
        #   Assert _total_batches == 3
        pass

    def test_record_batch_tracks_sizes(self, collector: MetricsCollector) -> None:
        """Batch sizes should be tracked for distribution analysis."""
        # TODO: Implement test:
        #   Record batches of sizes [2, 4, 6]
        #   Assert _batch_sizes == [2, 4, 6]
        pass

    def test_record_latency(self, collector: MetricsCollector) -> None:
        """Latency recordings should be stored."""
        # TODO: Implement test
        pass

    def test_record_gpu_time(self, collector: MetricsCollector) -> None:
        """GPU time recordings should accumulate."""
        # TODO: Implement test
        pass


class TestPercentileComputation:
    """Tests for latency percentile calculations."""

    def test_percentiles_with_known_values(self, collector: MetricsCollector) -> None:
        """Percentiles should match expected values for a known distribution."""
        # TODO: Implement test:
        #   values = list(range(1, 101))  # 1 to 100
        #   p50 should be ~50, p95 should be ~95, p99 should be ~99
        pass

    def test_percentiles_single_value(self, collector: MetricsCollector) -> None:
        """All percentiles should equal the single value."""
        # TODO: Implement test:
        #   values = [42.0]
        #   All percentiles should be 42.0
        pass

    def test_percentiles_empty_list(self, collector: MetricsCollector) -> None:
        """Empty list should return zeroed percentiles."""
        # TODO: Implement test
        pass

    def test_percentiles_two_values(self, collector: MetricsCollector) -> None:
        """Percentiles with two values should interpolate correctly."""
        # TODO: Implement test
        pass


class TestMetricsSnapshot:
    """Tests for the snapshot method."""

    def test_snapshot_after_recording(self, collector: MetricsCollector) -> None:
        """Snapshot should reflect recorded data."""
        # TODO: Implement test:
        #   1. Record several batches
        #   2. Record some latencies
        #   3. Take snapshot
        #   4. Assert total_requests, total_batches, avg_batch_size are correct
        pass

    def test_snapshot_throughput(self, collector: MetricsCollector) -> None:
        """Throughput should equal total_requests / elapsed_time."""
        # TODO: Implement test:
        #   1. Record batches
        #   2. Wait a known duration
        #   3. Take snapshot
        #   4. Assert throughput_rps is approximately correct
        pass

    def test_snapshot_empty_collector(self, collector: MetricsCollector) -> None:
        """Snapshot of empty collector should have zero values."""
        # TODO: Implement test
        pass

    def test_gpu_utilization_estimate(self, collector: MetricsCollector) -> None:
        """GPU utilization should be gpu_busy_time / total_elapsed_time."""
        # TODO: Implement test
        pass


class TestMetricsReset:
    """Tests for the reset method."""

    def test_reset_clears_all_metrics(self, collector: MetricsCollector) -> None:
        """Reset should zero out all counters and clear all lists."""
        # TODO: Implement test:
        #   1. Record some data
        #   2. Reset
        #   3. Assert all counters are 0 and lists are empty
        pass

    def test_snapshot_after_reset(self, collector: MetricsCollector) -> None:
        """Snapshot after reset should show zero values."""
        # TODO: Implement test
        pass
