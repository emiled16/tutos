"""Celery application configuration.

Creates and configures the Celery app with Redis as both
broker and result backend.
"""

from celery import Celery

from celery_fastapi.core.config import get_settings


def create_celery_app() -> Celery:
    """Create and configure the Celery application.

    Returns:
        A configured Celery instance ready to discover and run tasks.
    """
    settings = get_settings()

    app = Celery("ml_task_queue")

    # TODO: Implement Celery configuration:
    #   app.conf.update(
    #       broker_url=settings.celery_broker_url,
    #       result_backend=settings.celery_result_backend,
    #       task_serializer="json",
    #       accept_content=["json"],
    #       result_serializer="json",
    #       task_track_started=settings.celery_task_track_started,
    #       task_acks_late=settings.celery_task_acks_late,
    #       result_expires=settings.celery_result_expires,
    #       worker_concurrency=settings.celery_worker_concurrency,
    #       worker_prefetch_multiplier=1,
    #   )

    # TODO: Auto-discover tasks from the worker.tasks module:
    #   app.autodiscover_tasks(["celery_fastapi.worker"])

    return app


celery_app = create_celery_app()
