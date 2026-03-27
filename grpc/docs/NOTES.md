# gRPC for ML Model Serving — Theory & Notes

## gRPC vs REST

| Aspect | gRPC | REST |
|---|---|---|
| Protocol | HTTP/2 | HTTP/1.1 (mostly) |
| Serialization | Protocol Buffers (binary) | JSON (text) |
| Contract | Strict (.proto file) | Loose (OpenAPI optional) |
| Streaming | Native (4 patterns) | Limited (SSE, WebSocket) |
| Code generation | Built-in | Separate tooling |
| Browser support | Needs gRPC-Web proxy | Native |
| Performance | ~10x faster serialization | Slower but human-readable |
| Latency | Lower (binary, HTTP/2 multiplexing) | Higher |

### When to Use gRPC

- **Internal microservice communication** — Type safety, speed, streaming
- **High-throughput model serving** — Binary serialization of large tensors
- **Streaming predictions** — Real-time feeds, batch streaming
- **Polyglot environments** — Auto-generated clients in any language

### When to Use REST

- **Public APIs** — Browser-friendly, widely understood
- **Simple CRUD** — Over-engineering with gRPC
- **Debugging** — JSON is human-readable, curl-friendly

## Protocol Buffers (Protobuf)

Protocol Buffers are Google's language-neutral, platform-neutral mechanism for serializing structured data.

### Proto3 Syntax

```protobuf
syntax = "proto3";

message PredictRequest {
  string model_name = 1;      // field number, not default value
  NDArray features = 2;
  map<string, string> metadata = 3;
}

message NDArray {
  repeated int32 shape = 1;
  repeated float data = 2;
  string dtype = 3;
}
```

### Key Rules

- **Field numbers** are permanent — never reuse or change them
- **Default values** are not serialized (saves bandwidth)
- **Backward compatibility** — add new fields, don't remove old ones
- **Repeated fields** are ordered lists
- **Oneof** for mutually exclusive fields
- **Maps** for key-value pairs

### Compilation

```bash
python -m grpc_tools.protoc \
  --proto_path=. \
  --python_out=. \
  --grpc_python_out=. \
  model_serving.proto
```

This generates `model_serving_pb2.py` (messages) and `model_serving_pb2_grpc.py` (service stubs).

## gRPC Communication Patterns

### 1. Unary RPC

Standard request-response. Client sends one message, server responds with one message.

```protobuf
rpc Predict(PredictRequest) returns (PredictResponse);
```

Use for: Single prediction, model info queries.

### 2. Server-Streaming RPC

Client sends one request, server streams back multiple responses.

```protobuf
rpc StreamPredict(PredictRequest) returns (stream PredictResponse);
```

Use for: Batch prediction results streamed as they're computed, real-time monitoring.

### 3. Client-Streaming RPC

Client streams multiple requests, server responds with one message.

```protobuf
rpc BatchPredict(stream PredictRequest) returns (BatchResponse);
```

Use for: Uploading a large batch of inputs, aggregated results.

### 4. Bidirectional Streaming RPC

Both client and server stream messages independently.

```protobuf
rpc StreamingPredict(stream PredictRequest) returns (stream PredictResponse);
```

Use for: Real-time inference pipeline, interactive sessions.

## Interceptors

Interceptors are gRPC's equivalent of HTTP middleware. They wrap RPC handlers to add cross-cutting functionality.

### Server Interceptors

```python
class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        # Pre-processing: log request
        response = continuation(handler_call_details)
        # Post-processing: log response
        return response
```

Common server interceptors:
- **Logging** — Request/response timing, method names, status codes
- **Authentication** — Validate API keys or JWT tokens from metadata
- **Rate limiting** — Token bucket or sliding window per client IP
- **Metrics** — Prometheus counters/histograms

### Client Interceptors

```python
class RetryInterceptor(grpc.UnaryUnaryClientInterceptor):
    def intercept_unary_unary(self, continuation, client_call_details, request):
        # Add retry logic around the call
        ...
```

## Channel Management and Connection Pooling

### Channels

A gRPC channel represents a connection to a server. Channels:
- Are thread-safe — multiple RPCs share a channel
- Manage the underlying HTTP/2 connection
- Handle reconnection automatically

```python
channel = grpc.insecure_channel("localhost:50051")
stub = PredictServiceStub(channel)
```

### Connection Pooling

For high throughput, maintain multiple channels:

```python
channels = [grpc.insecure_channel(addr) for addr in server_addresses]
stubs = [PredictServiceStub(ch) for ch in channels]
```

Key considerations:
- One channel per server address is usually sufficient (HTTP/2 multiplexing)
- Pool size > number of servers is useful when exceeding HTTP/2 stream limits
- Channels should be reused, not created per-request

## Load Balancing

### Client-Side Load Balancing

The client maintains a list of server addresses and distributes requests.

