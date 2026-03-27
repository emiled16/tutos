"""Time-series data producer that simulates sensor readings with anomaly injection."""

from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass, field
from typing import AsyncIterator

import numpy as np

from socket_project.models.messages import DataPoint


@dataclass
class AnomalyConfig:
    """Controls how and when anomalies are injected into the stream."""

    probability: float = 0.05
    magnitude_range: tuple[float, float] = (5.0, 15.0)


@dataclass
class ProducerConfig:
    """Configuration for the data producer."""

    metric_name: str = "cpu_usage"
    base_value: float = 50.0
    noise_std: float = 2.0
    trend_slope: float = 0.0
    seasonality_amplitude: float = 5.0
    seasonality_period: int = 100
    interval_seconds: float = 0.1
    anomaly_config: AnomalyConfig = field(default_factory=AnomalyConfig)


class DataProducer:
    """Generates synthetic time-series data points with optional anomaly injection.

    The signal is composed of:
      - A base value with optional linear trend
      - Sinusoidal seasonality
      - Gaussian noise
      - Randomly injected anomalies (spikes or dips)
    """

    def __init__(self, config: ProducerConfig | None = None) -> None:
        self.config = config or ProducerConfig()
        self._step: int = 0
        self._running: bool = False

    def _generate_value(self) -> tuple[float, bool]:
        """Generate the next data point value.

        Returns:
            A tuple of (value, is_injected_anomaly).
        """
        # TODO: Implement signal generation combining base value, trend,
        # seasonality (sinusoidal), and Gaussian noise. Then with probability
        # config.anomaly_config.probability, inject an anomaly by adding a
        # large positive or negative spike drawn from magnitude_range.
        # Return the final value and whether an anomaly was injected.
        raise NotImplementedError

    def generate_one(self) -> DataPoint:
        """Generate a single data point synchronously."""
        # TODO: Implement using _generate_value, increment _step,
        # and return a DataPoint with the current timestamp and metric_name.
        raise NotImplementedError

    async def stream(self) -> AsyncIterator[DataPoint]:
        """Yield data points at the configured interval indefinitely.

        Stops when ``stop()`` is called.
        """
        self._running = True
        try:
            while self._running:
                yield self.generate_one()
                await asyncio.sleep(self.config.interval_seconds)
        finally:
            self._running = False

    def stop(self) -> None:
        """Signal the producer to stop streaming."""
        self._running = False
