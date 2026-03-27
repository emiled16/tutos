# Distributed ML Platform with Ray

## Overview

Build a production-grade distributed machine learning system using [Ray](https://www.ray.io/), covering the full ML lifecycle: hyperparameter tuning with Ray Tune, distributed training with Ray Train, and scalable model serving with Ray Serve. The project emphasizes proper resource management, fault tolerance, and autoscaling across a Ray cluster.

## Learning Objectives

- Understand Ray's architecture: Global Control Store (GCS), raylets, distributed object store
- Distinguish between Ray tasks and actors and know when to use each
- Build distributed data pipelines with Ray Data
- Configure and run hyperparameter searches with Ray Tune (ASHA, PBT, HyperBand schedulers)
- Implement data-parallel distributed training with Ray Train
- Deploy and compose models behind Ray Serve with autoscaling
- Monitor cluster health via the Ray Dashboard and custom metrics
- Manage CPU, GPU, and custom resources across heterogeneous nodes

## Project Description

The system processes a tabular or image dataset through three stages:

1. **Data Ingestion & Preprocessing** — Ray Data loads and transforms data in a streaming, distributed fashion.
2. **Hyperparameter Tuning** — Ray Tune explores a search space using configurable search algorithms and early-stopping schedulers.
3. **Distributed Training** — Ray Train scales the best configuration across workers with data parallelism.
4. **Model Serving** — Ray Serve deploys the trained model (or an ensemble) behind an HTTP endpoint with autoscaling.

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                    Ray Cluster                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Ray Data │→ │ Ray Tune │→ │   Ray Train      │   │
│  │ pipeline │  │ (ASHA /  │  │ (data parallel)  │   │
│  └──────────┘  │  PBT)    │  └────────┬─────────┘   │
│                └──────────┘           │              │
│                                       ▼              │
│                              ┌────────────────┐      │
│                              │   Ray Serve    │      │
│                              │  (ensemble /   │      │
│                              │   autoscale)   │      │
│                              └────────────────┘      │
│                                                      │
│  ┌──────────────────────────────────────────────┐    │
│  │           Monitoring & Dashboard             │    │
│  └──────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────┘
```

## Implementation Tasks

### Stage 1 — Cluster & Data

- [ ] Configure Ray cluster initialization with resource limits (`cluster/config.py`)
- [ ] Build a Ray Data pipeline for loading, splitting, and transforming data (`data/dataset.py`)
- [ ] Implement preprocessing actors for stateful transforms (`data/preprocessing.py`)

### Stage 2 — Hyperparameter Tuning

- [ ] Define search spaces with continuous, discrete, and conditional parameters (`tune/search_space.py`)
- [ ] Write a trainable function that reports metrics to Tune (`tune/trainable.py`)
- [ ] Configure ASHA, PBT, and HyperBand schedulers (`tune/scheduler.py`)
- [ ] Wire everything into a `Tuner` and run experiments (`tune/tuner.py`)

### Stage 3 — Distributed Training

- [ ] Scale the best trial to multi-worker data-parallel training (`train/trainer.py`)
- [ ] Add checkpointing and metric-logging callbacks (`train/callbacks.py`)

### Stage 4 — Serving

- [ ] Create a Ray Serve deployment for the trained model (`serve/deployment.py`)
- [ ] Build an ensemble router that composes multiple deployments (`serve/router.py`)
- [ ] Configure autoscaling policies (`serve/autoscaling.py`)

### Stage 5 — Monitoring

- [ ] Expose custom Prometheus metrics and integrate with the Ray Dashboard (`monitoring/dashboard.py`)

## Evaluation Criteria

| Area | What to demonstrate |
|---|---|
| **Correctness** | Tune finds improving configs; Train converges; Serve returns predictions |
| **Scalability** | Pipeline works on 1 node and scales to N without code changes |
| **Resource management** | CPU/GPU requests match availability; no OOM or resource starvation |
| **Fault tolerance** | Training recovers from a killed worker; Serve replicas restart |
| **Code quality** | Type hints, docstrings, dataclass models, clean separation of concerns |

## Resources

- [Ray Documentation](https://docs.ray.io/en/latest/)
- [Ray Tune Guide](https://docs.ray.io/en/latest/tune/index.html)
- [Ray Train Guide](https://docs.ray.io/en/latest/train/train.html)
- [Ray Serve Guide](https://docs.ray.io/en/latest/serve/index.html)
- [Ray Architecture Whitepaper](https://docs.ray.io/en/latest/ray-contribute/whitepaper.html)
- [Anyscale Academy](https://github.com/anyscale/academy)
