"""Dense vector similarity search."""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, Field
from qdrant_client import QdrantClient

from qdrant.indexing.embedder import DenseEmbedder

logger = logging.getLogger(__name__)


class SearchResult(BaseModel):
    """A single search result with score and payload."""

    point_id: str
    score: float
    text: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class DenseSearch:
    """Dense vector similarity search against a Qdrant collection.

    Embeds the query text with the same model used for indexing,
    then performs ANN search using Qdrant's HNSW index.
    """

    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
        embedder: DenseEmbedder,
    ) -> None:
        self.client = client
        self.collection_name = collection_name
        self.embedder = embedder

    def search(
        self,
        query: str,
        top_k: int = 10,
        score_threshold: float | None = None,
    ) -> list[SearchResult]:
        """Search for documents similar to the query.

        Args:
            query: Natural language search query.
            top_k: Number of results to return.
            score_threshold: Minimum similarity score (optional).

        Returns:
            Ranked list of search results.
        """
        # TODO: Implement dense search
        # 1. Embed query using self.embedder.embed_query()
        # 2. Call client.search() with query vector
        # 3. Apply score_threshold filter if provided
        # 4. Convert Qdrant ScoredPoint results to SearchResult models
        pass

    def search_with_vector(
        self,
        query_vector: list[float],
        top_k: int = 10,
    ) -> list[SearchResult]:
        """Search using a pre-computed query vector.

        Args:
            query_vector: Pre-embedded query vector.
            top_k: Number of results.

        Returns:
            Ranked list of search results.
        """
        # TODO: Implement vector-based search
        # Direct call to client.search() without embedding step
        pass
