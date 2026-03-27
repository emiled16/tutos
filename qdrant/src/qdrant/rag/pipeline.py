"""End-to-end RAG pipeline combining retrieval and generation."""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, Field

from qdrant.rag.generator import GeneratedAnswer, Generator
from qdrant.rag.retriever import RetrievedContext, Retriever

logger = logging.getLogger(__name__)


class RAGResponse(BaseModel):
    """Complete response from the RAG pipeline."""

    query: str
    answer: str
    citations: list[dict[str, Any]] = Field(default_factory=list)
    retrieved_contexts: list[RetrievedContext] = Field(default_factory=list)
    model: str = ""
    total_tokens: int = 0


class RAGPipeline:
    """End-to-end Retrieval-Augmented Generation pipeline.

    Combines retrieval (Qdrant hybrid search) with generation (LLM)
    to produce grounded, cited answers.
    """

    def __init__(
        self,
        retriever: Retriever,
        generator: Generator,
    ) -> None:
        self.retriever = retriever
        self.generator = generator

    def query(
        self,
        question: str,
        top_k: int | None = None,
        filters: dict[str, Any] | None = None,
    ) -> RAGResponse:
        """Run the full RAG pipeline: retrieve then generate.

        Args:
            question: The user's question.
            top_k: Override retriever's default top_k.
            filters: Optional metadata filters for retrieval.

        Returns:
            Complete RAG response with answer, citations, and sources.
        """
        # TODO: Implement RAG pipeline
        # 1. Retrieve relevant contexts
        # 2. Format context for the generator
        # 3. Generate answer with citations
        # 4. Build and return RAGResponse
        pass

    def query_with_history(
        self,
        question: str,
        conversation_history: list[dict[str, str]],
        top_k: int | None = None,
    ) -> RAGResponse:
        """Run RAG with conversation history for follow-up questions.

        Reformulates the question using conversation context before retrieval.

        Args:
            question: The follow-up question.
            conversation_history: Prior conversation turns.
            top_k: Override retriever's default top_k.

        Returns:
            RAG response for the contextualized question.
        """
        # TODO: Implement conversational RAG
        # 1. Reformulate the question using conversation history
        #    (e.g., resolve pronouns, add context from prior turns)
        # 2. Run standard RAG pipeline with reformulated question
        pass

    def _reformulate_query(
        self, question: str, history: list[dict[str, str]]
    ) -> str:
        """Reformulate a follow-up question to be self-contained.

        Uses the LLM to rewrite the question incorporating conversation context.

        Args:
            question: The follow-up question.
            history: Prior conversation turns.

        Returns:
            Self-contained reformulated question.
        """
        # TODO: Implement query reformulation
        # Prompt the LLM to rewrite the question so it makes sense
        # without the conversation history
        pass
