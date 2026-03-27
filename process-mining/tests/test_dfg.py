"""Tests for Directly-Follows Graph construction and filtering."""

from __future__ import annotations

from datetime import datetime

import pytest

from process_mining.event_log import Event, EventLog, Trace
from process_mining.models.dfg import DFGEdge, DirectlyFollowsGraph


@pytest.fixture
def sample_log() -> EventLog:
    """Log with three traces for DFG testing."""
    return EventLog(
        traces=[
            Trace(case_id="1", events=[
                Event(case_id="1", activity="A", timestamp=datetime(2024, 1, 1, 9, 0)),
                Event(case_id="1", activity="B", timestamp=datetime(2024, 1, 1, 10, 0)),
                Event(case_id="1", activity="C", timestamp=datetime(2024, 1, 1, 11, 0)),
            ]),
            Trace(case_id="2", events=[
                Event(case_id="2", activity="A", timestamp=datetime(2024, 1, 1, 9, 0)),
                Event(case_id="2", activity="B", timestamp=datetime(2024, 1, 1, 10, 0)),
                Event(case_id="2", activity="C", timestamp=datetime(2024, 1, 1, 11, 0)),
            ]),
            Trace(case_id="3", events=[
                Event(case_id="3", activity="A", timestamp=datetime(2024, 1, 1, 9, 0)),
                Event(case_id="3", activity="C", timestamp=datetime(2024, 1, 1, 10, 0)),
            ]),
        ]
    )


@pytest.fixture
def dfg(sample_log: EventLog) -> DirectlyFollowsGraph:
    return DirectlyFollowsGraph.from_event_log(sample_log)


class TestDFGConstruction:
    def test_activities(self, dfg: DirectlyFollowsGraph) -> None:
        # TODO: Implement — verify activities == {"A", "B", "C"}
        pass

    def test_edge_frequencies(self, dfg: DirectlyFollowsGraph) -> None:
        # TODO: Implement — verify A->B has frequency 2, B->C has frequency 2, A->C has frequency 1
        pass

    def test_start_activities(self, dfg: DirectlyFollowsGraph) -> None:
        # TODO: Implement — verify start_activities == {"A": 3}
        pass

    def test_end_activities(self, dfg: DirectlyFollowsGraph) -> None:
        # TODO: Implement — verify end_activities == {"C": 3}
        pass

    def test_activity_counts(self, dfg: DirectlyFollowsGraph) -> None:
        # TODO: Implement — verify A=3, B=2, C=3
        pass

    def test_avg_duration(self, dfg: DirectlyFollowsGraph) -> None:
        # TODO: Implement — verify A->B avg duration is 3600 seconds (1 hour)
        pass


class TestDFGEdge:
    def test_avg_duration_zero_frequency(self) -> None:
        edge = DFGEdge(source="A", target="B", frequency=0, total_duration=0.0)
        assert edge.avg_duration == 0.0

    def test_avg_duration_calculation(self) -> None:
        edge = DFGEdge(source="A", target="B", frequency=4, total_duration=100.0)
        assert edge.avg_duration == 25.0


class TestDFGFiltering:
    def test_filter_by_frequency(self, dfg: DirectlyFollowsGraph) -> None:
        # TODO: Implement — filter with min_frequency=2, verify A->C (freq=1) is removed
        pass

    def test_filter_by_percentage(self, dfg: DirectlyFollowsGraph) -> None:
        # TODO: Implement — keep top 50%, verify only most frequent edges remain
        pass


class TestDFGQueries:
    def test_get_frequency_existing_edge(self, dfg: DirectlyFollowsGraph) -> None:
        # TODO: Implement — verify get_frequency("A", "B") returns 2
        pass

    def test_get_frequency_nonexistent_edge(self, dfg: DirectlyFollowsGraph) -> None:
        # TODO: Implement — verify get_frequency("C", "A") returns 0
        pass

    def test_to_adjacency_matrix(self, dfg: DirectlyFollowsGraph) -> None:
        # TODO: Implement — verify adjacency matrix dimensions and values
        pass
