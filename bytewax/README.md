# Real-Time Feature Pipeline with Bytewax

## Overview

Build a streaming feature engineering pipeline using [Bytewax](https://bytewax.io/) that processes user clickstream events in real-time. The pipeline computes session-based features — session duration, click patterns, and engagement scores — and outputs them for downstream ML model consumption.

This project teaches you to think in terms of **dataflows**: composing stateless transforms, stateful operators, and windowed aggregations into a declarative streaming pipeline that can process unbounded event streams.

## Learning Objectives

- Understand the dataflow programming model and how Bytewax implements it in Python
- Implement stateful stream processing with sessionization logic
- Apply windowing strategies (tumbling, sliding, session) to aggregate streaming data
- Build custom input sources and output sinks
- Design Pydantic models for strongly-typed event processing
- Write testable streaming transforms in isolation
- Reason about event time vs. processing time and late-arriving data

## Project Description

You will build a pipeline that:

1. **Ingests** clickstream events from a simulated Kafka consumer or file-based replay source
2. **Parses and validates** raw JSON events into typed Pydantic models
3. **Keys** events by user ID for per-user processing
4. **Sessionizes** the click stream using a 30-minute inactivity timeout
5. **Computes features** within each session window: total clicks, unique pages, session duration, click velocity, and an engagement score
6. **Outputs** computed features to a feature store (simulated), stdout, or file sink

## Architecture

```
[Kafka / File Source]
        │
        ▼
  ┌─────────────┐
  │  Deserialize │  (JSON → ClickEvent)
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │   Key by    │  (user_id)
  │   User ID   │
  └──────┬──────┘
         │
         ▼
  ┌─────────────────┐
  │  Session Window  │  (30-min gap)
  └───────┬─────────┘
          │
          ▼
  ┌─────────────────┐
  │ Feature Compute  │  (aggregations)
  └───────┬─────────┘
          │
          ▼
  [Feature Store / File / Stdout]
```

## Implementation Tasks

### Phase 1: Data Models
- [ ] Define `ClickEvent` Pydantic model with timestamp, user_id, page_url, action, metadata
- [ ] Define `SessionFeatures` Pydantic model with computed feature fields
- [ ] Implement serialization helpers for JSON and optional Avro encoding

### Phase 2: Sources & Sinks
- [ ] Implement a file-based replay source that reads JSONL clickstream files
- [ ] Implement a simulated Kafka consumer source with configurable throughput
- [ ] Implement a stdout sink for debugging
- [ ] Implement a file sink that writes computed features as JSONL
- [ ] Implement a feature store writer sink (simulated with dict or file)

### Phase 3: Transforms & Windows
- [ ] Implement stateless event parsing and validation transform
- [ ] Define session window with 30-minute inactivity gap
- [ ] Define tumbling window (e.g., 5-minute fixed intervals)
- [ ] Define sliding window (e.g., 10-minute window, 2-minute slide)
- [ ] Implement sessionization logic as a stateful transform
- [ ] Implement feature computation: click count, unique pages, session duration, engagement score

### Phase 4: Pipeline Assembly
- [ ] Wire up the complete dataflow from source → transforms → sink
- [ ] Add error handling for malformed events
- [ ] Support configurable window parameters

### Phase 5: Testing
- [ ] Unit test each transform function with sample events
- [ ] Integration test the full pipeline with a small dataset
- [ ] Test model validation and edge cases

## Evaluation Criteria

- Pipeline processes a stream of events end-to-end without errors
- Session windows correctly group events by user with 30-minute gap detection
- Feature computations are accurate (verified by tests)
- Code is well-typed with Pydantic models throughout
- Transforms are pure functions that can be tested independently
- Pipeline handles malformed events gracefully

## Resources

- [Bytewax Documentation](https://docs.bytewax.io/)
- [Bytewax GitHub Examples](https://github.com/bytewax/bytewax/tree/main/examples)
- [Dataflow Programming (Wikipedia)](https://en.wikipedia.org/wiki/Dataflow_programming)
- [Streaming 101 – Tyler Akidau](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/)
- [Designing Data-Intensive Applications – Ch. 11: Stream Processing](https://dataintensive.net/)
