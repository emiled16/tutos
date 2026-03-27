# Real-Time Anomaly Detection Stream — Theory Notes

## WebSocket Protocol

### The Upgrade Handshake

WebSocket connections start as a standard HTTP/1.1 request with an `Upgrade: websocket` header. The client sends:

```
GET /stream HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

The server responds with `101 Switching Protocols`, and the TCP connection is then used for bidirectional WebSocket frames. The `Sec-WebSocket-Key` / `Sec-WebSocket-Accept` exchange prevents caching proxies from replaying old connections — it is **not** a security mechanism.

### Frame Structure

Every WebSocket message is wrapped in one or more frames:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |            (16/64)            |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+-------------------------------+
|     Masking-key (0 or 4 bytes)      |          Payload        |
+-------------------------------------+-------------------------+
```

- **FIN bit**: indicates whether this is the final fragment of a message
- **Opcode**: identifies the frame type
- **MASK bit**: client-to-server frames must be masked; server-to-client must not

### Opcodes

| Opcode | Meaning |
|--------|---------|
| `0x0`  | Continuation frame |
| `0x1`  | Text frame (UTF-8) |
| `0x2`  | Binary frame |
| `0x8`  | Connection close |
| `0x9`  | Ping |
| `0xA`  | Pong |

Control frames (close, ping, pong) can be interjected between fragments of a data message. Pings must be replied to with pongs carrying the same payload.

### Connection Lifecycle

1. **Opening** — HTTP upgrade handshake
2. **Open** — Bidirectional message exchange
3. **Closing** — Either side sends a close frame; the other replies with a close frame
4. **Closed** — TCP connection is torn down

Close frames carry a status code (e.g. 1000 = normal, 1001 = going away, 1011 = server error) and an optional UTF-8 reason string.

---

## WebSocket vs HTTP vs SSE

| Dimension | HTTP Polling | Server-Sent Events | WebSocket |
|-----------|-------------|--------------------:|-----------|
| Direction | Client → Server | Server → Client | Bidirectional |
| Transport | New TCP conn per request | Single HTTP conn | Single TCP conn (upgraded) |
| Overhead | HTTP headers every request | Small (text/event-stream) | 2–14 bytes per frame |
| Reconnect | Client manages | Built-in (`retry`) | Manual |
| Binary | Yes | No (text only) | Yes |
| Browser support | Universal | All modern | All modern |

**When to use each:**
- **HTTP polling/long-polling**: Simple read-heavy use cases, wide proxy compatibility
- **SSE**: Server-push only (dashboards, feeds), automatic reconnection is valuable
- **WebSocket**: True bidirectional real-time (chat, gaming, interactive streaming, this project)

---

## Socket Programming Fundamentals

WebSocket is built on top of TCP sockets. Key concepts:

- **Socket**: an endpoint for bidirectional communication, identified by (IP, port, protocol)
- **Bind/Listen/Accept**: server-side lifecycle for TCP
- **Non-blocking I/O**: required for handling many concurrent connections; Python's `asyncio` uses `select`/`epoll`/`kqueue` under the hood
- **Backlog**: the OS-level queue for incoming connections waiting to be accepted

The `websockets` library abstracts all of this, but understanding the TCP layer helps debug connection issues (TIME_WAIT, RST, FIN storms).

---

## Real-Time Streaming Patterns

### Fan-Out

A single data source (the anomaly detection pipeline) must broadcast to N connected clients. Strategies:

- **Iterate and send**: simple loop over all connections; a slow client blocks the others unless sends are done concurrently
- **asyncio.gather**: send to all clients concurrently; if one fails, handle its error independently
- **Per-client queues**: each client has an `asyncio.Queue`; a dedicated coroutine drains each queue. This decouples production from consumption and naturally handles backpressure

### Backpressure

When a consumer can't keep up with the producer:

- **Unbounded buffers**: memory grows until OOM — never do this in production
- **Bounded queues with drop**: drop oldest or newest messages when the queue is full (appropriate for monitoring data where freshness matters more than completeness)
- **Bounded queues with block**: pause the producer; appropriate when data loss is unacceptable
- **Rate limiting the producer**: throttle upstream; simplest but adds latency globally

### Heartbeat / Keepalive

WebSocket connections can silently die (NAT timeout, mobile network switch, proxy timeout). Solutions:

- **Ping/Pong frames**: WebSocket protocol has built-in ping/pong. `websockets` handles pongs automatically. Configure `ping_interval` and `ping_timeout`.
- **Application-level heartbeat**: send a custom JSON heartbeat message on a timer. Useful when you need to measure round-trip latency.
- **TCP keepalive**: OS-level mechanism; coarser-grained (minutes) and not always reliable through proxies

