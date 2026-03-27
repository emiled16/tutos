"""Writing agent that produces structured research reports."""

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

WRITER_SYSTEM_PROMPT = """\
You are an expert technical writer. Your job is to transform analyzed 
research findings into clear, well-structured reports.

Guidelines:
- Use clear, concise language appropriate for the target audience
- Structure reports with logical section flow
- Include citations for all claims
- Use headings, bullet points, and tables for readability
- Ensure smooth transitions between sections
"""


class ReportSection(BaseModel):
    """A section of the research report."""

    title: str
    content: str
    citations: list[str] = Field(default_factory=list)
    order: int = 0


class Report(BaseModel):
    """A complete research report."""

    title: str
    executive_summary: str = ""
    sections: list[ReportSection] = Field(default_factory=list)
    conclusion: str = ""
    references: list[str] = Field(default_factory=list)
    revision_number: int = 0


class WriterAgent(BaseAgent):
    """Agent specialized in producing structured research reports.

    Takes analysis output and produces a formatted, well-written report
    with proper citations and structure.
    """

    def __init__(
        self,
        message_bus: MessageBus,
        shared_memory: SharedMemory,
        model: str = "gpt-4o",
    ) -> None:
        config = AgentConfig(
            role=AgentRole.WRITER,
            model=model,
            temperature=0.7,
            system_prompt=WRITER_SYSTEM_PROMPT,
        )
        super().__init__(config, message_bus, shared_memory)

    async def execute(self, task: TaskAssignment) -> TaskResult:
        """Produce a structured report from analysis results.

        Steps:
        1. Retrieve analysis from shared memory
        2. Plan report structure
        3. Write each section
        4. Compile executive summary and conclusion
        5. Add citations and references
        6. Store report in shared memory

        Args:
            task: Task with writing parameters and any revision feedback.

        Returns:
            The generated report.
        """
        # TODO: Implement report writing workflow
        # 1. Fetch analysis output from shared memory
        # 2. Plan section structure based on themes
        # 3. Write each section with LLM
        # 4. Generate executive summary from completed sections
        # 5. Compile references list
        # 6. Build Report model and store in shared memory
        # 7. Return TaskResult with the report
        pass

    async def revise(self, report: Report, feedback: Feedback) -> Report:
        """Revise a report based on critic feedback.

        Args:
            report: The current report draft.
            feedback: Feedback with specific improvement suggestions.

        Returns:
            The revised report with incremented revision number.
        """
        # TODO: Implement revision logic
        # 1. Parse feedback suggestions
        # 2. Identify sections that need changes
        # 3. Rewrite affected sections with feedback context
        # 4. Increment revision_number
        pass

    async def _write_section(
        self, title: str, analysis_data: dict[str, Any], context: str
    ) -> ReportSection:
        """Write a single report section.

        Args:
            title: Section title.
            analysis_data: Relevant analysis findings for this section.
            context: Previously written sections for flow continuity.

        Returns:
            A completed report section with citations.
        """
        # TODO: Implement section writing
        # Use LLM with analysis data and prior context to write a cohesive section
        pass
