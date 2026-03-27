# Process Mining — Theory & Notes

## What Is Process Mining?

Process mining is a family of techniques that extract knowledge from event logs recorded by information systems. Unlike classical data mining (which focuses on patterns in static datasets), process mining focuses on *processes* — ordered sequences of activities that together accomplish a business goal.

Every time a case (patient visit, purchase order, support ticket) progresses through a system, it leaves behind a trail of events. Process mining reconstructs, analyzes, and improves processes from these trails.

### The Three Types

| Type | Question | Input | Output |
|------|----------|-------|--------|
| **Discovery** | What process is actually being followed? | Event log | Process model |
| **Conformance** | Does reality match the intended process? | Event log + reference model | Diagnostics (deviations, fitness) |
| **Enhancement** | Where can we improve? | Event log + model | Enriched model (bottlenecks, KPIs) |

## Core Concepts

### Event Logs

An event log is a collection of *events*, each belonging to a *case* (process instance). The minimum required attributes are:

- **Case ID** — Identifier grouping events into a single process instance (e.g., order number, patient ID)
- **Activity** — The action performed (e.g., "Register Request", "Approve Payment")
- **Timestamp** — When the event occurred (enables ordering and duration calculation)

Common optional attributes:

- **Resource** — Who or what performed the activity (person, department, system)
- **Lifecycle transition** — Start, complete, suspend, resume (for measuring service time vs waiting time)
- **Cost, priority, data payloads** — Domain-specific attributes

A **trace** is the ordered sequence of activities for a single case. A **variant** is a distinct trace pattern — if 100 cases follow the path A→B→C→D and 50 follow A→C→B→D, there are two variants.

### The XES Standard

XES (eXtensible Event Stream) is the IEEE standard format for event logs (IEEE 1849-2016). Structure:

```xml
<log>
  <trace>                              <!-- One per case -->
    <string key="concept:name" value="Case_1"/>
    <event>                            <!-- One per event -->
      <string key="concept:name" value="Register"/>
      <date key="time:timestamp" value="2024-01-15T09:30:00"/>
      <string key="org:resource" value="Alice"/>
    </event>
    <!-- more events -->
  </trace>
  <!-- more traces -->
</log>
```

Key XES extensions: `concept` (names), `time` (timestamps), `org` (organizational), `lifecycle` (transitions).

## Process Models

### Petri Nets

A Petri net is a bipartite directed graph with two types of nodes:

- **Places** (circles) — Represent conditions or states
- **Transitions** (rectangles) — Represent activities or events
- **Arcs** — Connect places to transitions and transitions to places (never place-to-place or transition-to-transition)

A **marking** assigns tokens to places, representing the current state. A transition is **enabled** when all its input places have at least one token. **Firing** a transition removes one token from each input place and adds one token to each output place.

**Initial marking**: tokens in the start place(s). **Final marking**: tokens in the end place(s).

**Soundness properties** for workflow nets:
1. For every reachable marking, there exists a firing sequence leading to the final marking (proper completion)
2. The final marking is the only marking reachable with a token in the final place (no dangling tokens)
3. Every transition can be fired in at least one reachable marking (no dead transitions)

### BPMN (Business Process Model and Notation)

A visual standard for modeling business processes. Key elements:

- **Start/End events** (circles) — Where the process begins and ends
- **Tasks** (rounded rectangles) — Activities to perform
- **Exclusive gateways** (X diamond) — XOR split/join — exactly one path
- **Parallel gateways** (+ diamond) — AND split/join — all paths concurrently
- **Inclusive gateways** (O diamond) — OR split/join — one or more paths

### Process Trees

A hierarchical representation used by the Inductive Miner. Operators:

- **→ (sequence)**: Execute children left to right
- **× (exclusive choice)**: Execute exactly one child
- **∧ (parallel)**: Execute all children concurrently (any interleaving)
- **↺ (loop)**: Execute first child, then optionally second child (redo), repeat