**Round-robin:** Rotate through servers in order. Simple but doesn't account for server load.

**Weighted round-robin:** Assign weights based on server capacity.

**Pick-first:** Always use the first available server. Simplest but no distribution.

### Server-Side Load Balancing

A proxy (e.g., Envoy, NGINX with gRPC support) sits between clients and servers.

- Clients connect to one address (the proxy)
- Proxy distributes to backends
- Better for large deployments, no client-side logic needed

### Look-Aside Load Balancing

Client queries a separate load balancer service for backend addresses, then connects directly. Used by Google's internal systems.

## Health Checking Protocol

gRPC defines a standard health checking protocol:

```protobuf
service Health {
  rpc Check(HealthCheckRequest) returns (HealthCheckResponse);
  rpc Watch(HealthCheckRequest) returns (stream HealthCheckResponse);
}
```

Status values:
- `UNKNOWN` — Not yet determined
- `SERVING` — Healthy and accepting requests
- `NOT_SERVING` — Unhealthy, should not receive traffic
- `SERVICE_UNKNOWN` — Requested service not registered

Health checks are per-service, allowing partial availability.

## Deadlines and Timeouts

gRPC uses **deadlines** (absolute time) rather than timeouts (relative duration):

```python
response = stub.Predict(request, timeout=5.0)  # 5-second deadline
```

If the deadline expires:
- Client receives `DEADLINE_EXCEEDED` status
- Server should check deadline and stop work if exceeded
- Deadlines propagate across chained RPCs

Best practices:
- Always set deadlines on the client
- Check deadlines in long-running server operations
- Account for network latency in deadline calculations

## Error Handling with Status Codes

gRPC uses a set of standard status codes:

| Code | Name | Use Case |
|---|---|---|
| 0 | OK | Success |
| 1 | CANCELLED | Client cancelled |
| 3 | INVALID_ARGUMENT | Bad input |
| 4 | DEADLINE_EXCEEDED | Timeout |
| 5 | NOT_FOUND | Model not loaded |
| 7 | PERMISSION_DENIED | Auth failure |
| 8 | RESOURCE_EXHAUSTED | Rate limited |
| 13 | INTERNAL | Server error |
| 14 | UNAVAILABLE | Server temporarily down |

```python
context.abort(grpc.StatusCode.NOT_FOUND, f"Model '{model_name}' not found")
```

### Error Details

Use `google.rpc.Status` with `Any`-packed details for rich error information:

```python
from google.rpc import error_details_pb2, status_pb2
```

## Reflection

gRPC Server Reflection allows clients to discover services at runtime:

```python
from grpc_reflection.v1alpha import reflection
reflection.enable_server_reflection(SERVICE_NAMES, server)
```

Useful for debugging tools like `grpcurl`:

```bash
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 describe PredictService
```

## gRPC-Web

gRPC-Web enables browser clients to call gRPC services via a proxy (Envoy):

- Browser → HTTP/1.1 + Base64-encoded protobuf → Envoy proxy → HTTP/2 gRPC → Server
- Supports unary and server-streaming only (no client-streaming or bidi)
- TypeScript/JavaScript client libraries available

## Best Practices

1. **Use deadlines everywhere** — Prevent hung requests from consuming resources
2. **Implement idempotent operations** — Retries should be safe
3. **Version your proto files** — Use package names like `v1`, `v2`
4. **Never change field numbers** — Add new fields, deprecate old ones
5. **Use streaming for large payloads** — Chunk large arrays into stream messages
6. **Enable keepalive** — Prevent connection drops through proxies/firewalls
7. **Implement graceful shutdown** — Drain in-flight RPCs before stopping

## Common Pitfalls

1. **Forgetting deadlines** — Requests hang forever when servers are slow
2. **Not handling UNAVAILABLE** — Transient errors need retries with backoff
3. **Large messages** — gRPC default max message size is 4MB; increase or stream
4. **Blocking in async handlers** — CPU-heavy model inference blocks the event loop
5. **Channel per request** — Creating channels is expensive; reuse them
6. **Ignoring status codes** — Treating all errors the same instead of using specific codes
7. **Proto field number reuse** — Changing field numbers breaks backward compatibility

## Key Terminology

- **Stub** — Client-side proxy generated from proto definitions
- **Servicer** — Server-side implementation of the service interface
- **Channel** — Client-side connection to a server
- **Metadata** — Key-value pairs sent with requests (like HTTP headers)
- **Interceptor** — Middleware that wraps RPC handlers
- **Deadline** — Absolute time by which an RPC must complete
- **Status code** — Standard error code returned with failed RPCs
- **Reflection** — Runtime service discovery for debugging
- **Protobuf** — Binary serialization format for structured data
- **Materialization** — The generated Python code from .proto files
- **Keepalive** — Periodic pings to maintain idle connections
