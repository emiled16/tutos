"""Communication protocols and message types for inter-agent messaging."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class MessageType(str, Enum):
    """Types of messages exchanged between agents."""

    TASK_ASSIGNMENT = "task_assignment"
    TASK_RESULT = "task_result"
    FEEDBACK = "feedback"
    STATUS_UPDATE = "status_update"
    ERROR = "error"
    REVISION_REQUEST = "revision_request"


class Priority(str, Enum):
    """Message priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class AgentRole(str, Enum):
    """Defined agent roles in the swarm."""

    ORCHESTRATOR = "orchestrator"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"
    CRITIC = "critic"


class Message(BaseModel):
    """A message exchanged between agents via the message bus."""

    id: UUID = Field(default_factory=uuid4)
    type: MessageType
    sender: AgentRole
    recipient: AgentRole | None = None  # None = broadcast
    content: dict[str, Any] = Field(default_factory=dict)
    priority: Priority = Priority.NORMAL
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: UUID | None = None  # links related messages
    metadata: dict[str, Any] = Field(default_factory=dict)


class TaskAssignment(BaseModel):
    """Payload for a task assignment message."""

    task_id: str
    description: str
    input_data: dict[str, Any] = Field(default_factory=dict)
    constraints: list[str] = Field(default_factory=list)
    max_iterations: int = 3
    deadline_seconds: float | None = None


class TaskResult(BaseModel):
    """Payload for a task result message."""

    task_id: str
    success: bool
    output: dict[str, Any] = Field(default_factory=dict)
    reasoning: str = ""
    confidence: float = 0.0
    sources: list[str] = Field(default_factory=list)
    token_usage: int = 0


class Feedback(BaseModel):
    """Payload for critic feedback on an agent's output."""

    task_id: str
    score: float = Field(ge=0.0, le=1.0)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    requires_revision: bool = False
