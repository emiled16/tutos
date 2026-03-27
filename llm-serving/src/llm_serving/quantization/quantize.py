"""Quantization utilities for GPTQ, AWQ, and GGUF conversion.

Provides functions to quantize a model using different methods
and save the quantized model for serving.
"""

from pathlib import Path
from typing import Any


def quantize_gptq(
    model_name: str,
    output_dir: str | Path,
    bits: int = 4,
    group_size: int = 128,
    calibration_dataset: str = "c4",
    num_calibration_samples: int = 128,
) -> Path:
    """Quantize a model using GPTQ.

    Args:
        model_name: HuggingFace model identifier.
        output_dir: Directory to save the quantized model.
        bits: Quantization bit width (3 or 4).
        group_size: Group size for quantization (128 is standard).
        calibration_dataset: Dataset to use for calibration.
        num_calibration_samples: Number of calibration samples.

    Returns:
        Path to the quantized model directory.
    """
    # TODO: Implement
    # 1. Load the model in fp16
    # 2. Load the calibration dataset
    # 3. Configure GPTQConfig(bits=bits, group_size=group_size, ...)
    # 4. Quantize the model
    # 5. Save the quantized model and tokenizer
    raise NotImplementedError


def quantize_awq(
    model_name: str,
    output_dir: str | Path,
    bits: int = 4,
    group_size: int = 128,
    zero_point: bool = True,
) -> Path:
    """Quantize a model using AWQ.

    Args:
        model_name: HuggingFace model identifier.
        output_dir: Directory to save the quantized model.
        bits: Quantization bit width.
        group_size: Group size for quantization.
        zero_point: Whether to use zero-point quantization.

    Returns:
        Path to the quantized model directory.
    """
    # TODO: Implement
    # 1. Load the model
    # 2. Configure AWQ quantization
    # 3. Quantize and save
    raise NotImplementedError


def convert_to_gguf(
    model_name: str,
    output_path: str | Path,
    quantization_type: str = "q4_k_m",
) -> Path:
    """Convert a model to GGUF format with quantization.

    Args:
        model_name: HuggingFace model identifier or local model path.
        output_path: Path for the output GGUF file.
        quantization_type: GGUF quantization type (e.g., "q4_k_m", "q5_k_s").

    Returns:
        Path to the GGUF file.
    """
    # TODO: Implement
    # 1. Download or locate the model
    # 2. Run the llama.cpp conversion script
    # 3. Apply quantization
    # 4. Return the output path
    raise NotImplementedError


def get_model_size_info(model_path: str | Path) -> dict[str, Any]:
    """Get size information about a model (quantized or not).

    Args:
        model_path: Path to the model directory or file.

    Returns:
        Dict with "total_size_gb", "num_files", "quantization_type",
        "estimated_gpu_memory_gb".
    """
    # TODO: Implement
    # 1. Walk the model directory
    # 2. Sum up file sizes
    # 3. Detect quantization type from config files
    # 4. Estimate GPU memory (model size + overhead)
    raise NotImplementedError
