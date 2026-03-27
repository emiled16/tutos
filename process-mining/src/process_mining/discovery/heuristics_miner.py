"""Heuristics Miner for noise-tolerant process discovery.

Uses frequency-based dependency measures to filter out noise and discover
robust causal nets. More practical than Alpha Miner for real-world logs.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from process_mining.event_log import EventLog
from process_mining.models.dfg import DirectlyFollowsGraph
from process_mining.models.petri_net import Marking, PetriNet


@dataclass
class HeuristicsThresholds:
    """Configuration thresholds for the Heuristics Miner.

    Attributes:
        dependency_threshold: Minimum dependency value to include a causal relation (0.0-1.0).
        positive_observations: Minimum |a > b| count to consider the relation.
        relative_to_best: Include if dependency is within this ratio of the best outgoing dependency.
        length_1_loop_threshold: Threshold for self-loop detection (a > a patterns).
        length_2_loop_threshold: Threshold for length-2 loop detection (a > b > a patterns).
    """

    dependency_threshold: float = 0.5
    positive_observations: int = 1
    relative_to_best: float = 0.05
    length_1_loop_threshold: float = 0.5
    length_2_loop_threshold: float = 0.5


@dataclass
class DependencyRelation:
    """A causal dependency between two activities with its strength measure."""

    source: str
    target: str
    dependency_value: float
    frequency: int


@dataclass
class CausalNet:
    """A Causal net (C-net) discovered by the Heuristics Miner.

    Each activity has a set of input bindings and output bindings that
    capture the causal dependencies.
    """

    activities: set[str] = field(default_factory=set)
    dependencies: list[DependencyRelation] = field(default_factory=list)
    input_bindings: dict[str, list[set[str]]] = field(default_factory=dict)
    output_bindings: dict[str, list[set[str]]] = field(default_factory=dict)
    start_activities: set[str] = field(default_factory=set)
    end_activities: set[str] = field(default_factory=set)


def compute_dependency_measure(
    follows_ab: int, follows_ba: int
) -> float:
    """Compute the dependency measure between activities a and b.

    Formula: (|a > b| - |b > a|) / (|a > b| + |b > a| + 1)

    Values near 1.0 indicate strong causal relation (a causes b).
    Values near -1.0 indicate reverse causality.
    Values near 0.0 indicate parallelism or no relation.

    Args:
        follows_ab: Count of a directly followed by b.
        follows_ba: Count of b directly followed by a.

    Returns:
        Dependency measure in range (-1.0, 1.0).
    """
    # TODO: Implement the dependency measure formula
    # dependency = (follows_ab - follows_ba) / (follows_ab + follows_ba + 1)
    raise NotImplementedError


def compute_length1_loop_measure(self_follows: int) -> float:
    """Compute the dependency measure for length-1 loops (self-loops).

    Formula: |a > a| / (|a > a| + 1)

    Args:
        self_follows: Count of activity a directly followed by itself.

    Returns:
        Self-loop dependency measure in range [0.0, 1.0).
    """
    # TODO: Implement length-1 loop measure
    raise NotImplementedError


def compute_length2_loop_measure(
    follows_ab: int, follows_ba: int
) -> float:
    """Compute the dependency measure for length-2 loops (a→b→a patterns).

    Formula: (|a > b| + |b > a|) / (|a > b| + |b > a| + 1)

    Args:
        follows_ab: Count of a directly followed by b.
        follows_ba: Count of b directly followed by a.

    Returns:
        Length-2 loop measure in range [0.0, 1.0).
    """
    # TODO: Implement length-2 loop measure
    raise NotImplementedError


def build_dependency_matrix(
    dfg: DirectlyFollowsGraph,
) -> dict[tuple[str, str], float]:
    """Build a dependency matrix from a DFG.

    Computes the dependency measure for every pair of activities.

    Args:
        dfg: Directly-Follows Graph with frequency data.

    Returns:
        Dictionary mapping (source, target) to dependency value.
    """
    # TODO: Implement dependency matrix construction
    # For each pair of activities (a, b):
    #   - Get |a > b| from dfg
    #   - Get |b > a| from dfg
    #   - Compute dependency_measure(|a > b|, |b > a|)
    raise NotImplementedError


def heuristics_miner(
    log: EventLog,
    thresholds: HeuristicsThresholds | None = None,
) -> CausalNet:
    """Discover a Causal net from an event log using the Heuristics Miner.

    Steps:
    1. Build a DFG from the event log
    2. Compute dependency measures for all activity pairs
    3. Detect length-1 loops (self-loops above threshold)
    4. Detect length-2 loops (a→b→a above threshold)
    5. Filter dependencies by threshold, positive observations, and relative-to-best
    6. Determine input/output bindings for each activity
    7. Build the Causal net

    Args:
        log: The event log to discover from.
        thresholds: Mining thresholds (defaults used if None).

    Returns:
        Discovered CausalNet.
    """
    # TODO: Implement the Heuristics Miner algorithm
    # 1. dfg = DirectlyFollowsGraph.from_event_log(log)
    # 2. dep_matrix = build_dependency_matrix(dfg)
    # 3. Filter by thresholds:
    #    - dependency_value >= thresholds.dependency_threshold
    #    - frequency >= thresholds.positive_observations
    #    - dependency_value >= best_outgoing - thresholds.relative_to_best
    # 4. Detect loops using length_1/2_loop thresholds
    # 5. Build CausalNet with input/output bindings
    raise NotImplementedError


def causal_net_to_petri_net(cnet: CausalNet) -> tuple[PetriNet, Marking, Marking]:
    """Convert a Causal net to a Petri net with initial and final markings.

    Args:
        cnet: The Causal net to convert.

    Returns:
        Tuple of (PetriNet, initial_marking, final_marking).
    """
    # TODO: Implement C-net to Petri net conversion
    # - Create transitions for each activity
    # - Create places for each dependency relation
    # - Add source/sink places with appropriate markings
    # - Handle bindings by creating appropriate place/arc structures
    raise NotImplementedError
