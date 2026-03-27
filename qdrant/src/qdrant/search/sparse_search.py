"""Sparse vector (BM25) search."""

from __future__ import annotations

import logging
from typing import Any

from qdrant_client import QdrantClient

from qdrant.indexing.embedder import SparseEmbedder
from qdrant.search.dense_search import SearchResult

logger = logging.getLogger(__name__)


class SparseSearch:
    """Sparse vector search using BM25-style scoring.

    Converts queries into sparse vectors and searches the sparse
    vector space in the Qdrant collection.
    """

    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
        embedder: SparseEmbedder,
    ) -> None:
        self.client = client
        self.collection_name = collection_name
        self.embedder = embedder

    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[SearchResult]:
        """Search using sparse (lexical) similarity.

        Args:
            query: Natural language search query.
            top_k: Number of results to return.

        Returns:
            Ranked list of search results.
        """
        # TODO: Implement sparse search
        # 1. Embed query using sparse embedder
        # 2. Build SparseVector from indices and values
        # 3. Call client.search() using named vector "sparse"
        # 4. Convert results to SearchResult models
        pass
