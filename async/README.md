# Async Batch Inference Engine

## Overview

Build an async Python service that handles concurrent ML model inference requests with request batching, priority queues, timeouts, and backpressure. The service exposes an HTTP API via aiohttp and dynamically batches incoming requests to maximize GPU/CPU throughput.

## Learning Objectives

- Master Python's asyncio event loop, coroutines, and async context managers
- Build an HTTP server with aiohttp that handles concurrent requests
- Implement dynamic request batching for efficient model inference
- Design priority queues with backpressure to prevent overload
- Add middleware for rate limiting, timeouts, and error handling
- Implement health checks, readiness probes, and Prometheus-style metrics
- Handle graceful shutdown and structured concurrency

## Project Description

You are building an inference serving layer for an ML platform. The service must:

1. **Accept requests** — Expose HTTP endpoints for single and batch inference
2. **Batch dynamically** — Group incoming requests into batches by size or time window for efficient processing
3. **Manage priority** — Support priority queues so high-priority requests are processed first
4. **Apply backpressure** — Reject or queue requests when the system is overloaded
5. **Enforce timeouts** — Cancel requests that exceed their deadline
6. **Expose metrics** — Track latency percentiles, throughput, queue depth, and error rates
7. **Health checks** — Provide /health and /ready endpoints for orchestrators

## Architecture

```
async_engine/
├── server.py       # aiohttp HTTP server with routes
├── batcher.py      # Dynamic request batcher (by size or timeout)
├── queue.py        # Priority async queue with backpressure
├── inference.py    # Async model inference wrapper
├── middleware.py   # Rate limiting, timeout, error handling
├── health.py       # Health check and readiness endpoints
└── metrics.py      # Prometheus-style metrics collector
```

## Implementation Tasks

### Phase 1: Core Infrastructure
- [ ] Implement the priority async queue with bounded capacity
- [ ] Implement the dynamic batcher with configurable batch size and timeout
- [ ] Create the async model inference wrapper (simulated)

### Phase 2: HTTP Server
- [ ] Set up aiohttp server with routes for /predict and /predict/batch
- [ ] Wire up the request flow: server → queue → batcher → inference → response
- [ ] Implement middleware for rate limiting and request timeouts

### Phase 3: Observability
- [ ] Implement health check and readiness endpoints
- [ ] Build metrics collector tracking latency, throughput, queue depth
- [ ] Add error rate tracking and circuit breaker patterns

### Phase 4: Resilience
- [ ] Implement graceful shutdown (drain queue, finish in-flight requests)
- [ ] Add request cancellation on timeout
- [ ] Test backpressure behavior under load

## Evaluation Criteria

- Server handles concurrent requests without blocking the event loop
- Batcher correctly groups requests by size and time window
- Priority queue processes high-priority requests first
- Backpressure correctly rejects requests when queue is full
- Timeouts cancel long-running requests
- Metrics accurately reflect system state
- Graceful shutdown completes in-flight requests
- No resource leaks (unclosed sessions, tasks, connections)

## Resources

- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [aiohttp Server Guide](https://docs.aiohttp.org/en/stable/web.html)
- [Python Concurrency with asyncio (O'Reilly)](https://www.oreilly.com/library/view/python-concurrency-with/9781617298660/)
- [Dynamic Batching for ML Inference](https://www.anyscale.com/blog/continuous-batching)
