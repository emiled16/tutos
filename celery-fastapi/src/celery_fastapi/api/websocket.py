"""WebSocket endpoint for real-time task progress streaming."""

import asyncio
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from celery_fastapi.api.schemas import ProgressUpdate

ws_router = APIRouter()


class ConnectionManager:
    """Manages active WebSocket connections and broadcasts progress updates.

    Tracks connections per task_id so that progress updates from workers
    can be routed to the correct clients.
    """

    def __init__(self) -> None:
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, task_id: str) -> None:
        """Accept a WebSocket connection and register it for a task.

        Args:
            websocket: The WebSocket connection to register.
            task_id: The task to subscribe to for progress updates.
        """
        # TODO: Implement — accept the websocket connection,
        #       add it to active_connections[task_id]
        raise NotImplementedError

    async def disconnect(self, websocket: WebSocket, task_id: str) -> None:
        """Remove a WebSocket connection from the registry.

        Args:
            websocket: The WebSocket connection to remove.
            task_id: The task the connection was subscribed to.
        """
        # TODO: Implement — remove from active_connections[task_id],
        #       clean up empty entries
        raise NotImplementedError

    async def broadcast_progress(self, task_id: str, update: ProgressUpdate) -> None:
        """Send a progress update to all clients watching a task.

        Args:
            task_id: The task whose progress changed.
            update: The progress update to broadcast.
        """
        # TODO: Implement — serialize the ProgressUpdate to JSON
        #       and send to all WebSocket connections in active_connections[task_id]
        #       Handle send errors gracefully (remove dead connections)
        raise NotImplementedError


manager = ConnectionManager()


@ws_router.websocket("/ws/{task_id}")
async def websocket_progress(websocket: WebSocket, task_id: str) -> None:
    """WebSocket endpoint for streaming task progress updates.

    Clients connect to /ws/{task_id} to receive real-time progress
    updates for a specific task.

    Args:
        websocket: The WebSocket connection.
        task_id: The task to monitor.
    """
    # TODO: Implement the WebSocket lifecycle:
    #   1. Accept the connection via manager.connect()
    #   2. Poll the Celery task state periodically (or subscribe to Redis Pub/Sub)
    #   3. Send ProgressUpdate messages as the task progresses
    #   4. Close the connection when the task completes or fails
    #   5. Handle WebSocketDisconnect exceptions
    #
    # Option A — Polling approach:
    #   while True:
    #       result = celery_app.AsyncResult(task_id)
    #       update = ProgressUpdate(task_id=task_id, status=result.state, ...)
    #       await manager.broadcast_progress(task_id, update)
    #       if result.ready():
    #           break
    #       await asyncio.sleep(1)
    #
    # Option B — Redis Pub/Sub approach (more efficient):
    #   Subscribe to a channel like f"task:{task_id}:progress"
    #   Forward messages to the WebSocket as they arrive
    raise NotImplementedError
