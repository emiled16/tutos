"""Input sources for the Bytewax feature pipeline.

Provides file-based replay and simulated Kafka consumer sources
that can be plugged into the dataflow.
"""

from pathlib import Path
from typing import Generator

from bytewax.inputs import FixedPartitionedSource, StatefulSourcePartition

from bytewax.models import ClickEvent


class FileReplayPartition(StatefulSourcePartition[str, int]):
    """A partition that replays clickstream events from a JSONL file.

    Reads one line at a time, yielding raw JSON strings.
    Maintains the current line offset as resumable state.
    """

    def __init__(self, file_path: Path, start_offset: int = 0) -> None:
        """Initialize the file replay partition.

        Args:
            file_path: Path to the JSONL file containing click events.
            start_offset: Line number to resume reading from.
        """
        self._file_path = file_path
        self._offset = start_offset
        # TODO: Open the file and seek to the start_offset line

    def next_batch(self) -> list[str]:
        """Read the next batch of lines from the file.

        Returns:
            A list of raw JSON strings, one per event.
        """
        # TODO: Implement — read the next batch of lines (e.g., up to 10),
        #       increment self._offset for each line read,
        #       return empty list when EOF is reached
        raise NotImplementedError

    def snapshot(self) -> int:
        """Return the current offset for checkpointing.

        Returns:
            The current line offset in the file.
        """
        # TODO: Implement — return the current offset
        raise NotImplementedError

    def close(self) -> None:
        """Close the file handle."""
        # TODO: Implement — close any open file handles
        raise NotImplementedError


class FileReplaySource(FixedPartitionedSource[str, int]):
    """Source that replays clickstream events from one or more JSONL files.

    Each file is treated as a separate partition for parallel processing.
    """

    def __init__(self, data_dir: Path) -> None:
        """Initialize the file replay source.

        Args:
            data_dir: Directory containing JSONL clickstream files.
        """
        self._data_dir = data_dir

    def list_parts(self) -> list[str]:
        """List all available partitions (one per JSONL file).

        Returns:
            A list of partition identifiers (filenames).
        """
        # TODO: Implement — list all .jsonl files in data_dir
        #       and return their filenames as partition keys
        raise NotImplementedError

    def build_part(
        self, step_id: str, for_part: str, resume_state: int | None
    ) -> FileReplayPartition:
        """Build a partition reader for the given file.

        Args:
            step_id: The dataflow step identifier.
            for_part: The partition key (filename).
            resume_state: The line offset to resume from, or None.

        Returns:
            A FileReplayPartition instance.
        """
        # TODO: Implement — construct a FileReplayPartition for the given file,
        #       using resume_state as the start offset (default 0)
        raise NotImplementedError


def generate_synthetic_events(
    num_users: int = 10,
    events_per_user: int = 50,
    session_gap_minutes: int = 30,
) -> Generator[ClickEvent, None, None]:
    """Generate synthetic clickstream events for testing.

    Produces events for multiple users with realistic session patterns:
    some users have single long sessions, others have multiple sessions
    separated by gaps exceeding the session timeout.

    Args:
        num_users: Number of distinct users to simulate.
        events_per_user: Average number of events per user.
        session_gap_minutes: Inactivity gap that defines session boundaries.

    Yields:
        ClickEvent instances in roughly chronological order.
    """
    # TODO: Implement — generate events with:
    #   - Random user IDs (user_001 through user_{num_users})
    #   - Realistic timestamps with some sessions separated by > session_gap_minutes
    #   - Mix of action types (click, view, scroll, submit)
    #   - Varied page URLs from a realistic set
    #   - Events yielded in approximate timestamp order
    raise NotImplementedError
