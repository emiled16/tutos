# Optimized LLM Inference Server — Theory & Notes

## LLM Inference Challenges

### The Three Bottlenecks

1. **Memory** — LLMs are large. A 7B parameter model in fp16 requires ~14GB just for weights. The KV-cache adds significant memory overhead that scales with sequence length and batch size.

2. **Compute** — Each token generation requires a full forward pass through the model. Autoregressive generation is inherently sequential for a single request.

3. **Latency** — Users expect fast responses. The time to first token (TTFT) and sustained tokens-per-second (TPS) both matter for user experience.

The fundamental challenge: GPUs are optimized for parallel compute, but autoregressive generation is sequential. The key insight is to batch multiple requests to keep the GPU saturated.

### Memory Breakdown for Inference

For a 7B model serving a batch of 16 requests at 2048 sequence length:

| Component | Memory (fp16) |
|-----------|--------------|
| Model weights | ~14 GB |
| KV-cache | ~8-16 GB |
| Activations | ~1-2 GB |
| CUDA overhead | ~1-2 GB |
| **Total** | **~24-34 GB** |

The KV-cache is often the largest variable component and the primary target for optimization.

## KV-Cache and Its Memory Footprint

### What Is the KV-Cache?

During autoregressive generation, the attention mechanism recomputes attention over all previous tokens. The KV-cache stores the key and value tensors from previous tokens so they don't need to be recomputed.

For each layer l, at position t:
- K_cache[l][t] = K projection of token t
- V_cache[l][t] = V projection of token t

### Memory Formula

```
KV-cache memory = 2 × n_layers × n_heads × head_dim × seq_len × batch_size × dtype_size
```

For Llama-2-7B (32 layers, 32 heads, 128 head_dim) with fp16:
- Per token per request: 2 × 32 × 32 × 128 × 2 bytes = 512 KB
- For 2048 tokens: ~1 GB per request
- For batch of 16: ~16 GB just for KV-cache

### The Fragmentation Problem

Traditional KV-cache allocation pre-allocates a contiguous block for each request at maximum sequence length. This leads to:
- **Internal fragmentation** — Short sequences waste their allocated memory
- **External fragmentation** — Memory becomes fragmented as requests complete at different times
- Typical memory utilization: 20-40% of allocated KV-cache is wasted

## PagedAttention (vLLM's Innovation)

### Core Idea

Inspired by virtual memory in operating systems, PagedAttention divides the KV-cache into fixed-size **blocks** (pages) instead of contiguous allocations.

- Each block holds KV vectors for a fixed number of tokens (e.g., 16)
- Blocks are allocated on demand as tokens are generated
- A block table maps logical positions to physical blocks (like a page table)
- Blocks can be non-contiguous in GPU memory

### Benefits

- **Near-zero waste** — Only the last block may have unused slots
- **Memory sharing** — Common prefixes (system prompts) share physical blocks via copy-on-write
- **Higher throughput** — More requests fit in memory simultaneously
- Typical improvement: 2-4x higher throughput vs naive implementations

### Preemption

When memory is exhausted, vLLM can preempt (evict) lower-priority requests:
- **Swap** — Move KV-cache blocks to CPU memory
- **Recompute** — Discard blocks and recompute them when the request resumes

## Continuous Batching vs Static Batching

### Static Batching

Wait for a full batch, process all requests together, wait for all to finish. Problems:
- Short requests must wait for long ones to finish
- GPU is idle while waiting to fill a batch
- Throughput is limited by the slowest request in the batch

### Continuous Batching (Iteration-Level Scheduling)

Process requests at the iteration (token) level:
- New requests can join the batch at any iteration
- Completed requests leave immediately, freeing their slot
- The batch is always as full as possible

This maximizes GPU utilization and reduces latency for short requests.

### vLLM's Scheduler

vLLM implements continuous batching with:
1. **Waiting queue** — Incoming requests
2. **Running batch** — Currently generating tokens
3. **Swap queue** — Preempted requests waiting to resume

