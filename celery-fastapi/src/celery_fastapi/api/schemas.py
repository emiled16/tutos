"""Pydantic request/response schemas for the ML task queue API."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ModelType(str, Enum):
    """Supported model types for training."""

    LINEAR_REGRESSION = "linear_regression"
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    NEURAL_NETWORK = "neural_network"


class TaskStatus(str, Enum):
    """Possible task states in the system."""

    PENDING = "PENDING"
    STARTED = "STARTED"
    PROGRESS = "PROGRESS"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    REVOKED = "REVOKED"
    RETRY = "RETRY"


class TrainingRequest(BaseModel):
    """Request schema for submitting a model training job.

    Attributes:
        dataset_path: Path or identifier for the training dataset.
        model_type: The type of ML model to train.
        hyperparameters: Model-specific hyperparameters.
        test_size: Fraction of data to reserve for evaluation.
        random_seed: Seed for reproducibility.
    """

    dataset_path: str
    model_type: ModelType = ModelType.RANDOM_FOREST
    hyperparameters: dict[str, int | float | str | bool] = Field(default_factory=dict)
    test_size: float = Field(default=0.2, ge=0.0, le=0.5)
    random_seed: int = 42


class TaskSubmitResponse(BaseModel):
    """Response returned when a task is successfully submitted.

    Attributes:
        task_id: Unique identifier for the submitted task.
        status: Initial status of the task (always PENDING).
        message: Human-readable confirmation message.
    """

    task_id: str
    status: TaskStatus = TaskStatus.PENDING
    message: str = "Task submitted successfully"


class TaskStatusResponse(BaseModel):
    """Response for task status queries.

    Attributes:
        task_id: The task identifier.
        status: Current task state.
        progress: Completion percentage (0-100) if available.
        current_step: Description of what the task is currently doing.
        created_at: When the task was submitted.
    """

    task_id: str
    status: TaskStatus
    progress: float | None = None
    current_step: str | None = None
    created_at: datetime | None = None


class TaskResultResponse(BaseModel):
    """Response containing completed task results.

    Attributes:
        task_id: The task identifier.
        status: Final task state (SUCCESS or FAILURE).
        result: The task output (model metrics, etc.).
        error: Error message if the task failed.
        duration_seconds: How long the task took to complete.
    """

    task_id: str
    status: TaskStatus
    result: dict | None = None
    error: str | None = None
    duration_seconds: float | None = None


class ProgressUpdate(BaseModel):
    """WebSocket message schema for real-time progress updates.

    Attributes:
        task_id: The task being tracked.
        status: Current task state.
        progress: Completion percentage (0-100).
        current_step: What the task is doing right now.
        message: Optional detail message.
    """

    task_id: str
    status: TaskStatus
    progress: float = 0.0
    current_step: str = ""
    message: str = ""
