# Adaptive ML Inference Batcher

A dynamic batching system for ML model inference that groups incoming requests into optimal batches, maximizing GPU throughput while keeping latency within acceptable bounds.

## Overview

Individual inference requests are highly inefficient on GPUs — kernel launch overhead, memory transfer costs, and underutilized parallelism all conspire to waste expensive compute. Dynamic batching solves this by accumulating requests and dispatching them together, amortizing fixed costs across many inputs. The fundamental tension is **latency vs throughput**: waiting longer to fill a batch improves throughput but degrades response time. This project explores that tradeoff through multiple batching strategies.

## Learning Objectives

- Understand why batching is critical for production ML serving and how GPUs benefit from parallel workloads
- Implement timeout-based and size-based batch formation using asyncio primitives (events, conditions, tasks)
- Reason about the latency–throughput tradeoff curve and how SLA constraints shape batching policy
- Handle the padding problem: variable-length inputs waste compute when naively padded to max length
- Build adaptive systems that adjust behavior based on observed traffic patterns
- Collect and interpret serving metrics (p50/p95/p99 latency, throughput, padding waste, batch utilization)
- Wire a batching layer into a FastAPI server to see end-to-end request flow
- Benchmark and compare strategies under synthetic load

## Project Description

The system receives individual inference requests via a FastAPI endpoint, accumulates them in a queue, and forms batches using one of several strategies:

1. **Naive (fixed timeout)** — waits a fixed duration or until the batch is full, whichever comes first
2. **Adaptive** — adjusts the timeout window based on an exponential moving average of inter-arrival times
3. **Padding-aware** — buckets requests by input length to minimize padding waste
4. **Priority** — respects per-request priority levels, flushing high-priority requests sooner

Once a batch is formed, it is dispatched to a `BatchExecutor` that simulates GPU inference. A `MetricsCollector` tracks batch sizes, wait times, padding ratios, throughput, and latency percentiles. A benchmarking tool generates synthetic load to compare strategies.

## Architecture

```
                    ┌──────────────┐
  POST /predict ──▶ │  FastAPI      │
                    │  Server       │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Request      │
                    │  Scheduler    │
                    └──────┬───────┘
                           │  routes to batcher instance
                    ┌──────▼───────┐
                    │  Dynamic      │◄── Strategy (Naive / Adaptive /
                    │  Batcher      │     PaddingAware / Priority)
                    └──────┬───────┘
                           │  batch ready
                    ┌──────▼───────┐
                    │  Batch        │
                    │  Executor     │──▶ simulated GPU inference
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Metrics      │
                    │  Collector    │──▶ batch size, latency, padding, throughput
                    └──────────────┘
```

## Implementation Tasks

### Phase 1: Data Models & Configuration
- [ ] Define `InferenceRequest` and `InferenceResponse` pydantic models (`request.py`)
- [ ] Define `BatcherConfig` pydantic settings with env-var support (`config.py`)
- [ ] Implement padding utilities and waste tracking (`padding.py`)

### Phase 2: Core Batching
- [ ] Implement base `BatchingStrategy` protocol and `NaiveBatcher` (`strategies.py`)
- [ ] Implement `AdaptiveBatcher` with EMA-based timeout adjustment (`strategies.py`)
- [ ] Implement `PaddingAwareBatcher` with length bucketing (`strategies.py`)
- [ ] Implement `PriorityBatcher` with priority queue (`strategies.py`)
- [ ] Implement `DynamicBatcher` that uses a strategy to form batches (`batcher.py`)

### Phase 3: Execution & Scheduling
- [ ] Implement `BatchExecutor` with sync and async execution modes (`executor.py`)
- [ ] Implement `RequestScheduler` for multi-model routing (`scheduler.py`)

### Phase 4: Metrics & Observability
- [ ] Implement `MetricsCollector` with percentile tracking (`metrics.py`)
- [ ] Add batch utilization and padding waste ratio metrics

### Phase 5: Server & Integration
- [ ] Build FastAPI server with `/predict` endpoint (`server.py`)
- [ ] Wire batcher, executor, scheduler, and metrics together
- [ ] Add health check and metrics endpoints

### Phase 6: Benchmarking
- [ ] Build synthetic load generator (`benchmark.py`)
- [ ] Implement throughput/latency measurement at varying request rates
- [ ] Compare all strategies and produce visualization plots

### Phase 7: Testing
- [ ] Write unit tests for batch formation logic
- [ ] Write tests for each batching strategy
- [ ] Write tests for padding utilities
- [ ] Write tests for metrics collection
- [ ] Write integration tests for the FastAPI server

## Evaluation Criteria

- **Correctness**: Batches form at the right time (timeout or max size), no requests are dropped or duplicated
- **Latency compliance**: Adaptive strategy should reduce average wait time under high load
- **Padding efficiency**: Padding-aware strategy should measurably reduce waste vs naive approach
- **Metrics accuracy**: Percentile calculations are correct, throughput tracking is accurate
- **Async correctness**: No race conditions, proper use of asyncio primitives, clean shutdown
- **Code quality**: Type hints throughout, clear separation of concerns, well-defined protocols/ABCs
- **Test coverage**: All strategies tested, edge cases covered (empty batches, single-request batches, timeout expiry)

## Resources

- [NVIDIA Triton Inference Server — Dynamic Batching](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_configuration.html#dynamic-batcher)
- [TensorFlow Serving — Batching Guide](https://www.tensorflow.org/tfx/serving/serving_config#batching_configuration)
- [vLLM — Continuous Batching for LLM Serving](https://docs.vllm.ai/en/latest/)
- [Orca: A Distributed Serving System for Transformer-Based Generative Models (paper)](https://www.usenix.org/conference/osdi22/presentation/yu)
- [Python asyncio — Event Loop Documentation](https://docs.python.org/3.11/library/asyncio.html)
- [FastAPI — Concurrency and async/await](https://fastapi.tiangolo.com/async/)
- [Pydantic — Settings Management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
