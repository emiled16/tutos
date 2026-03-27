"""Merge LoRA adapter weights back into the base model.

After merging, the model can be served without the PEFT library,
reducing inference overhead and simplifying deployment.
"""

from pathlib import Path

from peft import PeftModel
from transformers import AutoModelForCausalLM, PreTrainedModel, PreTrainedTokenizerBase

from llm_fine_tuning.data.tokenization import load_tokenizer


def load_model_with_adapter(
    base_model_name: str,
    adapter_path: str | Path,
    device_map: str = "cpu",
) -> tuple[PeftModel, PreTrainedTokenizerBase]:
    """Load the base model and apply the LoRA adapter for merging.

    Uses CPU device map and full precision to avoid quantization
    artifacts in the merged model.

    Args:
        base_model_name: HuggingFace model identifier.
        adapter_path: Path to the saved adapter weights.
        device_map: Device placement (use "cpu" for merging).

    Returns:
        Tuple of (PEFT model, tokenizer).
    """
    # TODO: Implement
    # 1. Load base model in fp16 (no quantization for merge)
    # 2. Load adapter with PeftModel.from_pretrained()
    # 3. Load tokenizer
    raise NotImplementedError


def merge_and_save(
    base_model_name: str,
    adapter_path: str | Path,
    output_path: str | Path,
    push_to_hub: bool = False,
    hub_model_id: str | None = None,
) -> Path:
    """Merge LoRA weights into the base model and save.

    Args:
        base_model_name: HuggingFace model identifier.
        adapter_path: Path to the LoRA adapter weights.
        output_path: Directory to save the merged model.
        push_to_hub: Whether to push the merged model to HuggingFace Hub.
        hub_model_id: Hub model identifier (required if push_to_hub is True).

    Returns:
        Path to the saved merged model.
    """
    # TODO: Implement
    # 1. Load model with adapter
    # 2. Call model.merge_and_unload()
    # 3. Save the merged model and tokenizer
    # 4. Optionally push to HuggingFace Hub
    # 5. Return the output path
    raise NotImplementedError


def verify_merge(
    adapter_model: PeftModel,
    merged_model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    test_prompts: list[str],
) -> bool:
    """Verify that merged model produces identical outputs to the adapter model.

    Args:
        adapter_model: The original model with adapter.
        merged_model: The merged model without adapter.
        tokenizer: Shared tokenizer.
        test_prompts: Prompts to test on.

    Returns:
        True if outputs match within tolerance, False otherwise.
    """
    # TODO: Implement
    # 1. Generate outputs from both models on the test prompts
    # 2. Compare logits (not generated text, since sampling is stochastic)
    # 3. Return True if all logits match within a small tolerance (1e-3)
    raise NotImplementedError
