"""Task callbacks for progress reporting and notifications.

Provides utilities that Celery tasks use to report progress
back to the API layer (via Redis Pub/Sub or direct state updates).
"""

import json
from typing import Any

from celery import Task


def update_progress(
    task: Task,
    progress: float,
    current_step: str,
    message: str = "",
) -> None:
    """Update task progress metadata and optionally publish to Redis.

    This function both updates the Celery task state (so polling clients
    can see progress) and optionally publishes to a Redis Pub/Sub channel
    (so WebSocket clients get real-time updates).

    Args:
        task: The bound Celery task instance (from bind=True).
        progress: Completion percentage (0.0 to 100.0).
        current_step: Short description of the current step.
        message: Optional detailed message.
    """
    # TODO: Implement progress reporting:
    #   1. Update Celery task state:
    #      task.update_state(
    #          state="PROGRESS",
    #          meta={"progress": progress, "current_step": current_step, "message": message}
    #      )
    #   2. Optionally publish to Redis Pub/Sub for WebSocket forwarding:
    #      redis_client.publish(f"task:{task.request.id}:progress", json.dumps({...}))
    raise NotImplementedError


def on_task_success(task_id: str, result: Any) -> None:
    """Callback invoked when a task completes successfully.

    Can be used to send notifications, update dashboards, or
    trigger downstream processes.

    Args:
        task_id: The completed task's identifier.
        result: The task's return value.
    """
    # TODO: Implement success handling:
    #   - Publish completion event to Redis Pub/Sub
    #   - Log the successful completion with task_id
    raise NotImplementedError


def on_task_failure(task_id: str, exception: Exception, traceback: str) -> None:
    """Callback invoked when a task fails after all retries.

    Args:
        task_id: The failed task's identifier.
        exception: The exception that caused the failure.
        traceback: The formatted traceback string.
    """
    # TODO: Implement failure handling:
    #   - Publish failure event to Redis Pub/Sub
    #   - Log the failure with task_id, exception, and traceback
    raise NotImplementedError
