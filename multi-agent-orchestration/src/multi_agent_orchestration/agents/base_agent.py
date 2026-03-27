"""Abstract base agent with common interface for all specialized agents."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field

from multi_agent_orchestration.communication.message_bus import MessageBus
from multi_agent_orchestration.communication.protocols import (
    AgentRole,
    Message,
    MessageType,
    TaskAssignment,
    TaskResult,
)
from multi_agent_orchestration.memory.agent_memory import AgentMemory
from multi_agent_orchestration.memory.shared_memory import SharedMemory

logger = logging.getLogger(__name__)


class AgentConfig(BaseModel):
    """Configuration for an agent instance."""

    role: AgentRole
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 4096
    system_prompt: str = ""
    max_iterations: int = 5
    retry_attempts: int = 3


class BaseAgent(ABC):
    """Abstract base class for all agents in the swarm.

    Provides lifecycle hooks, message handling, memory access, and a
    standard interface that the orchestrator depends on.
    """

    def __init__(
        self,
        config: AgentConfig,
        message_bus: MessageBus,
        shared_memory: SharedMemory,
    ) -> None:
        self.config = config
        self.message_bus = message_bus
        self.shared_memory = shared_memory
        self.memory = AgentMemory(agent_role=config.role)
        self._is_running = False

    @property
    def role(self) -> AgentRole:
        return self.config.role

    async def start(self) -> None:
        """Initialize the agent and subscribe to the message bus.

        Called by the orchestrator when the workflow begins.
        """
        # TODO: Implement agent startup
        # 1. Subscribe to message bus for this agent's role
        # 2. Call on_start lifecycle hook
        # 3. Set _is_running flag
        pass

    async def stop(self) -> None:
        """Gracefully shut down the agent.

        Called by the orchestrator when the workflow completes.
        """
        # TODO: Implement agent shutdown
        # 1. Call on_stop lifecycle hook
        # 2. Clear _is_running flag
        pass

    @abstractmethod
    async def execute(self, task: TaskAssignment) -> TaskResult:
        """Execute a task and return the result.

        This is the core method each specialized agent must implement.

        Args:
            task: The task assignment with description and input data.

        Returns:
            The result of task execution.
        """
        ...

    async def handle_message(self, message: Message) -> None:
        """Process an incoming message from the bus.

        Routes messages to appropriate handlers based on type.

        Args:
            message: The incoming message.
        """
        # TODO: Implement message routing
        # Route to execute() for TASK_ASSIGNMENT
        # Route to handle_feedback() for FEEDBACK
        # Log other message types
        pass

    async def handle_feedback(self, message: Message) -> None:
        """Process feedback from the critic agent.

        Args:
            message: Feedback message with scores and suggestions.
        """
        # TODO: Implement feedback handling
        # 1. Parse feedback from message content
        # 2. Store in agent memory
        # 3. If revision required, re-execute with feedback context
        pass

    async def _call_llm(self, messages: list[dict[str, str]]) -> str:
        """Call the LLM with the given messages.

        Args:
            messages: Chat messages in OpenAI format.

        Returns:
            The LLM response content.
        """
        # TODO: Implement LLM call using OpenAI client
        # 1. Build messages list with system prompt
        # 2. Call openai.chat.completions.create
        # 3. Handle errors and retries
        # 4. Track token usage in memory
        pass

    async def on_start(self) -> None:
        """Lifecycle hook called when the agent starts. Override in subclasses."""
        pass

    async def on_stop(self) -> None:
        """Lifecycle hook called when the agent stops. Override in subclasses."""
        pass
