"""Tests for custom LangSmith evaluators."""

from unittest.mock import MagicMock, patch

import pytest
from langsmith.schemas import Example, Run

from langsmith.evaluation.evaluators import (
    CorrectnessEvaluator,
    FaithfulnessEvaluator,
    RelevanceEvaluator,
    ToxicityEvaluator,
)


@pytest.fixture
def mock_run() -> Run:
    """Create a mock LangSmith Run for testing."""
    # TODO: Implement — create a mock Run with realistic inputs/outputs
    raise NotImplementedError


@pytest.fixture
def mock_example() -> Example:
    """Create a mock LangSmith Example with reference data."""
    # TODO: Implement — create a mock Example with expected outputs
    raise NotImplementedError


class TestCorrectnessEvaluator:
    """Tests for the CorrectnessEvaluator."""

    @patch("langsmith.evaluation.evaluators.ChatOpenAI")
    def test_correct_answer_scores_high(
        self, mock_llm_cls: MagicMock, mock_run: Run, mock_example: Example
    ) -> None:
        """A correct answer should receive a high correctness score."""
        # TODO: Implement
        # 1. Configure mock LLM to return a "correct" judgment
        # 2. Instantiate CorrectnessEvaluator
        # 3. Call evaluate_run
        # 4. Assert score >= 0.8
        raise NotImplementedError

    @patch("langsmith.evaluation.evaluators.ChatOpenAI")
    def test_incorrect_answer_scores_low(
        self, mock_llm_cls: MagicMock, mock_run: Run, mock_example: Example
    ) -> None:
        """An incorrect answer should receive a low correctness score."""
        # TODO: Implement
        raise NotImplementedError

    @patch("langsmith.evaluation.evaluators.ChatOpenAI")
    def test_result_has_comment(
        self, mock_llm_cls: MagicMock, mock_run: Run, mock_example: Example
    ) -> None:
        """The evaluation result should include a reasoning comment."""
        # TODO: Implement
        raise NotImplementedError


class TestRelevanceEvaluator:
    """Tests for the RelevanceEvaluator."""

    @patch("langsmith.evaluation.evaluators.ChatOpenAI")
    def test_relevant_answer(
        self, mock_llm_cls: MagicMock, mock_run: Run
    ) -> None:
        """An on-topic answer should score high on relevance."""
        # TODO: Implement
        raise NotImplementedError

    @patch("langsmith.evaluation.evaluators.ChatOpenAI")
    def test_irrelevant_answer(
        self, mock_llm_cls: MagicMock, mock_run: Run
    ) -> None:
        """An off-topic answer should score low on relevance."""
        # TODO: Implement
        raise NotImplementedError


class TestFaithfulnessEvaluator:
    """Tests for the FaithfulnessEvaluator."""

    @patch("langsmith.evaluation.evaluators.ChatOpenAI")
    def test_faithful_answer(
        self, mock_llm_cls: MagicMock, mock_run: Run
    ) -> None:
        """An answer grounded in the context should score high."""
        # TODO: Implement
        raise NotImplementedError

    @patch("langsmith.evaluation.evaluators.ChatOpenAI")
    def test_hallucinated_answer(
        self, mock_llm_cls: MagicMock, mock_run: Run
    ) -> None:
        """An answer with claims not in the context should score low."""
        # TODO: Implement
        raise NotImplementedError


class TestToxicityEvaluator:
    """Tests for the ToxicityEvaluator."""

    @patch("langsmith.evaluation.evaluators.ChatOpenAI")
    def test_clean_answer_scores_low(
        self, mock_llm_cls: MagicMock, mock_run: Run
    ) -> None:
        """A non-toxic answer should have a near-zero toxicity score."""
        # TODO: Implement
        raise NotImplementedError

    @patch("langsmith.evaluation.evaluators.ChatOpenAI")
    def test_toxic_answer_scores_high(
        self, mock_llm_cls: MagicMock, mock_run: Run
    ) -> None:
        """A toxic answer should have a high toxicity score."""
        # TODO: Implement
        raise NotImplementedError
