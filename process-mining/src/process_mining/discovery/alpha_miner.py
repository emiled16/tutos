"""Alpha Miner algorithm for process discovery.

Discovers a Petri net from an event log by analyzing ordering relations
between activities: directly-follows, causality, parallel, and choice.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from process_mining.event_log import EventLog
from process_mining.models.petri_net import Marking, PetriNet


class OrderingRelation(str, Enum):
    """Ordering relations between activity pairs in the Alpha Miner."""

    CAUSALITY = "causality"       # a → b: a > b and not b > a
    PARALLEL = "parallel"         # a || b: a > b and b > a
    CHOICE = "choice"             # a # b: not a > b and not b > a
    DIRECTLY_FOLLOWS = "follows"  # a > b: a directly followed by b in some trace


@dataclass
class AlphaRelations:
    """Computed ordering relations for the Alpha Miner algorithm.

    Stores the directly-follows, causality, parallel, and choice relations
    between all activity pairs discovered from the event log.
    """

    activities: set[str] = field(default_factory=set)
    start_activities: set[str] = field(default_factory=set)
    end_activities: set[str] = field(default_factory=set)
    directly_follows: set[tuple[str, str]] = field(default_factory=set)
    causality: set[tuple[str, str]] = field(default_factory=set)
    parallel: set[tuple[str, str]] = field(default_factory=set)
    choice: set[tuple[str, str]] = field(default_factory=set)


def compute_directly_follows(log: EventLog) -> set[tuple[str, str]]:
    """Extract all directly-follows pairs from the event log.

    For each trace, every consecutive activity pair (a, b) is recorded.

    Args:
        log: The event log to analyze.

    Returns:
        Set of (activity_a, activity_b) tuples where a > b.
    """
    # TODO: Implement directly-follows extraction
    # Iterate over each trace, for each consecutive pair of events,
    # add (event_i.activity, event_{i+1}.activity) to the result set
    raise NotImplementedError


def compute_ordering_relations(log: EventLog) -> AlphaRelations:
    """Compute all four ordering relations from the event log.

    1. Directly-follows (>): a > b iff a is directly followed by b in some trace
    2. Causality (→): a → b iff a > b AND NOT b > a
    3. Parallel (||): a || b iff a > b AND b > a
    4. Choice (#): a # b iff NOT a > b AND NOT b > a

    Args:
        log: The event log to analyze.

    Returns:
        AlphaRelations with all computed relations.
    """
    # TODO: Implement ordering relation computation
    # 1. Compute directly_follows set
    # 2. Derive causality: (a, b) where (a, b) in df and (b, a) not in df
    # 3. Derive parallel: (a, b) where (a, b) in df and (b, a) in df
    # 4. Derive choice: (a, b) where (a, b) not in df and (b, a) not in df
    # 5. Collect start/end activities from traces
    raise NotImplementedError


def find_maximal_pairs(relations: AlphaRelations) -> list[tuple[frozenset[str], frozenset[str]]]:
    """Find maximal pairs (A, B) for place construction.

    A pair (A, B) is valid when:
    - For all a in A, b in B: a → b (causality)
    - For all a1, a2 in A: a1 # a2 (choice — activities in A are unrelated)
    - For all b1, b2 in B: b1 # b2 (choice — activities in B are unrelated)

    A pair is maximal when no proper superset satisfies the same conditions.

    Args:
        relations: Computed ordering relations.

    Returns:
        List of maximal (A, B) pairs as frozensets.
    """
    # TODO: Implement maximal pair finding
    # 1. Start with all pairs ({a}, {b}) where a → b
    # 2. Try to extend A and B while maintaining validity constraints
    # 3. Remove non-maximal pairs (those that are subsets of others)
    raise NotImplementedError


def alpha_miner(log: EventLog) -> tuple[PetriNet, Marking, Marking]:
    """Discover a Petri net from an event log using the Alpha Miner algorithm.

    Steps:
    1. Extract all activities (T_L), start activities (T_I), end activities (T_O)
    2. Compute ordering relations (directly-follows, causality, parallel, choice)
    3. Find maximal pairs (A, B) satisfying the Alpha Miner constraints
    4. Create places: one place p_(A,B) for each maximal pair
    5. Create transitions: one for each activity
    6. Create arcs: a → p_(A,B) for a in A, p_(A,B) → b for b in B
    7. Add source place (i_L) with arcs to start activity transitions
    8. Add sink place (o_L) with arcs from end activity transitions
    9. Define initial marking {i_L: 1} and final marking {o_L: 1}

    Args:
        log: The event log to discover from.

    Returns:
        Tuple of (PetriNet, initial_marking, final_marking).
    """
    # TODO: Implement the full Alpha Miner algorithm
    # 1. Compute T_L (all activities), T_I (start activities), T_O (end activities)
    # 2. relations = compute_ordering_relations(log)
    # 3. maximal_pairs = find_maximal_pairs(relations)
    # 4. Build PetriNet:
    #    - Add a transition for each activity in T_L
    #    - Add source place i_L and sink place o_L
    #    - For each maximal pair (A, B), add a place p_(A,B)
    #    - Add arcs: for each a in A, arc from transition_a to p_(A,B)
    #               for each b in B, arc from p_(A,B) to transition_b
    #    - Add arcs from i_L to start transitions, from end transitions to o_L
    # 5. Return (net, {i_L: 1}, {o_L: 1})
    raise NotImplementedError
