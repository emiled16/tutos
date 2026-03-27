"""API route definitions for the ML task queue.

Provides endpoints for submitting training tasks, checking status,
retrieving results, and cancelling running tasks.
"""

from fastapi import APIRouter, HTTPException

from celery_fastapi.api.schemas import (
    TaskResultResponse,
    TaskStatusResponse,
    TaskSubmitResponse,
    TrainingRequest,
)

router = APIRouter(tags=["tasks"])


@router.post("/train", response_model=TaskSubmitResponse, status_code=202)
async def submit_training_task(request: TrainingRequest) -> TaskSubmitResponse:
    """Submit a new ML model training task.

    Validates the request, dispatches a Celery task chain
    (preprocess → train → evaluate), and returns the task ID.

    Args:
        request: The training configuration and parameters.

    Returns:
        A response containing the task ID for tracking.
    """
    # TODO: Implement — dispatch a Celery chain:
    #   from celery_fastapi.worker.tasks import preprocess_data, train_model, evaluate_model
    #   chain = preprocess_data.s(request.model_dump()) | train_model.s() | evaluate_model.s()
    #   result = chain.apply_async()
    #   Return TaskSubmitResponse with result.id
    raise NotImplementedError


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str) -> TaskStatusResponse:
    """Check the current status of a submitted task.

    Args:
        task_id: The unique identifier of the task.

    Returns:
        Current task state with optional progress information.
    """
    # TODO: Implement — use AsyncResult to get the task state:
    #   from celery_fastapi.worker.celery_app import celery_app
    #   result = celery_app.AsyncResult(task_id)
    #   Map result.state and result.info to TaskStatusResponse
    #   Handle the case where result.info contains progress metadata
    raise NotImplementedError


@router.get("/result/{task_id}", response_model=TaskResultResponse)
async def get_task_result(task_id: str) -> TaskResultResponse:
    """Retrieve the result of a completed task.

    Args:
        task_id: The unique identifier of the task.

    Returns:
        The task output including model metrics.

    Raises:
        HTTPException: 404 if task not found, 409 if task not yet complete.
    """
    # TODO: Implement — check if task is complete:
    #   result = celery_app.AsyncResult(task_id)
    #   If result.state == "SUCCESS": return TaskResultResponse with result.result
    #   If result.state == "FAILURE": return TaskResultResponse with error info
    #   If still running: raise HTTPException(409, "Task not yet complete")
    raise NotImplementedError


@router.delete("/cancel/{task_id}", status_code=204)
async def cancel_task(task_id: str) -> None:
    """Cancel a pending or running task.

    Args:
        task_id: The unique identifier of the task to cancel.

    Raises:
        HTTPException: 404 if task not found.
    """
    # TODO: Implement — revoke the task:
    #   celery_app.control.revoke(task_id, terminate=True, signal="SIGTERM")
    #   Consider checking if the task exists first
    raise NotImplementedError
