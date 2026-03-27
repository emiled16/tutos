"""Pydantic models for WebSocket messages exchanged between server and clients."""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Severity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CommandType(str, enum.Enum):
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    QUERY = "query"
    HEARTBEAT = "heartbeat"


class MessageType(str, enum.Enum):
    DATA = "data"
    ALERT = "alert"
    COMMAND = "command"
    ACK = "ack"
    ERROR = "error"


class DataPoint(BaseModel):
    """A single time-series observation from a sensor or metric source."""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metric_name: str
    value: float
    tags: dict[str, str] = Field(default_factory=dict)


class AnomalyScore(BaseModel):
    """Result from an anomaly detector for a single data point."""

    detector_name: str
    score: float
    is_anomaly: bool
    threshold: float
    details: dict[str, Any] = Field(default_factory=dict)


class Alert(BaseModel):
    """An alert generated when an anomaly is detected."""

    alert_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metric_name: str
    severity: Severity
    detector_name: str
    value: float
    score: float
    threshold: float
    message: str
    acknowledged: bool = False


class Command(BaseModel):
    """A command sent from a client to the server."""

    command_type: CommandType
    payload: dict[str, Any] = Field(default_factory=dict)


class WSMessage(BaseModel):
    """Top-level WebSocket message envelope."""

    type: MessageType
    payload: dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def data_message(cls, data_point: DataPoint) -> WSMessage:
        """Create a message wrapping a DataPoint."""
        return cls(type=MessageType.DATA, payload=data_point.model_dump(mode="json"))

    @classmethod
    def alert_message(cls, alert: Alert) -> WSMessage:
        """Create a message wrapping an Alert."""
        return cls(type=MessageType.ALERT, payload=alert.model_dump(mode="json"))

    @classmethod
    def ack_message(cls, detail: str = "ok") -> WSMessage:
        """Create an acknowledgement message."""
        return cls(type=MessageType.ACK, payload={"detail": detail})

    @classmethod
    def error_message(cls, detail: str) -> WSMessage:
        """Create an error message."""
        return cls(type=MessageType.ERROR, payload={"detail": detail})
