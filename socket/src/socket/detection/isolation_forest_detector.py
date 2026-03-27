"""Online Isolation Forest detector using mini-batch retraining."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

import numpy as np
from sklearn.ensemble import IsolationForest

from socket_project.detection.detector import AnomalyDetector
from socket_project.models.messages import AnomalyScore, DataPoint
from socket_project.streaming.stream_processor import WindowStats


@dataclass
class IsolationForestConfig:
    """Configuration for the streaming Isolation Forest."""

    window_size: int = 500
    retrain_interval: int = 100
    contamination: float = 0.05
    n_estimators: int = 100
    random_state: int = 42
    score_threshold: float = -0.5


class IsolationForestDetector(AnomalyDetector):
    """Anomaly detector using Isolation Forest with periodic retraining.

    Maintains a sliding window of recent observations. Every
    ``retrain_interval`` points, the forest is retrained on the current
    window. Incoming points are scored against the latest model.
    """

    def __init__(self, config: IsolationForestConfig | None = None) -> None:
        self.config = config or IsolationForestConfig()
        self._window: deque[float] = deque(maxlen=self.config.window_size)
        self._model: IsolationForest | None = None
        self._points_since_retrain: int = 0

    @property
    def name(self) -> str:
        return "isolation_forest"

    def _retrain(self) -> None:
        """Retrain the Isolation Forest on the current window contents."""
        # TODO: Implement — convert self._window to a numpy array (reshape to
        # column vector), create a new IsolationForest with the config
        # parameters, fit it on the data, and store as self._model.
        # Reset _points_since_retrain to 0.
        raise NotImplementedError

    def detect(
        self,
        point: DataPoint,
        stats: WindowStats | None = None,
    ) -> AnomalyScore:
        """Score a data point against the current Isolation Forest model.

        Adds the point to the window, triggers retraining if due, and
        scores the point using the latest model. Returns non-anomalous
        if no model has been trained yet.
        """
        # TODO: Implement:
        #   1. Append point.value to the window
        #   2. Increment _points_since_retrain
        #   3. If retrain is due (enough points and window is large enough), retrain
        #   4. If no model exists yet, return non-anomalous score
        #   5. Score the point: model.decision_function([[value]])[0]
        #   6. is_anomaly = score < config.score_threshold
        #   7. Return AnomalyScore with the raw score and details
        raise NotImplementedError

    def reset(self) -> None:
        self._window.clear()
        self._model = None
        self._points_since_retrain = 0
