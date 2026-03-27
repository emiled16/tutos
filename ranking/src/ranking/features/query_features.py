"""Query-level features for ranking.

Extracts features that depend only on the query (independent of documents):
query length, term frequency statistics, and intent classification.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum

import numpy as np


class QueryIntent(Enum):
    """Coarse query intent categories."""

    NAVIGATIONAL = "navigational"
    INFORMATIONAL = "informational"
    TRANSACTIONAL = "transactional"


@dataclass
class QueryFeatures:
    """Feature vector for a single query."""

    num_terms: int
    num_characters: int
    avg_term_length: float
    max_idf: float
    min_idf: float
    mean_idf: float
    std_idf: float
    intent: QueryIntent
    has_question_word: bool
    num_unique_terms: int

    def to_array(self) -> np.ndarray:
        """Convert features to a flat numpy array."""
        return np.array([
            self.num_terms,
            self.num_characters,
            self.avg_term_length,
            self.max_idf,
            self.min_idf,
            self.mean_idf,
            self.std_idf,
            self.intent.value == "navigational",
            self.intent.value == "informational",
            self.intent.value == "transactional",
            self.has_question_word,
            self.num_unique_terms,
        ], dtype=np.float64)


QUESTION_WORDS = {"who", "what", "where", "when", "why", "how", "which", "whom", "whose"}


@dataclass
class QueryFeatureExtractor:
    """Extracts query-level features.

    Requires a pre-computed IDF mapping from corpus statistics.
    """

    idf_map: dict[str, float] = field(default_factory=dict)
    default_idf: float = 0.0

    def extract(self, query: str) -> QueryFeatures:
        """Extract all query-level features from a raw query string.

        Args:
            query: Raw query string (may contain multiple terms).

        Returns:
            QueryFeatures with all fields populated.
        """
        terms = self._tokenize(query)
        idf_values = self._compute_idf_stats(terms)
        intent = self._classify_intent(terms, query)

        return QueryFeatures(
            num_terms=len(terms),
            num_characters=len(query),
            avg_term_length=np.mean([len(t) for t in terms]) if terms else 0.0,
            max_idf=float(np.max(idf_values)) if idf_values else 0.0,
            min_idf=float(np.min(idf_values)) if idf_values else 0.0,
            mean_idf=float(np.mean(idf_values)) if idf_values else 0.0,
            std_idf=float(np.std(idf_values)) if idf_values else 0.0,
            intent=intent,
            has_question_word=any(t.lower() in QUESTION_WORDS for t in terms),
            num_unique_terms=len(set(terms)),
        )

    def _tokenize(self, query: str) -> list[str]:
        """Tokenize query into terms.

        Args:
            query: Raw query string.

        Returns:
            List of lowercased terms.
        """
        # TODO: Implement tokenization — split on whitespace, lowercase, strip punctuation
        raise NotImplementedError

    def _compute_idf_stats(self, terms: list[str]) -> list[float]:
        """Look up IDF values for each term.

        Args:
            terms: Tokenized query terms.

        Returns:
            List of IDF values (uses default_idf for unknown terms).
        """
        # TODO: Implement IDF lookup from self.idf_map, falling back to self.default_idf
        raise NotImplementedError

    def _classify_intent(self, terms: list[str], raw_query: str) -> QueryIntent:
        """Classify query intent using simple heuristics.

        Args:
            terms: Tokenized query terms.
            raw_query: Original query string.

        Returns:
            Predicted QueryIntent category.
        """
        # TODO: Implement intent classification heuristics
        # - Navigational: contains domain-like tokens (e.g., ".com"), short queries with brand names
        # - Transactional: contains action words ("buy", "download", "price", "cheap")
        # - Informational: question words, longer queries, "how to" patterns
        raise NotImplementedError
