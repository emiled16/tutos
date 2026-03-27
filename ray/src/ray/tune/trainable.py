"""Trainable function and class for Ray Tune."""

from __future__ import annotations

from typing import Any

import torch
import torch.nn as nn
from ray import tune
from ray.train import Checkpoint


def build_model(config: dict[str, Any]) -> nn.Module:
    """Construct a PyTorch model from a Tune config dict.

    The model is a simple feed-forward network whose depth and width
    are controlled by ``config["num_layers"]`` and ``config["hidden_size"]``.

    Args:
        config: Hyperparameter dict containing at least ``num_layers``,
            ``hidden_size``, ``dropout``, and ``input_size``.

    Returns:
        An ``nn.Module`` ready for training.
    """
    # TODO: Build an nn.Sequential with config["num_layers"] hidden layers,
    #       each of width config["hidden_size"], using ReLU activations and
    #       config["dropout"] dropout. Input size comes from config["input_size"]
    #       and output size from config["output_size"].
    raise NotImplementedError


def build_optimizer(model: nn.Module, config: dict[str, Any]) -> torch.optim.Optimizer:
    """Create an optimizer from a Tune config dict.

    Supports ``adam``, ``sgd``, and ``adamw``.

    Args:
        model: The model whose parameters to optimize.
        config: Must contain ``optimizer``, ``learning_rate``, ``weight_decay``,
            and optionally ``momentum`` (for SGD).

    Returns:
        A PyTorch optimizer instance.
    """
    # TODO: Dispatch on config["optimizer"] to construct the appropriate
    #       torch.optim optimizer with learning_rate and weight_decay
    raise NotImplementedError


def trainable_function(config: dict[str, Any]) -> None:
    """A function-based trainable for Ray Tune.

    This function:
      1. Builds a model and optimizer from *config*.
      2. Loads training and validation data.
      3. Trains for ``config["epochs"]`` epochs.
      4. Reports ``train_loss`` and ``val_loss`` to Tune each epoch.
      5. Saves a checkpoint of the best model.

    Args:
        config: Hyperparameter dict (merged search space + fixed params).
    """
    # TODO: Implement the training loop:
    #   1. Call build_model(config) and build_optimizer(model, config)
    #   2. Load data (use config["data_path"] or synthetic data for testing)
    #   3. For each epoch up to config["epochs"]:
    #      a. Train one epoch, compute train_loss
    #      b. Evaluate on validation set, compute val_loss
    #      c. Report metrics with ray.train.report({"train_loss": ..., "val_loss": ...})
    #      d. Save checkpoint via Checkpoint.from_directory when val_loss improves
    raise NotImplementedError


class TrainableClass(tune.Trainable):
    """A class-based trainable for Ray Tune with checkpoint support.

    Use this when you need fine-grained control over setup, training steps,
    and checkpoint save/load lifecycle.
    """

    def setup(self, config: dict[str, Any]) -> None:
        """Initialize model, optimizer, and data.

        Args:
            config: Hyperparameter dict.
        """
        # TODO: Store config, build model and optimizer, load data,
        #       initialize best_val_loss tracking
        raise NotImplementedError

    def step(self) -> dict[str, float]:
        """Execute one training step (epoch) and return metrics.

        Returns:
            Dict with at least ``train_loss`` and ``val_loss``.
        """
        # TODO: Run one epoch of training and validation, return metrics dict
        raise NotImplementedError

    def save_checkpoint(self, tmp_checkpoint_dir: str) -> str:
        """Save model state to *tmp_checkpoint_dir*.

        Args:
            tmp_checkpoint_dir: Directory to write checkpoint files.

        Returns:
            Path to the checkpoint directory.
        """
        # TODO: Save model and optimizer state_dict to tmp_checkpoint_dir
        raise NotImplementedError

    def load_checkpoint(self, checkpoint_dir: str) -> None:
        """Restore model state from a checkpoint.

        Args:
            checkpoint_dir: Directory containing checkpoint files.
        """
        # TODO: Load model and optimizer state_dict from checkpoint_dir
        raise NotImplementedError
