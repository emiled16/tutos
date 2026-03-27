"""Model configuration for the LLM serving server.

Defines configuration for model loading, quantization settings,
tensor parallelism, and GPU memory management.
"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class ModelConfig(BaseSettings):
    """Configuration for the LLM model.

    Loaded from environment variables with the MODEL_ prefix.

    Attributes:
        name: HuggingFace model identifier or local path.
        quantization: Quantization method (None, "gptq", "awq").
        dtype: Model data type ("auto", "float16", "bfloat16").
        tensor_parallel_size: Number of GPUs for tensor parallelism.
        gpu_memory_utilization: Fraction of GPU memory for KV-cache.
        max_model_len: Maximum sequence length (prompt + generation).
        trust_remote_code: Whether to trust remote code in model repos.
        download_dir: Directory for model downloads.
        enforce_eager: Disable CUDA graphs for debugging.
    """

    name: str = Field(default="mistralai/Mistral-7B-Instruct-v0.2", alias="MODEL_NAME")
    quantization: str | None = None
    dtype: str = "auto"
    tensor_parallel_size: int = Field(default=1, ge=1, le=8, alias="TENSOR_PARALLEL_SIZE")
    gpu_memory_utilization: float = Field(
        default=0.9, ge=0.1, le=0.99, alias="GPU_MEMORY_UTILIZATION"
    )
    max_model_len: int = Field(default=4096, ge=128, le=131072, alias="MAX_MODEL_LEN")
    trust_remote_code: bool = False
    download_dir: str | None = None
    enforce_eager: bool = False

    model_config = {"env_prefix": "", "env_file": ".env"}

    @field_validator("quantization")
    @classmethod
    def validate_quantization(cls, v: str | None) -> str | None:
        """Validate quantization method."""
        # TODO: Implement
        # Allowed values: None, "gptq", "awq", "squeezellm"
        raise NotImplementedError

    @field_validator("dtype")
    @classmethod
    def validate_dtype(cls, v: str) -> str:
        """Validate model data type."""
        # TODO: Implement
        # Allowed values: "auto", "float16", "bfloat16", "float32"
        raise NotImplementedError

    @field_validator("tensor_parallel_size")
    @classmethod
    def validate_tp_power_of_two(cls, v: int) -> int:
        """Tensor parallel size should be a power of 2."""
        # TODO: Implement
        raise NotImplementedError
