"""Message handlers for different WebSocket event types."""

from __future__ import annotations

import json
import logging
from typing import Any

from socket_project.models.messages import Command, CommandType, WSMessage
from socket_project.server.connection_manager import ConnectionManager

logger = logging.getLogger(__name__)


class MessageHandler:
    """Routes incoming WebSocket messages to the appropriate handler method.

    Supported commands: subscribe, unsubscribe, query, heartbeat.
    """

    def __init__(self, connection_manager: ConnectionManager) -> None:
        self.connection_manager = connection_manager

    async def handle(self, client_id: str, raw_message: str) -> WSMessage:
        """Parse a raw JSON message and dispatch to the correct handler.

        Returns a WSMessage (ack or error) to send back to the client.
        """
        # TODO: Implement:
        #   1. Parse raw_message as JSON
        #   2. Validate it as a Command using Pydantic
        #   3. Dispatch based on command_type to _handle_subscribe,
        #      _handle_unsubscribe, _handle_query, or _handle_heartbeat
        #   4. Return an ack or error WSMessage
        #   5. Handle JSON decode errors and validation errors gracefully
        raise NotImplementedError

    async def _handle_subscribe(self, client_id: str, payload: dict[str, Any]) -> WSMessage:
        """Subscribe the client to a metric stream."""
        # TODO: Implement — extract metric_name from payload,
        # call connection_manager.subscribe, return ack.
        raise NotImplementedError

    async def _handle_unsubscribe(self, client_id: str, payload: dict[str, Any]) -> WSMessage:
        """Unsubscribe the client from a metric stream."""
        # TODO: Implement — extract metric_name from payload,
        # call connection_manager.unsubscribe, return ack.
        raise NotImplementedError

    async def _handle_query(self, client_id: str, payload: dict[str, Any]) -> WSMessage:
        """Handle a query command (e.g., list subscriptions, active alerts)."""
        # TODO: Implement — support at least "subscriptions" query type,
        # returning the client's current subscriptions.
        raise NotImplementedError

    async def _handle_heartbeat(self, client_id: str, payload: dict[str, Any]) -> WSMessage:
        """Respond to a heartbeat with an ack."""
        return WSMessage.ack_message("pong")
