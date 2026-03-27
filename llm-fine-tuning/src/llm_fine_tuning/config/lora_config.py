"""LoRA/QLoRA configuration with validation.

Defines the LoRA adapter configuration as a Pydantic model with
sensible defaults and constraint validation.
"""

from pydantic import BaseModel, Field, field_validator, model_validator


class LoRAConfig(BaseModel):
    """Configuration for LoRA adapter parameters.

    Attributes:
        r: LoRA rank (dimensionality of the low-rank matrices).
        lora_alpha: Scaling factor for LoRA updates.
        lora_dropout: Dropout probability for LoRA layers.
        target_modules: Which model layers to apply LoRA to.
        bias: Bias training strategy ("none", "all", "lora_only").
        task_type: The task type for PEFT ("CAUSAL_LM").
    """

    r: int = Field(default=16, ge=1, le=512)
    lora_alpha: int = Field(default=32, ge=1, le=1024)
    lora_dropout: float = Field(default=0.05, ge=0.0, le=0.5)
    target_modules: list[str] = Field(
        default_factory=lambda: ["q_proj", "k_proj", "v_proj", "o_proj"]
    )
    bias: str = "none"
    task_type: str = "CAUSAL_LM"

    @field_validator("bias")
    @classmethod
    def validate_bias(cls, v: str) -> str:
        """Validate the bias training strategy."""
        # TODO: Implement
        # Allowed values: "none", "all", "lora_only"
        raise NotImplementedError

    @field_validator("target_modules")
    @classmethod
    def validate_target_modules(cls, v: list[str]) -> list[str]:
        """Validate that target_modules is non-empty."""
        # TODO: Implement
        raise NotImplementedError

    @model_validator(mode="after")
    def validate_alpha_rank_ratio(self) -> "LoRAConfig":
        """Warn if alpha/rank ratio is unusual (typically alpha = 2*rank)."""
        # TODO: Implement
        # If lora_alpha / r is less than 0.5 or greater than 8, log a warning
        raise NotImplementedError

    def to_peft_config(self):
        """Convert to a PEFT LoraConfig object.

        Returns:
            A peft.LoraConfig instance.
        """
        # TODO: Implement
        # 1. Import LoraConfig from peft
        # 2. Map our fields to LoraConfig parameters
        # 3. Return the LoraConfig instance
        raise NotImplementedError


class QuantizationConfig(BaseModel):
    """Configuration for model quantization (QLoRA).

    Attributes:
        load_in_4bit: Use 4-bit quantization.
        load_in_8bit: Use 8-bit quantization.
        bnb_4bit_compute_dtype: Compute dtype for 4-bit (typically bf16).
        bnb_4bit_quant_type: Quantization type ("nf4" or "fp4").
        bnb_4bit_use_double_quant: Use double quantization to save memory.
    """

    load_in_4bit: bool = True
    load_in_8bit: bool = False
    bnb_4bit_compute_dtype: str = "bfloat16"
    bnb_4bit_quant_type: str = "nf4"
    bnb_4bit_use_double_quant: bool = True

    @model_validator(mode="after")
    def validate_mutual_exclusion(self) -> "QuantizationConfig":
        """Ensure 4-bit and 8-bit are not both enabled."""
        # TODO: Implement
        raise NotImplementedError

    def to_bnb_config(self):
        """Convert to a BitsAndBytesConfig object.

        Returns:
            A transformers.BitsAndBytesConfig instance.
        """
        # TODO: Implement
        # 1. Import BitsAndBytesConfig from transformers
        # 2. Map dtype string to torch dtype
        # 3. Return the config instance
        raise NotImplementedError
