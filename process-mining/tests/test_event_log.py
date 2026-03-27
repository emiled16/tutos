"""Tests for EventLog parsing, filtering, and statistics."""

from __future__ import annotations

from datetime import datetime

import pytest

from process_mining.event_log import Event, EventLog, LifecycleTransition, Trace


@pytest.fixture
def sample_traces() -> list[Trace]:
    """Three traces representing a simple order process."""
    return [
        Trace(
            case_id="1",
            events=[
                Event(case_id="1", activity="A", timestamp=datetime(2024, 1, 1, 9, 0), resource="Alice"),
                Event(case_id="1", activity="B", timestamp=datetime(2024, 1, 1, 10, 0), resource="Bob"),
                Event(case_id="1", activity="C", timestamp=datetime(2024, 1, 1, 11, 0), resource="Alice"),
            ],
        ),
        Trace(
            case_id="2",
            events=[
                Event(case_id="2", activity="A", timestamp=datetime(2024, 1, 1, 9, 30), resource="Alice"),
                Event(case_id="2", activity="C", timestamp=datetime(2024, 1, 1, 10, 30), resource="Bob"),
                Event(case_id="2", activity="B", timestamp=datetime(2024, 1, 1, 11, 30), resource="Charlie"),
            ],
        ),
        Trace(
            case_id="3",
            events=[
                Event(case_id="3", activity="A", timestamp=datetime(2024, 1, 2, 9, 0), resource="Bob"),
                Event(case_id="3", activity="B", timestamp=datetime(2024, 1, 2, 10, 0), resource="Alice"),
                Event(case_id="3", activity="C", timestamp=datetime(2024, 1, 2, 11, 0), resource="Bob"),
            ],
        ),
    ]


@pytest.fixture
def event_log(sample_traces: list[Trace]) -> EventLog:
    return EventLog(traces=sample_traces)


class TestTrace:
    def test_activities_returns_ordered_names(self, sample_traces: list[Trace]) -> None:
        # TODO: Implement — verify trace.activities returns ["A", "B", "C"]
        pass

    def test_duration_computes_seconds_between_first_and_last(
        self, sample_traces: list[Trace]
    ) -> None:
        # TODO: Implement — verify duration is 7200 seconds (2 hours) for trace 1
        pass

    def test_duration_returns_none_for_single_event(self) -> None:
        # TODO: Implement — verify None for a trace with only one event
        pass

    def test_len_returns_event_count(self, sample_traces: list[Trace]) -> None:
        # TODO: Implement — verify len(trace) == 3
        pass


class TestEventLogStatistics:
    def test_case_count(self, event_log: EventLog) -> None:
        # TODO: Implement — verify case_count == 3
        pass

    def test_event_count(self, event_log: EventLog) -> None:
        # TODO: Implement — verify event_count == 9
        pass

    def test_activities(self, event_log: EventLog) -> None:
        # TODO: Implement — verify activities == {"A", "B", "C"}
        pass

    def test_start_activities(self, event_log: EventLog) -> None:
        # TODO: Implement — verify start_activities == {"A"} (all traces start with A)
        pass

    def test_end_activities(self, event_log: EventLog) -> None:
        # TODO: Implement — verify end_activities == {"C", "B"}
        pass

    def test_variants(self, event_log: EventLog) -> None:
        # TODO: Implement — verify 2 unique variants: (A,B,C) with 2 traces, (A,C,B) with 1 trace
        pass

    def test_activity_frequencies(self, event_log: EventLog) -> None:
        # TODO: Implement — verify A=3, B=3, C=3
        pass


class TestEventLogFiltering:
    def test_filter_by_activities_include(self, event_log: EventLog) -> None:
        # TODO: Implement — filter keeping only events with activity in {"A", "B"}
        # Verify C is excluded from all traces
        pass

    def test_filter_by_activities_exclude(self, event_log: EventLog) -> None:
        # TODO: Implement — filter excluding activity "B"
        pass

    def test_filter_by_timeframe(self, event_log: EventLog) -> None:
        # TODO: Implement — filter to Jan 1 only, verify trace 3 (Jan 2) is excluded
        pass

    def test_filter_by_resource(self, event_log: EventLog) -> None:
        # TODO: Implement — filter to resource="Alice" only
        pass

    def test_filter_removes_empty_traces(self, event_log: EventLog) -> None:
        # TODO: Implement — filter that removes all events from a trace, verify trace is gone
        pass


class TestEventLogConversion:
    def test_to_dataframe(self, event_log: EventLog) -> None:
        # TODO: Implement — verify DataFrame has 9 rows and expected columns
        pass

    def test_from_dataframe_roundtrip(self, event_log: EventLog) -> None:
        # TODO: Implement — convert to DataFrame and back, verify same traces
        pass
