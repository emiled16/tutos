"""Critic agent that reviews and provides feedback on agent outputs."""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, Field

from multi_agent_orchestration.agents.base_agent import AgentConfig, BaseAgent
from multi_agent_orchestration.communication.message_bus import MessageBus
from multi_agent_orchestration.communication.protocols import (
    AgentRole,
    Feedback,
    TaskAssignment,
    TaskResult,
)
from multi_agent_orchestration.memory.shared_memory import SharedMemory

logger = logging.getLogger(__name__)

CRITIC_SYSTEM_PROMPT = """\
You are a rigorous critic and quality reviewer. Your job is to evaluate 
research reports for accuracy, completeness, and clarity.

Guidelines:
- Check all factual claims against provided sources
- Identify logical gaps or unsupported conclusions
- Assess writing quality and structure
- Provide specific, actionable improvement suggestions
- Score on a 0-1 scale across multiple dimensions
"""


class QualityDimension(BaseModel):
    """A single dimension of quality assessment."""

    name: str
    score: float = Field(ge=0.0, le=1.0)
    feedback: str = ""


class ReviewResult(BaseModel):
    """Structured review output from the critic."""

    dimensions: list[QualityDimension] = Field(default_factory=list)
    overall_score: float = Field(ge=0.0, le=1.0, default=0.0)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    requires_revision: bool = False
    revision_priority: list[str] = Field(default_factory=list)


QUALITY_DIMENSIONS = [
    "factual_accuracy",
    "completeness",
    "clarity",
    "structure",
    "citation_quality",
    "coherence",
]


class CriticAgent(BaseAgent):
    """Agent specialized in reviewing and providing quality feedback.

    Evaluates reports across multiple quality dimensions and produces
    actionable feedback for the writer agent.
    """

    def __init__(
        self,
        message_bus: MessageBus,
        shared_memory: SharedMemory,
        quality_threshold: float = 0.7,
        model: str = "gpt-4o",
    ) -> None:
        config = AgentConfig(
            role=AgentRole.CRITIC,
            model=model,
            temperature=0.3,
            system_prompt=CRITIC_SYSTEM_PROMPT,
        )
        super().__init__(config, message_bus, shared_memory)
        self.quality_threshold = quality_threshold

    async def execute(self, task: TaskAssignment) -> TaskResult:
        """Review a report and produce quality feedback.

        Steps:
        1. Retrieve report and research sources from shared memory
        2. Evaluate each quality dimension
        3. Determine if revision is needed
        4. Send feedback message to writer if revision required
        5. Return review result

        Args:
            task: Task with review parameters and quality thresholds.

        Returns:
            Review result with scores and feedback.
        """
        # TODO: Implement review workflow
        # 1. Fetch the report and original research from shared memory
        # 2. Evaluate each quality dimension using LLM
        # 3. Calculate overall score
        # 4. Determine if revision is needed (score < threshold)
        # 5. Build Feedback message and publish if revision needed
        # 6. Return TaskResult with ReviewResult
        pass

    async def _evaluate_dimension(
        self, dimension: str, report: dict[str, Any], sources: dict[str, Any]
    ) -> QualityDimension:
        """Evaluate the report on a single quality dimension.

        Args:
            dimension: Name of the quality dimension to assess.
            report: The report content to evaluate.
            sources: Original research sources for fact-checking.

        Returns:
            Quality score and feedback for this dimension.
        """
        # TODO: Implement dimension evaluation
        # Prompt LLM to score the report on this specific dimension
        # with reference to the original sources
        pass

    def _should_request_revision(self, review: ReviewResult) -> bool:
        """Determine if the report needs revision based on scores.

        Args:
            review: The completed review result.

        Returns:
            True if revision is needed.
        """
        # TODO: Implement revision decision logic
        # Return True if overall_score < self.quality_threshold
        # or any individual dimension score is critically low
        pass
