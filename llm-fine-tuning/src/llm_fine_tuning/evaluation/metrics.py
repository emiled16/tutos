"""Evaluation metrics for fine-tuned language models.

Implements perplexity, ROUGE, BERTScore, and domain-specific accuracy
metrics for comparing model outputs.
"""

import math
from typing import Any

import torch
from transformers import PreTrainedModel, PreTrainedTokenizerBase


def compute_perplexity(
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    texts: list[str],
    max_length: int = 2048,
    batch_size: int = 4,
) -> float:
    """Compute perplexity of the model on a set of texts.

    Lower perplexity indicates the model is less surprised by the text,
    meaning it models the data distribution better.

    Args:
        model: The language model.
        tokenizer: The tokenizer.
        texts: List of text strings to evaluate.
        max_length: Maximum sequence length.
        batch_size: Number of texts per batch.

    Returns:
        The perplexity score (float).
    """
    # TODO: Implement
    # 1. Tokenize all texts with padding and truncation
    # 2. Run model forward pass with labels = input_ids
    # 3. Collect the cross-entropy loss for each batch
    # 4. Compute perplexity as exp(average_loss)
    raise NotImplementedError


def compute_rouge_scores(
    predictions: list[str],
    references: list[str],
) -> dict[str, float]:
    """Compute ROUGE-1, ROUGE-2, and ROUGE-L scores.

    Args:
        predictions: List of model-generated texts.
        references: List of reference texts.

    Returns:
        Dict with "rouge1", "rouge2", "rougeL" F1 scores.
    """
    # TODO: Implement
    # 1. Load the ROUGE metric from evaluate library
    # 2. Compute scores
    # 3. Return as a dict
    raise NotImplementedError


def compute_bertscore(
    predictions: list[str],
    references: list[str],
    model_type: str = "microsoft/deberta-xlarge-mnli",
) -> dict[str, float]:
    """Compute BERTScore for semantic similarity.

    Args:
        predictions: List of model-generated texts.
        references: List of reference texts.
        model_type: The embedding model for BERTScore.

    Returns:
        Dict with "precision", "recall", "f1" average scores.
    """
    # TODO: Implement
    # 1. Load BERTScore metric from evaluate library
    # 2. Compute scores
    # 3. Average across examples
    # 4. Return as a dict
    raise NotImplementedError


def compute_domain_accuracy(
    predictions: list[str],
    references: list[str],
    key_phrases: list[list[str]] | None = None,
) -> dict[str, float]:
    """Compute domain-specific accuracy metrics.

    Checks whether predictions contain expected key information
    from the domain (e.g., correct technical terms, procedures).

    Args:
        predictions: List of model-generated texts.
        references: List of reference texts.
        key_phrases: Optional list of key phrases per example that should
                     appear in the prediction.

    Returns:
        Dict with "exact_match", "key_phrase_recall", "avg_length_ratio".
    """
    # TODO: Implement
    # 1. Compute exact match rate (case-insensitive, whitespace-normalized)
    # 2. If key_phrases provided, compute recall of key phrases in predictions
    # 3. Compute average length ratio (prediction length / reference length)
    raise NotImplementedError


def compute_all_metrics(
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    predictions: list[str],
    references: list[str],
    texts_for_perplexity: list[str] | None = None,
) -> dict[str, Any]:
    """Compute all evaluation metrics in one call.

    Args:
        model: The language model (for perplexity).
        tokenizer: The tokenizer.
        predictions: Model-generated texts.
        references: Reference texts.
        texts_for_perplexity: Optional separate texts for perplexity computation.

    Returns:
        Dict with all metric results nested by category.
    """
    # TODO: Implement
    # 1. Compute perplexity (on texts_for_perplexity or references)
    # 2. Compute ROUGE scores
    # 3. Compute BERTScore
    # 4. Compute domain accuracy
    # 5. Combine into a single results dict
    raise NotImplementedError
