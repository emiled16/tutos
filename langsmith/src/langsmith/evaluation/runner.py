"""Evaluation runner for comparing prompt versions against datasets.

Orchestrates running LLM chains against LangSmith datasets, collecting
evaluation results, and producing comparison reports.
"""

from dataclasses import dataclass, field

from langsmith import Client

from langsmith.evaluation.evaluators import (
    CorrectnessEvaluator,
    FaithfulnessEvaluator,
    RelevanceEvaluator,
    ToxicityEvaluator,
)
from langsmith.prompts.prompt_registry import PromptRegistry


@dataclass
class EvaluationResult:
    """Results from evaluating a single prompt version against a dataset.

    Attributes:
        prompt_version: Name of the prompt version evaluated.
        dataset_name: Name of the dataset used.
        scores: Dict mapping evaluator name to list of scores.
        avg_scores: Dict mapping evaluator name to average score.
        num_examples: Number of examples evaluated.
    """

    prompt_version: str
    dataset_name: str
    scores: dict[str, list[float]] = field(default_factory=dict)
    avg_scores: dict[str, float] = field(default_factory=dict)
    num_examples: int = 0


@dataclass
class ComparisonReport:
    """Comparison report across multiple prompt versions.

    Attributes:
        dataset_name: The dataset used for comparison.
        results: List of EvaluationResult, one per prompt version.
        best_version: Name of the prompt version with the highest average score.
    """

    dataset_name: str
    results: list[EvaluationResult] = field(default_factory=list)
    best_version: str = ""


class EvaluationRunner:
    """Runs evaluations of LLM chains against LangSmith datasets.

    Supports running a single prompt version or comparing multiple
    versions side-by-side.
    """

    def __init__(
        self,
        registry: PromptRegistry,
        client: Client | None = None,
    ) -> None:
        """Initialize the evaluation runner.

        Args:
            registry: The prompt registry to pull templates from.
            client: Optional LangSmith client.
        """
        # TODO: Implement — store registry, client, and instantiate evaluators
        raise NotImplementedError

    def evaluate_version(
        self,
        prompt_version: str,
        dataset_name: str,
        model: str = "gpt-4o-mini",
    ) -> EvaluationResult:
        """Run evaluation for a single prompt version against a dataset.

        Args:
            prompt_version: Name of the prompt version to evaluate.
            dataset_name: Name of the LangSmith dataset.
            model: The LLM model to use.

        Returns:
            EvaluationResult with scores from all evaluators.
        """
        # TODO: Implement
        # 1. Get the prompt template from the registry
        # 2. Build the QA chain with this prompt
        # 3. Use langsmith.evaluation.evaluate() to run against the dataset
        # 4. Collect scores from each evaluator
        # 5. Compute average scores
        # 6. Return EvaluationResult
        raise NotImplementedError

    def compare_versions(
        self,
        prompt_versions: list[str],
        dataset_name: str,
        model: str = "gpt-4o-mini",
    ) -> ComparisonReport:
        """Compare multiple prompt versions against the same dataset.

        Args:
            prompt_versions: List of prompt version names to compare.
            dataset_name: Name of the LangSmith dataset.
            model: The LLM model to use.

        Returns:
            ComparisonReport with results for each version and the best version.
        """
        # TODO: Implement
        # 1. Run evaluate_version for each prompt version
        # 2. Determine the best version by average correctness score
        # 3. Return ComparisonReport
        raise NotImplementedError

    def print_report(self, report: ComparisonReport) -> None:
        """Pretty-print a comparison report to stdout.

        Args:
            report: The ComparisonReport to display.
        """
        # TODO: Implement
        # Format a table showing each version's scores across evaluators
        raise NotImplementedError
