"""Benchmark comparison between fine-tuned and base models.

Runs both models on the same test set and produces a comparative
analysis of their performance.
"""

from dataclasses import dataclass, field
from pathlib import Path

from transformers import PreTrainedModel, PreTrainedTokenizerBase

from llm_fine_tuning.evaluation.metrics import compute_all_metrics
from llm_fine_tuning.inference.generate import generate_responses


@dataclass
class BenchmarkResult:
    """Results from benchmarking a single model.

    Attributes:
        model_name: Identifier for the model.
        metrics: Dict of all computed metrics.
        predictions: The model's generated responses.
        avg_generation_time: Average time per generation in seconds.
    """

    model_name: str
    metrics: dict = field(default_factory=dict)
    predictions: list[str] = field(default_factory=list)
    avg_generation_time: float = 0.0


@dataclass
class ComparisonResult:
    """Side-by-side comparison of two models.

    Attributes:
        base_result: Benchmark results for the base model.
        finetuned_result: Benchmark results for the fine-tuned model.
        improvements: Dict mapping metric name to percentage improvement.
    """

    base_result: BenchmarkResult
    finetuned_result: BenchmarkResult
    improvements: dict[str, float] = field(default_factory=dict)


def benchmark_model(
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    test_inputs: list[str],
    test_references: list[str],
    model_name: str = "model",
    max_new_tokens: int = 256,
) -> BenchmarkResult:
    """Run a full benchmark on a single model.

    Args:
        model: The model to benchmark.
        tokenizer: The tokenizer.
        test_inputs: List of input prompts.
        test_references: List of expected reference outputs.
        model_name: Human-readable name for the model.
        max_new_tokens: Maximum tokens to generate per input.

    Returns:
        BenchmarkResult with metrics and predictions.
    """
    # TODO: Implement
    # 1. Generate responses for all test inputs
    # 2. Compute all metrics (ROUGE, BERTScore, domain accuracy)
    # 3. Compute perplexity on the test references
    # 4. Measure average generation time
    # 5. Return BenchmarkResult
    raise NotImplementedError


def compare_models(
    base_model: PreTrainedModel,
    finetuned_model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    test_inputs: list[str],
    test_references: list[str],
) -> ComparisonResult:
    """Compare base and fine-tuned models side by side.

    Args:
        base_model: The original pre-trained model.
        finetuned_model: The fine-tuned model (with or without adapter).
        tokenizer: Shared tokenizer.
        test_inputs: List of test prompts.
        test_references: List of reference outputs.

    Returns:
        ComparisonResult with both benchmarks and improvement percentages.
    """
    # TODO: Implement
    # 1. Benchmark the base model
    # 2. Benchmark the fine-tuned model
    # 3. Compute percentage improvements for each metric
    # 4. Return ComparisonResult
    raise NotImplementedError


def print_comparison(result: ComparisonResult) -> None:
    """Pretty-print a model comparison table.

    Args:
        result: The ComparisonResult to display.
    """
    # TODO: Implement
    # Format a table with base vs finetuned metrics and improvement percentages
    raise NotImplementedError
