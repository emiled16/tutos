"""Social network analysis from event logs.

Mines organizational patterns: handover-of-work, working-together,
and subcontracting relationships between resources.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from process_mining.event_log import EventLog


@dataclass
class SocialNetwork:
    """A social network mined from event log resource interactions.

    Represents relationships between resources as a weighted directed graph.

    Attributes:
        resources: List of unique resource identifiers (defines matrix indices).
        matrix: Adjacency matrix where matrix[i][j] is the relationship
                strength between resources[i] and resources[j].
        metric_type: Type of social network metric used.
    """

    resources: list[str] = field(default_factory=list)
    matrix: np.ndarray = field(default_factory=lambda: np.array([]))
    metric_type: str = ""

    def get_weight(self, resource_a: str, resource_b: str) -> float:
        """Get the relationship weight between two resources.

        Args:
            resource_a: First resource identifier.
            resource_b: Second resource identifier.

        Returns:
            Weight value, or 0.0 if either resource is not found.
        """
        # TODO: Implement weight lookup via resource indices into matrix
        raise NotImplementedError

    def top_relationships(self, n: int = 10) -> list[tuple[str, str, float]]:
        """Return the top-N strongest relationships.

        Args:
            n: Number of top relationships to return.

        Returns:
            List of (resource_a, resource_b, weight) tuples sorted by weight descending.
        """
        # TODO: Implement — flatten matrix, sort, return top N with resource names
        raise NotImplementedError

    def to_networkx(self) -> Any:
        """Convert the social network to a NetworkX DiGraph.

        Returns:
            networkx.DiGraph with weighted edges between resources.
        """
        # TODO: Implement NetworkX conversion
        # - Create nx.DiGraph
        # - Add edges with weight attribute from matrix
        raise NotImplementedError


@dataclass
class CentralityMetrics:
    """Graph centrality metrics for resources in a social network.

    Attributes:
        degree_centrality: Fraction of resources each resource connects to.
        betweenness_centrality: Fraction of shortest paths passing through each resource.
        closeness_centrality: Inverse average distance to all other resources.
    """

    degree_centrality: dict[str, float] = field(default_factory=dict)
    betweenness_centrality: dict[str, float] = field(default_factory=dict)
    closeness_centrality: dict[str, float] = field(default_factory=dict)


def handover_of_work(log: EventLog, normalize: bool = False) -> SocialNetwork:
    """Build a handover-of-work social network.

    Entry (i, j) counts how often resource i's activity is directly
    followed by resource j's activity within the same case. Reveals
    work delegation and handoff patterns.

    Args:
        log: The event log to analyze.
        normalize: If True, normalize matrix rows to sum to 1.0.

    Returns:
        SocialNetwork with handover-of-work metric.
    """
    # TODO: Implement handover-of-work network construction
    # 1. Collect unique resources from the log
    # 2. For each trace, for each consecutive event pair (e_i, e_{i+1}):
    #    - If both have resources and resources differ: increment matrix[resource_i][resource_j]
    # 3. Optionally normalize each row
    raise NotImplementedError


def working_together(log: EventLog, normalize: bool = False) -> SocialNetwork:
    """Build a working-together social network.

    Entry (i, j) counts how often resources i and j both appear in the
    same case. Identifies teams that frequently collaborate.

    Args:
        log: The event log to analyze.
        normalize: If True, normalize by number of cases.

    Returns:
        SocialNetwork with working-together metric.
    """
    # TODO: Implement working-together network construction
    # 1. Collect unique resources
    # 2. For each trace, find all unique resources in that trace
    # 3. For each pair of resources in the trace: increment matrix[i][j] and matrix[j][i]
    # 4. Optionally normalize
    raise NotImplementedError


def subcontracting(log: EventLog, normalize: bool = False) -> SocialNetwork:
    """Build a subcontracting social network.

    Entry (i, j) counts how often resource i delegates work to resource j
    and gets it back: pattern resource_i → resource_j → resource_i within
    a trace. May indicate rework or approval loops.

    Args:
        log: The event log to analyze.
        normalize: If True, normalize by total pattern occurrences.

    Returns:
        SocialNetwork with subcontracting metric.
    """
    # TODO: Implement subcontracting network construction
    # 1. Collect unique resources
    # 2. For each trace, look for patterns: event[k].resource = r_i,
    #    event[k+1].resource = r_j, event[k+2].resource = r_i
    #    (where r_i != r_j) → increment matrix[r_i][r_j]
    # 3. Optionally normalize
    raise NotImplementedError


def compute_centrality(network: SocialNetwork) -> CentralityMetrics:
    """Compute centrality metrics for a social network.

    Uses NetworkX to calculate degree, betweenness, and closeness centrality.

    Args:
        network: The social network to analyze.

    Returns:
        CentralityMetrics with centrality scores for each resource.
    """
    # TODO: Implement centrality computation using NetworkX
    # 1. G = network.to_networkx()
    # 2. degree = nx.degree_centrality(G)
    # 3. betweenness = nx.betweenness_centrality(G, weight='weight')
    # 4. closeness = nx.closeness_centrality(G)
    # 5. Return CentralityMetrics
    raise NotImplementedError
