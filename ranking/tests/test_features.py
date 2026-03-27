"""Tests for feature extraction modules."""

from __future__ import annotations

from datetime import datetime

import numpy as np
import pytest

from ranking.features.document_features import (
    CorpusStatistics,
    Document,
    DocumentFeatureExtractor,
)
from ranking.features.interaction_features import InteractionFeatureExtractor
from ranking.features.query_features import QueryFeatureExtractor, QueryIntent


@pytest.fixture
def idf_map() -> dict[str, float]:
    return {
        "python": 2.5,
        "programming": 1.8,
        "tutorial": 3.0,
        "machine": 2.0,
        "learning": 1.5,
        "search": 2.2,
        "ranking": 3.5,
    }


@pytest.fixture
def corpus_stats() -> CorpusStatistics:
    return CorpusStatistics(
        total_docs=10000,
        avg_doc_length=500.0,
        doc_frequencies={"python": 1200, "programming": 3000, "tutorial": 800},
    )


@pytest.fixture
def sample_document() -> Document:
    return Document(
        doc_id="doc_001",
        title="Python Programming Tutorial",
        body="Learn python programming with this comprehensive tutorial on search ranking",
        url="https://example.com/tutorials/python",
        pagerank=0.5,
        num_inlinks=100,
        num_outlinks=10,
        published_date=datetime(2024, 6, 15),
    )


class TestQueryFeatureExtractor:
    def test_extract_returns_correct_num_terms(self, idf_map: dict[str, float]) -> None:
        # TODO: Test that num_terms matches the number of whitespace-separated tokens
        extractor = QueryFeatureExtractor(idf_map=idf_map, default_idf=1.0)
        features = extractor.extract("python programming tutorial")
        assert features.num_terms == 3

    def test_extract_detects_question_words(self, idf_map: dict[str, float]) -> None:
        # TODO: Test that queries starting with "how", "what", etc. set has_question_word
        extractor = QueryFeatureExtractor(idf_map=idf_map, default_idf=1.0)
        features = extractor.extract("how to learn python")
        assert features.has_question_word is True

    def test_extract_idf_stats_use_default_for_unknown_terms(
        self, idf_map: dict[str, float]
    ) -> None:
        # TODO: Test that unknown terms fall back to default_idf
        extractor = QueryFeatureExtractor(idf_map=idf_map, default_idf=0.5)
        features = extractor.extract("xyznonexistent")
        assert features.mean_idf == pytest.approx(0.5)

    def test_classify_informational_intent(self, idf_map: dict[str, float]) -> None:
        # TODO: Test that "how to" queries are classified as informational
        extractor = QueryFeatureExtractor(idf_map=idf_map, default_idf=1.0)
        features = extractor.extract("how to implement search ranking")
        assert features.intent == QueryIntent.INFORMATIONAL

    def test_to_array_shape(self, idf_map: dict[str, float]) -> None:
        # TODO: Test that to_array returns a 1-D array with the expected number of elements
        extractor = QueryFeatureExtractor(idf_map=idf_map, default_idf=1.0)
        features = extractor.extract("python tutorial")
        arr = features.to_array()
        assert arr.ndim == 1
        assert len(arr) == 12


class TestDocumentFeatureExtractor:
    def test_bm25_score_is_positive_for_matching_terms(
        self, corpus_stats: CorpusStatistics, sample_document: Document
    ) -> None:
        # TODO: Test that BM25 returns a positive score when query terms appear in the document
        extractor = DocumentFeatureExtractor(corpus_stats=corpus_stats)
        features = extractor.extract(sample_document, ["python", "programming"])
        assert features.bm25_score > 0.0

    def test_bm25_score_is_zero_for_absent_terms(
        self, corpus_stats: CorpusStatistics, sample_document: Document
    ) -> None:
        # TODO: Test that BM25 returns 0 when no query terms appear in the document
        extractor = DocumentFeatureExtractor(corpus_stats=corpus_stats)
        features = extractor.extract(sample_document, ["quantum", "physics"])
        assert features.bm25_score == pytest.approx(0.0)

    def test_freshness_positive_for_past_date(
        self, corpus_stats: CorpusStatistics, sample_document: Document
    ) -> None:
        # TODO: Test that freshness_days is positive for documents with a past publication date
        ref_date = datetime(2025, 1, 1)
        extractor = DocumentFeatureExtractor(corpus_stats=corpus_stats, reference_date=ref_date)
        features = extractor.extract(sample_document, ["python"])
        assert features.freshness_days > 0

    def test_url_depth(
        self, corpus_stats: CorpusStatistics, sample_document: Document
    ) -> None:
        # TODO: Test that URL depth counts path segments correctly
        extractor = DocumentFeatureExtractor(corpus_stats=corpus_stats)
        features = extractor.extract(sample_document, ["python"])
        assert features.url_depth == 2  # /tutorials/python


class TestInteractionFeatureExtractor:
    def test_exact_match_title(self, idf_map: dict[str, float]) -> None:
        # TODO: Test exact match detection when query phrase appears in title
        extractor = InteractionFeatureExtractor(idf_map=idf_map)
        features = extractor.extract(
            query_terms=["python", "programming"],
            doc_title="Python Programming Tutorial",
            doc_body="Some body text",
            doc_url="https://example.com",
        )
        assert features.exact_match_title is True

    def test_term_coverage_all_terms_present(self, idf_map: dict[str, float]) -> None:
        # TODO: Test that coverage is 1.0 when all query terms appear in the document
        extractor = InteractionFeatureExtractor(idf_map=idf_map)
        features = extractor.extract(
            query_terms=["python", "tutorial"],
            doc_title="Title",
            doc_body="python tutorial content",
            doc_url="https://example.com",
        )
        assert features.query_term_coverage == pytest.approx(1.0)

    def test_term_coverage_partial(self, idf_map: dict[str, float]) -> None:
        # TODO: Test coverage with only some query terms in the document
        extractor = InteractionFeatureExtractor(idf_map=idf_map)
        features = extractor.extract(
            query_terms=["python", "java"],
            doc_title="Title",
            doc_body="python is great",
            doc_url="https://example.com",
        )
        assert features.query_term_coverage == pytest.approx(0.5)

    def test_tfidf_cosine_identical_gives_high_similarity(
        self, idf_map: dict[str, float]
    ) -> None:
        # TODO: Test that identical query and document content produces high cosine similarity
        extractor = InteractionFeatureExtractor(idf_map=idf_map)
        features = extractor.extract(
            query_terms=["python", "ranking"],
            doc_title="Title",
            doc_body="python ranking",
            doc_url="https://example.com",
        )
        assert features.tfidf_cosine_similarity > 0.8
