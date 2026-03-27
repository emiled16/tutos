"""Load testing script for the LLM serving API.

Sends concurrent requests to measure throughput, latency distribution,
and behavior under load.
"""

import asyncio
import time
from dataclasses import dataclass, field

import httpx


@dataclass
class RequestResult:
    """Result from a single load test request.

    Attributes:
        request_id: Unique identifier.
        status_code: HTTP status code.
        ttft_ms: Time to first token (for streaming) in milliseconds.
        total_time_ms: Total request duration in milliseconds.
        tokens_generated: Number of tokens in the response.
        tps: Tokens per second for this request.
        error: Error message if the request failed.
    """

    request_id: int
    status_code: int = 0
    ttft_ms: float = 0.0
    total_time_ms: float = 0.0
    tokens_generated: int = 0
    tps: float = 0.0
    error: str | None = None


@dataclass
class LoadTestReport:
    """Aggregated results from a load test run.

    Attributes:
        num_requests: Total requests sent.
        num_successful: Requests that completed successfully.
        num_failed: Requests that failed.
        total_duration_s: Total test duration in seconds.
        requests_per_second: Overall throughput.
        avg_ttft_ms: Average time to first token.
        p50_ttft_ms: Median time to first token.
        p95_ttft_ms: 95th percentile TTFT.
        p99_ttft_ms: 99th percentile TTFT.
        avg_tps: Average tokens per second per request.
        total_tokens_per_second: Aggregate tokens per second.
        results: Individual request results.
    """

    num_requests: int = 0
    num_successful: int = 0
    num_failed: int = 0
    total_duration_s: float = 0.0
    requests_per_second: float = 0.0
    avg_ttft_ms: float = 0.0
    p50_ttft_ms: float = 0.0
    p95_ttft_ms: float = 0.0
    p99_ttft_ms: float = 0.0
    avg_tps: float = 0.0
    total_tokens_per_second: float = 0.0
    results: list[RequestResult] = field(default_factory=list)


async def send_request(
    client: httpx.AsyncClient,
    url: str,
    prompt: str,
    request_id: int,
    max_tokens: int = 128,
    stream: bool = False,
) -> RequestResult:
    """Send a single request to the LLM serving API.

    Args:
        client: The httpx async client.
        url: The API endpoint URL.
        prompt: The prompt to send.
        request_id: Unique identifier for this request.
        max_tokens: Maximum tokens to generate.
        stream: Whether to use streaming mode.

    Returns:
        RequestResult with timing and token metrics.
    """
    # TODO: Implement
    # 1. Build the request payload (OpenAI-compatible format)
    # 2. Record start time
    # 3. Send the request (handle streaming if enabled)
    # 4. For streaming: measure TTFT from first SSE chunk
    # 5. Record end time, count tokens
    # 6. Compute TPS
    # 7. Return RequestResult
    raise NotImplementedError


async def run_load_test(
    base_url: str,
    prompts: list[str],
    num_concurrent: int = 10,
    max_tokens: int = 128,
    stream: bool = False,
    timeout: float = 60.0,
) -> LoadTestReport:
    """Run a load test with concurrent requests.

    Args:
        base_url: Base URL of the serving API (e.g., "http://localhost:8000").
        prompts: List of prompts to send (cycled if fewer than num_concurrent).
        num_concurrent: Number of concurrent requests.
        max_tokens: Maximum tokens per request.
        stream: Whether to use streaming.
        timeout: Request timeout in seconds.

    Returns:
        LoadTestReport with aggregated metrics.
    """
    # TODO: Implement
    # 1. Create an httpx async client with timeout
    # 2. Create tasks for all concurrent requests
    # 3. Run all tasks with asyncio.gather()
    # 4. Aggregate results into LoadTestReport
    # 5. Compute percentile statistics
    raise NotImplementedError


def print_load_test_report(report: LoadTestReport) -> None:
    """Pretty-print a load test report.

    Args:
        report: The LoadTestReport to display.
    """
    # TODO: Implement
    # Format a summary with throughput, latency percentiles, and error count
    raise NotImplementedError
