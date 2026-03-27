"""Shared test fixtures for the celery-fastapi project.

Provides a configured FastAPI test client and a Celery app
running in eager mode for synchronous testing.
"""

from collections.abc import Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from celery_fastapi.api.app import create_app
from celery_fastapi.worker.celery_app import celery_app


@pytest.fixture(scope="session")
def celery_config() -> dict[str, Any]:
    """Override Celery configuration for testing.

    Runs tasks synchronously (eager mode) so tests don't need
    a running broker or workers.

    Returns:
        A dict of Celery config overrides.
    """
    # TODO: Implement — return a config dict that enables eager mode:
    #   {
    #       "task_always_eager": True,
    #       "task_eager_propagates": True,
    #       "broker_url": "memory://",
    #       "result_backend": "cache+memory://",
    #   }
    raise NotImplementedError


@pytest.fixture(scope="session", autouse=True)
def configure_celery_for_testing(celery_config: dict[str, Any]) -> None:
    """Apply test configuration to the Celery app.

    Args:
        celery_config: The test Celery configuration.
    """
    # TODO: Implement — apply config to the celery_app:
    #   celery_app.conf.update(celery_config)
    raise NotImplementedError


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a FastAPI test client.

    Yields:
        A TestClient instance configured with the application.
    """
    # TODO: Implement — create and yield a TestClient:
    #   app = create_app()
    #   with TestClient(app) as client:
    #       yield client
    raise NotImplementedError