---

## Online / Streaming Anomaly Detection Algorithms

Traditional anomaly detection operates on a fixed dataset. Streaming anomaly detection must:

- Process each data point **once** in arrival order
- Use **bounded memory** (no storing the full history)
- Adapt to **concept drift** (the data distribution changes over time)

### Z-Score Method

The simplest online detector. Maintain a running mean (μ) and standard deviation (σ), then flag a point x as anomalous if:

$$|z| = \frac{|x - \mu|}{\sigma} > \text{threshold}$$

Use Welford's online algorithm to compute running mean and variance in a single pass without catastrophic cancellation:

```
M₁ = x₁
For n ≥ 2:
  Mₙ = Mₙ₋₁ + (xₙ - Mₙ₋₁) / n
  Sₙ = Sₙ₋₁ + (xₙ - Mₙ₋₁)(xₙ - Mₙ)
  σ² = Sₙ / (n - 1)
```

**Strengths**: trivial to implement, O(1) memory, O(1) per point
**Weaknesses**: assumes stationarity and approximate normality; a single extreme outlier can inflate σ and mask future anomalies

### EWMA Control Charts

Exponentially Weighted Moving Average places more weight on recent observations, making it responsive to shifts:

$$\text{EWMA}_t = \lambda \cdot x_t + (1 - \lambda) \cdot \text{EWMA}_{t-1}$$

where λ ∈ (0, 1] is the smoothing factor (often called `span` via λ = 2/(span+1)).

Control limits:

$$UCL/LCL = \mu_0 \pm L \cdot \sigma \sqrt{\frac{\lambda}{2-\lambda}\left[1-(1-\lambda)^{2t}\right]}$$

where L is the control limit width (typically 2.5–3.0).

**Strengths**: detects small sustained shifts better than Z-score; tunable via λ
**Weaknesses**: still parametric; the steady-state term `[1-(1-λ)^{2t}]` converges quickly, so the limits become approximately constant

### Isolation Forest for Streaming

Isolation Forest works by randomly partitioning the feature space; anomalies require fewer partitions to isolate. For streaming:

1. Maintain a **window** of recent data (e.g. last 1000 points)
2. Periodically **retrain** the forest on the current window
3. Score incoming points against the current forest
4. Anomaly score < threshold → anomaly

This is a mini-batch approach rather than truly online, but it adapts to drift as the window slides.

**Strengths**: non-parametric, handles multivariate data, no distributional assumptions
**Weaknesses**: retraining cost, window size is a hyperparameter, latency spike during retrain

### Windowed Statistics

Many detectors benefit from computing statistics over a sliding window rather than all history:

- **Tumbling window**: non-overlapping fixed-size windows [0,N), [N,2N), ...
- **Sliding window**: overlapping windows that advance one point at a time
- **Exponential decay**: not a window per se, but recent points are weighted more (like EWMA)

Implementation options:
- `collections.deque(maxlen=N)` for fixed-size sliding windows
- Ring buffers for zero-allocation sliding windows
- Numpy arrays with modular indexing

---

## Alert Fatigue and Deduplication

A detector that fires on every outlier produces too many alerts. Production systems need:

- **Deduplication**: if the same detector is already firing for the same metric, suppress repeated alerts within a cooldown window
- **Severity classification**: not all anomalies are equal. Classify by magnitude (how many σ away), duration (how long has the anomaly persisted), and scope (how many metrics are affected)
- **Cooldown periods**: after an alert fires, suppress identical alerts for N seconds
- **Hysteresis**: require the signal to return to normal before re-alerting (prevents flapping)
- **Aggregation**: group related alerts (e.g. "5 sensors in building A are anomalous" rather than 5 separate alerts)

---

## Scaling WebSocket Servers

A single WebSocket server is limited by file descriptors and memory. Scaling strategies:

- **Vertical**: increase ulimits, optimize per-connection memory (a minimal WebSocket connection in Python uses ~30KB)
- **Horizontal**: run multiple server instances behind a load balancer. Requires:
  - **Sticky sessions** or connection-aware routing (L4 load balancer, not L7 with round-robin)
  - **Pub/sub backbone** (Redis Pub/Sub, NATS, Kafka) for cross-instance message distribution
- **Connection limits**: set a max connections per server and reject/redirect when full
- **Graceful shutdown**: drain connections by sending close frames, then stop accepting new ones

For this tutorial project, a single server is sufficient. The architecture is designed so that adding a pub/sub layer later is straightforward.
