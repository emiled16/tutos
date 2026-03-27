"""Pydantic models for clickstream events and computed session features."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """Types of user actions in the clickstream."""

    CLICK = "click"
    VIEW = "view"
    SCROLL = "scroll"
    SUBMIT = "submit"


class ClickEvent(BaseModel):
    """A single clickstream event from a user interaction.

    Attributes:
        event_id: Unique identifier for the event.
        user_id: Identifier of the user who generated the event.
        timestamp: When the event occurred (event time).
        page_url: The URL of the page where the event happened.
        action: The type of action performed.
        metadata: Optional additional context about the event.
    """

    event_id: str
    user_id: str
    timestamp: datetime
    page_url: str
    action: ActionType
    metadata: dict[str, str | int | float] = Field(default_factory=dict)

    # TODO: Add a model validator that ensures timestamp is not in the future

    def event_time_ms(self) -> int:
        """Return the event timestamp as milliseconds since epoch."""
        # TODO: Implement conversion from datetime to epoch milliseconds
        raise NotImplementedError


class SessionFeatures(BaseModel):
    """Computed features for a single user session.

    A session is a contiguous period of user activity bounded by
    inactivity gaps of 30 minutes or more.

    Attributes:
        user_id: The user this session belongs to.
        session_start: Timestamp of the first event in the session.
        session_end: Timestamp of the last event in the session.
        session_duration_seconds: Total duration of the session in seconds.
        total_clicks: Number of click events in the session.
        total_views: Number of page view events in the session.
        unique_pages: Number of distinct pages visited.
        pages_visited: Ordered list of pages visited during the session.
        click_velocity: Clicks per minute during the session.
        engagement_score: A composite score representing user engagement (0.0–1.0).
    """

    user_id: str
    session_start: datetime
    session_end: datetime
    session_duration_seconds: float = 0.0
    total_clicks: int = 0
    total_views: int = 0
    unique_pages: int = 0
    pages_visited: list[str] = Field(default_factory=list)
    click_velocity: float = 0.0
    engagement_score: float = 0.0

    # TODO: Add a model validator that computes session_duration_seconds from
    #       session_start and session_end if not provided


class SessionAccumulator(BaseModel):
    """Mutable accumulator for building session features incrementally.

    Used inside stateful operators to collect events and compute
    features as new events arrive.
    """

    user_id: str
    events: list[ClickEvent] = Field(default_factory=list)
    last_event_time: datetime | None = None

    def add_event(self, event: ClickEvent) -> None:
        """Add an event to this session accumulator.

        Args:
            event: The clickstream event to add.
        """
        # TODO: Implement — append the event, update last_event_time,
        #       maintain events sorted by timestamp
        raise NotImplementedError

    def compute_features(self) -> SessionFeatures:
        """Compute session features from the accumulated events.

        Returns:
            A SessionFeatures instance with all computed metrics.
        """
        # TODO: Implement feature computation:
        #   - session_duration_seconds from first to last event
        #   - total_clicks / total_views by counting action types
        #   - unique_pages from distinct page_url values
        #   - click_velocity as total_clicks / (duration_minutes or 1)
        #   - engagement_score as a weighted combination of the above
        raise NotImplementedError
