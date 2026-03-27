"""Custom LangSmith evaluators for measuring LLM output quality.

Each evaluator implements the LangSmith evaluator interface and scores
outputs on a specific quality dimension with a numerical score and reasoning.
"""

from langchain_openai import ChatOpenAI
from langsmith.evaluation import EvaluationResult, RunEvaluator
from langsmith.schemas import Example, Run


class CorrectnessEvaluator(RunEvaluator):
    """Evaluates whether the LLM output is factually correct.

    Uses an LLM-as-judge approach: a stronger model checks whether the
    answer is consistent with the provided reference answer.
    """

    def __init__(self, model: str = "gpt-4o") -> None:
        self.llm = ChatOpenAI(model=model, temperature=0.0)

    def evaluate_run(
        self,
        run: Run,
        example: Example | None = None,
    ) -> EvaluationResult:
        """Evaluate a single run for correctness.

        Args:
            run: The LangSmith run to evaluate (contains inputs/outputs).
            example: The dataset example with reference output.

        Returns:
            EvaluationResult with key "correctness", score 0.0-1.0, and comment.
        """
        # TODO: Implement
        # 1. Extract the prediction from run.outputs
        # 2. Extract the reference answer from example.outputs
        # 3. Construct a judge prompt asking whether the prediction matches the reference
        # 4. Call self.llm to get the judgment
        # 5. Parse the score and reasoning
        # 6. Return EvaluationResult(key="correctness", score=..., comment=...)
        raise NotImplementedError


class RelevanceEvaluator(RunEvaluator):
    """Evaluates whether the LLM output is relevant to the input question.

    This is a reference-free evaluator: it only checks that the answer
    addresses what was asked, regardless of correctness.
    """

    def __init__(self, model: str = "gpt-4o") -> None:
        self.llm = ChatOpenAI(model=model, temperature=0.0)

    def evaluate_run(
        self,
        run: Run,
        example: Example | None = None,
    ) -> EvaluationResult:
        """Evaluate a single run for relevance to the question.

        Args:
            run: The LangSmith run to evaluate.
            example: Optional dataset example (used for input question).

        Returns:
            EvaluationResult with key "relevance", score 0.0-1.0, and comment.
        """
        # TODO: Implement
        # 1. Extract the question from run.inputs
        # 2. Extract the answer from run.outputs
        # 3. Prompt the judge: "Does this answer address the question?"
        # 4. Return EvaluationResult(key="relevance", score=..., comment=...)
        raise NotImplementedError


class FaithfulnessEvaluator(RunEvaluator):
    """Evaluates whether the answer is faithful to the source documents.

    Checks for hallucinations by verifying that all claims in the answer
    are supported by the provided context documents.
    """

    def __init__(self, model: str = "gpt-4o") -> None:
        self.llm = ChatOpenAI(model=model, temperature=0.0)

    def evaluate_run(
        self,
        run: Run,
        example: Example | None = None,
    ) -> EvaluationResult:
        """Evaluate a single run for faithfulness to source documents.

        Args:
            run: The LangSmith run to evaluate.
            example: Optional dataset example.

        Returns:
            EvaluationResult with key "faithfulness", score 0.0-1.0, and comment.
        """
        # TODO: Implement
        # 1. Extract the context/documents from run.inputs
        # 2. Extract the answer from run.outputs
        # 3. Prompt the judge: "Is every claim in the answer supported by the context?"
        # 4. Return EvaluationResult(key="faithfulness", score=..., comment=...)
        raise NotImplementedError


class ToxicityEvaluator(RunEvaluator):
    """Evaluates whether the LLM output contains toxic or harmful content.

    Scores from 0.0 (no toxicity) to 1.0 (highly toxic). In practice,
    you want this score to be as close to 0.0 as possible.
    """

    def __init__(self, model: str = "gpt-4o") -> None:
        self.llm = ChatOpenAI(model=model, temperature=0.0)

    def evaluate_run(
        self,
        run: Run,
        example: Example | None = None,
    ) -> EvaluationResult:
        """Evaluate a single run for toxic content.

        Args:
            run: The LangSmith run to evaluate.
            example: Optional dataset example.

        Returns:
            EvaluationResult with key "toxicity", score 0.0-1.0, and comment.
        """
        # TODO: Implement
        # 1. Extract the answer from run.outputs
        # 2. Prompt the judge to check for harmful, biased, or toxic content
        # 3. Return EvaluationResult(key="toxicity", score=..., comment=...)
        raise NotImplementedError
