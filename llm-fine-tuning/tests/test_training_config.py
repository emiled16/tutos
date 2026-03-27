"""Tests for training and LoRA configuration validation."""

import pytest
from pydantic import ValidationError

from llm_fine_tuning.config.lora_config import LoRAConfig, QuantizationConfig
from llm_fine_tuning.config.training_config import TrainingConfig


class TestTrainingConfig:
    """Tests for TrainingConfig validation."""

    def test_default_values(self) -> None:
        """Default config should be valid."""
        # TODO: Implement
        # Instantiate TrainingConfig() and check key defaults
        raise NotImplementedError

    def test_invalid_epochs(self) -> None:
        """Epochs < 1 should raise ValidationError."""
        # TODO: Implement
        raise NotImplementedError

    def test_invalid_learning_rate(self) -> None:
        """Learning rate <= 0 or >= 1 should raise ValidationError."""
        # TODO: Implement
        raise NotImplementedError

    def test_invalid_scheduler_type(self) -> None:
        """Unsupported scheduler type should raise ValidationError."""
        # TODO: Implement
        raise NotImplementedError

    def test_valid_scheduler_types(self) -> None:
        """All supported scheduler types should be accepted."""
        # TODO: Implement
        raise NotImplementedError

    def test_effective_batch_size(self) -> None:
        """effective_batch_size should be batch_size * accumulation_steps."""
        # TODO: Implement
        raise NotImplementedError

    def test_to_training_arguments(self) -> None:
        """to_training_arguments should return a dict with expected keys."""
        # TODO: Implement
        raise NotImplementedError


class TestLoRAConfig:
    """Tests for LoRAConfig validation."""

    def test_default_values(self) -> None:
        """Default LoRA config should be valid."""
        # TODO: Implement
        raise NotImplementedError

    def test_invalid_rank(self) -> None:
        """Rank < 1 or > 512 should raise ValidationError."""
        # TODO: Implement
        raise NotImplementedError

    def test_invalid_bias(self) -> None:
        """Unsupported bias value should raise ValidationError."""
        # TODO: Implement
        raise NotImplementedError

    def test_empty_target_modules(self) -> None:
        """Empty target_modules should raise ValidationError."""
        # TODO: Implement
        raise NotImplementedError

    def test_alpha_rank_ratio_warning(self) -> None:
        """Unusual alpha/rank ratio should trigger a warning."""
        # TODO: Implement
        raise NotImplementedError

    def test_to_peft_config(self) -> None:
        """to_peft_config should return a valid peft.LoraConfig."""
        # TODO: Implement
        raise NotImplementedError


class TestQuantizationConfig:
    """Tests for QuantizationConfig validation."""

    def test_default_is_4bit(self) -> None:
        """Default config should use 4-bit quantization."""
        # TODO: Implement
        raise NotImplementedError

    def test_mutual_exclusion(self) -> None:
        """Cannot enable both 4-bit and 8-bit."""
        # TODO: Implement
        raise NotImplementedError

    def test_to_bnb_config(self) -> None:
        """to_bnb_config should return a valid BitsAndBytesConfig."""
        # TODO: Implement
        raise NotImplementedError
