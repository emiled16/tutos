# High-Performance Model Server

## Overview

Build a gRPC service for serving ML models with Protocol Buffer serialization, streaming predictions, interceptors for logging and authentication, and health checking. The project covers server and client implementation, connection management, and load balancing.

## Learning Objectives

- Understand gRPC communication patterns (unary, server-streaming, client-streaming, bidirectional)
- Define Protocol Buffer service and message types for ML model serving
- Implement a gRPC server with unary and streaming prediction RPCs
- Build server interceptors for logging, authentication, and rate limiting
- Implement gRPC health checking protocol
- Build a gRPC client with connection pooling and retry logic
- Implement client-side load balancing (round-robin)
- Handle model loading, versioning, and hot-reload

## Project Description

You are building a high-performance model serving infrastructure using gRPC. The system must:

1. **Define the API** — Protocol Buffer definitions for prediction requests/responses with numpy array serialization
2. **Implement the server** — gRPC server with unary and streaming prediction endpoints
3. **Add interceptors** — Server-side middleware for logging, token-based auth, and rate limiting
4. **Health checking** — Standard gRPC health checking for load balancer integration
5. **Manage models** — Load, version, and hot-reload ML models without downtime
6. **Build the client** — Client with connection pooling, retries, and round-robin load balancing
7. **Serialize arrays** — Efficient numpy array ↔ protobuf conversion

## Architecture

```
grpc/
├── protos/
│   └── model_serving.proto      # Protobuf service & message definitions
├── server/
│   ├── server.py                # gRPC server setup and lifecycle
│   ├── servicer.py              # PredictServicer (unary + streaming RPCs)
│   ├── interceptors.py          # Logging, auth, rate-limiting interceptors
│   ├── health.py                # gRPC health checking service
│   └── model_manager.py         # Model loading, versioning, hot-reload
├── client/
│   ├── client.py                # gRPC client with retries and pooling
│   └── load_balancer.py         # Client-side round-robin load balancing
├── models/
│   └── predictor.py             # ML model wrapper for inference
└── utils/
    └── serialization.py         # Numpy ↔ protobuf conversion
```

## Implementation Tasks

### Phase 1: Protobuf & Serialization
- [ ] Define protobuf messages (PredictRequest, PredictResponse, NDArray, ModelInfo)
- [ ] Define PredictService with Predict (unary) and StreamPredict (server-streaming) RPCs
- [ ] Implement numpy array to/from protobuf conversion with dtype preservation

### Phase 2: Server
- [ ] Implement PredictServicer with unary and streaming prediction handlers
- [ ] Implement model manager with load, list, and hot-reload capabilities
- [ ] Build server startup with graceful shutdown
- [ ] Add gRPC health checking service

### Phase 3: Interceptors
- [ ] Implement logging interceptor (request/response timing, metadata)
- [ ] Implement authentication interceptor (API key from metadata)
- [ ] Implement rate limiting interceptor (token bucket per client)

### Phase 4: Client
- [ ] Build client with channel management and automatic retries
- [ ] Implement connection pooling across multiple server addresses
- [ ] Implement round-robin load balancing
- [ ] Add client-side deadline (timeout) support

## Evaluation Criteria

- Protobuf definitions compile without errors
- Server starts and accepts connections on the configured port
- Unary prediction returns correct results for valid input
- Streaming prediction yields results incrementally
- Auth interceptor rejects requests without valid API key
- Rate limiter throttles excess requests
- Health check reports serving/not-serving status correctly
- Client retries on transient failures
- Load balancer distributes requests across servers
- Numpy arrays round-trip through protobuf without data loss

## Resources

- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
- [Protocol Buffers Language Guide](https://protobuf.dev/programming-guides/proto3/)
- [gRPC Health Checking Protocol](https://github.com/grpc/grpc/blob/master/doc/health-checking.md)
- [gRPC Interceptors](https://grpc.io/docs/guides/interceptors/)
- [gRPC Load Balancing](https://grpc.io/blog/grpc-load-balancing/)
- [Serving ML Models with gRPC (blog)](https://neptune.ai/blog/ml-model-serving)
