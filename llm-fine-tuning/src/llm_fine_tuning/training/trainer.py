"""Training loop using HuggingFace Trainer with PEFT.

Loads the base model, applies LoRA adapters, and runs the training
loop with the configured hyperparameters.
"""

from pathlib import Path

from datasets import Dataset
from peft import PeftModel
from transformers import (
    AutoModelForCausalLM,
    PreTrainedModel,
    PreTrainedTokenizerBase,
    Trainer,
    TrainingArguments,
)

from llm_fine_tuning.config.lora_config import LoRAConfig, QuantizationConfig
from llm_fine_tuning.config.training_config import TrainingConfig
from llm_fine_tuning.data.data_collator import CausalLMDataCollator


def load_base_model(
    model_name: str,
    quantization_config: QuantizationConfig | None = None,
    device_map: str = "auto",
) -> PreTrainedModel:
    """Load a pre-trained causal LM, optionally quantized.

    Args:
        model_name: HuggingFace model identifier.
        quantization_config: Optional quantization settings for QLoRA.
        device_map: Device placement strategy.

    Returns:
        The loaded model (quantized if config provided).
    """
    # TODO: Implement
    # 1. Build BitsAndBytesConfig if quantization_config is provided
    # 2. Load with AutoModelForCausalLM.from_pretrained()
    # 3. Enable gradient checkpointing if supported
    # 4. Prepare for kbit training if quantized
    raise NotImplementedError


def apply_lora(
    model: PreTrainedModel,
    lora_config: LoRAConfig,
) -> PeftModel:
    """Apply LoRA adapters to the base model.

    Args:
        model: The base pre-trained model.
        lora_config: LoRA adapter configuration.

    Returns:
        The model wrapped with PEFT LoRA adapters.
    """
    # TODO: Implement
    # 1. Convert LoRAConfig to peft.LoraConfig
    # 2. Apply get_peft_model()
    # 3. Print trainable parameters summary
    raise NotImplementedError


def create_trainer(
    model: PeftModel,
    tokenizer: PreTrainedTokenizerBase,
    train_dataset: Dataset,
    eval_dataset: Dataset,
    training_config: TrainingConfig,
    callbacks: list | None = None,
) -> Trainer:
    """Create a configured HuggingFace Trainer.

    Args:
        model: The PEFT-wrapped model.
        tokenizer: The tokenizer.
        train_dataset: Training dataset.
        eval_dataset: Evaluation dataset.
        training_config: Training hyperparameters.
        callbacks: Optional list of custom training callbacks.

    Returns:
        A configured Trainer ready to call train().
    """
    # TODO: Implement
    # 1. Convert training_config to TrainingArguments
    # 2. Create the data collator
    # 3. Instantiate Trainer with all components
    raise NotImplementedError


def train(
    training_config: TrainingConfig,
    lora_config: LoRAConfig,
    quantization_config: QuantizationConfig | None = None,
    data_path: str | Path = "data/technical_support.jsonl",
) -> Path:
    """Full training pipeline: load, prepare, train, save.

    Args:
        training_config: Training hyperparameters.
        lora_config: LoRA adapter configuration.
        quantization_config: Optional quantization config.
        data_path: Path to the training data.

    Returns:
        Path to the saved adapter checkpoint.
    """
    # TODO: Implement
    # 1. Load tokenizer
    # 2. Prepare dataset
    # 3. Load base model (with optional quantization)
    # 4. Apply LoRA
    # 5. Create trainer
    # 6. Run training
    # 7. Save the adapter
    # 8. Return the checkpoint path
    raise NotImplementedError
