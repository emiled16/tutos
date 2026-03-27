# Dynamic Batching — Theory & Notes

## Why Dynamic Batching Matters

GPUs achieve high throughput through massive parallelism — thousands of cores executing the same operation on different data (SIMD/SIMT). A single inference request uses a tiny fraction of available parallelism. Batching groups multiple requests so the GPU can process them in one kernel launch, amortizing:

- **Kernel launch overhead**: Each CUDA kernel launch has fixed overhead (~5–10 μs). Processing 1 request or 64 requests costs nearly the same launch overhead.
- **Memory bandwidth**: Moving model weights from GPU global memory to compute units is the bottleneck for many models. With batching, weights are loaded once and reused across all items in the batch.
- **PCIe transfer costs**: Data moves between CPU and GPU over PCIe. Fewer, larger transfers are more efficient than many small ones.

A rough mental model: inference time ≈ `fixed_overhead + marginal_cost × batch_size`. When `fixed_overhead >> marginal_cost`, batching yields near-linear throughput gains.

## Core Concepts

### Batch Formation Triggers

A batch can be flushed on two conditions:

1. **Max batch size reached** — the batch is full, dispatch immediately
2. **Timeout expired** — waited long enough, dispatch whatever we have

The system uses whichever trigger fires first. This is the fundamental "size-or-time" pattern.

### The Latency–Throughput Tradeoff

```
Throughput ▲
           │           ╭────────── throughput plateau
           │         ╱
           │       ╱
           │     ╱
           │   ╱
           │ ╱
           └──────────────────▶ Batch wait time / Batch size

Latency   ▲
           │                  ╱
           │                ╱
           │              ╱
           │            ╱
           │──────────╱  ◄── latency grows linearly with wait time
           └──────────────────▶ Batch wait time
```

Larger batches = higher throughput but also higher latency (requests wait in the queue). SLA constraints (e.g., "p99 latency < 100ms") place an upper bound on how long we can wait. The optimal batch size lives at the intersection of the throughput curve and the SLA constraint.

### Arrival Rate and Adaptive Timeout

Under high load, requests arrive fast and batches fill quickly — a long timeout is wasteful because the batch will hit max size before the timer fires. Under low load, requests trickle in and we should wait longer to accumulate a reasonable batch. An adaptive strategy adjusts the timeout based on observed inter-arrival times:

```
timeout = min(max_wait, k / arrival_rate)
```

Where `arrival_rate` is estimated via an exponential moving average (EMA) of inter-arrival intervals:

```
ema_interval = α × latest_interval + (1 - α) × ema_interval
arrival_rate = 1 / ema_interval
```

## The Padding Problem

When inputs have variable lengths (e.g., text sequences of different token counts), they must be padded to a uniform length for batched tensor operations. Naive padding to the max length in the batch wastes compute:

```
Batch: ["hello" (5 tokens), "hi" (2 tokens), "good morning everyone" (15 tokens)]
Padded to 15 → waste = (10 + 13 + 0) / (15 × 3) = 51% wasted compute
```

### Mitigation Strategies

1. **Sorting**: Sort requests by length before batching. Adjacent items have similar lengths, reducing padding within each batch.
2. **Bucketing**: Define length buckets (e.g., 0–16, 17–32, 33–64) and batch requests within the same bucket together. Each bucket has its own batcher instance.
3. **Sort-and-pad**: Sort the full queue by length, then slice into batches. Minimizes total padding but may increase latency for some requests.
4. **Padding waste metric**: `waste_ratio = 1 - (sum_of_actual_lengths / (batch_size × max_length_in_batch))`. Track this to evaluate strategy effectiveness.

## Batching Strategies

### 1. Naive Fixed-Timeout Batcher
- Uses a constant `max_wait_ms` timeout and `max_batch_size`
- Simple to implement and reason about
- Suboptimal under variable load — too slow under high load, too eager under low load

### 2. Adaptive Batcher
- Adjusts timeout based on EMA of inter-arrival times
- Under high load: shorter timeout (batch fills fast anyway)
- Under low load: longer timeout (wait for more requests)
- Parameters: `alpha` (EMA smoothing), `min_wait_ms`, `max_wait_ms`

### 3. Padding-Aware Batcher
- Groups requests by input length using buckets
- Each bucket maintains its own batch queue
- Dramatically reduces padding waste for variable-length inputs
- Tradeoff: may increase latency for uncommon lengths (their bucket fills slowly)

### 4. Priority Batcher
- Requests carry a priority level (e.g., 0=high, 1=normal, 2=low)
- High-priority requests trigger earlier batch flushes
- Uses a priority queue internally
- Useful when some requests have tighter SLAs than others

## Continuous Batching vs Request-Level Batching

**Request-level batching** (what this project implements): entire requests are batched together and processed as a unit. A new batch cannot start until the current one finishes.

