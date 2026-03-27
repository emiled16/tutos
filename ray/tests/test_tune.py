"""Tests for the Ray Tune hyperparameter tuning pipeline."""

from __future__ import annotations

import pytest

from ray_project.tune.search_space import SearchSpaceConfig, build_search_space
from ray_project.tune.scheduler import SchedulerType, create_scheduler
from ray_project.tune.trainable import build_model, build_optimizer
from ray_project.tune.tuner import TunerConfig


class TestSearchSpace:
    """Validate search space construction."""

    def test_build_search_space_returns_all_keys(self) -> None:
        """build_search_space should return a dict with one key per hyperparameter."""
        # TODO: Instantiate a default SearchSpaceConfig, call build_search_space,
        #       assert the result contains expected keys (learning_rate, batch_size, etc.)
        raise NotImplementedError

    def test_build_search_space_custom_ranges(self) -> None:
        """Custom ranges in SearchSpaceConfig should propagate to tune samplers."""
        # TODO: Create a SearchSpaceConfig with non-default ranges, build the space,
        #       verify the sampler bounds match
        raise NotImplementedError


class TestScheduler:
    """Validate scheduler factory."""

    @pytest.mark.parametrize("stype", list(SchedulerType))
    def test_create_scheduler_returns_scheduler(self, stype: SchedulerType) -> None:
        """create_scheduler should return a TrialScheduler for each type."""
        # TODO: Call create_scheduler with each SchedulerType, assert the
        #       result is an instance of TrialScheduler
        raise NotImplementedError

    def test_create_scheduler_invalid_type_raises(self) -> None:
        """An invalid scheduler type should raise ValueError."""
        # TODO: Pass an invalid scheduler_type and assert ValueError is raised
        raise NotImplementedError


class TestTrainable:
    """Validate model and optimizer construction."""

    def test_build_model_output_shape(self) -> None:
        """build_model should produce a model whose output matches output_size."""
        # TODO: Build a model with known config, pass a dummy input tensor,
        #       assert output shape is (batch, output_size)
        raise NotImplementedError

    def test_build_optimizer_types(self) -> None:
        """build_optimizer should return the correct optimizer class."""
        # TODO: For each optimizer name (adam, sgd, adamw), build the optimizer
        #       and verify its class
        raise NotImplementedError


class TestTunerConfig:
    """Validate TunerConfig defaults."""

    def test_defaults(self) -> None:
        """TunerConfig should have sensible defaults."""
        config = TunerConfig()
        assert config.metric == "val_loss"
        assert config.mode == "min"
        assert config.num_samples == 50