Process trees always produce sound models (unlike arbitrary Petri nets).

## Directly-Follows Graphs (DFG)

A DFG captures which activities directly follow which other activities in the log.

**Construction**: For each consecutive pair of events (a, b) within a case, increment the edge count a→b.

**Frequency DFG**: Edge weight = how many times a is directly followed by b across all cases.

**Performance DFG**: Edge weight = average (or median, min, max) time between a and b.

**Filtering**: Remove edges below a frequency threshold to simplify complex graphs.

**Limitations**: DFGs cannot distinguish between concurrency and choice. If activities B and C both follow A and both precede D, a DFG shows the same structure whether B and C happen in parallel (AND) or as alternatives (XOR). This is why DFGs are useful for exploration but insufficient as formal process models.

## Discovery Algorithms

### Alpha Miner

The Alpha Miner discovers a Petri net from an event log through four ordering relations:

1. **Directly-follows (>)**: `a > b` iff there exists a trace where a is directly followed by b
2. **Causality (→)**: `a → b` iff `a > b` and NOT `b > a`
3. **Parallel (||)**: `a || b` iff `a > b` AND `b > a`
4. **Choice (#)**: `a # b` iff NOT `a > b` AND NOT `b > a`

**Algorithm steps**:
1. Compute the set of all activities T_L
2. Compute the set of start activities T_I (first activity in each trace)
3. Compute the set of end activities T_O (last activity in each trace)
4. Compute all ordering relations between activity pairs
5. Find maximal pairs (A, B) where: all elements of A are in causality with all elements of B, elements within A are in choice relation, elements within B are in choice relation
6. Create places for each maximal pair, connect with arcs
7. Add source place (connected to start activities) and sink place (connected from end activities)

**Limitations**: Cannot handle loops of length 1 or 2, assumes complete logs, no noise tolerance, sensitive to infrequent behavior.

### Heuristics Miner

Improves on Alpha Miner by using frequency-based thresholds to filter out noise.

**Dependency measure** between activities a and b:

```
dependency(a, b) = (|a > b| - |b > a|) / (|a > b| + |b > a| + 1)
```

- Values close to 1.0 indicate strong causal dependency (a causes b)
- Values close to -1.0 indicate reverse dependency
- Values close to 0.0 indicate parallelism or no relation

**Key thresholds**:
- **Dependency threshold**: Minimum dependency value to include an edge (e.g., 0.5)
- **Positive observations threshold**: Minimum `|a > b|` count
- **Relative-to-best threshold**: Include if dependency is within X% of the best outgoing dependency
- **Length-1 loop threshold**: For self-loops, `dependency(a, a) = |a > a| / (|a > a| + 1)`
- **Length-2 loop threshold**: For a→b→a patterns

Produces a **Causal net** (C-net) or **Heuristics net** rather than a Petri net.

### Inductive Miner

Guarantees a **sound** process model by recursively decomposing the log.

**Algorithm**:
1. Construct the directly-follows graph of the (sub)log
2. Detect the type of **cut** that splits the activities:
   - **Sequence cut**: Activities can be partitioned into groups where all edges go left-to-right
   - **Exclusive choice cut**: The DFG has disconnected components
   - **Parallel cut**: Every activity pair has edges in both directions between groups
   - **Loop cut**: One group has the start/end activities, others are redo parts
3. Split the log according to the cut
4. Recurse on each sub-log
5. Base case: single activity → leaf node

**Variants**:
- **Inductive Miner (IM)**: Basic version, requires cut to exist
- **Inductive Miner — infrequent (IMf)**: Filters infrequent edges before cut detection
- **Inductive Miner — incompleteness (IMd)**: Handles incomplete logs by falling back to flower models

**Guarantee**: Always produces a sound process tree (and hence a sound Petri net).

## Conformance Checking

### Token-Based Replay

Replay each trace on the Petri net, tracking tokens:

- **Produced (p)**: Tokens added to places during replay
- **Consumed (c)**: Tokens removed from places during replay
- **Missing (m)**: Tokens that were needed but absent (transition not enabled — indicates deviation)
- **Remaining (r)**: Tokens left after replay that shouldn't be there

**Fitness formula**:

```
fitness = 0.5 * (1 - m/c) + 0.5 * (1 - r/p)
```

A fitness of 1.0 means the trace perfectly fits the model. Values below 1.0 indicate deviations.

**Limitations**: May produce misleading results for complex models (e.g., invisible transitions, duplicate labels). Greedy — doesn't find optimal replay.

### Alignment-Based Conformance

Computes the **optimal alignment** between a log trace and the model using A* search.

An alignment is a sequence of **moves**:
- **Synchronous move (a, a)**: Both log and model perform activity a — no cost
- **Log move (a, >>)**: Log has activity a, model skips — cost represents deviation in the log
- **Model move (>>, a)**: Model performs activity a, log skips — cost represents missing behavior

**Cost function**: Typically 1 for each log/model move, 0 for synchronous moves.

**A* search**:
- State: (position in trace, marking of Petri net)
- Goal: (end of trace, final marking)
- Heuristic: Remaining mismatches (admissible, ensures optimality)

**Fitness from alignments**:

```
fitness = 1 - (cost of optimal alignment) / (cost of worst-case alignment)
```

More precise than token replay but computationally more expensive (exponential in worst case).

## Process Model Quality Dimensions

Four dimensions to evaluate a discovered model against the log:

1. **Fitness**: Can the model reproduce the observed behavior? (Do the traces fit?)
2. **Precision**: Does the model allow too much behavior not seen in the log? (Is it overly general?)
3. **Generalization**: Can the model handle unseen but plausible behavior? (Does it overfit?)
4. **Simplicity**: Is the model as simple as possible? (Occam's razor)

These dimensions often trade off: a "flower model" (allowing everything) has perfect fitness but zero precision. A model that only allows exact observed traces has perfect precision but poor generalization.

## Bottleneck Analysis

### Waiting Time vs Service Time

- **Service time**: Duration the activity is actively being worked on (start → complete)
- **Waiting time**: Duration between the previous activity completing and this activity starting
- **Sojourn time**: Total time = waiting time + service time

### Critical Path

The longest path through the process determines the minimum possible throughput time. Activities on the critical path are bottlenecks — improving them directly reduces end-to-end time.

### Resource Contention

When multiple cases compete for the same resource, queuing delays increase waiting times. Detecting resource contention:
- High waiting time correlates with high resource utilization
- Cases processed by the same resource show serialization patterns

## Social Network Mining

### Handover-of-Work

Build a matrix where entry (i, j) counts how often resource i's activity is directly followed by resource j's activity (within the same case). Reveals collaboration patterns and handoff chains.

### Working-Together

Entry (i, j) counts how often resources i and j both appear in the same case. Identifies teams that frequently collaborate.

### Subcontracting

Entry (i, j) counts how often resource i delegates work to j and gets it back (i→j→i pattern). May indicate rework or approval loops.

### Centrality Metrics

Apply graph centrality measures (degree, betweenness, closeness) to the social network to identify:
- **Key resources** (high degree centrality)
- **Bottleneck resources** (high betweenness centrality)
- **Isolated resources** (low closeness centrality)

## Key Terminology

| Term | Definition |
|------|-----------|
| **Case** | A single instance of a process (e.g., one patient visit, one order) |
| **Trace** | The ordered sequence of activities for a case |
| **Variant** | A distinct trace pattern; many cases may share the same variant |
| **Event log** | Collection of events grouped by case, ordered by timestamp |
| **XES** | eXtensible Event Stream — IEEE standard for event log interchange |
| **Petri net** | Bipartite graph (places + transitions) with token-based execution semantics |
| **Marking** | Assignment of tokens to places — represents a process state |
| **Workflow net** | A Petri net with one source place, one sink place, all nodes on a path between them |
| **DFG** | Directly-Follows Graph — directed graph of activity succession frequencies |
| **BPMN** | Business Process Model and Notation — visual process modeling standard |
| **Process tree** | Hierarchical process model with operators (seq, choice, parallel, loop) |
| **Fitness** | Degree to which a model can reproduce observed behavior |
| **Precision** | Degree to which a model restricts behavior to what was observed |
| **Generalization** | Ability of a model to handle unseen behavior |
| **Alignment** | Optimal mapping between a trace and a model execution |
| **Token replay** | Simulating trace execution on a Petri net, tracking token production/consumption |
| **Flower model** | A model that allows any sequence of activities — perfect fitness, zero precision |
| **Spaghetti process** | A process with so many variants it looks like tangled spaghetti when visualized |
| **Concept drift** | Process behavior changes over time (e.g., new regulations, system updates) |

## Real-World Applications

- **Healthcare**: Analyzing patient pathways through a hospital — where do delays occur? Where do patients deviate from clinical protocols?
- **IT Service Management**: Mining incident/ticket resolution processes — how do tickets actually flow through support tiers?
- **Order-to-Cash**: From purchase order to payment — where are the approval bottlenecks?
- **Purchase-to-Pay**: Procurement processes — compliance checking against procurement policies
- **Insurance claims**: Claim handling process — fraud detection through unusual process patterns
- **Manufacturing**: Production process analysis — identifying quality control bottlenecks

## Best Practices

1. **Start with the DFG** for initial exploration before running discovery algorithms
2. **Filter infrequent variants** before discovery — the 80/20 rule usually applies (20% of variants cover 80% of cases)
3. **Choose the right algorithm**: Alpha Miner for learning concepts, Heuristics Miner for noisy real-world logs, Inductive Miner when you need guaranteed soundness
4. **Always measure all four quality dimensions** — a model with high fitness but low precision is useless
5. **Use alignments over token replay** for precise conformance results on complex models
6. **Combine process mining with domain expertise** — the model shows what happens, experts explain why

## Common Pitfalls

- **Incomplete logs**: Missing events lead to incorrect directly-follows relations and broken discovery
- **Concept drift**: Processes change over time; mining the entire log as one may obscure temporal patterns
- **Spaghetti processes**: Real-world processes can have hundreds of variants — filter aggressively or use hierarchical approaches
- **Over-fitting to noise**: Alpha Miner treats every observed relation as significant; use Heuristics or Inductive Miner for noisy data
- **DFG ≠ Process model**: DFGs conflate concurrency and choice — never use a DFG alone for conformance checking
- **Timestamp granularity**: If timestamps have low resolution (e.g., day-level), event ordering within a case may be unreliable
- **Missing start/complete lifecycle**: Without both, you cannot compute service time (only sojourn time)
- **Resource granularity**: "System" as a resource is not informative — use specific user or role identifiers

## pm4py Reference

[pm4py](https://pm4py.fit.fraunhofer.de/) is the standard Python library for process mining. We implement core algorithms from scratch to understand them deeply, but pm4py serves as a reference for:

- Correct algorithm output to validate against
- Additional algorithms (e.g., directly-follows model, transition systems)
- Advanced conformance metrics (precision, generalization)
- XES import/export utilities

Key pm4py equivalents of our implementations:
- `pm4py.discover_petri_net_alpha()` → our `alpha_miner.py`
- `pm4py.discover_petri_net_heuristics()` → our `heuristics_miner.py`
- `pm4py.discover_petri_net_inductive()` → our `inductive_miner.py`
- `pm4py.conformance_diagnostics_token_based_replay()` → our `token_replay.py`
- `pm4py.conformance_diagnostics_alignments()` → our `alignment.py`
