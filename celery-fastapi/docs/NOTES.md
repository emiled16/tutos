# Task Queues, Celery & FastAPI — Theory Notes

## Core Concepts

### Task Queue Architecture

A task queue decouples the submission of work from its execution. The three main components:

1. **Producer** (API server): creates task messages and publishes them to the broker
2. **Broker** (Redis/RabbitMQ): a message transport that holds tasks until workers consume them
3. **Worker** (Celery process): pulls tasks from the broker, executes them, stores results

This separation means the API can respond immediately ("accepted, here's your task ID") while heavy computation runs asynchronously.

### Broker vs Backend

- **Broker**: the message queue that transports task messages from producer to worker. Redis and RabbitMQ are the most common. The broker must be fast and reliable — if it goes down, no new tasks can be dispatched.
- **Result Backend**: where task results are stored after completion. Workers write results here; the API reads them. Redis, databases, or S3 can serve as backends. The backend is optional — if you don't need results, skip it.

Using Redis for both broker and backend is common for simplicity, but has a trade-off: results consume Redis memory.

## Celery Worker Model

### Worker Process Architecture

Celery workers are separate processes that run independently from the API server. Each worker:
1. Connects to the broker
2. Subscribes to one or more queues
3. Pulls task messages
4. Deserializes and executes tasks
5. Stores results in the backend

### Concurrency Models

| Pool | How it works | Best for |
|------|-------------|----------|
| **prefork** (default) | Multiple OS processes | CPU-bound tasks (ML training, data processing) |
| **eventlet** | Green threads (cooperative) | I/O-bound tasks (API calls, file downloads) |
| **gevent** | Green threads (cooperative) | Similar to eventlet, different implementation |
| **solo** | Single thread, no concurrency | Debugging, simple setups |

For ML workloads, **prefork** is almost always correct — training is CPU-bound and benefits from OS-level process isolation.

## Task States and Lifecycle

```
PENDING → STARTED → (RETRY →)* SUCCESS
                              → FAILURE
                              → REVOKED
```

- **PENDING**: task is queued but not yet picked up by a worker (also the default state for unknown task IDs)
- **STARTED**: a worker has begun executing the task (requires `task_track_started=True`)
- **RETRY**: task failed and is waiting to be retried
- **SUCCESS**: task completed without errors
- **FAILURE**: task raised an unhandled exception after all retries exhausted
- **REVOKED**: task was cancelled before or during execution

Important: PENDING is the default state for *any* task ID, including ones that don't exist. You cannot distinguish "queued" from "unknown" without additional tracking.

## Retry Strategies

### Exponential Backoff

When a task fails due to a transient error (network timeout, resource unavailable), retrying immediately may fail again. Exponential backoff spaces out retries:

```
Attempt 1: immediate
Attempt 2: wait 4 seconds
Attempt 3: wait 16 seconds
Attempt 4: wait 64 seconds
```

Formula: `delay = base ** retry_number` (with optional jitter to prevent thundering herd).

### Configuration

```python
@app.task(bind=True, max_retries=3, default_retry_delay=60)
def my_task(self):
    try:
        ...
    except TransientError as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
```

Key parameters:
- `max_retries`: upper limit on retry attempts
- `countdown`: seconds to wait before the next attempt
- `retry_backoff`: enable automatic exponential backoff
- `retry_jitter`: add randomness to prevent coordinated retries

## Canvas Primitives: Composing Tasks

Celery's canvas lets you compose tasks into workflows:

### Chain
Sequential execution: each task receives the result of the previous one.
```python
chain(preprocess.s(data), train.s(), evaluate.s())()
```
preprocess → train → evaluate, where each step's output feeds the next.

### Group
Parallel execution: all tasks run concurrently.
```python
group(train.s(config1), train.s(config2), train.s(config3))()
```

### Chord
A group followed by a callback: the callback runs after all group tasks complete.
```python
chord(group(train.s(c) for c in configs))(aggregate_results.s())
```

### Chord Error Handling
If any task in a chord group fails, the callback receives the error. Handle this explicitly — don't assume all results will be successful.

## Monitoring with Flower

