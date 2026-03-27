"""FastAPI gateway with OpenAI-compatible API endpoints.

Exposes /v1/chat/completions and /v1/completions endpoints that are
compatible with the OpenAI Python client.
"""

import time
import uuid
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from vllm import AsyncLLMEngine

from llm_serving.monitoring.metrics import track_request
from llm_serving.server.streaming import stream_response
from llm_serving.server.vllm_server import build_sampling_params


# --- Request/Response Models ---


class ChatMessage(BaseModel):
    """A single message in a chat conversation."""

    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str


class ChatCompletionRequest(BaseModel):
    """OpenAI-compatible chat completion request.

    Attributes:
        model: The model identifier.
        messages: The conversation history.
        temperature: Sampling temperature.
        top_p: Nucleus sampling threshold.
        max_tokens: Maximum tokens to generate.
        stream: Whether to stream the response.
        stop: Optional stop sequences.
        presence_penalty: Penalty for tokens already present.
        frequency_penalty: Penalty for tokens by frequency.
    """

    model: str = "default"
    messages: list[ChatMessage]
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    max_tokens: int = Field(default=256, ge=1, le=4096)
    stream: bool = False
    stop: list[str] | None = None
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)


class CompletionRequest(BaseModel):
    """OpenAI-compatible text completion request."""

    model: str = "default"
    prompt: str
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    max_tokens: int = Field(default=256, ge=1, le=4096)
    stream: bool = False
    stop: list[str] | None = None


class ChatCompletionChoice(BaseModel):
    """A single completion choice."""

    index: int
    message: ChatMessage
    finish_reason: str | None = None


class Usage(BaseModel):
    """Token usage statistics."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    """OpenAI-compatible chat completion response."""

    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[ChatCompletionChoice]
    usage: Usage


# --- Application Factory ---


def create_app(engine: AsyncLLMEngine, model_name: str = "default") -> FastAPI:
    """Create the FastAPI application with all routes.

    Args:
        engine: The initialized vLLM engine.
        model_name: The model name to report in responses.

    Returns:
        A configured FastAPI application.
    """
    app = FastAPI(title="LLM Serving API", version="0.1.0")

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint."""
        # TODO: Implement — return status and model name
        raise NotImplementedError

    @app.get("/v1/models")
    async def list_models() -> dict:
        """List available models (OpenAI-compatible)."""
        # TODO: Implement — return model list in OpenAI format
        raise NotImplementedError

    @app.post("/v1/chat/completions")
    async def chat_completions(
        request: ChatCompletionRequest,
    ) -> ChatCompletionResponse | StreamingResponse:
        """Handle chat completion requests.

        Supports both streaming and non-streaming modes.

        Args:
            request: The chat completion request.

        Returns:
            ChatCompletionResponse for non-streaming, StreamingResponse for streaming.
        """
        # TODO: Implement
        # 1. Convert messages to a prompt string (apply chat template or join)
        # 2. Build SamplingParams from request parameters
        # 3. Generate a unique request_id
        # 4. If request.stream: return StreamingResponse with SSE
        # 5. Otherwise: generate full response and return ChatCompletionResponse
        # 6. Track metrics (TTFT, TPS, total tokens)
        raise NotImplementedError

    @app.post("/v1/completions")
    async def completions(request: CompletionRequest) -> dict:
        """Handle text completion requests.

        Args:
            request: The completion request.

        Returns:
            OpenAI-compatible completion response.
        """
        # TODO: Implement
        # Similar to chat_completions but for raw text completion
        raise NotImplementedError

    return app
