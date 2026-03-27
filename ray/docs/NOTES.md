# Distributed ML Platform — Theory Notes

## 1. Distributed Computing Fundamentals

Distributed computing splits work across multiple networked machines (or cores) to achieve parallelism, fault tolerance, and scalability. Key concerns:

- **Data partitioning** — how data is split and moved between workers.
- **Communication overhead** — serialization, network latency, collective operations (all-reduce, broadcast).
- **Consistency models** — strong vs. eventual consistency of shared state.
- **Fault tolerance** — detecting failures, re-executing lost work, checkpointing.
- **Scheduling** — assigning tasks to workers with heterogeneous resources.

### CAP Theorem (quick refresher)

In a distributed system you can guarantee at most two of: **Consistency**, **Availability**, **Partition tolerance**. Ray favors availability and partition tolerance for tasks, while the GCS provides linearizable metadata.

---

## 2. Ray Architecture

Ray is a general-purpose distributed computing framework built around three pillars: **tasks**, **actors**, and **objects**.

### 2.1 Global Control Store (GCS)

The GCS is a centralized (optionally HA) metadata service that tracks:

- Node membership and heartbeats
- Actor locations and ownership
- Placement group state
- Job metadata

In production the GCS is backed by Redis (or an internal KV store in newer versions). The head node runs the GCS; worker nodes contact it to register and discover actors.

### 2.2 Raylet

Every node runs a **raylet** — a shared-memory daemon consisting of:

- **Node manager** — communicates with the GCS, manages local workers, enforces resource limits.
- **Object manager** — handles object transfers between nodes via gRPC.

The raylet is the local scheduler: it decides whether a task runs locally or must be forwarded to another node based on resource availability.

### 2.3 Object Store (Plasma)

Each node has an in-process **object store** (based on Apache Arrow / Plasma):

- Objects are immutable, reference-counted, and zero-copy within a node.
- Cross-node transfers are pull-based: a worker requests an object, and the object manager fetches it.
- Large objects are spilled to disk when memory pressure is high.

### 2.4 Workers and Drivers

- **Driver** — the process that calls `ray.init()` and submits tasks.
- **Worker** — a process (Python or Java) that executes tasks/actors. Workers are pre-forked or started on demand.

---

## 3. Tasks vs. Actors

| | Tasks | Actors |
|---|---|---|
| **State** | Stateless | Stateful (instance persists across calls) |
| **Invocation** | `remote_fn.remote()` → returns `ObjectRef` | `ActorClass.remote()` → handle; then `handle.method.remote()` |
| **Scheduling** | Can run on any node with resources | Pinned to the node where created |
| **Fault tolerance** | Automatic retry (configurable `max_retries`) | Restart via `max_restarts`; callers see `RayActorError` |
| **Use when** | Pure functions, embarrassingly parallel work | Maintaining state (model weights, DB connections, counters) |

### Anti-patterns

- Passing large objects as task arguments instead of using `ray.put()` and passing `ObjectRef`s.
- Creating thousands of actors when stateless tasks suffice — each actor consumes a worker slot.

---

## 4. Object References and the Object Store

```python
ref: ray.ObjectRef = ray.put(large_array)   # pin in object store
result = ray.get(ref)                        # block and fetch
ready, not_ready = ray.wait(refs, num_returns=1)  # non-blocking poll
```

Key semantics:

- `ray.put()` serializes once; passing the `ObjectRef` to multiple tasks avoids re-serialization.
- `ray.get()` blocks the caller; prefer `ray.wait()` for pipelining.
- Objects are automatically reference-counted and evicted when no references remain.
- **Spilling**: when the object store is full, least-recently-used objects spill to local disk (configurable).

---

## 5. Ray Data (batch processing)

Ray Data (`ray.data.Dataset`) provides streaming, distributed data pipelines:

```python
ds = ray.data.read_parquet("s3://bucket/data/")
ds = ds.map_batches(preprocess, batch_size=256)
ds = ds.random_shuffle()
```

Features:

- **Streaming execution** — operators are pipelined to reduce memory footprint.
- **Heterogeneous compute** — `.map_batches()` accepts `num_gpus` to run on GPU workers.
- **Integration** — direct conversion to/from Torch DataLoaders, TF datasets, Pandas.
- **Fault tolerance** — lineage-based recomputation of lost blocks.

