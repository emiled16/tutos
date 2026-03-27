"""Python client for the LLM serving API with streaming support.

Provides both synchronous and asynchronous interfaces for interacting
with the OpenAI-compatible serving API.
"""

from dataclasses import dataclass
from typing import AsyncGenerator, Generator

import httpx


@dataclass
class CompletionResponse:
    """Parsed completion response.

    Attributes:
        text: The generated text.
        model: The model that generated the response.
        prompt_tokens: Number of prompt tokens.
        completion_tokens: Number of generated tokens.
        total_tokens: Total tokens used.
        finish_reason: Why generation stopped.
    """

    text: str
    model: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    finish_reason: str = ""


class LLMClient:
    """Synchronous client for the LLM serving API."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        timeout: float = 60.0,
    ) -> None:
        """Initialize the client.

        Args:
            base_url: Base URL of the serving API.
            timeout: Request timeout in seconds.
        """
        # TODO: Implement — create httpx.Client
        raise NotImplementedError

    def chat(
        self,
        messages: list[dict[str, str]],
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 256,
        **kwargs,
    ) -> CompletionResponse:
        """Send a chat completion request.

        Args:
            messages: List of message dicts with "role" and "content".
            model: Model identifier.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.
            **kwargs: Additional parameters (top_p, stop, etc.).

        Returns:
            Parsed CompletionResponse.
        """
        # TODO: Implement
        # 1. Build the request payload
        # 2. POST to /v1/chat/completions
        # 3. Parse the response into CompletionResponse
        raise NotImplementedError

    def chat_stream(
        self,
        messages: list[dict[str, str]],
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 256,
        **kwargs,
    ) -> Generator[str, None, None]:
        """Send a streaming chat completion request.

        Args:
            messages: List of message dicts.
            model: Model identifier.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.
            **kwargs: Additional parameters.

        Yields:
            Token strings as they are generated.
        """
        # TODO: Implement
        # 1. Build request payload with stream=True
        # 2. Use httpx streaming to iterate over SSE chunks
        # 3. Parse each "data: {...}" line
        # 4. Extract content delta and yield it
        # 5. Stop on "data: [DONE]"
        raise NotImplementedError

    def complete(
        self,
        prompt: str,
        model: str = "default",
        max_tokens: int = 256,
        **kwargs,
    ) -> CompletionResponse:
        """Send a text completion request.

        Args:
            prompt: The input text.
            model: Model identifier.
            max_tokens: Maximum tokens to generate.
            **kwargs: Additional parameters.

        Returns:
            Parsed CompletionResponse.
        """
        # TODO: Implement
        raise NotImplementedError

    def health(self) -> dict[str, str]:
        """Check server health.

        Returns:
            Health status dict.
        """
        # TODO: Implement
        raise NotImplementedError

    def close(self) -> None:
        """Close the HTTP client."""
        # TODO: Implement
        raise NotImplementedError


class AsyncLLMClient:
    """Asynchronous client for the LLM serving API."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        timeout: float = 60.0,
    ) -> None:
        """Initialize the async client.

        Args:
            base_url: Base URL of the serving API.
            timeout: Request timeout in seconds.
        """
        # TODO: Implement — create httpx.AsyncClient
        raise NotImplementedError

    async def chat(
        self,
        messages: list[dict[str, str]],
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 256,
        **kwargs,
    ) -> CompletionResponse:
        """Send an async chat completion request.

        Args:
            messages: List of message dicts.
            model: Model identifier.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.
            **kwargs: Additional parameters.

        Returns:
            Parsed CompletionResponse.
        """
        # TODO: Implement
        raise NotImplementedError

    async def chat_stream(
        self,
        messages: list[dict[str, str]],
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 256,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """Send an async streaming chat completion request.

        Args:
            messages: List of message dicts.
            model: Model identifier.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.
            **kwargs: Additional parameters.

        Yields:
            Token strings as they are generated.
        """
        # TODO: Implement
        # 1. Build request payload with stream=True
        # 2. Use httpx async streaming
        # 3. Parse SSE chunks and yield content deltas
        raise NotImplementedError

    async def close(self) -> None:
        """Close the async HTTP client."""
        # TODO: Implement
        raise NotImplementedError
