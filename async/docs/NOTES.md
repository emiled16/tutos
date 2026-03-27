# Async Python — Theory & Notes

## The asyncio Event Loop

The event loop is the core of asyncio. It runs in a single thread and manages:

- Scheduling and running coroutines
- Handling I/O events (network, file descriptors)
- Running callbacks and timers
- Managing subprocesses

```python
import asyncio

async def main():
    await asyncio.sleep(1)

asyncio.run(main())  # Creates event loop, runs coroutine, closes loop
```

### How the Event Loop Works

1. The loop checks for ready callbacks/coroutines
2. Executes them one at a time until they `await` something
3. When a coroutine awaits, control returns to the event loop
4. The loop checks for I/O readiness and timers
5. Repeat

**Key insight:** Async code achieves concurrency by *cooperatively yielding* control at `await` points, not by running in parallel threads.

## Coroutines vs Threads vs Processes

| Feature | Coroutines (asyncio) | Threads | Processes |
|---|---|---|---|
| **Concurrency model** | Cooperative (single thread) | Preemptive (OS-scheduled) | True parallelism |
| **GIL impact** | N/A (single thread) | Limited by GIL for CPU work | No GIL constraint |
| **Context switching** | Very cheap (~ns) | Moderate (~μs) | Expensive (~ms) |
| **Memory overhead** | ~1KB per coroutine | ~8MB stack per thread | Full process memory |
| **Best for** | I/O-bound (network, DB) | Mixed I/O + some CPU | CPU-bound work |
| **Shared state** | Direct (same thread) | Needs locks | IPC needed |
| **Debugging** | Deterministic ordering | Race conditions | Isolation helps |

### When to Use asyncio

- High-concurrency I/O: HTTP servers, database clients, API gateways
- Thousands of concurrent connections
- When thread overhead is too high

### When NOT to Use asyncio

- CPU-bound computation (use multiprocessing)
- Libraries without async support (use threads via `loop.run_in_executor`)

## Async Generators

```python
async def fetch_pages(url: str):
    page = 1
    while True:
        data = await http_client.get(f"{url}?page={page}")
        if not data:
            break
        yield data
        page += 1

async for page in fetch_pages("https://api.example.com/items"):
    process(page)
```

Async generators lazily produce values, pausing between yields while waiting for I/O.

## Async Context Managers

```python
class AsyncDBConnection:
    async def __aenter__(self):
        self.conn = await connect_to_db()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

async with AsyncDBConnection() as db:
    await db.query("SELECT 1")
```

Use `async with` for resources that need async setup/teardown (connections, sessions, locks).

## aiohttp vs FastAPI

| Feature | aiohttp | FastAPI |
|---|---|---|
| **Type** | Low-level async HTTP | High-level ASGI framework |
| **Performance** | Excellent | Excellent (via Starlette) |
| **Validation** | Manual | Built-in (Pydantic) |
| **Documentation** | Manual | Auto-generated OpenAPI |
| **WebSocket** | Built-in | Built-in |
| **Client** | Built-in (aiohttp.ClientSession) | Requires httpx |
| **Learning curve** | Moderate | Lower |

This project uses aiohttp for its lower-level control over the event loop and connection lifecycle, which is valuable for understanding async internals.

## Backpressure Patterns

Backpressure prevents a fast producer from overwhelming a slow consumer.

### Bounded Queue

```python
queue = asyncio.Queue(maxsize=100)

# Producer — blocks when queue is full
await queue.put(item)

# Or non-blocking with timeout
try:
    queue.put_nowait(item)
except asyncio.QueueFull:
    return HTTP_503_SERVICE_UNAVAILABLE
```

### Strategies

1. **Block:** Producer waits until space is available (blocks upstream)
2. **Drop:** Discard new items when full (lossy but prevents blocking)
3. **Reject:** Return an error to the caller (HTTP 503)
4. **Adaptive:** Dynamically adjust processing rate or batch size

### Why Backpressure Matters for ML Inference

- GPU memory is finite; too many concurrent batches → OOM
- Without backpressure, request latency grows unbounded under load
- Better to reject fast and let clients retry than queue indefinitely

