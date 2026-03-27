"""Document-level features for ranking.

Extracts features that depend only on the document (independent of query):
BM25 corpus statistics, PageRank, freshness, and structural properties.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime

import numpy as np


@dataclass
class DocumentFeatures:
    """Feature vector for a single document."""

    bm25_score: float
    pagerank: float
    doc_length: int
    num_unique_terms: int
    freshness_days: float
    url_depth: int
    num_inlinks: int
    num_outlinks: int
    spam_score: float
    content_type_is_html: bool
    title_length: int
    has_structured_data: bool

    def to_array(self) -> np.ndarray:
        """Convert features to a flat numpy array."""
        return np.array([
            self.bm25_score,
            self.pagerank,
            self.doc_length,
            self.num_unique_terms,
            self.freshness_days,
            self.url_depth,
            self.num_inlinks,
            self.num_outlinks,
            self.spam_score,
            self.content_type_is_html,
            self.title_length,
            self.has_structured_data,
        ], dtype=np.float64)


@dataclass
class Document:
    """Raw document representation."""

    doc_id: str
    title: str
    body: str
    url: str
    pagerank: float = 0.0
    num_inlinks: int = 0
    num_outlinks: int = 0
    spam_score: float = 0.0
    published_date: datetime | None = None
    content_type: str = "text/html"
    has_structured_data: bool = False


@dataclass
class CorpusStatistics:
    """Pre-computed statistics needed for BM25 scoring."""

    total_docs: int
    avg_doc_length: float
    doc_frequencies: dict[str, int] = field(default_factory=dict)


class DocumentFeatureExtractor:
    """Extracts document-level features.

    Requires corpus statistics for BM25 computation and a reference
    datetime for freshness calculation.
    """

    def __init__(
        self,
        corpus_stats: CorpusStatistics,
        reference_date: datetime | None = None,
        bm25_k1: float = 1.2,
        bm25_b: float = 0.75,
    ) -> None:
        self.corpus_stats = corpus_stats
        self.reference_date = reference_date or datetime.now()
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b

    def extract(self, document: Document, query_terms: list[str]) -> DocumentFeatures:
        """Extract all document-level features.

        Args:
            document: The document to extract features from.
            query_terms: Tokenized query terms (needed for BM25).

        Returns:
            DocumentFeatures with all fields populated.
        """
        return DocumentFeatures(
            bm25_score=self._compute_bm25(document, query_terms),
            pagerank=document.pagerank,
            doc_length=len(document.body.split()),
            num_unique_terms=len(set(document.body.lower().split())),
            freshness_days=self._compute_freshness(document),
            url_depth=self._compute_url_depth(document.url),
            num_inlinks=document.num_inlinks,
            num_outlinks=document.num_outlinks,
            spam_score=document.spam_score,
            content_type_is_html=document.content_type == "text/html",
            title_length=len(document.title.split()),
            has_structured_data=document.has_structured_data,
        )

    def _compute_bm25(self, document: Document, query_terms: list[str]) -> float:
        """Compute BM25 score for a document given query terms.

        Uses the standard BM25 formula with k1 and b parameters from
        the instance configuration and corpus-level statistics.

        Args:
            document: Document to score.
            query_terms: Tokenized query.

        Returns:
            BM25 relevance score.
        """
        # TODO: Implement BM25 scoring using term frequency and inverse document frequency
        # 1. Tokenize the document body
        # 2. Compute term frequencies for each query term in the document
        # 3. For each query term, compute IDF using corpus_stats.doc_frequencies
        # 4. Apply the BM25 formula with length normalization using corpus_stats.avg_doc_length
        # 5. Sum the per-term scores
        raise NotImplementedError

    def _compute_freshness(self, document: Document) -> float:
        """Compute document freshness as days since publication.

        Args:
            document: Document with optional published_date.

        Returns:
            Days since publication, or -1.0 if no date is available.
        """
        # TODO: Implement freshness calculation using self.reference_date
        raise NotImplementedError

    def _compute_url_depth(self, url: str) -> int:
        """Count the path depth of a URL.

        Args:
            url: Full URL string.

        Returns:
            Number of path segments (e.g., "https://a.com/b/c" → 2).
        """
        # TODO: Implement URL depth by counting path segments after the domain
        raise NotImplementedError
