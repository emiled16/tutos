"""Metadata and tagging utilities for LangSmith runs.

Helpers for constructing structured metadata and tags that make
runs easier to filter and analyze in the LangSmith dashboard.
"""

from datetime import datetime, timezone
from typing import Any


def build_run_metadata(
    prompt_version: str,
    model: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a metadata dict for a LangSmith run.

    Includes standard fields (prompt version, model, timestamp) plus
    any additional custom metadata.

    Args:
        prompt_version: The prompt template version used.
        model: The LLM model identifier.
        extra: Optional additional metadata key-value pairs.

    Returns:
        A metadata dict ready to attach to a LangSmith run.
    """
    # TODO: Implement
    # 1. Create base metadata with prompt_version, model, timestamp
    # 2. Merge in extra metadata if provided
    # 3. Return the combined dict
    raise NotImplementedError


def build_run_tags(
    prompt_version: str,
    environment: str = "development",
    custom_tags: list[str] | None = None,
) -> list[str]:
    """Build a list of tags for a LangSmith run.

    Tags enable quick filtering in the LangSmith dashboard.

    Args:
        prompt_version: The prompt version (added as "prompt:<version>").
        environment: The environment name (added as "env:<environment>").
        custom_tags: Additional custom tags to include.

    Returns:
        A list of string tags.
    """
    # TODO: Implement
    # 1. Start with prompt version and environment tags
    # 2. Append custom tags if provided
    # 3. Return the combined list
    raise NotImplementedError


def build_experiment_metadata(
    experiment_name: str,
    prompt_versions: list[str],
    dataset_name: str,
    description: str = "",
) -> dict[str, Any]:
    """Build metadata for an A/B evaluation experiment.

    Args:
        experiment_name: Name of the experiment.
        prompt_versions: The prompt versions being compared.
        dataset_name: The dataset used for evaluation.
        description: Human-readable experiment description.

    Returns:
        Metadata dict for the experiment.
    """
    # TODO: Implement
    raise NotImplementedError
