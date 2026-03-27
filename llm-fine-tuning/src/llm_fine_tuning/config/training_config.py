"""Training hyperparameters as validated Pydantic models.

Centralizes all training configuration with type checking, validation,
and sensible defaults for LoRA fine-tuning.
"""

from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class TrainingConfig(BaseModel):
    """Complete training configuration for fine-tuning.

    Attributes:
        model_name: HuggingFace model identifier.
        output_dir: Directory to save checkpoints and final model.
        num_train_epochs: Number of training epochs.
        per_device_train_batch_size: Batch size per GPU for training.
        per_device_eval_batch_size: Batch size per GPU for evaluation.
        gradient_accumulation_steps: Number of steps to accumulate before backward.
        learning_rate: Peak learning rate.
        weight_decay: L2 regularization factor.
        warmup_ratio: Fraction of total steps used for LR warmup.
        lr_scheduler_type: Learning rate scheduler type.
        max_seq_length: Maximum sequence length for tokenization.
        logging_steps: Log metrics every N steps.
        eval_steps: Run evaluation every N steps.
        save_steps: Save checkpoint every N steps.
        save_total_limit: Maximum number of checkpoints to keep.
        fp16: Use mixed-precision fp16 training.
        bf16: Use mixed-precision bf16 training.
        gradient_checkpointing: Trade compute for memory.
        seed: Random seed for reproducibility.
        report_to: Logging integrations (e.g., "wandb", "tensorboard").
    """

    model_name: str = "mistralai/Mistral-7B-v0.1"
    output_dir: Path = Path("./outputs")
    num_train_epochs: int = Field(default=3, ge=1, le=100)
    per_device_train_batch_size: int = Field(default=4, ge=1)
    per_device_eval_batch_size: int = Field(default=4, ge=1)
    gradient_accumulation_steps: int = Field(default=4, ge=1)
    learning_rate: float = Field(default=2e-4, gt=0, lt=1)
    weight_decay: float = Field(default=0.01, ge=0, lt=1)
    warmup_ratio: float = Field(default=0.03, ge=0, le=1)
    lr_scheduler_type: str = "cosine"
    max_seq_length: int = Field(default=2048, ge=128, le=32768)
    logging_steps: int = Field(default=10, ge=1)
    eval_steps: int = Field(default=50, ge=1)
    save_steps: int = Field(default=100, ge=1)
    save_total_limit: int = Field(default=3, ge=1)
    fp16: bool = False
    bf16: bool = True
    gradient_checkpointing: bool = True
    seed: int = 42
    report_to: list[str] = Field(default_factory=lambda: ["wandb"])

    @field_validator("lr_scheduler_type")
    @classmethod
    def validate_scheduler(cls, v: str) -> str:
        """Validate that the scheduler type is supported."""
        # TODO: Implement
        # Check against allowed values: linear, cosine, cosine_with_restarts,
        # polynomial, constant, constant_with_warmup
        raise NotImplementedError

    @field_validator("model_name")
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        """Validate model name is non-empty and looks like a HF identifier."""
        # TODO: Implement
        raise NotImplementedError

    def to_training_arguments(self) -> dict:
        """Convert to a dict suitable for HuggingFace TrainingArguments.

        Returns:
            Dict of keyword arguments for TrainingArguments().
        """
        # TODO: Implement
        # Map our fields to TrainingArguments parameter names
        raise NotImplementedError

    @property
    def effective_batch_size(self) -> int:
        """Calculate the effective batch size including gradient accumulation.

        Returns:
            per_device_train_batch_size * gradient_accumulation_steps
        """
        # TODO: Implement
        raise NotImplementedError
