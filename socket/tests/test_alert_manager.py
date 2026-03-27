"""Tests for alert management, deduplication, and cooldown logic."""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from socket_project.alerting.alert_manager import AlertConfig, AlertManager
from socket_project.models.messages import AnomalyScore, DataPoint, Severity


def _make_point(value: float = 100.0, metric: str = "cpu_usage") -> DataPoint:
    return DataPoint(timestamp=datetime.utcnow(), metric_name=metric, value=value)


def _make_anomaly_score(
    score: float = 4.0,
    is_anomaly: bool = True,
    detector: str = "zscore",
    threshold: float = 3.0,
) -> AnomalyScore:
    return AnomalyScore(
        detector_name=detector,
        score=score,
        is_anomaly=is_anomaly,
        threshold=threshold,
    )


class TestAlertManager:
    """Tests for AlertManager alert lifecycle."""

    @pytest.fixture
    def manager(self) -> AlertManager:
        config = AlertConfig(cooldown_seconds=60.0)
        return AlertManager(config)

    def test_non_anomalous_score_returns_none(self, manager: AlertManager) -> None:
        # TODO: Implement — process a non-anomalous score, assert None is returned.
        pass

    def test_anomalous_score_produces_alert(self, manager: AlertManager) -> None:
        # TODO: Implement — process an anomalous score, assert an Alert
        # is returned with correct metric_name and detector_name.
        pass

    def test_duplicate_alert_in_cooldown_is_suppressed(self, manager: AlertManager) -> None:
        # TODO: Implement — process the same anomaly twice within
        # cooldown_seconds, assert the second returns None.
        pass

    def test_alert_after_cooldown_is_not_suppressed(self, manager: AlertManager) -> None:
        # TODO: Implement — process an anomaly, manually adjust the
        # _alert_history timestamp to be older than cooldown_seconds,
        # process again, assert a new Alert is returned.
        pass

    def test_different_metrics_are_independent(self, manager: AlertManager) -> None:
        # TODO: Implement — process anomalies for "cpu_usage" and
        # "memory_usage", assert both produce alerts (different dedup keys).
        pass

    def test_different_detectors_are_independent(self, manager: AlertManager) -> None:
        # TODO: Implement — process anomalies from "zscore" and "ewma"
        # for the same metric, assert both produce alerts.
        pass


class TestSeverityClassification:
    """Tests for severity level classification."""

    @pytest.fixture
    def manager(self) -> AlertManager:
        return AlertManager()

    def test_low_severity(self, manager: AlertManager) -> None:
        # TODO: Implement — classify a score of 2.5 (above LOW threshold
        # but below MEDIUM), assert Severity.LOW.
        pass

    def test_critical_severity(self, manager: AlertManager) -> None:
        # TODO: Implement — classify a score of 6.0 (above CRITICAL
        # threshold), assert Severity.CRITICAL.
        pass


class TestAlertAcknowledgement:
    """Tests for acknowledging alerts."""

    @pytest.fixture
    def manager(self) -> AlertManager:
        return AlertManager()

    def test_acknowledge_existing_alert(self, manager: AlertManager) -> None:
        # TODO: Implement — produce an alert, acknowledge it by ID,
        # assert acknowledge returns True and the alert is marked acknowledged.
        pass

    def test_acknowledge_nonexistent_alert(self, manager: AlertManager) -> None:
        # TODO: Implement — acknowledge a random ID, assert returns False.
        pass

    def test_get_active_alerts_excludes_acknowledged(self, manager: AlertManager) -> None:
        # TODO: Implement — produce an alert, acknowledge it, assert
        # get_active_alerts returns an empty list.
        pass
