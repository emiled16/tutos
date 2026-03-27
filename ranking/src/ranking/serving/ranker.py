"""Online ranking service with feature computation.

Wraps the trained model with a feature pipeline to provide end-to-end
ranking from raw queries and documents to scored results.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ranking.features.document_features import CorpusStatistics, Document
from ranking.features.feature_pipeline import FeaturePipeline
from ranking.models.lambdamart import LambdaMARTRanker


@dataclass
class ScoredDocument:
    """A document with its ranking score."""

    doc_id: str
    title: str
    score: float
    rank: int


class OnlineRanker:
    """End-to-end online ranking service.

    Combines feature extraction and model inference to rank documents
    given a raw query and candidate document list.
    """

    def __init__(
        self,
        model_path: Path,
        corpus_stats: CorpusStatistics,
        idf_map: dict[str, float],
    ) -> None:
        self.pipeline = FeaturePipeline(
            corpus_stats=corpus_stats,
            idf_map=idf_map,
        )
        self.model = LambdaMARTRanker()
        self._load_model(model_path)

    def _load_model(self, path: Path) -> None:
        """Load the trained ranking model.

        Args:
            path: Path to the saved LambdaMART model file.
        """
        # TODO: Implement model loading via self.model.load(path)
        raise NotImplementedError

    def rank(
        self,
        query: str,
        documents: list[Document],
        top_k: int = 10,
    ) -> list[ScoredDocument]:
        """Rank documents for a query, returning the top-k results.

        Args:
            query: Raw query string.
            documents: Candidate documents to rank.
            top_k: Number of top results to return.

        Returns:
            List of ScoredDocument sorted by score descending, limited to top_k.
        """
        # TODO: Implement end-to-end ranking
        # 1. Extract features for each query-document pair using self.pipeline.extract_single
        # 2. Stack features into a matrix
        # 3. Get scores from self.model.predict
        # 4. Sort by score descending and take top_k
        # 5. Build ScoredDocument list with ranks starting at 1
        raise NotImplementedError

    def score_single(self, query: str, document: Document) -> float:
        """Score a single query-document pair.

        Args:
            query: Raw query string.
            document: Document to score.

        Returns:
            Predicted relevance score.
        """
        # TODO: Implement single-document scoring
        # 1. Extract features via self.pipeline.extract_single
        # 2. Predict with self.model
        raise NotImplementedError
