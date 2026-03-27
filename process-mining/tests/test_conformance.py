"""Tests for conformance checking: token replay and alignments."""

from __future__ import annotations

from datetime import datetime

import pytest

from process_mining.conformance.token_replay import (
    ReplayResults,
    TokenReplayResult,
    replay_trace,
    token_replay,
)
from process_mining.event_log import Event, EventLog, Trace
from process_mining.models.petri_net import Marking, PetriNet, Place, Transition


@pytest.fixture
def simple_net() -> tuple[PetriNet, Marking, Marking]:
    """A simple Petri net for A -> B -> C with source/sink places."""
    net = PetriNet()
    p_start = Place(id="p_start", name="start")
    p1 = Place(id="p1", name="p1")
    p2 = Place(id="p2", name="p2")
    p_end = Place(id="p_end", name="end")

    t_a = Transition(id="t_a", label="A")
    t_b = Transition(id="t_b", label="B")
    t_c = Transition(id="t_c", label="C")

    # TODO: Add places, transitions, and arcs to net
    # p_start -> t_a -> p1 -> t_b -> p2 -> t_c -> p_end

    initial = Marking({p_start: 1})
    final = Marking({p_end: 1})
    return net, initial, final


@pytest.fixture
def fitting_trace() -> Trace:
    """A trace that perfectly fits the A->B->C model."""
    return Trace(
        case_id="fit",
        events=[
            Event(case_id="fit", activity="A", timestamp=datetime(2024, 1, 1, 9, 0)),
            Event(case_id="fit", activity="B", timestamp=datetime(2024, 1, 1, 10, 0)),
            Event(case_id="fit", activity="C", timestamp=datetime(2024, 1, 1, 11, 0)),
        ],
    )


@pytest.fixture
def non_fitting_trace() -> Trace:
    """A trace with wrong order: A->C->B (skips B, does C early)."""
    return Trace(
        case_id="nofit",
        events=[
            Event(case_id="nofit", activity="A", timestamp=datetime(2024, 1, 1, 9, 0)),
            Event(case_id="nofit", activity="C", timestamp=datetime(2024, 1, 1, 10, 0)),
            Event(case_id="nofit", activity="B", timestamp=datetime(2024, 1, 1, 11, 0)),
        ],
    )


class TestTokenReplayResult:
    def test_is_fitting_when_perfect(self) -> None:
        result = TokenReplayResult(trace=Trace(case_id="t"), produced=5, consumed=5, missing=0, remaining=0)
        assert result.is_fitting is True

    def test_is_not_fitting_with_missing_tokens(self) -> None:
        result = TokenReplayResult(trace=Trace(case_id="t"), produced=5, consumed=5, missing=1, remaining=0)
        assert result.is_fitting is False

    def test_is_not_fitting_with_remaining_tokens(self) -> None:
        result = TokenReplayResult(trace=Trace(case_id="t"), produced=5, consumed=4, missing=0, remaining=1)
        assert result.is_fitting is False

    def test_trace_fitness_perfect(self) -> None:
        # TODO: Implement — fitness should be 1.0 when missing=0 and remaining=0
        pass

    def test_trace_fitness_partial(self) -> None:
        # TODO: Implement — verify fitness formula for non-zero missing/remaining
        pass


class TestReplayTrace:
    def test_fitting_trace_has_perfect_fitness(
        self,
        simple_net: tuple[PetriNet, Marking, Marking],
        fitting_trace: Trace,
    ) -> None:
        # TODO: Implement — replay fitting trace, verify is_fitting=True and fitness=1.0
        pass

    def test_non_fitting_trace_has_lower_fitness(
        self,
        simple_net: tuple[PetriNet, Marking, Marking],
        non_fitting_trace: Trace,
    ) -> None:
        # TODO: Implement — replay non-fitting trace, verify missing > 0
        pass


class TestTokenReplay:
    def test_log_fitness_with_all_fitting(
        self, simple_net: tuple[PetriNet, Marking, Marking]
    ) -> None:
        # TODO: Implement — create log with only fitting traces, verify log_fitness=1.0
        pass

    def test_log_fitness_with_mixed_traces(
        self, simple_net: tuple[PetriNet, Marking, Marking]
    ) -> None:
        # TODO: Implement — mix fitting and non-fitting traces, verify 0 < fitness < 1
        pass

    def test_fitting_ratio(
        self, simple_net: tuple[PetriNet, Marking, Marking]
    ) -> None:
        # TODO: Implement — verify fitting_ratio = fitting_traces / total_traces
        pass


class TestReplayResults:
    def test_empty_results(self) -> None:
        results = ReplayResults()
        assert results.fitting_traces == 0
        assert results.fitting_ratio == 0.0
