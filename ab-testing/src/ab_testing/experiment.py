"""Experiment configuration and lifecycle management for A/B tests."""

from __future__ import annotations

from dataclasses import field
from datetime import datetime
from enum import Enum

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field


class MetricType(str, Enum):
    """Type of metric being tracked in the experiment."""

    CONTINUOUS = "continuous"
    BINARY = "binary"
    COUNT = "count"


class ExperimentStatus(str, Enum):
    """Current status of an experiment."""

    DRAFT = "draft"
    RUNNING = "running"
    STOPPED = "stopped"
    COMPLETED = "completed"


class Variant(BaseModel):
    """A single variant (control or treatment) in an A/B test."""

    name: str
    description: str = ""
    traffic_fraction: float = Field(ge=0.0, le=1.0, default=0.5)
    observations: list[float] = Field(default_factory=list)

    @property
    def sample_size(self) -> int:
        """Return the number of observations collected."""
        return len(self.observations)

    @property
    def mean(self) -> float:
        """Return the mean of observations."""
        # TODO: Implement mean calculation. Return 0.0 if no observations.
        raise NotImplementedError

    @property
    def variance(self) -> float:
        """Return the sample variance (ddof=1) of observations."""
        # TODO: Implement variance calculation. Return 0.0 if fewer than 2 observations.
        raise NotImplementedError


class ExperimentConfig(BaseModel):
    """Configuration for an A/B test experiment."""

    name: str
    description: str = ""
    metric_name: str = "conversion_rate"
    metric_type: MetricType = MetricType.BINARY
    significance_level: float = Field(default=0.05, ge=0.001, le=0.5)
    power: float = Field(default=0.80, ge=0.5, le=0.99)
    minimum_detectable_effect: float = Field(default=0.02, gt=0.0)
    max_duration_days: int = Field(default=14, ge=1)


class Experiment:
    """Manages the lifecycle of an A/B test experiment.

    An experiment contains a control and treatment variant, tracks
    observations, and determines when the test has reached significance
    or the maximum duration.
    """

    def __init__(self, config: ExperimentConfig) -> None:
        self.config = config
        self.control = Variant(name="control")
        self.treatment = Variant(name="treatment")
        self.status = ExperimentStatus.DRAFT
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None

    def start(self) -> None:
        """Start the experiment and record the start time.

        Raises:
            ValueError: If the experiment is not in DRAFT status.
        """
        # TODO: Implement experiment start logic.
        # - Validate that status is DRAFT
        # - Set status to RUNNING
        # - Record start_time as datetime.utcnow()
        raise NotImplementedError

    def stop(self, reason: str = "") -> None:
        """Stop the experiment early.

        Args:
            reason: Optional reason for stopping the experiment.

        Raises:
            ValueError: If the experiment is not in RUNNING status.
        """
        # TODO: Implement experiment stop logic.
        # - Validate that status is RUNNING
        # - Set status to STOPPED
        # - Record end_time
        raise NotImplementedError

    def add_observation(self, variant_name: str, value: float) -> None:
        """Add a single observation to the specified variant.

        Args:
            variant_name: Either "control" or "treatment".
            value: The observed metric value.

        Raises:
            ValueError: If variant_name is invalid or experiment is not running.
        """
        # TODO: Implement observation recording.
        # - Validate experiment is RUNNING
        # - Validate variant_name is "control" or "treatment"
        # - Append value to the correct variant's observations
        raise NotImplementedError

    def add_observations_batch(
        self, variant_name: str, values: list[float]
    ) -> None:
        """Add a batch of observations to the specified variant.

        Args:
            variant_name: Either "control" or "treatment".
            values: List of observed metric values.
        """
        # TODO: Implement batch observation recording.
        raise NotImplementedError

    def is_complete(self) -> bool:
        """Check if the experiment has reached its maximum duration.

        Returns:
            True if the experiment has run for max_duration_days or more.
        """
        # TODO: Implement duration check.
        # - Return False if experiment hasn't started
        # - Compare elapsed time against max_duration_days
        raise NotImplementedError

    def summary(self) -> dict:
        """Return a summary of the experiment state.

        Returns:
            Dictionary with experiment name, status, sample sizes,
            means, and elapsed time.
        """
        # TODO: Implement summary generation.
        # Include: name, status, control/treatment sample sizes and means,
        # elapsed time in hours, config parameters
        raise NotImplementedError
