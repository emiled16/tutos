"""RAG generator that produces answers with citations from retrieved context."""

from __future__ import annotations

import logging
import os
from typing import Any

from pydantic import BaseModel, Field

from qdrant.rag.retriever import RetrievedContext

logger = logging.getLogger(__name__)

RAG_SYSTEM_PROMPT = """\
You are a helpful assistant that answers questions based on the provided context.

Rules:
- Only use information from the provided context to answer
- Cite your sources using [Source N] notation
- If the context doesn't contain enough information, say so
- Be concise and direct
"""


class Citation(BaseModel):
    """A citation linking a claim to its source."""

    source_index: int
    source_text: str = ""
    chunk_id: str = ""


class GeneratedAnswer(BaseModel):
    """A generated answer with citations."""

    answer: str
    citations: list[Citation] = Field(default_factory=list)
    model: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0


class Generator:
    """RAG generator that produces grounded answers from retrieved context.

    Uses an LLM to generate answers that cite specific source chunks.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.3,
        max_tokens: int = 1024,
        api_key: str | None = None,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")

    def generate(
        self,
        query: str,
        contexts: list[RetrievedContext],
        system_prompt: str = RAG_SYSTEM_PROMPT,
    ) -> GeneratedAnswer:
        """Generate an answer from the query and retrieved contexts.

        Args:
            query: The user's question.
            contexts: Retrieved context chunks with source info.
            system_prompt: System prompt for the LLM.

        Returns:
            Generated answer with citations.
        """
        # TODO: Implement answer generation
        # 1. Format contexts into the prompt
        # 2. Build messages list [system, user]
        # 3. Call OpenAI API
        # 4. Extract citations from the response (parse [Source N] references)
        # 5. Return GeneratedAnswer with citations and token usage
        pass

    def _build_user_prompt(
        self, query: str, formatted_context: str
    ) -> str:
        """Build the user message with context and question.

        Args:
            query: The user's question.
            formatted_context: Formatted context from retriever.

        Returns:
            Complete user prompt string.
        """
        # TODO: Implement prompt construction
        # Format as:
        # Context:
        # {formatted_context}
        #
        # Question: {query}
        #
        # Answer:
        pass

    def _extract_citations(
        self,
        answer: str,
        contexts: list[RetrievedContext],
    ) -> list[Citation]:
        """Extract [Source N] citations from the generated answer.

        Args:
            answer: The generated answer text.
            contexts: The original retrieved contexts.

        Returns:
            List of citations found in the answer.
        """
        # TODO: Implement citation extraction
        # 1. Use regex to find all [Source N] references
        # 2. Map each N back to the corresponding context
        # 3. Build Citation objects
        pass