**Continuous batching** (used in LLM serving, e.g., vLLM, Orca): the system processes tokens in a streaming fashion. When one sequence in the batch finishes, a new sequence can immediately take its slot. This eliminates "batch bubbles" where finished sequences waste GPU cycles waiting for the longest sequence to complete.

Continuous batching is more complex but essential for autoregressive generation where output lengths vary dramatically.

## Backpressure and Queue Management

When load exceeds serving capacity, the request queue grows unboundedly. Backpressure mechanisms:

- **Queue depth limit**: Reject requests with HTTP 503 when the queue exceeds a threshold
- **Timeout on enqueue**: Requests waiting too long in the queue are cancelled
- **Load shedding**: Drop low-priority requests first
- **Admission control**: Rate-limit incoming requests upstream

Without backpressure, latency degrades catastrophically as queue depth grows (Little's Law: `L = λ × W` — queue length equals arrival rate times wait time).

## Batch Formation Algorithms

### Timeout-Based
```
while running:
    wait until (timeout expires OR batch is full)
    dispatch current batch
```

Implemented with `asyncio.wait_for` or `asyncio.Event` with timeout.

### Size-Based
```
while running:
    wait until batch reaches max_batch_size
    dispatch current batch
```

Pure size-based batching has unbounded latency under low load.

### Hybrid (Standard Approach)
```
while running:
    wait until (timeout expires OR max_batch_size reached)
    if batch is non-empty:
        dispatch batch
```

This is the standard pattern used by most production systems.

## Real-World Implementations

| System | Approach | Key Features |
|--------|----------|-------------|
| **NVIDIA Triton** | Configurable dynamic batcher | max_batch_size, max_queue_delay, preferred_batch_size, priority levels |
| **TensorFlow Serving** | Batching scheduler | batch_timeout_micros, max_batch_size, num_batch_threads |
| **TorchServe** | Micro-batching | batch_size, max_batch_delay, configurable per-model |
| **vLLM** | Continuous batching | PagedAttention, iteration-level scheduling |
| **Ray Serve** | `@serve.batch` decorator | max_batch_size, batch_wait_timeout_s |

## Key Metrics

| Metric | What It Measures | Why It Matters |
|--------|-----------------|----------------|
| **Batch size** (avg, distribution) | How full batches are | Underfilled batches waste GPU potential |
| **Time-to-first-response** | Time from request arrival to response start | User-facing latency |
| **Queue wait time** | Time spent in the batcher queue | Dominated by timeout parameter |
| **Padding ratio** | Fraction of padded (wasted) compute | High ratio → poor length grouping |
| **Throughput** (req/sec) | Requests processed per second | Key capacity metric |
| **Latency percentiles** (p50, p95, p99) | Tail latency distribution | SLA compliance |
| **GPU utilization estimate** | Fraction of time GPU is doing useful work | Batch gaps and padding reduce this |
| **Queue depth** | Number of pending requests | Growing depth signals capacity issues |

## Connection to Async Programming

Dynamic batching is inherently an async problem:

- **Futures/Promises**: Each request gets a `Future` that resolves when its batch completes. The caller `await`s the future.
- **Event loops**: The batcher runs as an asyncio task, using `asyncio.Event` or `asyncio.Condition` to coordinate batch formation.
- **Condition variables**: Used to signal "batch ready" between the accumulation loop and the dispatch loop.
- **Task groups**: Python 3.11's `TaskGroup` can manage the batcher's background tasks with structured concurrency.
- **Cancellation**: Clean shutdown requires cancelling pending futures and draining the queue.

## Key Terminology

| Term | Definition |
|------|-----------|
| **Dynamic batching** | Grouping inference requests into batches at runtime based on arrival patterns |
| **Batch window / timeout** | Maximum time to wait for a batch to fill before dispatching |
| **Max batch size** | Upper limit on the number of requests in a single batch |
| **Padding** | Adding dummy values to make variable-length inputs uniform for tensor operations |
| **Padding waste** | Fraction of compute spent on padded (non-real) values |
| **Bucketing** | Grouping inputs by length range to reduce padding within batches |
| **Arrival rate** | Number of requests per unit time (λ in queueing theory) |
| **EMA (Exponential Moving Average)** | Weighted average giving more weight to recent observations; used for smoothing arrival rate estimates |
| **SLA (Service Level Agreement)** | Latency/availability guarantees (e.g., "p99 < 100ms") |
| **Backpressure** | Mechanism to slow or reject incoming requests when the system is overloaded |
| **Continuous batching** | Iteration-level scheduling where new requests join mid-batch as slots free up |
| **Little's Law** | L = λW — relates queue length, arrival rate, and wait time in a stable system |
| **Throughput** | Total requests successfully processed per second |
| **Tail latency** | High-percentile latency (p95, p99) — often more important than average |
