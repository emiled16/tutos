"""Output quality comparison across serving configurations.

Compares generation quality between different model configurations
(quantization levels, temperatures, etc.) using the same prompts.
"""

from dataclasses import dataclass, field

import httpx


@dataclass
class QualityResult:
    """Quality assessment for a single configuration.

    Attributes:
        config_name: Name of the configuration being tested.
        outputs: Generated outputs for each prompt.
        avg_length: Average response length in tokens.
        coherence_score: Self-assessed coherence (0-1).
        consistency_score: Consistency across similar prompts (0-1).
    """

    config_name: str
    outputs: list[str] = field(default_factory=list)
    avg_length: float = 0.0
    coherence_score: float = 0.0
    consistency_score: float = 0.0


async def generate_for_config(
    base_url: str,
    prompts: list[str],
    config_name: str,
    temperature: float = 0.0,
    max_tokens: int = 256,
) -> QualityResult:
    """Generate outputs for a single serving configuration.

    Args:
        base_url: API base URL.
        prompts: List of evaluation prompts.
        config_name: Name for this configuration.
        temperature: Sampling temperature (use 0 for deterministic comparison).
        max_tokens: Maximum tokens to generate.

    Returns:
        QualityResult with outputs and basic metrics.
    """
    # TODO: Implement
    # 1. Send each prompt to the API
    # 2. Collect outputs
    # 3. Compute average length
    # 4. Return QualityResult
    raise NotImplementedError


async def compare_configurations(
    base_urls: dict[str, str],
    prompts: list[str],
    temperature: float = 0.0,
) -> list[QualityResult]:
    """Compare outputs across multiple serving configurations.

    Each configuration runs at a different URL (different model/quantization).

    Args:
        base_urls: Dict mapping config name to API base URL.
        prompts: Evaluation prompts.
        temperature: Sampling temperature for all configs.

    Returns:
        List of QualityResult, one per configuration.
    """
    # TODO: Implement
    # 1. Run generate_for_config for each configuration
    # 2. Return all results
    raise NotImplementedError


def print_quality_comparison(
    results: list[QualityResult],
    prompts: list[str],
) -> None:
    """Print a side-by-side quality comparison.

    Args:
        results: List of QualityResult to compare.
        prompts: The prompts used.
    """
    # TODO: Implement
    # Show each prompt with outputs from each configuration side by side
    raise NotImplementedError
