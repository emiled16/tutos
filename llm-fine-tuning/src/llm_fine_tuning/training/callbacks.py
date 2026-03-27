"""Custom training callbacks for logging, early stopping, and checkpointing.

Extends HuggingFace Trainer's callback system with domain-specific
logging and training control logic.
"""

import logging
from pathlib import Path
from typing import Any

from transformers import TrainerCallback, TrainerControl, TrainerState, TrainingArguments

logger = logging.getLogger(__name__)


class DetailedLoggingCallback(TrainerCallback):
    """Logs detailed training metrics at each logging step.

    Tracks loss trends, learning rate, GPU memory usage, and
    tokens processed.
    """

    def __init__(self, log_every_n_steps: int = 10) -> None:
        self.log_every_n_steps = log_every_n_steps
        self._loss_history: list[float] = []

    def on_log(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        logs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Called when the trainer logs metrics.

        Args:
            args: Training arguments.
            state: Current trainer state.
            control: Trainer control object.
            logs: Dict of logged metrics.
        """
        # TODO: Implement
        # 1. Extract loss, learning_rate, epoch from logs
        # 2. Track loss in _loss_history
        # 3. Log a formatted message with step, loss, lr, and loss trend
        raise NotImplementedError

    def on_epoch_end(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs: Any,
    ) -> None:
        """Called at the end of each epoch.

        Args:
            args: Training arguments.
            state: Current trainer state.
            control: Trainer control object.
        """
        # TODO: Implement
        # Log epoch summary with average loss for the epoch
        raise NotImplementedError


class EarlyStoppingOnPlateau(TrainerCallback):
    """Stop training when evaluation loss plateaus.

    More flexible than HuggingFace's built-in EarlyStoppingCallback:
    supports configurable patience and minimum delta.
    """

    def __init__(
        self,
        patience: int = 3,
        min_delta: float = 0.01,
    ) -> None:
        """Initialize early stopping.

        Args:
            patience: Number of evaluations to wait for improvement.
            min_delta: Minimum change in eval loss to qualify as improvement.
        """
        self.patience = patience
        self.min_delta = min_delta
        self._best_loss: float | None = None
        self._wait_count: int = 0

    def on_evaluate(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        metrics: dict[str, float] | None = None,
        **kwargs: Any,
    ) -> None:
        """Check if training should be stopped.

        Args:
            args: Training arguments.
            state: Current trainer state.
            control: Trainer control object (set should_training_stop=True to stop).
            metrics: Evaluation metrics dict.
        """
        # TODO: Implement
        # 1. Extract eval_loss from metrics
        # 2. Compare with best_loss - min_delta
        # 3. If improved: update best_loss, reset wait_count
        # 4. If not improved: increment wait_count
        # 5. If wait_count >= patience: set control.should_training_stop = True
        raise NotImplementedError


class CheckpointCallback(TrainerCallback):
    """Save best model checkpoint based on evaluation loss."""

    def __init__(self, output_dir: str | Path = "checkpoints/best") -> None:
        self.output_dir = Path(output_dir)
        self._best_loss: float | None = None

    def on_evaluate(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        metrics: dict[str, float] | None = None,
        model: Any = None,
        **kwargs: Any,
    ) -> None:
        """Save the model if evaluation loss improved.

        Args:
            args: Training arguments.
            state: Current trainer state.
            control: Trainer control object.
            metrics: Evaluation metrics.
            model: The model to save.
        """
        # TODO: Implement
        # 1. Extract eval_loss from metrics
        # 2. If this is the best loss so far, save the model adapter
        # 3. Log the checkpoint save event
        raise NotImplementedError
