"""Celery task definitions for ML training workflows.

Each task represents a stage in the ML pipeline:
preprocess_data → train_model → evaluate_model
"""

import time
from typing import Any

from celery import shared_task

from celery_fastapi.worker.callbacks import update_progress


@shared_task(bind=True, name="preprocess_data", max_retries=3)
def preprocess_data(self, request_data: dict[str, Any]) -> dict[str, Any]:
    """Preprocess the dataset for model training.

    Simulates data loading, cleaning, feature engineering,
    and train/test splitting. Reports progress via task metadata.

    Args:
        request_data: The training request configuration including
            dataset_path, test_size, and random_seed.

    Returns:
        A dict containing preprocessed data references and metadata:
        {"train_path": ..., "test_path": ..., "n_features": ..., "n_samples": ...}

    Raises:
        self.retry: On transient errors with exponential backoff.
    """
    # TODO: Implement preprocessing simulation:
    #   1. Update progress: "Loading dataset..." (10%)
    #      self.update_state(state="PROGRESS", meta={"progress": 10, "step": "Loading dataset"})
    #   2. Simulate work with time.sleep(2)
    #   3. Update progress: "Cleaning data..." (30%)
    #   4. Update progress: "Engineering features..." (60%)
    #   5. Update progress: "Splitting train/test..." (90%)
    #   6. Return preprocessed data metadata
    #
    #   Wrap in try/except for transient errors:
    #   except Exception as exc:
    #       raise self.retry(exc=exc, countdown=2 ** self.request.retries)
    raise NotImplementedError


@shared_task(bind=True, name="train_model", max_retries=3)
def train_model(self, preprocessed_data: dict[str, Any]) -> dict[str, Any]:
    """Train an ML model on the preprocessed data.

    Simulates a training loop with epoch-level progress reporting.

    Args:
        preprocessed_data: Output from the preprocess_data task containing
            data references and configuration.

    Returns:
        A dict containing the trained model reference and training history:
        {"model_path": ..., "epochs_completed": ..., "final_loss": ...}
    """
    # TODO: Implement training simulation:
    #   total_epochs = 10
    #   for epoch in range(total_epochs):
    #       time.sleep(1)  # Simulate training
    #       progress = ((epoch + 1) / total_epochs) * 100
    #       self.update_state(
    #           state="PROGRESS",
    #           meta={"progress": progress, "step": f"Training epoch {epoch + 1}/{total_epochs}"}
    #       )
    #   Return model metadata with simulated metrics
    raise NotImplementedError


@shared_task(bind=True, name="evaluate_model", max_retries=3)
def evaluate_model(self, training_result: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the trained model and compute metrics.

    Args:
        training_result: Output from the train_model task containing
            model reference and training history.

    Returns:
        A dict containing evaluation metrics:
        {"accuracy": ..., "precision": ..., "recall": ..., "f1_score": ..., "model_path": ...}
    """
    # TODO: Implement evaluation simulation:
    #   1. Update progress: "Loading model..." (20%)
    #   2. Update progress: "Running predictions..." (50%)
    #   3. Update progress: "Computing metrics..." (80%)
    #   4. Return simulated evaluation metrics (random but realistic values)
    raise NotImplementedError
