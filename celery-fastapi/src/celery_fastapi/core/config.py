"""Application settings managed with pydantic-settings.

Reads configuration from environment variables and .env files.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration.

    All values can be overridden via environment variables.

    Attributes:
        app_name: Name of the application.
        redis_url: Redis connection URL for general use.
        celery_broker_url: Redis URL for the Celery message broker.
        celery_result_backend: Redis URL for storing task results.
        celery_task_track_started: Whether to report STARTED state.
        celery_task_acks_late: Acknowledge tasks after completion, not receipt.
        celery_result_expires: Seconds before results are auto-deleted.
        celery_worker_concurrency: Number of concurrent worker processes.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "ML Task Queue"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    celery_task_track_started: bool = True
    celery_task_acks_late: bool = True
    celery_result_expires: int = 3600
    celery_worker_concurrency: int = 2


def get_settings() -> Settings:
    """Create and return application settings.

    Returns:
        A Settings instance populated from environment variables.
    """
    # TODO: Implement — return a Settings instance
    #       Consider caching with functools.lru_cache for performance
    raise NotImplementedError
