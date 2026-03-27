"""Alert management with deduplication, severity classification, and cooldown."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from socket_project.models.messages import Alert, AnomalyScore, DataPoint, Severity


@dataclass
class AlertConfig:
    """Configuration for alert management behavior."""

    cooldown_seconds: float = 60.0
    severity_thresholds: dict[Severity, float] = field(
        default_factory=lambda: {
            Severity.LOW: 2.0,
            Severity.MEDIUM: 3.0,
            Severity.HIGH: 4.0,
            Severity.CRITICAL: 5.0,
        }
    )


@dataclass
class AlertRecord:
    """Tracks the last alert fired for a (metric, detector) pair."""

    last_fired: datetime
    alert: Alert
    count: int = 1


class AlertManager:
    """Manages alert lifecycle: creation, severity classification,
    deduplication, and cooldown enforcement.

    Deduplication key is (metric_name, detector_name). If an alert was
    fired for the same key within the cooldown window, the new alert is
    suppressed.
    """

    def __init__(self, config: AlertConfig | None = None) -> None:
        self.config = config or AlertConfig()
        self._alert_history: dict[tuple[str, str], AlertRecord] = {}

    def classify_severity(self, score: float) -> Severity:
        """Map an anomaly score magnitude to a severity level.

        Iterates severity thresholds from highest to lowest and returns
        the first level whose threshold the score exceeds.
        """
        # TODO: Implement — compare abs(score) against thresholds in
        # descending order (CRITICAL → HIGH → MEDIUM → LOW).
        # Return Severity.LOW as fallback.
        raise NotImplementedError

    def _is_in_cooldown(self, key: tuple[str, str], now: datetime) -> bool:
        """Check if the given (metric, detector) pair is in cooldown."""
        # TODO: Implement — look up key in _alert_history, compare
        # now - last_fired against cooldown_seconds. Return True if
        # still in cooldown.
        raise NotImplementedError

    def process(
        self,
        point: DataPoint,
        anomaly_score: AnomalyScore,
    ) -> Alert | None:
        """Evaluate an anomaly score and produce an Alert if warranted.

        Returns None if the score is not anomalous or if the alert is
        suppressed by the cooldown window.
        """
        # TODO: Implement:
        #   1. If not anomaly_score.is_anomaly, return None
        #   2. Build dedup key = (point.metric_name, anomaly_score.detector_name)
        #   3. If in cooldown, increment count on existing record and return None
        #   4. Classify severity from the score
        #   5. Create an Alert with a uuid, severity, and descriptive message
        #   6. Store an AlertRecord in _alert_history
        #   7. Return the Alert
        raise NotImplementedError

    def acknowledge(self, alert_id: str) -> bool:
        """Mark an alert as acknowledged. Returns True if found."""
        # TODO: Implement — search _alert_history for the alert_id,
        # set acknowledged = True, return whether it was found.
        raise NotImplementedError

    def get_active_alerts(self) -> list[Alert]:
        """Return all un-acknowledged alerts."""
        return [
            record.alert
            for record in self._alert_history.values()
            if not record.alert.acknowledged
        ]
