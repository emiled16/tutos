"""Feature materialization from offline to online store."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from feast import FeatureStore


def get_feature_store(repo_path: str | Path | None = None) -> FeatureStore:
    """Initialize and return a Feast FeatureStore instance.

    Args:
        repo_path: Path to the Feast feature repository.
                   Defaults to FEAST_REPO_PATH env var or
                   "src/feature_store/feature_repo".

    Returns:
        Configured FeatureStore instance.
    """
    # TODO: Implement
    # - Read repo_path from argument, then FEAST_REPO_PATH env var, then default
    # - Return FeatureStore(repo_path=str(repo_path))
    raise NotImplementedError


def materialize_features(
    store: FeatureStore,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> None:
    """Materialize features from offline to online store.

    Args:
        store: Feast FeatureStore instance.
        start_date: Start of the materialization window.
                    Defaults to 30 days ago.
        end_date: End of the materialization window.
                  Defaults to now.
    """
    # TODO: Implement
    # - Set default start_date to 30 days ago if None
    # - Set default end_date to now if None
    # - Call store.materialize(start_date, end_date)
    # - Log the materialization window
    raise NotImplementedError


def materialize_incremental(
    store: FeatureStore,
    end_date: datetime | None = None,
) -> None:
    """Incrementally materialize features since the last materialization.

    Only materializes new data since the last successful run.

    Args:
        store: Feast FeatureStore instance.
        end_date: End of the materialization window. Defaults to now.
    """
    # TODO: Implement
    # - Set default end_date to now if None
    # - Call store.materialize_incremental(end_date)
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: Implement CLI entry point
    # - Parse optional --start-date and --end-date arguments
    # - Initialize the feature store
    # - Run materialize_features or materialize_incremental
    pass
