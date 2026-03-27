"""Tests for the SSE streaming response handler."""

import json
from unittest.mock import AsyncMock

import pytest

from llm_serving.server.streaming import collect_stream, format_sse_chunk, stream_response


class TestFormatSSEChunk:
    """Tests for SSE chunk formatting."""

    def test_content_chunk(self) -> None:
        """A content chunk should have the correct SSE format."""
        # TODO: Implement
        # 1. Call format_sse_chunk with content_delta="Hello"
        # 2. Assert it starts with "data: "
        # 3. Assert it ends with "\n\n"
        # 4. Assert the JSON contains the delta content
        raise NotImplementedError

    def test_finish_chunk(self) -> None:
        """A finish chunk should include the finish_reason."""
        # TODO: Implement
        # 1. Call format_sse_chunk with finish_reason="stop"
        # 2. Parse the JSON and verify finish_reason is set
        raise NotImplementedError

    def test_chunk_has_required_fields(self) -> None:
        """Each chunk should have id, object, created, model, choices."""
        # TODO: Implement
        # Parse the JSON from a chunk and verify all required fields exist
        raise NotImplementedError

    def test_chunk_object_type(self) -> None:
        """Chunk object should be 'chat.completion.chunk'."""
        # TODO: Implement
        raise NotImplementedError


class TestStreamResponse:
    """Tests for the full streaming response generator."""

    @pytest.fixture
    def mock_engine(self) -> AsyncMock:
        """Create a mock vLLM engine that yields incremental outputs."""
        # TODO: Implement
        # Configure AsyncMock to yield RequestOutput objects with incremental text
        raise NotImplementedError

    async def test_stream_yields_chunks(self, mock_engine: AsyncMock) -> None:
        """stream_response should yield SSE chunks."""
        # TODO: Implement
        # 1. Call stream_response with mock_engine
        # 2. Collect all yielded chunks
        # 3. Assert chunks are non-empty
        raise NotImplementedError

    async def test_stream_ends_with_done(self, mock_engine: AsyncMock) -> None:
        """The last chunk should be 'data: [DONE]'."""
        # TODO: Implement
        raise NotImplementedError

    async def test_stream_incremental_deltas(self, mock_engine: AsyncMock) -> None:
        """Each chunk should contain only the new tokens, not the full text."""
        # TODO: Implement
        raise NotImplementedError


class TestCollectStream:
    """Tests for collecting a stream into a single string."""

    async def test_collect_basic_stream(self) -> None:
        """collect_stream should concatenate all deltas."""
        # TODO: Implement
        # 1. Create an async generator that yields known SSE chunks
        # 2. Collect and assert the full text matches expected output
        raise NotImplementedError

    async def test_collect_empty_stream(self) -> None:
        """An empty stream should return an empty string."""
        # TODO: Implement
        raise NotImplementedError
