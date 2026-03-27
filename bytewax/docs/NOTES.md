# Stream Processing & Bytewax — Theory Notes

## Core Concepts

### What is Stream Processing?

Stream processing is the continuous computation over unbounded datasets. Unlike batch processing where you operate on a finite, complete dataset, stream processing handles data that arrives incrementally over time, potentially without end.

Key distinction: **bounded** (batch) vs **unbounded** (stream) data. Streaming systems must produce results *incrementally* as data arrives rather than waiting for the entire dataset.

### The Dataflow Programming Model

Bytewax uses a **dataflow** model where you describe computation as a directed acyclic graph (DAG) of operators. Data flows through the graph, being transformed at each node.

```
Source → Map → Filter → Reduce → Sink
```

Each operator is a self-contained unit of computation. The runtime handles parallelism, data routing, and state management — you only define *what* happens at each step.

### Stateless vs Stateful Operators

**Stateless operators** produce output solely from the current input element:
- `map` — transform each element independently
- `filter` — include/exclude based on a predicate
- `flat_map` — one input → zero or more outputs

**Stateful operators** maintain internal state across elements:
- `reduce` — accumulate values by key
- `stateful_map` — arbitrary per-key state
- `fold_window` — accumulate within a window

Stateful operators are powerful but introduce complexity: state must be checkpointed for fault tolerance, and it grows with the key cardinality.

## Windowing Strategies

Windows group unbounded streams into finite chunks for aggregation.

### Tumbling Windows

Fixed-size, non-overlapping time intervals.

```
|----W1----|----W2----|----W3----|
0         5         10         15   (minutes)
```

- Every event belongs to exactly one window
- Simple to reason about
- Use case: "Count clicks per 5-minute interval"

### Sliding Windows

Fixed-size windows that advance by a smaller slide interval, creating overlap.

```
|------W1------|
    |------W2------|
        |------W3------|
```

- Events can belong to multiple windows
- Produces smoother aggregations
- Use case: "Average click rate over 10 minutes, updated every 2 minutes"

### Session Windows

Dynamic windows based on activity gaps. A session ends after a period of inactivity (the gap duration).

```
|--Session 1--|  (gap > 30m)  |---Session 2---|
```

- Window boundaries are data-driven, not clock-driven
- Natural fit for user activity analysis
- Requires stateful tracking of the last event per key
- Use case: "Compute features per user browsing session"

## Event Time vs Processing Time

**Event time**: when the event actually occurred (embedded in the event payload).
**Processing time**: when the system processes the event.

These can differ due to network delays, buffering, or out-of-order delivery. Streaming systems must decide which clock to use for windowing.

### Watermarks

A watermark is the system's estimate of how far it has progressed through event time. It declares: "I believe I have seen all events with timestamps up to this point."

Events arriving after their window's watermark has passed are called **late data**. Strategies:
- **Drop** late events (simplest)
- **Allow** a grace period to recompute window results
- **Accumulate** and emit updated results

## Delivery Semantics

### At-Most-Once
Events may be lost but never duplicated. Fastest, least overhead. Acceptable when occasional data loss is tolerable.

### At-Least-Once
Every event is processed, but some may be processed more than once. Requires idempotent operations or deduplication downstream.

### Exactly-Once
Each event affects the output exactly once. Most expensive — requires coordination between source, processor, and sink (often via transactions or idempotent writes).

Bytewax provides at-least-once semantics with its recovery system. Exactly-once can be achieved when combined with idempotent sinks.

## Backpressure

When a downstream operator is slower than upstream, events queue up. Without backpressure, this leads to unbounded memory growth or data loss.

Strategies:
- **Blocking**: slow down the producer (Bytewax's default)
- **Buffering**: absorb bursts in a buffer with bounded capacity
- **Dropping**: shed load by discarding excess events
- **Sampling**: process only a subset of events

## Recovery and Checkpointing

Bytewax supports **recovery** through periodic checkpointing of operator state. On failure, the system restores from the last checkpoint and replays events from that point.

Key concepts:
- **Checkpoint interval**: frequency of state snapshots (latency vs durability tradeoff)
- **Recovery store**: where checkpoints are persisted (SQLite, filesystem)
- **Replay**: source must support rewinding to re-read events after a checkpoint

## Bytewax vs Alternatives

| Aspect | Bytewax | Apache Flink | Spark Structured Streaming |
|--------|---------|-------------|---------------------------|
| Language | Python-native | Java/Scala (Python API) | Scala/Python |
| Model | Dataflow | Dataflow | Micro-batch / continuous |
| State | Per-key, in-process | Per-key, distributed | DataFrame-based |
| Scaling | Multi-worker | Full cluster | Spark cluster |
| Latency | Low (true streaming) | Low (true streaming) | Higher (micro-batch) |
| Learning curve | Low | High | Medium |
| Use case sweet spot | Python-native streaming | Large-scale production | Batch + streaming unification |

## Best Practices

1. **Keep transforms pure**: stateless transforms should be pure functions — easy to test, easy to reason about
2. **Minimize state**: only use stateful operators when you truly need cross-event computation
3. **Choose the right window**: tumbling for periodic snapshots, session for user activity, sliding for smooth trends
4. **Design for late data**: decide your strategy upfront — drop, allow grace period, or accumulate
5. **Test transforms independently**: extract logic into plain functions and unit test them before wiring into the dataflow
6. **Use Pydantic for event schemas**: catch data issues early with validation
7. **Monitor key cardinality**: stateful operators allocate state per key — unbounded key spaces can exhaust memory

## Common Pitfalls

- **Forgetting that state grows with keys**: each unique key in a stateful operator holds memory. Clean up expired state.
- **Confusing event time and processing time**: using processing time for windows when events arrive out-of-order gives incorrect results.
- **Testing with too little data**: streaming edge cases (late events, out-of-order, session gaps) only surface with realistic test data.
- **Ignoring serialization costs**: JSON parsing per event adds up at high throughput. Consider binary formats (Avro, MessagePack) for production.
- **Over-windowing**: applying multiple overlapping windows without need wastes computation.

## Key Terminology

- **Dataflow**: a DAG of operators that data flows through
- **Operator**: a processing step in the dataflow (map, filter, reduce, etc.)
- **Watermark**: the system's progress indicator through event time
- **Window**: a finite grouping of events from an unbounded stream
- **Sessionization**: grouping events into sessions based on an inactivity gap
- **Checkpoint**: a snapshot of operator state for fault recovery
- **Backpressure**: mechanism to slow producers when consumers can't keep up
- **Keyed stream**: a stream partitioned by a key (e.g., user_id) for per-key processing
- **Sink**: the output destination for processed data
- **Source**: the input origin of raw data
