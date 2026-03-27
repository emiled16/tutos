"""WebSocket client for testing and demonstrating the anomaly detection server."""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass

import websockets

from socket_project.models.messages import CommandType, WSMessage

logger = logging.getLogger(__name__)


@dataclass
class ClientConfig:
    """Configuration for the WebSocket test client."""

    uri: str = "ws://localhost:8765"
    auto_subscribe: list[str] | None = None
    reconnect_interval: float = 5.0
    max_reconnect_attempts: int = 10


class AnomalyDetectionClient:
    """WebSocket client that connects to the anomaly detection server,
    subscribes to metric streams, and displays incoming alerts.
    """

    def __init__(self, config: ClientConfig | None = None) -> None:
        self.config = config or ClientConfig()
        self._running: bool = False
        self._websocket: object | None = None

    async def _send_command(
        self,
        command_type: CommandType,
        payload: dict | None = None,
    ) -> None:
        """Send a command message to the server."""
        # TODO: Implement — construct a Command, wrap it in a WSMessage
        # (or send the command JSON directly), and send over the websocket.
        raise NotImplementedError

    async def subscribe(self, metric_name: str) -> None:
        """Subscribe to a metric stream."""
        await self._send_command(
            CommandType.SUBSCRIBE,
            {"metric_name": metric_name},
        )

    async def unsubscribe(self, metric_name: str) -> None:
        """Unsubscribe from a metric stream."""
        await self._send_command(
            CommandType.UNSUBSCRIBE,
            {"metric_name": metric_name},
        )

    async def _handle_message(self, raw_message: str) -> None:
        """Process an incoming message from the server."""
        # TODO: Implement — parse the JSON message, determine its type
        # (data, alert, ack, error), and handle accordingly:
        #   - data: log or display the data point
        #   - alert: prominently display the alert with severity
        #   - ack: log the acknowledgement
        #   - error: log the error
        raise NotImplementedError

    async def connect(self) -> None:
        """Connect to the server with automatic reconnection."""
        # TODO: Implement connection loop with reconnection:
        #   1. Attempt to connect to self.config.uri
        #   2. On success, auto-subscribe to configured metrics
        #   3. Enter receive loop, passing messages to _handle_message
        #   4. On disconnect, wait reconnect_interval and retry
        #   5. Give up after max_reconnect_attempts
        raise NotImplementedError

    def stop(self) -> None:
        """Signal the client to stop."""
        self._running = False


async def main() -> None:
    """Entry point for running the client directly."""
    logging.basicConfig(level=logging.INFO)
    config = ClientConfig(auto_subscribe=["cpu_usage"])
    client = AnomalyDetectionClient(config)
    await client.connect()


if __name__ == "__main__":
    asyncio.run(main())
