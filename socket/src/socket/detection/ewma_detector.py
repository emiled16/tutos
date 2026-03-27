"""EWMA (Exponentially Weighted Moving Average) control chart detector."""

from __future__ import annotations

from dataclasses import dataclass, field

from socket_project.detection.detector import AnomalyDetector
from socket_project.models.messages import AnomalyScore, DataPoint
from socket_project.streaming.stream_processor import WindowStats


@dataclass
class EWMAState:
    """Internal state for the EWMA control chart."""

    ewma: float | None = None
    target_mean: float | None = None
    target_std: float | None = None
    step: int = 0


class EWMADetector(AnomalyDetector):
    """Detects anomalies using EWMA control chart methodology.

    The EWMA statistic is:
        EWMA_t = λ * x_t + (1 - λ) * EWMA_{t-1}

    Control limits:
        UCL/LCL = μ₀ ± L * σ * sqrt(λ/(2-λ) * [1-(1-λ)^{2t}])

    where L is the control limit width factor and λ = 2/(span+1).
    """

    def __init__(
        self,
        span: int = 20,
        control_limit_width: float = 3.0,
        warmup_period: int = 30,
    ) -> None:
        self.lambda_: float = 2.0 / (span + 1)
        self.control_limit_width = control_limit_width
        self.warmup_period = warmup_period
        self._state = EWMAState()
        self._warmup_values: list[float] = []

    @property
    def name(self) -> str:
        return "ewma"

    def _initialize_from_warmup(self) -> None:
        """Set target mean and std from warmup observations."""
        # TODO: Implement — compute mean and std of self._warmup_values,
        # store them in self._state.target_mean and self._state.target_std,
        # and initialize self._state.ewma to the mean.
        raise NotImplementedError

    def detect(
        self,
        point: DataPoint,
        stats: WindowStats | None = None,
    ) -> AnomalyScore:
        """Update EWMA and check if the point violates control limits.

        During the warmup period, accumulates values and returns non-anomalous.
        After warmup, applies the EWMA recurrence and compares against
        dynamically computed UCL/LCL.
        """
        # TODO: Implement:
        #   1. If in warmup period, collect values and call _initialize_from_warmup
        #      when warmup_period is reached. Return non-anomalous score.
        #   2. After warmup:
        #      a. Update EWMA: ewma = λ * value + (1-λ) * ewma
        #      b. Increment step
        #      c. Compute control limits using the EWMA formula
        #      d. Check if ewma is outside [LCL, UCL]
        #      e. Return AnomalyScore
        raise NotImplementedError

    def reset(self) -> None:
        self._state = EWMAState()
        self._warmup_values.clear()
