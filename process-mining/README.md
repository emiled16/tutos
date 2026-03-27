# Process Discovery & Conformance Engine

A process mining pipeline that discovers process models from event logs, performs conformance checking, identifies bottlenecks, and generates actionable insights.

## Overview

Process mining bridges data science and business process management. It uses event logs from operational systems (ERP, CRM, ticketing, hospital information systems) to reconstruct how processes actually execute, compare them against intended models, and surface optimization opportunities.

This project implements the three pillars of process mining from scratch:

- **Discovery** — Extract a process model (Petri net, DFG, BPMN) from raw event logs
- **Conformance Checking** — Compare observed behavior against a normative model to find deviations
- **Enhancement** — Enrich discovered models with performance data to find bottlenecks and resource patterns

## Learning Objectives

- Understand event log structure (case ID, activity, timestamp, resource) and the XES standard
- Implement three process discovery algorithms: Alpha Miner, Heuristics Miner, Inductive Miner
- Model processes using Petri nets (places, transitions, markings, firing semantics) and BPMN
- Build and interpret Directly-Follows Graphs (DFGs) with frequency and performance annotations
- Perform conformance checking via token-based replay and alignment-based techniques (A* search)
- Analyze process bottlenecks (waiting time vs service time, critical path identification)
- Mine social networks from event logs (handover-of-work, working-together patterns)
- Visualize process models with Graphviz, color-coded by frequency or performance metrics
- Generate synthetic event logs with configurable process patterns for testing

## Project Description

Given event logs in CSV or XES format, the engine:

1. Parses and normalizes events into a structured `EventLog` with case-level trace grouping
2. Discovers a process model using one of three algorithms (Alpha, Heuristics, or Inductive Miner)
3. Checks conformance of the log against a model using token replay or optimal alignments
4. Enhances the model with timing data to identify bottlenecks, slow transitions, and resource contention
5. Produces visualizations (DFG, Petri net, BPMN) and summary dashboards with process KPIs

## Architecture

```
src/process_mining/
├── event_log.py                  # EventLog class — parsing, filtering, statistics
├── models/
│   ├── petri_net.py              # Petri net — places, transitions, arcs, markings
│   ├── dfg.py                    # Directly-Follows Graph — frequency/performance
│   └── bpmn.py                   # BPMN model representation
├── discovery/
│   ├── alpha_miner.py            # Alpha Miner algorithm
│   ├── heuristics_miner.py       # Heuristics Miner (noise-tolerant)
│   └── inductive_miner.py        # Inductive Miner (guarantees soundness)
├── conformance/
│   ├── token_replay.py           # Token-based replay fitness
│   └── alignment.py              # Alignment-based conformance (A* search)
├── enhancement/
│   ├── bottleneck.py             # Bottleneck & performance analysis
│   └── social_network.py         # Social network mining from logs
├── visualization/
│   ├── graph_renderer.py         # Graphviz rendering for DFG & Petri nets
│   └── dashboard.py              # Summary statistics & process KPIs
└── data/
    ├── log_generator.py          # Synthetic event log generation
    └── xes_parser.py             # XES format parser

tests/
├── test_event_log.py             # Event log parsing & statistics
├── test_alpha_miner.py           # Alpha Miner discovery correctness
├── test_conformance.py           # Token replay & alignment tests
├── test_dfg.py                   # DFG construction & filtering
└── test_bottleneck.py            # Bottleneck analysis tests
```

## Implementation Tasks

### Phase 1: Data Foundation

- [ ] Implement `EventLog` class with CSV and XES parsing
- [ ] Implement XES parser (`xes_parser.py`) using lxml
- [ ] Implement log filtering (by time window, activity, resource)
- [ ] Compute basic log statistics (case count, variant distribution, activity frequencies)
- [ ] Build synthetic log generator with configurable patterns

### Phase 2: Process Models

- [ ] Implement `PetriNet` class (places, transitions, arcs, markings, firing)
- [ ] Implement `DirectlyFollowsGraph` with frequency and performance edges
- [ ] Implement `BPMNModel` with conversion from Petri net
- [ ] Add Graphviz visualization for Petri nets and DFGs

### Phase 3: Discovery Algorithms

- [ ] Implement Alpha Miner (directly-follows → causality → parallel → choice → places)
- [ ] Implement Heuristics Miner with dependency measure and noise thresholds
- [ ] Implement Inductive Miner with cut detection (sequence, exclusive, parallel, loop)

### Phase 4: Conformance Checking

- [ ] Implement token-based replay with fitness scoring
- [ ] Implement alignment-based conformance using A* search
- [ ] Compare fitness, precision, and generalization across methods

### Phase 5: Enhancement & Insights

- [ ] Implement bottleneck analysis (waiting time, service time, critical path)
- [ ] Implement social network mining (handover-of-work, working-together, subcontracting)
- [ ] Build dashboard with throughput time, case duration distribution, activity frequencies
- [ ] Color-code visualizations by performance metrics

### Phase 6: Integration & Polish

- [ ] End-to-end pipeline: load log → discover → check conformance → enhance → visualize
- [ ] Test with realistic synthetic logs (sequences, choices, parallelism, loops, noise)
- [ ] Document findings and compare algorithm trade-offs

## Evaluation Criteria

- **Correctness**: Alpha Miner produces valid Petri nets for known process patterns (sequences, XOR splits, AND splits)
- **Conformance accuracy**: Token replay and alignment produce consistent fitness scores; perfectly fitting logs score 1.0
- **Noise tolerance**: Heuristics Miner and Inductive Miner handle noisy logs gracefully where Alpha Miner fails
- **Performance insights**: Bottleneck analysis correctly identifies the slowest activities and transitions
- **Visualization clarity**: Generated graphs are readable, properly labeled, and color-coded
- **Code quality**: Clean separation of concerns, comprehensive type hints, well-structured Pydantic models

## Resources

- [Process Mining: Data Science in Action](https://www.springer.com/gp/book/9783662498507) — Wil van der Aalst (the foundational textbook)
- [pm4py Documentation](https://pm4py.fit.fraunhofer.de/) — Reference Python library for process mining
- [IEEE XES Standard](https://xes-standard.org/) — Event log interchange format
- [Alpha Miner Algorithm](https://en.wikipedia.org/wiki/Alpha_algorithm) — Wikipedia overview
- [Conformance Checking and Diagnosis in Process Mining](https://link.springer.com/book/10.1007/978-3-319-49451-7) — Carmona et al.
- [Process Mining Manifesto](https://www.win.tue.nl/ieeetfpm/doku.php?id=shared:process_mining_manifesto) — IEEE Task Force on Process Mining
- [Graphviz Python Bindings](https://graphviz.readthedocs.io/) — Graph visualization library
