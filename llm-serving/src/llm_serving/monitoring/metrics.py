"""Prometheus metrics for LLM serving monitoring.

Tracks key performance indicators: time to first token, tokens per second,
queue depth, GPU utilization, and request counts.
"""

import time
from contextlib import contextmanager
from typing import Generator

from prometheus_client import Counter, Gauge, Histogram, Summary, start_http_server


# --- Metric Definitions ---

REQUEST_COUNT = Counter(
    "llm_request_total",
    "Total number of requests received",
    ["method", "status"],
)

REQUEST_DURATION = Histogram(
    "llm_request_duration_seconds",
    "Request duration in seconds",
    ["method"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
)

TIME_TO_FIRST_TOKEN = Histogram(
    "llm_ttft_seconds",
    "Time to first token in seconds",
    buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0],
)

TOKENS_PER_SECOND = Summary(
    "llm_tokens_per_second",
    "Tokens generated per second per request",
)

ACTIVE_REQUESTS = Gauge(
    "llm_active_requests",
    "Number of currently active requests",
)

QUEUE_DEPTH = Gauge(
    "llm_queue_depth",
    "Number of requests waiting in the queue",
)

TOKENS_GENERATED = Counter(
    "llm_tokens_generated_total",
    "Total tokens generated",
)

GPU_MEMORY_USED = Gauge(
    "llm_gpu_memory_used_bytes",
    "GPU memory used in bytes",
    ["gpu_id"],
)

GPU_UTILIZATION = Gauge(
    "llm_gpu_utilization_percent",
    "GPU utilization percentage",
    ["gpu_id"],
)


def start_metrics_server(port: int = 9090) -> None:
    """Start the Prometheus metrics HTTP server.

    Args:
        port: Port to expose metrics on.
    """
    # TODO: Implement
    # Call start_http_server(port)
    raise NotImplementedError


@contextmanager
def track_request(method: str = "chat") -> Generator[dict, None, None]:
    """Context manager for tracking request metrics.

    Automatically tracks request count, duration, and active requests.
    The yielded dict can be updated with additional metrics (ttft, tps).

    Args:
        method: The API method being called.

    Yields:
        A mutable dict where callers can set "ttft", "tps", "tokens".

    Example:
        with track_request("chat") as metrics:
            result = await process_request()
            metrics["ttft"] = result.ttft
            metrics["tps"] = result.tps
            metrics["tokens"] = result.num_tokens
    """
    # TODO: Implement
    # 1. Increment ACTIVE_REQUESTS
    # 2. Record start time
    # 3. Yield the metrics dict
    # 4. On exit: record duration, decrement ACTIVE_REQUESTS
    # 5. Update REQUEST_COUNT, REQUEST_DURATION, TTFT, TPS, TOKENS_GENERATED
    raise NotImplementedError


def update_gpu_metrics() -> None:
    """Update GPU memory and utilization metrics.

    Reads current GPU stats using pynvml or torch.cuda and updates
    the Prometheus gauges.
    """
    # TODO: Implement
    # 1. Check if CUDA is available
    # 2. For each GPU:
    #    a. Get memory used/total
    #    b. Get utilization percentage
    #    c. Update GPU_MEMORY_USED and GPU_UTILIZATION gauges
    raise NotImplementedError


def record_queue_depth(depth: int) -> None:
    """Update the queue depth gauge.

    Args:
        depth: Current number of requests in the queue.
    """
    # TODO: Implement
    raise NotImplementedError
