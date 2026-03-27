"""Notification dispatcher — routes alerts to WebSocket clients, logs, and webhooks."""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from typing import Protocol

from socket_project.models.messages import Alert, WSMessage

logger = logging.getLogger(__name__)


class NotificationSink(Protocol):
    """Protocol for anything that can receive an alert notification."""

    async def send_alert(self, alert: Alert) -> None: ...


@dataclass
class WebSocketSink:
    """Pushes alerts to all connected WebSocket clients via the connection manager."""

    broadcast_fn: object = None  # Will be set to ConnectionManager.broadcast

    async def send_alert(self, alert: Alert) -> None:
        """Serialize the alert and broadcast to all connected clients."""
        # TODO: Implement — create a WSMessage.alert_message(alert),
        # serialize to JSON, and call self.broadcast_fn with the payload.
        raise NotImplementedError


@dataclass
class LogSink:
    """Logs alerts at the appropriate severity level."""

    async def send_alert(self, alert: Alert) -> None:
        """Log the alert with severity-appropriate log level."""
        # TODO: Implement — map alert.severity to a log level
        # (LOW→info, MEDIUM→warning, HIGH→error, CRITICAL→critical)
        # and emit a structured log message.
        raise NotImplementedError


@dataclass
class WebhookSink:
    """Posts alerts to an external webhook URL."""

    url: str = ""
    timeout: float = 5.0

    async def send_alert(self, alert: Alert) -> None:
        """POST the alert as JSON to the configured webhook URL."""
        # TODO: Implement — use aiohttp or urllib to POST the alert
        # payload to self.url. Handle timeouts and connection errors
        # gracefully (log and continue, don't crash the pipeline).
        raise NotImplementedError


class Notifier:
    """Dispatches alerts to multiple notification sinks concurrently."""

    def __init__(self, sinks: list[NotificationSink] | None = None) -> None:
        self.sinks: list[NotificationSink] = sinks or []

    def add_sink(self, sink: NotificationSink) -> None:
        """Register a new notification sink."""
        self.sinks.append(sink)

    async def notify(self, alert: Alert) -> list[Exception | None]:
        """Send an alert to all registered sinks concurrently.

        Returns a list of results (None for success, Exception for failure)
        in the same order as self.sinks.
        """
        # TODO: Implement — use asyncio.gather with return_exceptions=True
        # to dispatch alert to all sinks concurrently. Log any exceptions
        # but don't let one failed sink prevent others from receiving the alert.
        raise NotImplementedError
