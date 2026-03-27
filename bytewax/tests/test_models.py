"""Tests for clickstream event and session feature models."""

from datetime import datetime, timedelta

import pytest

from bytewax.models import ActionType, ClickEvent, SessionAccumulator, SessionFeatures


@pytest.fixture
def sample_click_event() -> ClickEvent:
    """Create a sample click event for testing."""
    return ClickEvent(
        event_id="evt_001",
        user_id="user_42",
        timestamp=datetime(2024, 1, 15, 10, 30, 0),
        page_url="/products/widget",
        action=ActionType.CLICK,
        metadata={"referrer": "google.com"},
    )


@pytest.fixture
def sample_events() -> list[ClickEvent]:
    """Create a sequence of click events forming a single session."""
    base_time = datetime(2024, 1, 15, 10, 0, 0)
    return [
        ClickEvent(
            event_id=f"evt_{i:03d}",
            user_id="user_42",
            timestamp=base_time + timedelta(minutes=i * 2),
            page_url=f"/page/{i % 5}",
            action=ActionType.CLICK if i % 2 == 0 else ActionType.VIEW,
        )
        for i in range(10)
    ]


class TestClickEvent:
    def test_valid_event_creation(self, sample_click_event: ClickEvent) -> None:
        """Test that a valid click event can be created."""
        # TODO: Implement — assert fields are set correctly
        raise NotImplementedError

    def test_event_time_ms_conversion(self, sample_click_event: ClickEvent) -> None:
        """Test that event_time_ms returns correct epoch milliseconds."""
        # TODO: Implement — call event_time_ms() and verify the result
        raise NotImplementedError

    def test_invalid_action_type_raises(self) -> None:
        """Test that an invalid action type raises a validation error."""
        # TODO: Implement — attempt to create a ClickEvent with action="invalid"
        #       and assert it raises a ValidationError
        raise NotImplementedError

    def test_default_metadata_is_empty_dict(self) -> None:
        """Test that metadata defaults to an empty dict when not provided."""
        # TODO: Implement — create a ClickEvent without metadata,
        #       assert metadata == {}
        raise NotImplementedError


class TestSessionAccumulator:
    def test_add_first_event(self, sample_click_event: ClickEvent) -> None:
        """Test adding the first event to an empty accumulator."""
        # TODO: Implement — create accumulator, add event,
        #       assert events list has one item and last_event_time is set
        raise NotImplementedError

    def test_add_multiple_events_maintains_order(self, sample_events: list[ClickEvent]) -> None:
        """Test that events are maintained in chronological order."""
        # TODO: Implement — add events in random order,
        #       assert they're stored sorted by timestamp
        raise NotImplementedError

    def test_compute_features_single_event(self, sample_click_event: ClickEvent) -> None:
        """Test feature computation with a single event (degenerate session)."""
        # TODO: Implement — add one event, compute features,
        #       verify duration is 0 and counts are correct
        raise NotImplementedError

    def test_compute_features_full_session(self, sample_events: list[ClickEvent]) -> None:
        """Test feature computation with a multi-event session."""
        # TODO: Implement — add all sample events, compute features,
        #       verify duration, click counts, unique pages, velocity
        raise NotImplementedError


class TestSessionFeatures:
    def test_engagement_score_bounds(self) -> None:
        """Test that engagement score is between 0.0 and 1.0."""
        # TODO: Implement — create SessionFeatures with various values,
        #       assert engagement_score is always in [0.0, 1.0]
        raise NotImplementedError
