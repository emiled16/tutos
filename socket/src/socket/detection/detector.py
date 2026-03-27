"""Abstract interface for online anomaly detectors."""

from __future__ import annotations

from abc import ABC, abstractmethod

from socket_project.models.messages import AnomalyScore, DataPoint
from socket_project.streaming.stream_processor import WindowStats


class AnomalyDetector(ABC):
    """Base class for all anomaly detectors.

    Each detector receives a DataPoint and optional WindowStats, updates its
    internal state, and returns an AnomalyScore indicating whether the point
    is anomalous.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name identifying this detector."""
        ...

    @abstractmethod
    def detect(
        self,
        point: DataPoint,
        stats: WindowStats | None = None,
    ) -> AnomalyScore:
        """Evaluate a single data point and return an anomaly score.

        Args:
            point: The incoming data point.
            stats: Optional windowed statistics for context.

        Returns:
            An AnomalyScore with the detection result.
        """
        ...

    @abstractmethod
    def reset(self) -> None:
        """Reset the detector's internal state."""
        ...
