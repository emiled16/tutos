"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from celery_fastapi.api.schemas import ModelType, TaskStatus


class TestSubmitTrainingTask:
    def test_submit_valid_training_request(self, client: TestClient) -> None:
        """Test that a valid training request returns 202 with a task ID."""
        # TODO: Implement — POST /api/v1/train with valid TrainingRequest body,
        #       assert status_code == 202,
        #       assert response contains task_id and status == "PENDING"
        raise NotImplementedError

    def test_submit_with_custom_hyperparameters(self, client: TestClient) -> None:
        """Test submission with custom hyperparameters."""
        # TODO: Implement — POST with hyperparameters={"n_estimators": 100, "max_depth": 5},
        #       assert 202 response
        raise NotImplementedError

    def test_submit_invalid_model_type(self, client: TestClient) -> None:
        """Test that an invalid model type returns 422."""
        # TODO: Implement — POST with model_type="invalid",
        #       assert status_code == 422
        raise NotImplementedError

    def test_submit_invalid_test_size(self, client: TestClient) -> None:
        """Test that test_size > 0.5 returns 422."""
        # TODO: Implement — POST with test_size=0.9,
        #       assert status_code == 422
        raise NotImplementedError


class TestGetTaskStatus:
    def test_get_status_of_submitted_task(self, client: TestClient) -> None:
        """Test getting status of a recently submitted task."""
        # TODO: Implement — submit a task, then GET /api/v1/status/{task_id},
        #       assert response contains valid TaskStatus
        raise NotImplementedError

    def test_get_status_of_unknown_task(self, client: TestClient) -> None:
        """Test getting status of a non-existent task ID."""
        # TODO: Implement — GET /api/v1/status/nonexistent-id,
        #       assert status is PENDING (Celery returns PENDING for unknown IDs)
        raise NotImplementedError


class TestGetTaskResult:
    def test_get_result_of_completed_task(self, client: TestClient) -> None:
        """Test retrieving results of a successfully completed task."""
        # TODO: Implement — submit a task, wait for completion (eager mode),
        #       GET /api/v1/result/{task_id},
        #       assert response contains metrics
        raise NotImplementedError

    def test_get_result_of_incomplete_task(self, client: TestClient) -> None:
        """Test that getting results of a running task returns 409."""
        # TODO: Implement — if possible in eager mode, or mock a STARTED state,
        #       GET /api/v1/result/{task_id}, assert 409
        raise NotImplementedError


class TestCancelTask:
    def test_cancel_pending_task(self, client: TestClient) -> None:
        """Test cancelling a pending task returns 204."""
        # TODO: Implement — submit a task, DELETE /api/v1/cancel/{task_id},
        #       assert status_code == 204
        raise NotImplementedError