## Dynamic Batching Strategies

Dynamic batching groups individual inference requests into batches for efficient processing:

### By Size

Collect requests until the batch reaches a target size, then process:

```python
batch = []
while len(batch) < max_batch_size:
    request = await queue.get()
    batch.append(request)
process_batch(batch)
```

**Problem:** If traffic is low, the last few requests wait indefinitely.

### By Timeout

Process the batch after a time window, regardless of size:

```python
batch = []
deadline = time.monotonic() + max_wait_seconds
while time.monotonic() < deadline and len(batch) < max_batch_size:
    try:
        request = await asyncio.wait_for(queue.get(), timeout=remaining)
        batch.append(request)
    except asyncio.TimeoutError:
        break
process_batch(batch)
```

This is the preferred approach: it bounds both batch size (throughput) and wait time (latency).

## Graceful Shutdown

A well-behaved async service should:

1. **Stop accepting new requests** (close the listener)
2. **Drain the queue** (process remaining queued items)
3. **Wait for in-flight requests** (with a timeout)
4. **Clean up resources** (close connections, sessions)

```python
async def shutdown(app):
    app["accepting_requests"] = False
    await app["batcher"].drain()
    await app["session"].close()
```

Register shutdown handlers with signal handlers or aiohttp's `on_shutdown` hooks.

## Structured Concurrency

Structured concurrency ensures that async tasks have clear ownership and lifecycles:

```python
async with asyncio.TaskGroup() as tg:
    tg.create_task(fetch_a())
    tg.create_task(fetch_b())
# Both tasks are guaranteed to complete (or fail) here
```

Benefits:
- No orphaned tasks
- Exceptions propagate cleanly
- Resources are properly cleaned up

`asyncio.TaskGroup` (Python 3.11+) is the preferred way to manage concurrent tasks.

## Common Pitfalls

### 1. Blocking the Event Loop

```python
# BAD — blocks the event loop for all coroutines
async def handler(request):
    result = heavy_computation()  # Synchronous CPU work
    return web.json_response(result)

# GOOD — offload to a thread pool
async def handler(request):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, heavy_computation)
    return web.json_response(result)
```

### 2. Forgetting `await`

```python
# BAD — coroutine is created but never awaited (silently does nothing)
async def handler(request):
    save_to_database(data)  # Missing await!

# GOOD
async def handler(request):
    await save_to_database(data)
```

Python will issue a "coroutine was never awaited" RuntimeWarning, but it's easy to miss.

### 3. Creating Tasks Without Tracking

```python
# BAD — task may be garbage collected before completing
asyncio.create_task(background_work())

# GOOD — keep a reference
task = asyncio.create_task(background_work())
background_tasks.add(task)
task.add_done_callback(background_tasks.discard)
```

### 4. Not Handling Cancellation

When a task is cancelled (e.g., timeout), `asyncio.CancelledError` is raised. If you catch `Exception`, you'll swallow the cancellation:

```python
# BAD
try:
    await some_work()
except Exception:
    pass  # Swallows CancelledError!

# GOOD
try:
    await some_work()
except asyncio.CancelledError:
    # Clean up, then re-raise
    raise
except Exception:
    handle_error()
```

### 5. Resource Leaks

Always use `async with` for sessions and connections:

```python
# BAD
session = aiohttp.ClientSession()
# ... if an exception occurs, session is never closed

# GOOD
async with aiohttp.ClientSession() as session:
    ...  # session is closed even on exception
```

## Key Terminology

- **Coroutine:** A function defined with `async def` that can be paused and resumed at `await` points
- **Future:** A placeholder for a result that hasn't been computed yet
- **Task:** A Future that wraps a coroutine and schedules it on the event loop
- **Event loop:** The central coordinator that runs coroutines and handles I/O
- **Backpressure:** Mechanism to slow down producers when consumers can't keep up
- **Dynamic batching:** Grouping individual requests into batches for efficient processing
- **Structured concurrency:** Pattern ensuring async tasks have clear ownership and lifecycles
- **Graceful shutdown:** Stopping a service while completing in-flight work
