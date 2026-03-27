"""Z-score based anomaly detector using Welford's online algorithm."""

from __future__ import annotations

from dataclasses import dataclass

from socket_project.detection.detector import AnomalyDetector
from socket_project.models.messages import AnomalyScore, DataPoint
from socket_project.streaming.stream_processor import WindowStats


@dataclass
class WelfordState:
    """Running state for Welford's online mean/variance algorithm."""

    n: int = 0
    mean: float = 0.0
    m2: float = 0.0

    @property
    def variance(self) -> float:
        if self.n < 2:
            return 0.0
        return self.m2 / (self.n - 1)

    @property
    def std(self) -> float:
        return self.variance ** 0.5


class ZScoreDetector(AnomalyDetector):
    """Flags data points whose Z-score exceeds a configurable threshold.

    Uses Welford's online algorithm to maintain running mean and variance
    in O(1) space per update.
    """

    def __init__(self, threshold: float = 3.0) -> None:
        self.threshold = threshold
        self._state = WelfordState()

    @property
    def name(self) -> str:
        return "zscore"

    def detect(
        self,
        point: DataPoint,
        stats: WindowStats | None = None,
    ) -> AnomalyScore:
        """Compute Z-score for the point and flag if |z| > threshold.

        Updates running statistics via Welford's algorithm before scoring.
        """
        # TODO: Implement Welford's online update:
        #   1. Increment n
        #   2. Compute delta = value - old_mean
        #   3. Update mean: mean += delta / n
        #   4. Compute delta2 = value - new_mean
        #   5. Update m2: m2 += delta * delta2
        #   6. Compute z-score = (value - mean) / std (handle std == 0)
        #   7. Return AnomalyScore with is_anomaly = |z| > threshold
        raise NotImplementedError

    def reset(self) -> None:
        self._state = WelfordState()
