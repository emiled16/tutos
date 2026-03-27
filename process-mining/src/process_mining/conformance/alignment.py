"""Alignment-based conformance checking using A* search.

Computes optimal alignments between log traces and a Petri net model.
More precise than token replay but computationally more expensive.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from enum import Enum
from typing import NamedTuple

from process_mining.event_log import EventLog, Trace
from process_mining.models.petri_net import Marking, PetriNet, Transition


class MoveType(str, Enum):
    """Types of moves in an alignment."""

    SYNC = "sync"    # (a, a): both log and model perform activity a
    LOG = "log"      # (a, >>): log has activity, model skips
    MODEL = "model"  # (>>, a): model performs activity, log skips


class AlignmentMove(NamedTuple):
    """A single move in an alignment."""

    move_type: MoveType
    log_activity: str | None
    model_activity: str | None
    cost: float


@dataclass
class Alignment:
    """An optimal alignment between a trace and a model.

    Attributes:
        trace: The original log trace.
        moves: Sequence of alignment moves.
        cost: Total alignment cost (sum of move costs).
    """

    trace: Trace
    moves: list[AlignmentMove] = field(default_factory=list)

    @property
    def cost(self) -> float:
        """Total cost of the alignment."""
        return sum(m.cost for m in self.moves)

    @property
    def fitness(self) -> float:
        """Fitness score derived from this alignment.

        Formula: 1 - cost / worst_case_cost
        Worst case = all log moves + all model moves to reach final marking.

        Returns:
            Fitness in range [0.0, 1.0].
        """
        # TODO: Implement alignment fitness calculation
        # worst_case = len(trace) * log_move_cost + shortest_model_path * model_move_cost
        # fitness = 1 - self.cost / worst_case
        raise NotImplementedError

    @property
    def sync_moves(self) -> list[AlignmentMove]:
        """Return only synchronous moves."""
        return [m for m in self.moves if m.move_type == MoveType.SYNC]

    @property
    def log_moves(self) -> list[AlignmentMove]:
        """Return only log moves (deviations in the log)."""
        return [m for m in self.moves if m.move_type == MoveType.LOG]

    @property
    def model_moves(self) -> list[AlignmentMove]:
        """Return only model moves (deviations in the model)."""
        return [m for m in self.moves if m.move_type == MoveType.MODEL]


@dataclass
class AlignmentResults:
    """Aggregated alignment results for an event log."""

    alignments: list[Alignment] = field(default_factory=list)

    @property
    def log_fitness(self) -> float:
        """Overall log fitness from alignments.

        Returns:
            Average fitness across all traces.
        """
        # TODO: Implement aggregate fitness from all alignments
        raise NotImplementedError

    @property
    def perfectly_fitting(self) -> int:
        """Number of traces with zero-cost alignments."""
        return sum(1 for a in self.alignments if a.cost == 0.0)


@dataclass(frozen=True)
class SearchState:
    """State in the A* search space for alignment computation.

    Attributes:
        trace_index: Current position in the log trace (0 to len(trace)).
        marking: Current Petri net marking (as a frozenset for hashing).
    """

    trace_index: int
    marking: frozenset[tuple[str, int]]

    @classmethod
    def from_marking(cls, trace_index: int, marking: Marking) -> SearchState:
        """Create a SearchState from a mutable Marking."""
        frozen = frozenset((p.name, count) for p, count in marking.items())
        return cls(trace_index=trace_index, marking=frozen)


def _compute_heuristic(
    state: SearchState,
    trace: Trace,
    net: PetriNet,
    final_marking: Marking,
) -> float:
    """Compute an admissible heuristic for A* search.

    A simple admissible heuristic: remaining log events that cannot possibly
    be synchronized (lower bound on future cost).

    Args:
        state: Current search state.
        trace: The full trace being aligned.
        net: The Petri net model.
        final_marking: Target marking.

    Returns:
        Heuristic cost estimate (must not overestimate).
    """
    # TODO: Implement admissible heuristic
    # Simple heuristic: number of remaining trace events (each costs at least 0 if synced)
    # Better heuristic: use marking equation or ILP relaxation
    raise NotImplementedError


def compute_alignment(
    trace: Trace,
    net: PetriNet,
    initial_marking: Marking,
    final_marking: Marking,
    sync_cost: float = 0.0,
    log_move_cost: float = 1.0,
    model_move_cost: float = 1.0,
) -> Alignment:
    """Compute the optimal alignment between a trace and a Petri net using A*.

    The search explores states (trace_position, marking) and finds the
    minimum-cost sequence of moves to consume the entire trace and reach
    the final marking.

    Possible moves from state (i, M):
    - Synchronous move: if trace[i] matches an enabled transition t,
      fire t and advance to (i+1, M')  — cost: sync_cost
    - Log move: skip trace[i], advance to (i+1, M) — cost: log_move_cost
    - Model move: fire an enabled transition t (visible or invisible),
      stay at (i, M') — cost: model_move_cost (0 for invisible transitions)

    Args:
        trace: The trace to align.
        net: The Petri net model.
        initial_marking: Starting marking.
        final_marking: Target marking.
        sync_cost: Cost of a synchronous move (default 0).
        log_move_cost: Cost of a log move (default 1).
        model_move_cost: Cost of a model move for visible transitions (default 1).

    Returns:
        Optimal Alignment.
    """
    # TODO: Implement A* search for optimal alignment
    # 1. Initialize priority queue with (heuristic, SearchState(0, initial_marking))
    # 2. Track g_cost (actual cost to reach state) and parent pointers
    # 3. While queue not empty:
    #    a. Pop state with lowest f = g + h
    #    b. If state is goal (trace_index == len(trace) and marking == final_marking): reconstruct path
    #    c. Generate successors:
    #       - Sync move: match trace[i] to enabled transition, fire, advance trace
    #       - Log move: skip trace[i], advance trace index
    #       - Model move: fire any enabled transition, keep trace index
    #    d. For each successor, compute g' and h', add to queue if better
    # 4. Reconstruct alignment from parent pointers
    raise NotImplementedError


def compute_alignments(
    log: EventLog,
    net: PetriNet,
    initial_marking: Marking,
    final_marking: Marking,
    sync_cost: float = 0.0,
    log_move_cost: float = 1.0,
    model_move_cost: float = 1.0,
) -> AlignmentResults:
    """Compute optimal alignments for all traces in an event log.

    Args:
        log: The event log.
        net: The Petri net model.
        initial_marking: Starting marking.
        final_marking: Target marking.
        sync_cost: Cost of synchronous moves.
        log_move_cost: Cost of log moves.
        model_move_cost: Cost of model moves.

    Returns:
        AlignmentResults with individual alignments and aggregate metrics.
    """
    # TODO: Implement log-level alignment computation
    # alignments = [compute_alignment(trace, net, ...) for trace in log]
    # Return AlignmentResults(alignments=alignments)
    raise NotImplementedError
