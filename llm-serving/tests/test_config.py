"""Tests for model and serving configuration validation."""

import pytest
from pydantic import ValidationError

from llm_serving.config.model_config import ModelConfig
from llm_serving.config.serving_config import ServingConfig


class TestModelConfig:
    """Tests for ModelConfig validation."""

    def test_default_values(self) -> None:
        """Default ModelConfig should be valid."""
        # TODO: Implement
        raise NotImplementedError

    def test_invalid_quantization(self) -> None:
        """Unsupported quantization method should raise error."""
        # TODO: Implement
        raise NotImplementedError

    def test_valid_quantization_methods(self) -> None:
        """gptq, awq, squeezellm, and None should be accepted."""
        # TODO: Implement
        raise NotImplementedError

    def test_invalid_dtype(self) -> None:
        """Unsupported dtype should raise error."""
        # TODO: Implement
        raise NotImplementedError

    def test_gpu_memory_utilization_range(self) -> None:
        """gpu_memory_utilization must be between 0.1 and 0.99."""
        # TODO: Implement
        raise NotImplementedError

    def test_tensor_parallel_power_of_two(self) -> None:
        """tensor_parallel_size should be a power of 2."""
        # TODO: Implement
        raise NotImplementedError

    def test_max_model_len_range(self) -> None:
        """max_model_len must be between 128 and 131072."""
        # TODO: Implement
        raise NotImplementedError

    def test_from_env_vars(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Config should load from environment variables."""
        # TODO: Implement
        # Use monkeypatch to set MODEL_NAME, GPU_MEMORY_UTILIZATION, etc.
        raise NotImplementedError


class TestServingConfig:
    """Tests for ServingConfig validation."""

    def test_default_values(self) -> None:
        """Default ServingConfig should be valid."""
        # TODO: Implement
        raise NotImplementedError

    def test_invalid_log_level(self) -> None:
        """Unsupported log level should raise error."""
        # TODO: Implement
        raise NotImplementedError

    def test_valid_log_levels(self) -> None:
        """All standard log levels should be accepted."""
        # TODO: Implement
        raise NotImplementedError

    def test_port_range(self) -> None:
        """Port must be between 1 and 65535."""
        # TODO: Implement
        raise NotImplementedError

    def test_timeout_range(self) -> None:
        """Request timeout must be between 1 and 600 seconds."""
        # TODO: Implement
        raise NotImplementedError

    def test_to_uvicorn_kwargs(self) -> None:
        """to_uvicorn_kwargs should return valid uvicorn configuration."""
        # TODO: Implement
        raise NotImplementedError