### When to use Ray Data vs. a plain DataLoader

Use Ray Data when preprocessing is CPU-heavy and you want to overlap it with GPU training, or when data exceeds single-node memory.

---

## 6. Ray Tune

Ray Tune is a hyperparameter optimization library that orchestrates **trials** (individual training runs) across a cluster.

### 6.1 Search Algorithms

| Algorithm | Type | Notes |
|---|---|---|
| **Random search** | Uninformed | Good baseline; embarrassingly parallel |
| **Grid search** | Uninformed | Exhaustive; combinatorial explosion in high dimensions |
| **Bayesian optimization** (e.g., `BayesOptSearch`) | Model-based | Builds a surrogate (GP or TPE); sample-efficient but sequential |
| **Optuna** (`OptunaSearch`) | Model-based | TPE + pruning integration |
| **HyperOpt** (`HyperOptSearch`) | Model-based | TPE; well-established |

### 6.2 Schedulers (early stopping)

Schedulers decide whether to **continue**, **pause**, or **stop** a trial based on intermediate metrics.

#### ASHA (Async Successive Halving Algorithm)

- Asynchronous: does not wait for a full rung before promoting.
- Aggressively kills low-performing trials early.
- Parameters: `max_t` (max training iterations), `grace_period` (min iterations before stopping), `reduction_factor`.
- Best for large-scale searches where you can afford to discard trials early.

#### PBT (Population-Based Training)

- Maintains a **population** of trials running in parallel.
- Periodically **exploits** (copies weights from a better trial) and **explores** (perturbs hyperparameters).
- Discovers schedules, not just point configs (e.g., learning rate warm-up → decay emerges naturally).
- Parameters: `perturbation_interval`, `hyperparam_mutations`.
- Requires checkpointing support in the trainable.

#### HyperBand

- Synchronous bracket-based successive halving.
- Runs multiple brackets with different resource-vs-trial trade-offs.
- More principled than ASHA when synchronous execution is acceptable.

### 6.3 Putting it together

```python
from ray import tune
from ray.tune.schedulers import ASHAScheduler

tuner = tune.Tuner(
    trainable,
    param_space=search_space,
    tune_config=tune.TuneConfig(
        metric="val_loss",
        mode="min",
        scheduler=ASHAScheduler(max_t=100, grace_period=10),
        num_samples=50,
    ),
)
results = tuner.fit()
best = results.get_best_result()
```

---

## 7. Ray Train

Ray Train provides distributed training primitives, primarily **data parallelism**.

### 7.1 Data Parallelism

Each worker holds a full model replica and processes a shard of the data. Gradients are synchronized via **all-reduce** (ring or tree).

```
Worker 0: data shard 0 → forward → backward → all-reduce ─┐
Worker 1: data shard 1 → forward → backward → all-reduce ─┤→ averaged gradients → step
Worker 2: data shard 2 → forward → backward → all-reduce ─┘
```

Ray Train wraps PyTorch DDP / DeepSpeed / FSDP:

```python
from ray.train.torch import TorchTrainer

trainer = TorchTrainer(
    train_loop_per_worker,
    scaling_config=ScalingConfig(num_workers=4, use_gpu=True),
)
result = trainer.fit()
```

### 7.2 Model Parallelism

Splits a single model across devices when it doesn't fit in one GPU's memory. Techniques:

- **Pipeline parallelism** — layers assigned to different GPUs; micro-batches pipelined.
- **Tensor parallelism** — individual layers (e.g., large linear) sharded across GPUs.
- Ray Train integrates with DeepSpeed ZeRO and PyTorch FSDP for memory-efficient training.

### 7.3 Checkpointing

Ray Train's `Checkpoint` API stores model state, optimizer state, and epoch number. Checkpoints can be stored on shared storage (NFS, S3) for fault recovery.

---

## 8. Ray Serve

Ray Serve is a scalable model-serving framework built on top of Ray actors.

### 8.1 Deployments

A **deployment** is a group of replicas (actors) behind a load balancer:

```python
@serve.deployment(num_replicas=2)
class ModelDeployment:
    def __init__(self):
        self.model = load_model()

    async def __call__(self, request):
        return self.model.predict(request.json())
```

### 8.2 Handles and Composition

Deployments can call other deployments via **handles**, enabling:

