"""Manage connected WebSocket clients, rooms/subscriptions, and broadcasting."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field

import websockets
from websockets.server import WebSocketServerProtocol

logger = logging.getLogger(__name__)


@dataclass
class ClientInfo:
    """Metadata about a connected client."""

    websocket: WebSocketServerProtocol
    client_id: str
    subscriptions: set[str] = field(default_factory=set)
    connected_at: float = 0.0


class ConnectionManager:
    """Tracks connected clients and handles subscription-based fan-out.

    Clients subscribe to metric names (rooms). Broadcasts can target
    all clients or only those subscribed to a specific metric.
    """

    def __init__(self) -> None:
        self._clients: dict[str, ClientInfo] = {}
        self._rooms: dict[str, set[str]] = {}

    @property
    def client_count(self) -> int:
        return len(self._clients)

    async def connect(self, websocket: WebSocketServerProtocol, client_id: str) -> None:
        """Register a new client connection."""
        # TODO: Implement — create a ClientInfo, store it in _clients,
        # and log the connection.
        raise NotImplementedError

    async def disconnect(self, client_id: str) -> None:
        """Unregister a client and remove it from all rooms."""
        # TODO: Implement — remove the client from _clients and from
        # every room in _rooms. Clean up empty rooms.
        raise NotImplementedError

    def subscribe(self, client_id: str, metric_name: str) -> None:
        """Subscribe a client to a metric room."""
        # TODO: Implement — add the metric to the client's subscriptions
        # and add the client_id to the room's set.
        raise NotImplementedError

    def unsubscribe(self, client_id: str, metric_name: str) -> None:
        """Unsubscribe a client from a metric room."""
        # TODO: Implement — remove the metric from the client's subscriptions
        # and remove the client_id from the room's set.
        raise NotImplementedError

    async def broadcast(self, message: str, metric_name: str | None = None) -> None:
        """Send a message to clients.

        If metric_name is specified, only send to clients subscribed to that
        metric. Otherwise, send to all connected clients.

        Uses asyncio.gather to send concurrently. Failed sends trigger
        disconnect cleanup.
        """
        # TODO: Implement — determine the target client set, send the
        # message to each concurrently via asyncio.gather. Catch
        # websockets.ConnectionClosed and call disconnect for failed clients.
        raise NotImplementedError

    async def send_to(self, client_id: str, message: str) -> None:
        """Send a message to a specific client by ID."""
        # TODO: Implement — look up the client, send the message,
        # handle ConnectionClosed.
        raise NotImplementedError

    def get_subscriptions(self, client_id: str) -> set[str]:
        """Return the set of metrics a client is subscribed to."""
        info = self._clients.get(client_id)
        return info.subscriptions.copy() if info else set()
