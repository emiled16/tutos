"""Search with metadata payload filters."""

from __future__ import annotations

import logging
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchValue,
    Range,
)

from qdrant.indexing.embedder import DenseEmbedder
from qdrant.search.dense_search import SearchResult

logger = logging.getLogger(__name__)


class FilteredSearch:
    """Dense vector search with payload-based filtering.

    Supports must, should, and must_not filter conditions
    on indexed payload fields.
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
        must: list[dict[str, Any]] | None = None,
        should: list[dict[str, Any]] | None = None,
        must_not: list[dict[str, Any]] | None = None,
    ) -> list[SearchResult]:
        """Search with metadata filters applied.

        Filter dicts have the form:
        - {"field": "category", "match": "science"}      (exact match)
        - {"field": "year", "gte": 2020}                  (range)
        - {"field": "year", "lte": 2024, "gte": 2020}    (range)

        Args:
            query: Natural language search query.
            top_k: Number of results.
            must: Conditions that ALL must be true (AND).
            should: Conditions where AT LEAST ONE must be true (OR).
            must_not: Conditions that must NOT be true (NOT).

        Returns:
            Filtered and ranked search results.
        """
        # TODO: Implement filtered search
        # 1. Embed query
        # 2. Build Filter object from must/should/must_not dicts
        # 3. Call client.search() with query_filter parameter
        # 4. Convert to SearchResult list
        pass

    def _build_filter(
        self,
        must: list[dict[str, Any]] | None,
        should: list[dict[str, Any]] | None,
        must_not: list[dict[str, Any]] | None,
    ) -> Filter | None:
        """Build a Qdrant Filter from condition dictionaries.

        Args:
            must: AND conditions.
            should: OR conditions.
            must_not: NOT conditions.

        Returns:
            A Qdrant Filter object, or None if no conditions.
        """
        # TODO: Implement filter construction
        # 1. For each condition dict, create a FieldCondition
        # 2. If "match" key present, use MatchValue
        # 3. If "gte"/"lte" keys present, use Range
        # 4. Build Filter(must=[...], should=[...], must_not=[...])
        pass

    def _build_field_condition(
        self, condition: dict[str, Any]
    ) -> FieldCondition:
        """Convert a condition dict to a FieldCondition.

        Args:
            condition: Dict with "field" and match/range parameters.

        Returns:
            A FieldCondition for Qdrant filtering.
        """
        # TODO: Implement field condition construction
        pass
