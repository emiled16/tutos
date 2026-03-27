"""Query-document interaction features for ranking.

Extracts features that depend on the relationship between query and document:
TF-IDF cosine similarity, exact match signals, and term coverage.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass
class InteractionFeatures:
    """Feature vector capturing query-document interactions."""

    tfidf_cosine_similarity: float
    exact_match_title: bool
    exact_match_body: bool
    exact_match_url: bool
    query_term_coverage: float
    bm25_title: float
    bm25_body: float
    min_query_term_position: int
    avg_query_term_proximity: float
    query_terms_in_title_ratio: float
    query_terms_in_body_ratio: float

    def to_array(self) -> np.ndarray:
        """Convert features to a flat numpy array."""
        return np.array([
            self.tfidf_cosine_similarity,
            self.exact_match_title,
            self.exact_match_body,
            self.exact_match_url,
            self.query_term_coverage,
            self.bm25_title,
            self.bm25_body,
            self.min_query_term_position,
            self.avg_query_term_proximity,
            self.query_terms_in_title_ratio,
            self.query_terms_in_body_ratio,
        ], dtype=np.float64)


class InteractionFeatureExtractor:
    """Extracts features from the interaction between a query and document.

    These features capture how well a document's content matches the query,
    considering both lexical overlap and semantic similarity.
    """

    def __init__(self, idf_map: dict[str, float], default_idf: float = 0.0) -> None:
        self.idf_map = idf_map
        self.default_idf = default_idf

    def extract(
        self,
        query_terms: list[str],
        doc_title: str,
        doc_body: str,
        doc_url: str,
    ) -> InteractionFeatures:
        """Extract query-document interaction features.

        Args:
            query_terms: Tokenized, lowercased query terms.
            doc_title: Document title text.
            doc_body: Document body text.
            doc_url: Document URL.

        Returns:
            InteractionFeatures with all fields populated.
        """
        title_terms = doc_title.lower().split()
        body_terms = doc_body.lower().split()

        return InteractionFeatures(
            tfidf_cosine_similarity=self._tfidf_cosine(query_terms, body_terms),
            exact_match_title=self._exact_match(query_terms, doc_title),
            exact_match_body=self._exact_match(query_terms, doc_body),
            exact_match_url=self._exact_match_url(query_terms, doc_url),
            query_term_coverage=self._term_coverage(query_terms, body_terms),
            bm25_title=0.0,  # Computed by DocumentFeatureExtractor if needed
            bm25_body=0.0,
            min_query_term_position=self._min_term_position(query_terms, body_terms),
            avg_query_term_proximity=self._avg_proximity(query_terms, body_terms),
            query_terms_in_title_ratio=self._term_ratio(query_terms, title_terms),
            query_terms_in_body_ratio=self._term_ratio(query_terms, body_terms),
        )

    def _tfidf_cosine(self, query_terms: list[str], doc_terms: list[str]) -> float:
        """Compute TF-IDF cosine similarity between query and document.

        Builds TF-IDF vectors for both query and document over the union
        of their vocabularies, then computes cosine similarity.

        Args:
            query_terms: Query term list.
            doc_terms: Document term list.

        Returns:
            Cosine similarity in [0, 1].
        """
        # TODO: Implement TF-IDF cosine similarity
        # 1. Build term frequency dicts for query and document
        # 2. Weight by IDF from self.idf_map
        # 3. Compute cosine similarity between the two TF-IDF vectors
        raise NotImplementedError

    def _exact_match(self, query_terms: list[str], text: str) -> bool:
        """Check whether the full query appears as an exact substring.

        Args:
            query_terms: Query terms.
            text: Text to search within.

        Returns:
            True if the joined query appears in the lowercased text.
        """
        # TODO: Implement exact match check for full query phrase in text
        raise NotImplementedError

    def _exact_match_url(self, query_terms: list[str], url: str) -> bool:
        """Check whether query terms appear in the URL path or domain.

        Args:
            query_terms: Query terms.
            url: Document URL.

        Returns:
            True if any query term appears in the URL.
        """
        # TODO: Implement URL-based matching (consider hyphen/underscore separated tokens)
        raise NotImplementedError

    def _term_coverage(self, query_terms: list[str], doc_terms: list[str]) -> float:
        """Fraction of unique query terms that appear in the document.

        Args:
            query_terms: Query terms.
            doc_terms: Document terms.

        Returns:
            Coverage ratio in [0, 1].
        """
        # TODO: Implement query term coverage as |Q ∩ D| / |Q|
        raise NotImplementedError

    def _min_term_position(self, query_terms: list[str], doc_terms: list[str]) -> int:
        """Find the earliest position of any query term in the document.

        Args:
            query_terms: Query terms.
            doc_terms: Document terms.

        Returns:
            0-based position of earliest match, or -1 if no match.
        """
        # TODO: Implement by scanning doc_terms for the first occurrence of any query term
        raise NotImplementedError

    def _avg_proximity(self, query_terms: list[str], doc_terms: list[str]) -> float:
        """Average minimum distance between query terms in the document.

        Measures how close together the query terms appear in the document.

        Args:
            query_terms: Query terms.
            doc_terms: Document terms.

        Returns:
            Average token distance between consecutive query term occurrences,
            or -1.0 if fewer than 2 query terms appear.
        """
        # TODO: Implement proximity scoring
        # 1. Find all positions where each query term appears in doc_terms
        # 2. Compute minimum pairwise distances between different query terms
        # 3. Return the average of these minimum distances
        raise NotImplementedError

    def _term_ratio(self, query_terms: list[str], field_terms: list[str]) -> float:
        """Fraction of query terms found in a document field.

        Args:
            query_terms: Query terms.
            field_terms: Tokenized field (title or body).

        Returns:
            Ratio in [0, 1].
        """
        # TODO: Implement as count of matching unique query terms / total unique query terms
        raise NotImplementedError
