"""Feature pipeline that combines all feature groups into a single vector.

Orchestrates query, document, and interaction feature extractors to produce
the final feature matrix used for model training and inference.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from ranking.features.document_features import (
    CorpusStatistics,
    Document,
    DocumentFeatureExtractor,
)
from ranking.features.interaction_features import InteractionFeatureExtractor
from ranking.features.query_features import QueryFeatureExtractor


@dataclass
class QueryDocumentPair:
    """A single query-document pair for feature extraction."""

    query: str
    document: Document
    relevance_label: int | None = None


@dataclass
class FeatureVector:
    """Combined feature vector with metadata."""

    query_id: str
    doc_id: str
    features: np.ndarray
    relevance_label: int | None = None


FEATURE_NAMES: list[str] = [
    "q_num_terms", "q_num_characters", "q_avg_term_length",
    "q_max_idf", "q_min_idf", "q_mean_idf", "q_std_idf",
    "q_intent_nav", "q_intent_info", "q_intent_trans",
    "q_has_question_word", "q_num_unique_terms",
    "d_bm25_score", "d_pagerank", "d_doc_length", "d_num_unique_terms",
    "d_freshness_days", "d_url_depth", "d_num_inlinks", "d_num_outlinks",
    "d_spam_score", "d_is_html", "d_title_length", "d_has_structured_data",
    "i_tfidf_cosine", "i_exact_title", "i_exact_body", "i_exact_url",
    "i_term_coverage", "i_bm25_title", "i_bm25_body",
    "i_min_position", "i_avg_proximity",
    "i_title_ratio", "i_body_ratio",
]


class FeaturePipeline:
    """Combines query, document, and interaction feature extractors.

    Produces a unified feature vector for each query-document pair, suitable
    for training and inference with ranking models.
    """

    def __init__(
        self,
        corpus_stats: CorpusStatistics,
        idf_map: dict[str, float],
        default_idf: float = 0.0,
    ) -> None:
        self.query_extractor = QueryFeatureExtractor(idf_map=idf_map, default_idf=default_idf)
        self.doc_extractor = DocumentFeatureExtractor(corpus_stats=corpus_stats)
        self.interaction_extractor = InteractionFeatureExtractor(
            idf_map=idf_map, default_idf=default_idf
        )

    def extract_single(self, query: str, document: Document) -> np.ndarray:
        """Extract the full feature vector for one query-document pair.

        Args:
            query: Raw query string.
            document: Document to score.

        Returns:
            1-D numpy array of all features.
        """
        # TODO: Implement single-pair feature extraction
        # 1. Tokenize query
        # 2. Extract query features via self.query_extractor.extract(query)
        # 3. Extract document features via self.doc_extractor.extract(document, query_terms)
        # 4. Extract interaction features via self.interaction_extractor.extract(...)
        # 5. Concatenate all feature arrays
        raise NotImplementedError

    def extract_batch(
        self,
        pairs: list[QueryDocumentPair],
        query_ids: list[str] | None = None,
    ) -> list[FeatureVector]:
        """Extract features for a batch of query-document pairs.

        Args:
            pairs: List of query-document pairs.
            query_ids: Optional query identifiers (auto-generated if missing).

        Returns:
            List of FeatureVector objects.
        """
        # TODO: Implement batch feature extraction
        # 1. Iterate over pairs, calling extract_single for each
        # 2. Wrap results in FeatureVector with appropriate metadata
        raise NotImplementedError

    def to_dataframe(self, feature_vectors: list[FeatureVector]) -> pd.DataFrame:
        """Convert feature vectors to a pandas DataFrame.

        Args:
            feature_vectors: List of extracted feature vectors.

        Returns:
            DataFrame with FEATURE_NAMES as columns plus query_id, doc_id,
            and relevance_label columns.
        """
        # TODO: Implement DataFrame construction from feature vectors
        # 1. Stack feature arrays into a matrix
        # 2. Create DataFrame with FEATURE_NAMES columns
        # 3. Add metadata columns (query_id, doc_id, relevance_label)
        raise NotImplementedError
