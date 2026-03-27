"""Two-stage recommendation: candidate generation then ranking."""

from dataclasses import dataclass, field

import numpy as np
from scipy import sparse

from recsys.models.base import BaseRecommender


@dataclass
class CandidateSet:
    """Result of candidate generation for a user."""

    user_id: int
    item_ids: np.ndarray
    scores: np.ndarray
    source: str


class CandidateGenerator:
    """Fast candidate generation stage.

    Retrieves a broad set of candidate items using lightweight models
    (popularity, item-CF, approximate nearest neighbors on embeddings).
    Multiple generators run in parallel and their results are merged.
    """

    def __init__(
        self,
        generators: dict[str, BaseRecommender],
        candidates_per_generator: int = 100,
    ) -> None:
        """Initialize with multiple candidate generators.

        Args:
            generators: Named recommender models for candidate generation.
            candidates_per_generator: How many candidates each generator produces.
        """
        self.generators = generators
        self.candidates_per_generator = candidates_per_generator

    def generate(self, user_id: int) -> list[CandidateSet]:
        """Generate candidates from all sources for a user.

        Args:
            user_id: The user to generate candidates for.

        Returns:
            List of CandidateSets, one per generator.
        """
        # TODO: For each generator, call recommend(user_id, candidates_per_generator)
        # TODO: Wrap each result in a CandidateSet with the generator name as source
        # TODO: Handle generator failures gracefully (log and skip)
        raise NotImplementedError

    def merge_candidates(
        self,
        candidate_sets: list[CandidateSet],
    ) -> tuple[np.ndarray, np.ndarray]:
        """Merge candidates from multiple sources, deduplicating items.

        For items appearing in multiple candidate sets, keep the highest score.

        Args:
            candidate_sets: List of CandidateSets to merge.

        Returns:
            Tuple of (unique_item_ids, max_scores) arrays.
        """
        # TODO: Collect all (item_id, score) pairs across candidate sets
        # TODO: For duplicate items, keep the maximum score
        # TODO: Return deduplicated arrays sorted by score descending
        raise NotImplementedError


class TwoStageRecommender(BaseRecommender):
    """Two-stage recommender: candidate generation followed by re-ranking.

    Stage 1 (fast): Generate a broad candidate set using lightweight models.
    Stage 2 (precise): Re-rank candidates with an expressive model.
    """

    def __init__(
        self,
        candidate_generator: CandidateGenerator,
        ranker: BaseRecommender,
        n_candidates: int = 200,
    ) -> None:
        super().__init__(name="TwoStage")
        self.candidate_generator = candidate_generator
        self.ranker = ranker
        self.n_candidates = n_candidates
        self.interaction_matrix: sparse.csr_matrix | None = None
        self._user_ids: np.ndarray | None = None
        self._item_ids: np.ndarray | None = None

    def fit(
        self,
        interaction_matrix: sparse.csr_matrix,
        user_ids: np.ndarray,
        item_ids: np.ndarray,
    ) -> "TwoStageRecommender":
        self.interaction_matrix = interaction_matrix
        self._user_ids = user_ids
        self._item_ids = item_ids

        # TODO: Verify candidate generators and ranker are fitted
        # TODO: Set self.is_fitted = True
        raise NotImplementedError

    def recommend(
        self,
        user_id: int,
        n: int = 10,
        exclude_seen: bool = True,
    ) -> list[tuple[int, float]]:
        self._check_is_fitted()

        # TODO: Stage 1 — Generate candidates using self.candidate_generator
        # TODO: Merge candidate sets
        # TODO: Stage 2 — Score each candidate using self.ranker.predict(user_id, item_id)
        # TODO: Sort by ranker score, optionally exclude seen items
        # TODO: Return top-n (item_id, score) tuples
        raise NotImplementedError

    def predict(self, user_id: int, item_id: int) -> float:
        self._check_is_fitted()

        # TODO: Delegate to the ranker model
        raise NotImplementedError
