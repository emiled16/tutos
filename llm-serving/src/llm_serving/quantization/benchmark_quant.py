"""Compare quality and speed across quantization methods.

Runs the same prompts through models quantized with different methods
and compares perplexity, generation quality, speed, and memory usage.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class QuantBenchmarkResult:
    """Results from benchmarking a single quantized model.

    Attributes:
        method: Quantization method name (e.g., "gptq-4bit", "awq-4bit").
        model_size_gb: Size of the quantized model on disk.
        gpu_memory_gb: GPU memory usage during inference.
        perplexity: Perplexity on the evaluation set.
        tokens_per_second: Average tokens per second during generation.
        ttft_ms: Average time to first token in milliseconds.
        sample_outputs: A few sample outputs for qualitative comparison.
    """

    method: str
    model_size_gb: float = 0.0
    gpu_memory_gb: float = 0.0
    perplexity: float = 0.0
    tokens_per_second: float = 0.0
    ttft_ms: float = 0.0
    sample_outputs: list[str] = field(default_factory=list)


def benchmark_quantized_model(
    model_path: str | Path,
    method_name: str,
    eval_prompts: list[str],
    eval_texts: list[str] | None = None,
    num_generate_tokens: int = 128,
) -> QuantBenchmarkResult:
    """Benchmark a single quantized model.

    Args:
        model_path: Path to the quantized model.
        method_name: Name of the quantization method.
        eval_prompts: Prompts to generate from.
        eval_texts: Texts for perplexity evaluation.
        num_generate_tokens: Tokens to generate per prompt.

    Returns:
        QuantBenchmarkResult with all metrics.
    """
    # TODO: Implement
    # 1. Load the quantized model
    # 2. Measure GPU memory usage
    # 3. Compute perplexity on eval_texts
    # 4. Generate responses for eval_prompts, measuring TPS and TTFT
    # 5. Collect sample outputs
    # 6. Return QuantBenchmarkResult
    raise NotImplementedError


def compare_quantization_methods(
    model_paths: dict[str, str | Path],
    eval_prompts: list[str],
    eval_texts: list[str] | None = None,
) -> list[QuantBenchmarkResult]:
    """Compare multiple quantization methods side by side.

    Args:
        model_paths: Dict mapping method name to model path.
        eval_prompts: Prompts for generation benchmarking.
        eval_texts: Texts for perplexity evaluation.

    Returns:
        List of QuantBenchmarkResult, one per method.
    """
    # TODO: Implement
    # 1. Benchmark each model
    # 2. Sort by tokens_per_second (or user-specified metric)
    # 3. Return results
    raise NotImplementedError


def print_comparison_table(results: list[QuantBenchmarkResult]) -> None:
    """Print a formatted comparison table.

    Args:
        results: List of benchmark results to compare.
    """
    # TODO: Implement
    # Format a table with columns: method, size, GPU mem, PPL, TPS, TTFT
    raise NotImplementedError