- **Ensemble** — route a request to multiple models, aggregate predictions.
- **Pipeline** — chain preprocessor → model → postprocessor deployments.

```python
@serve.deployment
class Ensemble:
    def __init__(self, model_a, model_b):
        self.a = model_a
        self.b = model_b

    async def __call__(self, request):
        a_pred, b_pred = await asyncio.gather(
            self.a.predict.remote(request),
            self.b.predict.remote(request),
        )
        return combine(a_pred, b_pred)
```

### 8.3 Autoscaling

Ray Serve autoscales replicas based on request load:

- `min_replicas`, `max_replicas` — bounds.
- `target_ongoing_requests` — the controller adds replicas when the queue exceeds this.
- `downscale_delay_s` — how long to wait before removing idle replicas.

---

## 9. Autoscaling (cluster-level)

Ray's autoscaler adds/removes **nodes** from the cluster:

- Monitors pending resource requests vs. available resources.
- Launches new nodes from a cloud provider (AWS, GCP, Azure) or Kubernetes.
- Configured via `cluster.yaml` or KubeRay `RayCluster` CRD.
- `idle_timeout_minutes` controls when idle nodes are terminated.

---

## 10. Fault Tolerance

| Component | Mechanism |
|---|---|
| **Tasks** | Automatic retry up to `max_retries` (default 3). Lineage-based re-execution. |
| **Actors** | `max_restarts` to restart the actor process; `max_task_retries` for pending calls. Callers receive `RayActorError` if unrecoverable. |
| **Object store** | Lineage reconstruction or disk spilling. Pinned objects survive worker crashes. |
| **GCS** | HA mode: GCS state persisted to external Redis; a standby head node takes over. |
| **Ray Train** | Worker failure triggers checkpoint restore and training restart on remaining/new workers. |
| **Ray Serve** | Failed replicas are restarted automatically; in-flight requests are retried if idempotent. |

---

## 11. Resource Management

### CPUs and GPUs

```python
@ray.remote(num_cpus=2, num_gpus=1)
def train_step(batch):
    ...
```

Resources are **logical** labels used for scheduling — Ray does not enforce actual CPU affinity or GPU isolation (use `CUDA_VISIBLE_DEVICES` env var for GPU isolation, which Ray sets automatically).

### Custom Resources

```python
ray.init(resources={"special_hardware": 2})

@ray.remote(resources={"special_hardware": 1})
def use_special():
    ...
```

### Placement Groups

Bundle resource requests to ensure co-location:

```python
from ray.util.placement_group import placement_group

pg = placement_group([{"CPU": 4, "GPU": 1}] * 2, strategy="PACK")
ray.get(pg.ready())
```

Strategies: `PACK` (same node if possible), `SPREAD` (distribute), `STRICT_PACK`, `STRICT_SPREAD`.

---

## 12. Ray vs. Dask vs. Spark

| Dimension | Ray | Dask | Spark |
|---|---|---|---|
| **Primary abstraction** | Tasks, actors, objects | Delayed computations, futures, collections | RDDs, DataFrames |
| **Language** | Python-first (Java, C++ core) | Python | Scala/Java/Python/R |
| **State** | First-class actors | Limited (worker plugins) | Accumulators, broadcast vars |
| **ML ecosystem** | Tune, Train, Serve, RLlib | dask-ml, integrations | MLlib, third-party |
| **Streaming** | Ray Serve, Ray Data streaming | Dask Streams (experimental) | Structured Streaming |
| **Scheduling** | Distributed, bottom-up | Centralized scheduler | DAG-based (driver) |
| **GPU support** | Native (`num_gpus`) | Manual | Rapids (GPU DataFrames) |
| **Best for** | ML workloads, RL, serving, heterogeneous compute | Scaling NumPy/Pandas workflows | ETL, SQL analytics, batch |

### When to choose Ray

- You need **actors** (stateful services, RL environments, parameter servers).
- You want a unified framework for training **and** serving.
- Your workload mixes CPU preprocessing with GPU training.
- You need fine-grained, dynamic task graphs (not just DAGs).

### When to choose Dask

- Your workload is mostly Pandas/NumPy and you want a familiar API.
- You need a drop-in distributed DataFrame.

### When to choose Spark

- You have large-scale ETL / SQL workloads.
- Your organization already has Spark infrastructure.
- You need mature exactly-once streaming guarantees.
