"""Research agent that gathers information from external sources."""

from __future__ import annotations

import logging
from typing import Any

from multi_agent_orchestration.agents.base_agent import AgentConfig, BaseAgent
from multi_agent_orchestration.communication.message_bus import MessageBus
from multi_agent_orchestration.communication.protocols import (
    AgentRole,
    TaskAssignment,
    TaskResult,
)
from multi_agent_orchestration.memory.shared_memory import SharedMemory
from multi_agent_orchestration.tools.search_tool import SearchTool

logger = logging.getLogger(__name__)

RESEARCHER_SYSTEM_PROMPT = """\
You are a thorough research agent. Your job is to gather comprehensive, 
accurate information about a given topic from multiple sources.

Guidelines:
- Search for diverse perspectives and authoritative sources
- Extract key facts, statistics, and quotes
- Note the source URL for every piece of information
- Flag any conflicting information you find
- Organize findings by subtopic
"""


class ResearcherAgent(BaseAgent):
    """Agent specialized in gathering information from web sources.

    Uses search tools to find relevant documents, extracts key information,
    and stores structured research findings in shared memory.
    """

    def __init__(
        self,
        message_bus: MessageBus,
        shared_memory: SharedMemory,
        search_tool: SearchTool | None = None,
        model: str = "gpt-4o",
    ) -> None:
        config = AgentConfig(
            role=AgentRole.RESEARCHER,
            model=model,
            system_prompt=RESEARCHER_SYSTEM_PROMPT,
        )
        super().__init__(config, message_bus, shared_memory)
        self.search_tool = search_tool or SearchTool()

    async def execute(self, task: TaskAssignment) -> TaskResult:
        """Gather information about the topic described in the task.

        Steps:
        1. Generate search queries from the task description
        2. Execute searches and collect raw results
        3. Use LLM to extract and structure key findings
        4. Store findings in shared memory
        5. Return structured research output

        Args:
            task: Task containing the research topic and constraints.

        Returns:
            Research findings with sources and confidence score.
        """
        # TODO: Implement research workflow
        # 1. Generate 3-5 search queries from task description using LLM
        # 2. Execute searches using self.search_tool
        # 3. Deduplicate and rank results
        # 4. Use LLM to extract structured findings from search results
        # 5. Store in shared memory under task_id key
        # 6. Return TaskResult with findings and source URLs
        pass

    async def _generate_search_queries(self, topic: str) -> list[str]:
        """Use the LLM to generate diverse search queries for a topic.

        Args:
            topic: The research topic.

        Returns:
            List of search query strings.
        """
        # TODO: Implement query generation
        # Prompt the LLM to create 3-5 search queries covering different
        # angles of the topic
        pass

    async def _extract_findings(
        self, topic: str, search_results: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Extract structured findings from raw search results.

        Args:
            topic: The research topic for context.
            search_results: Raw search results from the search tool.

        Returns:
            Structured findings with key facts, quotes, and sources.
        """
        # TODO: Implement finding extraction
        # Use LLM to read search results and extract:
        # - key_facts: list of important facts
        # - statistics: numerical data points
        # - quotes: relevant expert quotes
        # - sources: source URLs with relevance scores
        # - conflicts: any contradictory information found
        pass