At each iteration, the scheduler decides which requests to admit, continue, or preempt based on available memory.

## Quantization Methods

### GPTQ (GPT Quantization)

- **Type**: Post-training quantization (PTQ)
- **Precision**: Typically 4-bit or 3-bit
- **Method**: Layer-by-layer quantization minimizing reconstruction error using a calibration dataset
- **Pros**: Good quality, well-supported by vLLM
- **Cons**: Requires calibration data, slow quantization process (hours)
- **Speed**: Fast inference with optimized CUDA kernels (ExLlama, Marlin)

### AWQ (Activation-Aware Weight Quantization)

- **Type**: Post-training quantization
- **Precision**: 4-bit
- **Method**: Identifies salient weight channels by analyzing activation distributions, preserves important weights at higher precision
- **Pros**: Often higher quality than GPTQ, faster quantization
- **Cons**: Slightly newer ecosystem
- **Speed**: Competitive with GPTQ, especially with Marlin kernels

### GGUF (GPT-Generated Unified Format)

- **Type**: Post-training quantization
- **Precision**: 2-bit to 8-bit, with mixed-precision variants (Q4_K_M, Q5_K_S, etc.)
- **Method**: k-quant methods with per-block quantization and importance-based mixed precision
- **Pros**: CPU-friendly, very flexible precision options, great for edge deployment
- **Cons**: Primarily designed for llama.cpp, less optimized for GPU-only serving
- **Speed**: Excellent on CPU, good on GPU with recent improvements

### Quantization Quality Comparison

| Method | Perplexity Increase | Memory Savings | Inference Speed |
|--------|-------------------|----------------|-----------------|
| fp16 (baseline) | 0% | 0% | 1.0x |
| GPTQ-4bit | 1-3% | ~75% | 1.5-2.5x |
| AWQ-4bit | 0.5-2% | ~75% | 1.5-2.5x |
| GGUF Q4_K_M | 1-2% | ~75% | 1.3-2.0x |
| GPTQ-3bit | 3-8% | ~81% | 1.5-2.0x |

## Parallelism Strategies

### Tensor Parallelism (TP)

Split individual layers across multiple GPUs. Each GPU holds a shard of each weight matrix and computes its portion of the output. Requires all-reduce communication between GPUs at each layer.

- **Best for**: Low-latency, single-node, NVLink-connected GPUs
- **Overhead**: Requires fast inter-GPU communication
- **Example**: TP=2 on 2×A100 halves per-GPU memory, adds ~10% overhead

### Pipeline Parallelism (PP)

Assign entire layers to different GPUs. GPU 0 runs layers 0-15, GPU 1 runs layers 16-31. Requires passing activations between GPUs only at the boundary.

- **Best for**: Multi-node setups, slower interconnects
- **Overhead**: Pipeline bubbles reduce efficiency
- **Example**: PP=2 on 2 nodes with separate GPU pools

### When to Use Which

- Single GPU: No parallelism needed
- 2-4 GPUs with NVLink: Tensor parallelism
- Multi-node: Pipeline parallelism (or hybrid TP+PP)

## Speculative Decoding

### Core Idea

Use a small, fast "draft" model to generate N candidate tokens, then verify all N in a single forward pass of the large "target" model. If the draft model is often correct, this amortizes the cost of the large model across multiple tokens.

- **Draft model**: 2-3x smaller than target (e.g., 1B for a 7B target)
- **Typical speedup**: 1.5-2.5x for well-matched draft/target pairs
- **Guarantee**: Output distribution is mathematically identical to the target model

### Trade-offs

- Requires a well-matched draft model
- Speedup depends on the draft model's acceptance rate
- Adds complexity to the serving pipeline

## FlashAttention

### Problem

Standard attention computes Q·K^T (an N×N matrix), stores it in HBM, applies softmax, then multiplies by V. This requires O(N²) HBM reads/writes.

