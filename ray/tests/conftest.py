"""Shared fixtures for Ray-based tests."""

from __future__ import annotations

from typing import Generator

import pytest
import ray


@pytest.fixture(scope="session")
def ray_cluster() -> Generator[None, None, None]:
    """Start a local Ray instance for the test session and shut it down after.

    Yields control to tests while Ray is running.  Uses minimal resources
    to keep CI fast.
    """
    # TODO: Call ray.init(num_cpus=2, num_gpus=0) if not already initialized,
    #       yield, then call ray.shutdown()
    raise NotImplementedError


@pytest.fixture
def sample_data() -> dict[str, list[list[float]]]:
    """Provide a small synthetic dataset for unit tests.

    Returns:
        Dict with ``"features"`` (2-D list) and ``"labels"`` (1-D list).
    """
    # TODO: Generate a small deterministic dataset (e.g. 100 samples, 4 features)
    #       suitable for testing training and serving pipelines
    raise NotImplementedError
