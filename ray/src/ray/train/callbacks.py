"""Training callbacks for checkpointing and logging."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class MetricsRecord:
    """A single snapshot of training metrics for one epoch.

    Attributes:
        epoch: The epoch number (0-indexed).
        train_loss: Training loss.
        val_loss: Validation loss.
        extra: Any additional metrics (accuracy, learning rate, etc.).
    """

    epoch: int
    train_loss: float
    val_loss: float
    extra: dict[str, float] = field(default_factory=dict)


class MetricsLogger:
    """Accumulates per-epoch metrics and persists them to a JSON file."""

    def __init__(self, log_dir: str | Path) -> None:
        """
        Args:
            log_dir: Directory where the metrics JSON will be written.
        """
        self.log_dir = Path(log_dir)
        self.history: list[MetricsRecord] = []

    def log(self, record: MetricsRecord) -> None:
        """Append a metrics record and flush to disk.

        Args:
            record: The epoch's metrics.
        """
        # TODO: Append record to self.history, create log_dir if needed,
        #       and write the full history as JSON to log_dir / "metrics.json"
        raise NotImplementedError

    def get_best_epoch(self, metric: str = "val_loss", mode: str = "min") -> MetricsRecord:
        """Return the record with the best value for *metric*.

        Args:
            metric: Attribute name on :class:`MetricsRecord` (or key in ``extra``).
            mode: ``"min"`` or ``"max"``.

        Returns:
            The :class:`MetricsRecord` for the best epoch.

        Raises:
            ValueError: If no metrics have been logged.
        """
        # TODO: Search self.history for the record with the best value of
        #       the given metric. Support both direct attributes and extra keys.
        raise NotImplementedError


class CheckpointManager:
    """Manages model checkpoint saving with a configurable keep policy."""

    def __init__(
        self,
        checkpoint_dir: str | Path,
        keep_top_k: int = 3,
        metric: str = "val_loss",
        mode: str = "min",
    ) -> None:
        """
        Args:
            checkpoint_dir: Base directory for checkpoints.
            keep_top_k: Number of best checkpoints to retain.
            metric: Metric used to rank checkpoints.
            mode: ``"min"`` or ``"max"``.
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.keep_top_k = keep_top_k
        self.metric = metric
        self.mode = mode
        self.checkpoints: list[dict[str, Any]] = []

    def should_save(self, metrics: dict[str, float]) -> bool:
        """Decide whether the current metrics warrant a new checkpoint.

        Args:
            metrics: Current epoch metrics.

        Returns:
            True if a checkpoint should be saved.
        """
        # TODO: Return True if we have fewer than keep_top_k checkpoints or
        #       the current metric value is better than the worst kept checkpoint
        raise NotImplementedError

    def save(self, state_dict: dict[str, Any], metrics: dict[str, float], epoch: int) -> Path:
        """Persist a checkpoint and prune old ones beyond keep_top_k.

        Args:
            state_dict: Model (and optimizer) state dict to save.
            metrics: Metrics associated with this checkpoint.
            epoch: Epoch number.

        Returns:
            Path to the saved checkpoint file.
        """
        # TODO: Save state_dict to checkpoint_dir / f"checkpoint_epoch_{epoch}.pt",
        #       record the checkpoint metadata, sort by metric, and delete
        #       checkpoints beyond keep_top_k
        raise NotImplementedError

    def get_best_checkpoint_path(self) -> Path | None:
        """Return the path to the best checkpoint, or None if none exist."""
        # TODO: Return the path to the checkpoint with the best metric value
        raise NotImplementedError
