# Distributed ML Task Queue with Celery & FastAPI

## Overview

Build a [FastAPI](https://fastapi.tiangolo.com/) application that accepts machine learning training requests and delegates them to [Celery](https://docs.celeryq.dev/) workers with Redis as the message broker. The system provides real-time progress tracking via WebSocket, result caching, task chaining for multi-step ML workflows, and robust retry logic for fault tolerance.

This project teaches you to build production-style async task processing systems where long-running ML workloads are decoupled from the request/response cycle.

## Learning Objectives

- Design a task queue architecture with broker, workers, and result backend
- Implement FastAPI endpoints that submit, monitor, and cancel async tasks
- Configure Celery workers with appropriate concurrency and serialization
- Build task chains and groups using Celery's canvas primitives
- Implement WebSocket-based real-time progress reporting
- Write idempotent tasks with proper retry strategies
- Test async task flows using Celery's eager mode
- Manage configuration with pydantic-settings

## Project Description

You will build a system that:

1. **Accepts** ML training requests via a REST API with dataset parameters, model configuration, and hyperparameters
2. **Validates** requests using Pydantic schemas and returns a task ID immediately
3. **Dispatches** work to Celery workers that simulate preprocessing, training, and evaluation steps
4. **Tracks progress** of running tasks and broadcasts updates via WebSocket
5. **Chains tasks** so that preprocessing → training → evaluation runs as a pipeline
6. **Handles failures** with exponential backoff retries and graceful cancellation
7. **Caches results** in Redis and exposes them via a GET endpoint

## Architecture

```
┌──────────────┐     POST /train     ┌───────────────┐
│   Client     │────────────────────▶│   FastAPI      │
│              │◀────────────────────│   Application  │
│              │     task_id         │                │
│              │                     └───────┬───────┘
│              │                             │
│              │   WebSocket /ws/{task_id}   │  task.delay()
│              │◀─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
│              │   progress updates         │
└──────────────┘                     ┌──────▼───────┐
                                     │    Redis      │
                                     │   (Broker +   │
                                     │    Backend)   │
                                     └──────┬───────┘
                                            │
                              ┌─────────────┼─────────────┐
                              │             │             │
                        ┌─────▼────┐  ┌─────▼────┐  ┌────▼─────┐
                        │ Worker 1 │  │ Worker 2 │  │ Worker N │
                        │          │  │          │  │          │
                        │ preproc  │  │  train   │  │  eval    │
                        └──────────┘  └──────────┘  └──────────┘
```

## Implementation Tasks

### Phase 1: Configuration & Setup
- [ ] Define settings with pydantic-settings (Redis URL, Celery config)
- [ ] Configure the Celery application with Redis broker and backend
- [ ] Set up FastAPI application with lifespan management

### Phase 2: API Layer
- [ ] Define Pydantic request/response schemas for training jobs
- [ ] Implement POST /train endpoint to submit training tasks
- [ ] Implement GET /status/{task_id} to check task state
- [ ] Implement GET /result/{task_id} to retrieve completed results
- [ ] Implement DELETE /cancel/{task_id} to revoke running tasks

### Phase 3: Task Implementation
- [ ] Implement `preprocess_data` task with progress reporting
- [ ] Implement `train_model` task with simulated training loop and progress
- [ ] Implement `evaluate_model` task that computes metrics
- [ ] Wire tasks into a chain: preprocess → train → evaluate
- [ ] Add retry logic with exponential backoff (max 3 retries)

### Phase 4: Real-Time Updates
- [ ] Implement WebSocket endpoint for task progress streaming
- [ ] Add task callbacks that publish progress to a channel
- [ ] Handle WebSocket connection lifecycle (connect, disconnect, errors)

### Phase 5: Testing
- [ ] Test API endpoints with FastAPI TestClient
- [ ] Test Celery tasks in eager mode (synchronous execution)
- [ ] Test task chaining and error handling
- [ ] Set up test fixtures for FastAPI client and Celery app

## Evaluation Criteria

- API accepts training requests and returns task IDs without blocking
- Task status correctly reflects the Celery task lifecycle (PENDING → STARTED → SUCCESS/FAILURE)
- WebSocket delivers real-time progress updates to connected clients
- Task chains execute preprocessing → training → evaluation in sequence
- Failed tasks retry with exponential backoff and eventually report failure
- Cancelled tasks are properly revoked
- All endpoints return well-structured JSON responses with proper HTTP status codes

## Resources

- [Celery Documentation](https://docs.celeryq.dev/)
- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Celery Canvas (Chains, Groups, Chords)](https://docs.celeryq.dev/en/stable/userguide/canvas.html)
- [FastAPI WebSocket](https://fastapi.tiangolo.com/advanced/websockets/)
- [Pydantic Settings Management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Redis Pub/Sub](https://redis.io/docs/manual/pubsub/)
