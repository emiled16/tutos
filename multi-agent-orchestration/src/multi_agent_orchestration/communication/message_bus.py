"""Message bus for inter-agent communication."""

from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from typing import Any, Callable, Coroutine

from multi_agent_orchestration.communication.protocols import (
    AgentRole,
    Message,
    MessageType,
)

logger = logging.getLogger(__name__)

Subscriber = Callable[[Message], Coroutine[Any, Any, None]]


class MessageBus:
    """Central message bus that routes messages between agents.

    Supports:
    - Direct messaging (one-to-one)
    - Broadcast messaging (one-to-all)
    - Topic-based pub/sub via message types
    - Message history for debugging
    """

    def __init__(self, max_history: int = 1000) -> None:
        self._subscribers: dict[AgentRole, list[Subscriber]] = defaultdict(list)
        self._type_subscribers: dict[MessageType, list[Subscriber]] = defaultdict(list)
        self._history: list[Message] = []
        self._max_history = max_history

    def subscribe(self, role: AgentRole, handler: Subscriber) -> None:
        """Subscribe an agent to receive messages addressed to its role.

        Args:
            role: The agent role to subscribe as.
            handler: Async callback invoked when a message is received.
        """
        # TODO: Implement subscription registration
        pass

    def subscribe_to_type(self, msg_type: MessageType, handler: Subscriber) -> None:
        """Subscribe to all messages of a given type regardless of recipient.

        Args:
            msg_type: The message type to listen for.
            handler: Async callback invoked when a matching message is published.
        """
        # TODO: Implement type-based subscription
        pass

    async def publish(self, message: Message) -> None:
        """Publish a message to the bus, routing it to appropriate subscribers.

        If ``message.recipient`` is set, deliver only to that role's subscribers.
        If ``message.recipient`` is None, broadcast to all subscribers.
        Also deliver to any type-based subscribers.

        Args:
            message: The message to publish.
        """
        # TODO: Implement message routing logic
        # 1. Record message in history
        # 2. Route to recipient or broadcast
        # 3. Route to type-based subscribers
        # 4. Log the message for observability
        pass

    def get_history(
        self,
        sender: AgentRole | None = None,
        recipient: AgentRole | None = None,
        msg_type: MessageType | None = None,
        limit: int = 50,
    ) -> list[Message]:
        """Retrieve message history with optional filters.

        Args:
            sender: Filter by sender role.
            recipient: Filter by recipient role.
            msg_type: Filter by message type.
            limit: Max number of messages to return.

        Returns:
            Filtered list of messages, most recent first.
        """
        # TODO: Implement filtered history retrieval
        pass

    def clear_history(self) -> None:
        """Clear all stored message history."""
        # TODO: Implement history clearing
        pass
