"""Tests for distributed training with Ray Train."""

from __future__ import annotations

import pytest

from ray_project.train.trainer import TrainerConfig, create_trainer
from ray_project.train.callbacks import MetricsLogger, MetricsRecord, CheckpointManager


class TestTrainerConfig:
    """Validate TrainerConfig construction."""

    def test_defaults(self) -> None:
        """TrainerConfig should have sensible defaults."""
        config = TrainerConfig()
        assert config.num_workers == 2
        assert config.use_gpu is False
        assert config.epochs == 10

    def test_custom_config(self) -> None:
        """TrainerConfig should accept custom values."""
        config = TrainerConfig(num_workers=4, use_gpu=True, epochs=50)
        assert config.num_workers == 4
        assert config.use_gpu is True
        assert config.epochs == 50


class TestMetricsLogger:
    """Validate metrics logging and best-epoch retrieval."""

    def test_log_appends_record(self, tmp_path: pytest.TempPathFactory) -> None:
        """Logging a record should add it to history."""
        # TODO: Create a MetricsLogger with tmp_path, log a MetricsRecord,
        #       assert len(logger.history) == 1
        raise NotImplementedError

    def test_get_best_epoch_min(self, tmp_path: pytest.TempPathFactory) -> None:
        """get_best_epoch(mode='min') should return the epoch with lowest val_loss."""
        # TODO: Log several records with different val_loss values, call
        #       get_best_epoch, assert the returned record has the minimum val_loss
        raise NotImplementedError

    def test_get_best_epoch_empty_raises(self, tmp_path: pytest.TempPathFactory) -> None:
        """get_best_epoch on empty history should raise ValueError."""
        # TODO: Create a fresh MetricsLogger, call get_best_epoch, expect ValueError
        raise NotImplementedError


class TestCheckpointManager:
    """Validate checkpoint save and prune logic."""

    def test_should_save_when_under_limit(self, tmp_path: pytest.TempPathFactory) -> None:
        """should_save should return True when fewer than keep_top_k checkpoints exist."""
        # TODO: Create a CheckpointManager with keep_top_k=3, assert should_save
        #       returns True for the first checkpoint
        raise NotImplementedError

    def test_prune_keeps_top_k(self, tmp_path: pytest.TempPathFactory) -> None:
        """After saving more than keep_top_k checkpoints, only the best K remain."""
        # TODO: Save keep_top_k + 2 checkpoints with varying metrics, verify
        #       that only keep_top_k checkpoint files exist on disk
        raise NotImplementedError

    @pytest.mark.integration
    def test_create_trainer_builds_torch_trainer(self, ray_cluster: None) -> None:
        """create_trainer should return a TorchTrainer instance."""
        # TODO: Call create_trainer with a default TrainerConfig, assert
        #       the result is a TorchTrainer
        raise NotImplementedError
