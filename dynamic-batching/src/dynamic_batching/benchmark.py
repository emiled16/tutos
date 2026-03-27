"""Benchmarking tool for comparing batching strategies."""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
import numpy as np

from dynamic_batching.batcher import DynamicBatcher
from dynamic_batching.config import BatcherConfig, BatchingStrategyName
from dynamic_batching.executor import BatchExecutor
from dynamic_batching.metrics import MetricsCollector, MetricsSnapshot
from dynamic_batching.request import InferenceRequest

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    """Results from a single benchmark run.

    Attributes:
        strategy: Name of the batching strategy tested.
        request_rate: Target requests per second.
        total_requests: Number of requests sent.
        elapsed_seconds: Total benchmark duration.
        metrics: Final metrics snapshot.
        latencies_ms: Per-request latencies for histogram plotting.
    """

    strategy: str = ""
    request_rate: float = 0.0
    total_requests: int = 0
    elapsed_seconds: float = 0.0
    metrics: MetricsSnapshot | None = None
    latencies_ms: list[float] = field(default_factory=list)


@dataclass
class BenchmarkSuite:
    """Collection of benchmark results across strategies and request rates.

    Attributes:
        results: All collected benchmark results.
    """

    results: list[BenchmarkResult] = field(default_factory=list)


def generate_synthetic_requests(
    count: int,
    min_length: int = 5,
    max_length: int = 128,
    priority_distribution: tuple[float, float, float] = (0.1, 0.7, 0.2),
) -> list[InferenceRequest]:
    """Generate synthetic inference requests with variable lengths.

    Args:
        count: Number of requests to generate.
        min_length: Minimum sequence length.
        max_length: Maximum sequence length.
        priority_distribution: Probability distribution over (HIGH, NORMAL, LOW).

    Returns:
        List of synthetic InferenceRequest objects.
    """
    # TODO: Implement synthetic request generation:
    #   1. Sample sequence lengths from a log-normal distribution (clipped to [min, max])
    #   2. For each length, generate random payload of that length
    #   3. Assign priorities according to priority_distribution using np.random.choice
    #   4. Set sequence_length on each request
    #   5. Return list of requests
    pass


async def run_benchmark(
    config: BatcherConfig,
    request_rate: float,
    total_requests: int = 1000,
    warmup_requests: int = 50,
) -> BenchmarkResult:
    """Run a single benchmark: send requests at a fixed rate and measure performance.

    Args:
        config: Batcher configuration to test.
        request_rate: Target requests per second.
        total_requests: Total number of requests to send.
        warmup_requests: Number of warmup requests (not included in metrics).

    Returns:
        BenchmarkResult with performance measurements.
    """
    # TODO: Implement benchmark runner:
    #   1. Create executor, metrics, and batcher from config
    #   2. Start the batcher
    #   3. Generate synthetic requests
    #   4. Send warmup_requests first, then reset metrics
    #   5. Send remaining requests at the target rate (sleep 1/rate between sends)
    #   6. Collect all response futures
    #   7. Wait for all responses
    #   8. Record latencies (response time - submit time)
    #   9. Take metrics snapshot
    #   10. Stop the batcher
    #   11. Return BenchmarkResult
    pass


async def compare_strategies(
    request_rates: list[float] | None = None,
    total_requests: int = 1000,
    base_config: BatcherConfig | None = None,
) -> BenchmarkSuite:
    """Compare all batching strategies across multiple request rates.

    Args:
        request_rates: List of request rates to test (req/sec).
        total_requests: Requests per benchmark run.
        base_config: Base configuration (strategy will be overridden).

    Returns:
        BenchmarkSuite with results for all strategy × rate combinations.
    """
    # TODO: Implement strategy comparison:
    #   1. Default request_rates to [10, 50, 100, 200, 500, 1000] if not provided
    #   2. For each strategy in BatchingStrategyName:
    #       3. For each rate in request_rates:
    #           4. Create config with the current strategy
    #           5. Run benchmark
    #           6. Append result to suite
    #   7. Return suite
    pass


def plot_throughput_latency(suite: BenchmarkSuite, output_path: str = "benchmark.png") -> None:
    """Plot throughput vs latency curves for each strategy.

    Produces a figure with:
    - Left panel: throughput (req/sec) vs request rate
    - Right panel: p95 latency vs request rate

    Args:
        suite: Benchmark results to plot.
        output_path: File path to save the figure.
    """
    # TODO: Implement plotting:
    #   1. Group results by strategy
    #   2. For each strategy, extract (request_rate, throughput, p95_latency) series
    #   3. Create 1×2 subplot figure
    #   4. Left: plot throughput vs request_rate for each strategy
    #   5. Right: plot p95 latency vs request_rate for each strategy
    #   6. Add legends, labels, title
    #   7. Save to output_path
    pass


def plot_latency_histogram(
    results: list[BenchmarkResult],
    output_path: str = "latency_hist.png",
) -> None:
    """Plot latency distribution histograms for multiple strategies.

    Args:
        results: Benchmark results to plot (typically at the same request rate).
        output_path: File path to save the figure.
    """
    # TODO: Implement histogram plotting:
    #   1. Create one subplot per result
    #   2. Plot histogram of latencies_ms
    #   3. Add vertical lines for p50, p95, p99
    #   4. Add labels and title
    #   5. Save to output_path
    pass


async def main() -> None:
    """Entry point for running the full benchmark suite from the command line."""
    # TODO: Implement CLI entry point:
    #   1. Configure logging
    #   2. Run compare_strategies with default parameters
    #   3. Print summary table of results
    #   4. Generate plots
    pass


if __name__ == "__main__":
    asyncio.run(main())
