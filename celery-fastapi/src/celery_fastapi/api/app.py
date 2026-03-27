"""FastAPI application factory and lifespan management."""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from celery_fastapi.api.routes import router
from celery_fastapi.api.websocket import ws_router
from celery_fastapi.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown lifecycle.

    Sets up shared resources (Redis connection pool) on startup
    and cleans them up on shutdown.

    Args:
        app: The FastAPI application instance.
    """
    # TODO: Implement startup logic:
    #   - Initialize Redis connection pool
    #   - Store it in app.state for access in route handlers
    #   - Verify Celery broker connectivity
    yield
    # TODO: Implement shutdown logic:
    #   - Close Redis connection pool
    #   - Clean up any background tasks


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        A fully configured FastAPI instance with routes and middleware.
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Submit, monitor, and retrieve ML training tasks",
        version="0.1.0",
        lifespan=lifespan,
    )

    # TODO: Include the API router and WebSocket router
    #   app.include_router(router, prefix="/api/v1")
    #   app.include_router(ws_router)

    return app


app = create_app()