### Solution

FlashAttention fuses the attention computation into a single kernel that:
1. Tiles the computation to fit in SRAM (on-chip memory)
2. Never materializes the full N×N attention matrix in HBM
3. Uses online softmax to avoid the two-pass problem

Result: 2-4x speedup and significant memory savings. vLLM uses FlashAttention by default.

## Key Metrics

### Time to First Token (TTFT)

The latency from receiving the request to generating the first output token. Includes:
- Prompt processing (prefill phase)
- Scheduling overhead
- KV-cache allocation

For interactive applications, TTFT < 500ms is ideal.

### Tokens Per Second (TPS)

The rate of token generation during the decode phase. Measured per-request (how fast one response generates) or system-wide (total tokens across all concurrent requests).

- Per-request TPS: 30-60 TPS is typical for a 7B model on A100
- System throughput: 500-2000 TPS depending on batch size and model

### Throughput

Total requests completed per unit time. Depends on:
- Batch size (more concurrent requests = higher throughput)
- Sequence length (longer sequences = fewer concurrent requests)
- Model size and quantization

### Queue Depth

Number of requests waiting in the queue. Indicates whether the server is keeping up with demand. A growing queue suggests the server is overloaded.

## vLLM vs TGI vs Triton

| Feature | vLLM | TGI (HuggingFace) | Triton (NVIDIA) |
|---------|------|--------------------|-----------------|
| PagedAttention | Yes (inventor) | Yes (adopted) | Via backend |
| Continuous batching | Yes | Yes | Yes |
| OpenAI-compatible API | Yes | Yes | Via extension |
| Quantization | GPTQ, AWQ, FP8 | GPTQ, AWQ, EETQ | All via backends |
| Tensor parallelism | Yes | Yes | Yes |
| Speculative decoding | Yes | No | Via backend |
| Ease of use | High | High | Medium |
| Customizability | Medium | Low | High |
| Multi-model serving | Limited | No | Yes |

## Serving Optimization Strategies

1. **Right-size the model** — Use the smallest model that meets quality requirements
2. **Quantize** — 4-bit quantization gives ~75% memory savings with minimal quality loss
3. **Tune batch size** — Larger batches = higher throughput but higher latency
4. **Set appropriate max_model_len** — Don't allocate KV-cache for sequences longer than needed
5. **Use tensor parallelism** — Spread across GPUs for lower latency
6. **Enable prefix caching** — Share KV-cache for common system prompts
7. **Monitor and alert** — Track TTFT, TPS, and queue depth in production

## GPU Memory Management

### gpu_memory_utilization

vLLM's key parameter. Controls what fraction of GPU memory is available for KV-cache (after model weights are loaded).

- `0.9` (default): Use 90% of remaining GPU memory for KV-cache
- `0.8`: More conservative, leaves headroom for spikes
- `0.95`: Aggressive, maximizes concurrent requests

### Memory Allocation Flow

1. Load model weights → fixed memory
2. Allocate KV-cache blocks → gpu_memory_utilization × remaining memory
3. Scheduler assigns blocks to requests as needed
4. Completed requests release their blocks

## Key Terminology

- **TTFT** — Time to First Token: latency until the first generated token
- **TPS** — Tokens Per Second: generation speed
- **KV-cache** — Cached key/value tensors from attention to avoid recomputation
- **PagedAttention** — vLLM's block-based KV-cache management system
- **Continuous batching** — Adding/removing requests at every generation step
- **Prefill** — The initial phase where the prompt is processed
- **Decode** — The autoregressive phase where tokens are generated one by one
- **Quantization** — Reducing model weight precision to save memory and speed up inference
- **Tensor parallelism** — Splitting layers across GPUs
- **Speculative decoding** — Using a small draft model to speed up generation
- **FlashAttention** — Fused attention kernel that avoids materializing the attention matrix
- **SSE** — Server-Sent Events: protocol for streaming server-to-client messages
