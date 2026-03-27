# Real-Time Anomaly Detection Stream

## Overview

Build a WebSocket-based real-time anomaly detection system that streams time-series data, applies online anomaly detection algorithms, and pushes alerts to connected clients in real-time.

This project teaches you to work with persistent bidirectional connections, streaming data pipelines, and online machine learning algorithms — all skills essential for building production monitoring, IoT analytics, and real-time alerting systems.

## Learning Objectives

- Understand the WebSocket protocol: upgrade handshake, frame structure, opcodes, and lifecycle
- Compare WebSocket vs HTTP polling vs Server-Sent Events for real-time communication
- Build an async WebSocket server with connection management and fan-out broadcasting
- Implement online anomaly detection algorithms (Z-score, EWMA, Isolation Forest)
- Design alert management with deduplication, severity classification, and cooldown periods
- Handle backpressure, heartbeats, and graceful degradation in streaming systems
- Structure a streaming data pipeline with windowing and aggregation

## Project Description

The system consists of:

1. **Data Producer** — Simulates time-series sensor data with injected anomalies
2. **Stream Processor** — Applies windowed statistics and aggregation over the data stream
3. **Anomaly Detectors** — Pluggable detection algorithms that evaluate each data point
4. **Alert Manager** — Deduplicates, classifies severity, and manages alert cooldowns
5. **WebSocket Server** — Accepts client connections, manages subscriptions, and broadcasts alerts
6. **WebSocket Client** — Connects to the server, subscribes to streams, and displays alerts

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌────────────────┐
│ Data        │────▶│ Stream           │────▶│ Anomaly        │
│ Producer    │     │ Processor        │     │ Detectors      │
└─────────────┘     └──────────────────┘     └───────┬────────┘
                                                     │
                                                     ▼
┌─────────────┐     ┌──────────────────┐     ┌────────────────┐
│ WebSocket   │◀────│ WebSocket        │◀────│ Alert          │
│ Clients     │     │ Server           │     │ Manager        │
└─────────────┘     └──────────────────┘     └────────────────┘
```

Data flows left-to-right through the pipeline. The WebSocket server maintains persistent connections with clients and fans out alerts as they are produced.

## Implementation Tasks

### Phase 1: Foundation
- [ ] Define Pydantic models for `DataPoint`, `Alert`, `Command`, and WebSocket messages
- [ ] Implement the `DataProducer` to generate synthetic time-series data with configurable anomaly injection
- [ ] Build the `StreamProcessor` with sliding window statistics

### Phase 2: Detection
- [ ] Implement the `AnomalyDetector` abstract interface
- [ ] Build the `ZScoreDetector` with configurable threshold
- [ ] Build the `EWMADetector` using exponentially weighted moving average control charts
- [ ] Build the `IsolationForestDetector` for streaming data using mini-batch retraining

### Phase 3: Alerting
- [ ] Implement `AlertManager` with deduplication, severity classification, and cooldown
- [ ] Build the `Notifier` to dispatch alerts via WebSocket, logging, and webhooks

### Phase 4: WebSocket Server
- [ ] Implement the WebSocket server with connection lifecycle management
- [ ] Build `ConnectionManager` for tracking clients, rooms, and subscriptions
- [ ] Implement message handlers for subscribe/unsubscribe/query commands
- [ ] Wire the full pipeline: producer → processor → detector → alerter → server → clients

### Phase 5: Testing & Polish
- [ ] Write unit tests for detectors with known anomalous inputs
- [ ] Write integration tests for the WebSocket server
- [ ] Write tests for alert deduplication and cooldown logic
- [ ] Add heartbeat/keepalive and graceful shutdown

## Evaluation Criteria

- **Correctness** — Detectors identify injected anomalies with reasonable precision/recall
- **Architecture** — Clean separation between streaming, detection, alerting, and transport layers
- **Async proficiency** — Proper use of `asyncio`, `async/await`, and concurrent connection handling
- **Protocol understanding** — Correct WebSocket lifecycle management (connect, message, close, error)
- **Resilience** — Graceful handling of disconnects, backpressure, and malformed messages
- **Test coverage** — Meaningful tests that validate detection accuracy and system behavior

## Resources

- [RFC 6455 — The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)
- [websockets library documentation](https://websockets.readthedocs.io/)
- [Python asyncio documentation](https://docs.python.org/3.11/library/asyncio.html)
- [Isolation Forest paper (Liu et al., 2008)](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf)
- [EWMA Control Charts — NIST](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc324.htm)
- [Pydantic V2 documentation](https://docs.pydantic.dev/latest/)
