"""Inference pipeline for the fine-tuned model.

Provides utilities for loading a fine-tuned model (with adapter or merged)
and generating responses from prompts.
"""

from pathlib import Path

import torch
from peft import PeftModel
from transformers import (
    AutoModelForCausalLM,
    GenerationConfig,
    PreTrainedModel,
    PreTrainedTokenizerBase,
)

from llm_fine_tuning.data.tokenization import load_tokenizer


def load_finetuned_model(
    base_model_name: str,
    adapter_path: str | Path,
    device_map: str = "auto",
) -> tuple[PeftModel, PreTrainedTokenizerBase]:
    """Load a fine-tuned model with its LoRA adapter.

    Args:
        base_model_name: HuggingFace identifier for the base model.
        adapter_path: Path to the saved LoRA adapter weights.
        device_map: Device placement strategy.

    Returns:
        Tuple of (model with adapter, tokenizer).
    """
    # TODO: Implement
    # 1. Load the base model
    # 2. Load the LoRA adapter with PeftModel.from_pretrained()
    # 3. Load the tokenizer
    # 4. Return (model, tokenizer)
    raise NotImplementedError


def create_generation_config(
    max_new_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.9,
    top_k: int = 50,
    repetition_penalty: float = 1.1,
    do_sample: bool = True,
) -> GenerationConfig:
    """Create a generation configuration for inference.

    Args:
        max_new_tokens: Maximum number of tokens to generate.
        temperature: Sampling temperature.
        top_p: Nucleus sampling probability threshold.
        top_k: Top-k sampling parameter.
        repetition_penalty: Penalty for repeating tokens.
        do_sample: Whether to use sampling (False = greedy).

    Returns:
        A GenerationConfig instance.
    """
    # TODO: Implement
    raise NotImplementedError


def generate_response(
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    prompt: str,
    generation_config: GenerationConfig | None = None,
) -> str:
    """Generate a single response from a prompt.

    Args:
        model: The fine-tuned model.
        tokenizer: The tokenizer.
        prompt: The input prompt text.
        generation_config: Optional generation parameters.

    Returns:
        The generated response text (excluding the prompt).
    """
    # TODO: Implement
    # 1. Tokenize the prompt
    # 2. Move to model's device
    # 3. Generate with torch.no_grad()
    # 4. Decode only the newly generated tokens
    # 5. Return the response string
    raise NotImplementedError


def generate_responses(
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    prompts: list[str],
    generation_config: GenerationConfig | None = None,
    batch_size: int = 4,
) -> list[str]:
    """Generate responses for multiple prompts.

    Args:
        model: The fine-tuned model.
        tokenizer: The tokenizer.
        prompts: List of input prompts.
        generation_config: Optional generation parameters.
        batch_size: Number of prompts to process at once.

    Returns:
        List of generated response strings.
    """
    # TODO: Implement
    # 1. Process prompts in batches
    # 2. Tokenize batch with padding
    # 3. Generate for the batch
    # 4. Decode and collect results
    raise NotImplementedError
