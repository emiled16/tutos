"""Token-based replay for conformance checking.

Replays event log traces on a Petri net, tracking produced, consumed,
missing, and remaining tokens to compute a fitness score.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from process_mining.event_log import EventLog, Trace
from process_mining.models.petri_net import Marking, PetriNet, Transition


@dataclass
class TokenReplayResult:
    """Result of replaying a single trace on a Petri net.

    Attributes:
        trace: The replayed trace.
        produced: Total tokens produced during replay.
        consumed: Total tokens consumed during replay.
        missing: Tokens that were needed but not available (forced firing).
        remaining: Tokens left in non-final places after replay.
        is_fitting: True if the trace perfectly fits the model (missing=0, remaining=0).
    """

    trace: Trace
    produced: int = 0
    consumed: int = 0
    missing: int = 0
    remaining: int = 0

    @property
    def is_fitting(self) -> bool:
        """True if the trace perfectly fits (no missing or remaining tokens)."""
        return self.missing == 0 and self.remaining == 0

    @property
    def trace_fitness(self) -> float:
        """Fitness score for this individual trace.

        Formula: 0.5 * (1 - missing/consumed) + 0.5 * (1 - remaining/produced)

        Returns:
            Fitness score in range [0.0, 1.0].
        """
        # TODO: Implement per-trace fitness calculation
        # Handle edge cases: consumed=0 or produced=0
        raise NotImplementedError


@dataclass
class ReplayResults:
    """Aggregated results of replaying an entire event log.

    Attributes:
        trace_results: Individual replay result for each trace.
        log_fitness: Overall fitness score for the log.
    """

    trace_results: list[TokenReplayResult] = field(default_factory=list)

    @property
    def log_fitness(self) -> float:
        """Overall log fitness score.

        Aggregates fitness across all traces using total token counts.

        Formula: 0.5 * (1 - Σmissing/Σconsumed) + 0.5 * (1 - Σremaining/Σproduced)

        Returns:
            Log fitness in range [0.0, 1.0].
        """
        # TODO: Implement aggregate fitness from all trace results
        # Sum produced, consumed, missing, remaining across all traces
        # Apply the fitness formula
        raise NotImplementedError

    @property
    def fitting_traces(self) -> int:
        """Number of traces that perfectly fit the model."""
        return sum(1 for r in self.trace_results if r.is_fitting)

    @property
    def fitting_ratio(self) -> float:
        """Fraction of traces that perfectly fit."""
        if not self.trace_results:
            return 0.0
        return self.fitting_traces / len(self.trace_results)


def _find_transition_for_activity(
    net: PetriNet, activity: str
) -> Transition | None:
    """Find the visible transition in the net corresponding to an activity.

    Args:
        net: The Petri net.
        activity: Activity name to match.

    Returns:
        Matching Transition, or None if not found.
    """
    # TODO: Implement transition lookup by activity label
    # Search net.transitions for a visible transition whose label matches activity
    raise NotImplementedError


def replay_trace(
    trace: Trace,
    net: PetriNet,
    initial_marking: Marking,
    final_marking: Marking,
) -> TokenReplayResult:
    """Replay a single trace on a Petri net using token-based replay.

    For each event in the trace:
    1. Find the corresponding transition in the net
    2. If the transition is enabled, fire it normally (consume and produce tokens)
    3. If not enabled, force-fire by adding missing tokens (count as "missing")

    After replay, count remaining tokens in non-final places.

    Args:
        trace: The trace to replay.
        net: The Petri net model.
        initial_marking: Starting token distribution.
        final_marking: Expected final token distribution.

    Returns:
        TokenReplayResult with token counts.
    """
    # TODO: Implement token-based replay for a single trace
    # 1. Initialize marking = copy of initial_marking
    # 2. produced = sum of initial marking tokens
    # 3. For each event in trace:
    #    a. Find transition for event.activity
    #    b. If transition not found, skip (log warning)
    #    c. Check if transition is enabled
    #    d. If not enabled, count missing tokens needed and add them
    #    e. Fire the transition (update marking, track consumed/produced)
    # 4. Count remaining tokens in non-final places
    # 5. Return TokenReplayResult
    raise NotImplementedError


def token_replay(
    log: EventLog,
    net: PetriNet,
    initial_marking: Marking,
    final_marking: Marking,
) -> ReplayResults:
    """Replay all traces in an event log on a Petri net.

    Args:
        log: The event log to replay.
        net: The Petri net model.
        initial_marking: Starting token distribution.
        final_marking: Expected final token distribution.

    Returns:
        ReplayResults with individual and aggregate fitness metrics.
    """
    # TODO: Implement log-level token replay
    # Replay each trace and collect results
    # results = [replay_trace(trace, net, initial_marking, final_marking) for trace in log]
    # Return ReplayResults(trace_results=results)
    raise NotImplementedError
