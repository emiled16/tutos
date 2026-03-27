"""Directly-Follows Graph (DFG) for process mining.

Builds a DFG from an event log, capturing activity succession patterns
with frequency and performance (timing) annotations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from process_mining.event_log import EventLog


@dataclass
class DFGEdge:
    """An edge in the Directly-Follows Graph.

    Attributes:
        source: Source activity name.
        target: Target activity name.
        frequency: Number of times source is directly followed by target.
        total_duration: Sum of time deltas (seconds) between source and target events.
    """

    source: str
    target: str
    frequency: int = 0
    total_duration: float = 0.0

    @property
    def avg_duration(self) -> float:
        """Average time (seconds) between source and target activities."""
        if self.frequency == 0:
            return 0.0
        return self.total_duration / self.frequency


@dataclass
class DirectlyFollowsGraph:
    """A Directly-Follows Graph constructed from an event log.

    Nodes are activity names. Edges carry frequency counts and optional
    performance data (timing between consecutive activities).
    """

    edges: dict[tuple[str, str], DFGEdge] = field(default_factory=dict)
    start_activities: dict[str, int] = field(default_factory=dict)
    end_activities: dict[str, int] = field(default_factory=dict)
    activity_counts: dict[str, int] = field(default_factory=dict)

    @classmethod
    def from_event_log(cls, log: EventLog) -> DirectlyFollowsGraph:
        """Construct a DFG from an event log.

        For each trace, iterates over consecutive event pairs and records:
        - Directly-follows frequency (how often a is followed by b)
        - Time delta between events (for performance analysis)
        - Start/end activity counts
        - Overall activity occurrence counts

        Args:
            log: The event log to analyze.

        Returns:
            Populated DirectlyFollowsGraph.
        """
        # TODO: Implement DFG construction from event log
        # For each trace:
        #   - Record first activity as start activity
        #   - Record last activity as end activity
        #   - For each consecutive pair (events[i], events[i+1]):
        #     - Increment edge frequency
        #     - Accumulate time delta for performance DFG
        #   - Count each activity occurrence
        raise NotImplementedError

    @property
    def activities(self) -> set[str]:
        """Return the set of all activity names in the DFG."""
        # TODO: Implement — collect all unique activities from edges and activity_counts
        raise NotImplementedError

    def get_frequency(self, source: str, target: str) -> int:
        """Get the directly-follows frequency between two activities.

        Args:
            source: Source activity name.
            target: Target activity name.

        Returns:
            Frequency count, or 0 if the edge does not exist.
        """
        # TODO: Implement — look up edge in self.edges
        raise NotImplementedError

    def get_avg_duration(self, source: str, target: str) -> float:
        """Get the average duration (seconds) between two activities.

        Args:
            source: Source activity name.
            target: Target activity name.

        Returns:
            Average duration, or 0.0 if the edge does not exist.
        """
        # TODO: Implement — look up edge and return avg_duration
        raise NotImplementedError

    def filter_by_frequency(self, min_frequency: int) -> DirectlyFollowsGraph:
        """Create a filtered DFG keeping only edges above a frequency threshold.

        Args:
            min_frequency: Minimum edge frequency to retain.

        Returns:
            New DirectlyFollowsGraph with infrequent edges removed.
        """
        # TODO: Implement frequency-based filtering
        # - Keep edges where frequency >= min_frequency
        # - Recalculate activity_counts, start_activities, end_activities
        #   based on remaining edges
        raise NotImplementedError

    def filter_by_percentage(self, keep_percentage: float) -> DirectlyFollowsGraph:
        """Keep only the top N% most frequent edges.

        Args:
            keep_percentage: Fraction of edges to keep (0.0 to 1.0).

        Returns:
            New filtered DirectlyFollowsGraph.
        """
        # TODO: Implement percentage-based filtering
        # - Sort edges by frequency descending
        # - Keep top keep_percentage fraction
        raise NotImplementedError

    def to_adjacency_matrix(self) -> tuple[list[str], list[list[int]]]:
        """Convert the DFG to an adjacency matrix.

        Returns:
            Tuple of (activity_names, matrix) where matrix[i][j] is the
            frequency of activity_names[i] -> activity_names[j].
        """
        # TODO: Implement adjacency matrix conversion
        raise NotImplementedError

    def to_networkx(self) -> Any:
        """Convert the DFG to a NetworkX DiGraph.

        Returns:
            networkx.DiGraph with frequency and duration edge attributes.
        """
        # TODO: Implement NetworkX conversion
        # - Create nx.DiGraph
        # - Add edges with frequency and avg_duration attributes
        raise NotImplementedError

    def to_graphviz(
        self, measure: str = "frequency", min_edge_width: float = 1.0, max_edge_width: float = 5.0
    ) -> Any:
        """Render the DFG as a Graphviz Digraph.

        Args:
            measure: 'frequency' or 'performance' — determines edge labels and coloring.
            min_edge_width: Minimum edge width for visualization scaling.
            max_edge_width: Maximum edge width for visualization scaling.

        Returns:
            graphviz.Digraph object.
        """
        # TODO: Implement Graphviz visualization
        # - Nodes as rounded rectangles with activity name and count
        # - Edges labeled with frequency or average duration
        # - Edge width scaled by frequency (or duration)
        # - Color gradient from green (fast/infrequent) to red (slow/frequent)
        raise NotImplementedError

    def __repr__(self) -> str:
        return (
            f"DirectlyFollowsGraph(activities={len(self.activities)}, "
            f"edges={len(self.edges)})"
        )
