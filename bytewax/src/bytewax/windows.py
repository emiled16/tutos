"""Window definitions for the Bytewax feature pipeline.

Provides factory functions for creating tumbling, sliding, and session
window configurations used by the dataflow operators.
"""

from datetime import timedelta

from bytewax.operators.windowing import EventClock, SessionWindower, SlidingWindower, TumblingWindower

from bytewax.models import ClickEvent


def get_event_clock() -> EventClock[ClickEvent]:
    """Create an EventClock that extracts timestamps from ClickEvent instances.

    The clock uses the event's timestamp field to determine event time,
    enabling event-time-based windowing instead of processing-time.

    Returns:
        An EventClock configured for ClickEvent.
    """
    # TODO: Implement — create an EventClock that:
    #   - Extracts the timestamp from ClickEvent.timestamp
    #   - Sets a reasonable watermark lag (e.g., 10 seconds)
    raise NotImplementedError


def tumbling_window(duration: timedelta = timedelta(minutes=5)) -> TumblingWindower:
    """Create a tumbling window of the specified duration.

    Tumbling windows are fixed-size, non-overlapping time intervals.
    Every event belongs to exactly one window.

    Args:
        duration: The fixed size of each window.

    Returns:
        A TumblingWindower instance.
    """
    # TODO: Implement — create and return a TumblingWindower with the given duration
    raise NotImplementedError


def sliding_window(
    duration: timedelta = timedelta(minutes=10),
    slide: timedelta = timedelta(minutes=2),
) -> SlidingWindower:
    """Create a sliding window with the specified duration and slide interval.

    Sliding windows overlap: each event can appear in multiple windows.
    This produces smoother aggregations than tumbling windows.

    Args:
        duration: The total size of each window.
        slide: How far each window advances from the previous one.

    Returns:
        A SlidingWindower instance.
    """
    # TODO: Implement — create and return a SlidingWindower
    raise NotImplementedError


def session_window(
    gap: timedelta = timedelta(minutes=30),
) -> SessionWindower:
    """Create a session window with the specified inactivity gap.

    Session windows are data-driven: they close when no events arrive
    for longer than the gap duration. This naturally groups user activity.

    Args:
        gap: Maximum inactivity period before the session window closes.

    Returns:
        A SessionWindower instance.
    """
    # TODO: Implement — create and return a SessionWindower with the given gap
    raise NotImplementedError
