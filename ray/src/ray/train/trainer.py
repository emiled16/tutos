"""Distributed training with Ray Train (data parallel)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import torch
import torch.nn as nn
from ray.train import RunConfig, ScalingConfig
from ray.train.torch import TorchTrainer


@dataclass
class TrainerConfig:
    """Configuration for a distributed training run.

    Attributes:
        num_workers: Number of parallel training workers.
        use_gpu: Whether each worker should request a GPU.
        epochs: Total training epochs.
        batch_size_per_worker: Per-worker batch size (global = this × num_workers).
        learning_rate: Base learning rate (scaled linearly with num_workers).
        checkpoint_frequency: Save a checkpoint every N epochs.
        storage_path: Directory for run artifacts and checkpoints.
        experiment_name: Human-readable run name.
    """

    num_workers: int = 2
    use_gpu: bool = False
    epochs: int = 10
    batch_size_per_worker: int = 64
    learning_rate: float = 1e-3
    checkpoint_frequency: int = 5
    storage_path: str = "./ray_train_results"
    experiment_name: str = "distributed_training"


def train_loop_per_worker(config: dict[str, Any]) -> None:
    """Training loop executed on each Ray Train worker.

    This function runs inside a distributed context managed by Ray Train.
    It must:
      1. Build (or receive) the model and wrap it with
         ``ray.train.torch.prepare_model``.
      2. Build a DataLoader and wrap it with
         ``ray.train.torch.prepare_data_loader``.
      3. Run the training loop for ``config["epochs"]`` epochs.
      4. Report metrics and checkpoints via ``ray.train.report``.

    Args:
        config: Merged hyperparameter + infrastructure config dict.
    """
    # TODO: Implement the per-worker training loop:
    #   1. Build or deserialize the model, call prepare_model(model)
    #   2. Create a DataLoader, call prepare_data_loader(dataloader)
    #   3. Build optimizer (optionally apply linear LR scaling)
    #   4. For each epoch:
    #      a. Train one epoch
    #      b. Evaluate on validation data
    #      c. Report metrics and checkpoint via ray.train.report(
    #             metrics, checkpoint=Checkpoint.from_dict({...}))
    raise NotImplementedError


def create_trainer(
    trainer_config: TrainerConfig,
    train_loop_config: dict[str, Any] | None = None,
) -> TorchTrainer:
    """Build a :class:`TorchTrainer` from configuration.

    Args:
        trainer_config: Infrastructure and training settings.
        train_loop_config: Extra config merged into each worker's config dict.

    Returns:
        A configured ``TorchTrainer`` ready to call ``.fit()``.
    """
    # TODO: Build ScalingConfig from trainer_config (num_workers, use_gpu).
    #       Build RunConfig with storage_path, name, and checkpoint config.
    #       Merge train_loop_config with trainer_config fields.
    #       Return TorchTrainer(train_loop_per_worker, ...).
    raise NotImplementedError


def run_training(trainer: TorchTrainer) -> Any:
    """Execute a distributed training run.

    Args:
        trainer: A configured ``TorchTrainer``.

    Returns:
        The :class:`ray.train.Result` from the completed run.
    """
    # TODO: Call trainer.fit() and return the Result object
    raise NotImplementedError


def load_best_checkpoint(result: Any, model_cls: type[nn.Module], model_kwargs: dict[str, Any]) -> nn.Module:
    """Restore the best model from a training result's checkpoint.

    Args:
        result: The ``Result`` returned by ``trainer.fit()``.
        model_cls: The model class to instantiate.
        model_kwargs: Constructor arguments for the model.

    Returns:
        The model with weights loaded from the best checkpoint.
    """
    # TODO: Get the best checkpoint from result, load state_dict, apply to
    #       a freshly constructed model_cls(**model_kwargs), and return it
    raise NotImplementedError
