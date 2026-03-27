"""Tests for anomaly detection algorithms."""

from __future__ import annotations

from datetime import datetime

import numpy as np
import pytest

from socket_project.detection.ewma_detector import EWMADetector
from socket_project.detection.isolation_forest_detector import (
    IsolationForestConfig,
    IsolationForestDetector,
)
from socket_project.detection.zscore_detector import ZScoreDetector
from socket_project.models.messages import DataPoint


def _make_point(value: float, metric: str = "test_metric") -> DataPoint:
    return DataPoint(timestamp=datetime.utcnow(), metric_name=metric, value=value)


class TestZScoreDetector:
    """Tests for Z-score based anomaly detection."""

    @pytest.fixture
    def detector(self) -> ZScoreDetector:
        return ZScoreDetector(threshold=3.0)

    def test_normal_points_are_not_anomalous(self, detector: ZScoreDetector) -> None:
        # TODO: Implement — feed 100 points drawn from N(50, 2),
        # assert none are flagged as anomalous (after warmup).
        pass

    def test_extreme_point_is_flagged(self, detector: ZScoreDetector) -> None:
        # TODO: Implement — feed 100 normal points, then feed a point
        # at mean + 10*std. Assert it is flagged as anomalous.
        pass

    def test_welford_mean_converges(self, detector: ZScoreDetector) -> None:
        # TODO: Implement — feed known values, verify the running mean
        # matches np.mean of the same values.
        pass

    def test_welford_std_converges(self, detector: ZScoreDetector) -> None:
        # TODO: Implement — feed known values, verify the running std
        # matches np.std(values, ddof=1).
        pass

    def test_reset_clears_state(self, detector: ZScoreDetector) -> None:
        # TODO: Implement — feed some points, reset, verify state is
        # back to initial (n=0, mean=0, m2=0).
        pass


class TestEWMADetector:
    """Tests for EWMA control chart detector."""

    @pytest.fixture
    def detector(self) -> EWMADetector:
        return EWMADetector(span=20, control_limit_width=3.0, warmup_period=30)

    def test_warmup_period_is_not_anomalous(self, detector: EWMADetector) -> None:
        # TODO: Implement — feed fewer than warmup_period points,
        # assert none are flagged as anomalous.
        pass

    def test_shift_after_warmup_is_detected(self, detector: EWMADetector) -> None:
        # TODO: Implement — feed warmup_period normal points, then
        # feed a sustained shift (e.g., mean + 5*std for 10 points).
        # Assert at least some are flagged.
        pass

    def test_reset_clears_ewma_state(self, detector: EWMADetector) -> None:
        # TODO: Implement — feed points, reset, verify internal state
        # is cleared (ewma is None, step is 0).
        pass


class TestIsolationForestDetector:
    """Tests for streaming Isolation Forest detector."""

    @pytest.fixture
    def detector(self) -> IsolationForestDetector:
        config = IsolationForestConfig(
            window_size=200,
            retrain_interval=50,
            contamination=0.05,
            random_state=42,
        )
        return IsolationForestDetector(config)

    def test_no_model_before_first_retrain(self, detector: IsolationForestDetector) -> None:
        # TODO: Implement — feed fewer than retrain_interval points,
        # assert all return is_anomaly=False (no model trained yet).
        pass

    def test_outlier_detected_after_training(self, detector: IsolationForestDetector) -> None:
        # TODO: Implement — feed enough normal points to trigger
        # retraining, then feed a clear outlier (e.g., value=1000
        # when training data is N(50, 2)). Assert it is flagged.
        pass

    def test_reset_clears_model_and_window(self, detector: IsolationForestDetector) -> None:
        # TODO: Implement — feed points, reset, verify _model is None
        # and _window is empty.
        pass