[Flower](https://flower.readthedocs.io/) is a real-time web UI for monitoring Celery:
- Active/reserved/scheduled tasks per worker
- Task history with success/failure rates
- Worker resource utilization
- Task details with arguments and results

Launch: `celery -A worker.celery_app flower`

## Serialization Considerations

Celery serializes task arguments and results for transport through the broker. Default is JSON, but options include:

| Format | Pros | Cons |
|--------|------|------|
| JSON | Human-readable, safe | Limited types (no datetime, bytes) |
| pickle | Any Python object | Security risk (arbitrary code execution) |
| msgpack | Fast, compact | Limited types |

For ML workloads, JSON is safest. Pass file paths or IDs rather than large objects — don't serialize an entire DataFrame through the broker.

## Idempotency in Distributed Tasks

A task is **idempotent** if executing it multiple times produces the same result as executing it once. This is critical because:

1. Workers may crash mid-execution and the task gets redelivered
2. Retry logic explicitly re-executes failed tasks
3. Network partitions can cause duplicate delivery

Strategies for idempotency:
- Use unique task IDs to check if work was already done
- Write results atomically (don't partially update)
- Use database transactions or conditional writes
- Design tasks as "set state to X" rather than "increment by Y"

## FastAPI Integration

### Dependency Injection

FastAPI's `Depends` system manages shared resources:
```python
async def get_redis() -> Redis:
    return Redis.from_url(settings.REDIS_URL)

@app.get("/status/{task_id}")
async def status(task_id: str, redis: Redis = Depends(get_redis)):
    ...
```

Benefits: testability (inject mocks), lifecycle management, clean separation.

### WebSocket Lifecycle

WebSocket connections in FastAPI follow this lifecycle:
1. **Handshake**: client sends upgrade request, server accepts
2. **Connected**: bidirectional communication (server pushes progress updates)
3. **Disconnected**: either side closes the connection

Key considerations:
- Handle `WebSocketDisconnect` exceptions gracefully
- Clean up subscriptions when clients disconnect
- Use Redis Pub/Sub to broadcast progress from workers to the API server, then to WebSocket clients
- Don't block the event loop — use `asyncio` patterns

## Best Practices

1. **Keep tasks small and focused**: one task = one logical unit of work. Use chains for multi-step pipelines.
2. **Don't pass large objects through the broker**: pass file paths, database IDs, or S3 keys instead.
3. **Always set task timeouts**: prevent zombie tasks from consuming workers indefinitely.
4. **Use `bind=True`**: access `self.request` for task metadata (retries, ID, etc.).
5. **Track task started state**: set `task_track_started=True` to distinguish queued from running.
6. **Implement idempotent tasks**: assume every task may run more than once.
7. **Use structured logging**: include task_id in log messages for traceability.
8. **Test with eager mode**: `CELERY_ALWAYS_EAGER=True` runs tasks synchronously in tests.

## Common Pitfalls

- **PENDING doesn't mean queued**: it's the default state for any task ID, including non-existent ones. Track task creation separately if you need this distinction.
- **Forgetting to handle chord errors**: if one task in a chord group fails, the callback still fires — with an error, not results.
- **Blocking the event loop**: running synchronous Celery calls (`.get()`) in an async FastAPI handler blocks the entire server. Use `asyncio.to_thread()` or check status asynchronously.
- **Memory leaks from result backends**: results accumulate in Redis. Set `result_expires` to auto-clean old results.
- **Pickle serialization in production**: allows arbitrary code execution. Use JSON.
- **Not setting `task_acks_late`**: by default, tasks are acknowledged when received, not when completed. If a worker crashes, the task is lost. Set `task_acks_late=True` for at-least-once delivery.

## Key Terminology

- **Broker**: message transport between producers and consumers (Redis, RabbitMQ)
- **Backend**: storage for task results and state
- **Worker**: process that executes tasks
- **Canvas**: Celery's API for composing tasks (chain, group, chord)
- **Eager mode**: runs tasks synchronously in the same process (for testing)
- **Prefork pool**: worker concurrency via OS process forking
- **Task signature**: a serializable reference to a task with its arguments (`task.s(args)`)
- **Countdown**: delay in seconds before a retried task is re-queued
- **Revoke**: cancel a pending or running task
- **Idempotent**: a task that produces the same result regardless of how many times it runs
- **Ack**: acknowledgment that a task message was received/completed
