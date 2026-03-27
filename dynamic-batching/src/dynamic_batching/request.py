"""Pydantic models for inference requests and responses."""

from __future__ import annotations

import time
import uuid
from enum import IntEnum

from pydantic import BaseModel, Field


class Priority(IntEnum):
    """Request priority levels. Lower value = higher priority."""

    HIGH = 0
    NORMAL = 1
    LOW = 2


class InferenceRequest(BaseModel):
    """A single inference request submitted to the batcher.

    Attributes:
        request_id: Unique identifier for this request.
        payload: The input data (e.g., token IDs, feature vectors).
        priority: Priority level for scheduling.
        created_at: Timestamp when the request was created.
        sequence_length: Length of the input sequence (for padding calculations).
    """

    request_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    payload: list[float] = Field(default_factory=list)
    priority: Priority = Priority.NORMAL
    created_at: float = Field(default_factory=time.monotonic)
    sequence_length: int = 0

    def model_post_init(self, __context: object) -> None:
        """Set sequence_length from payload if not explicitly provided."""
        # TODO: Implement auto-detection of sequence_length from payload when not set
        pass


class InferenceResponse(BaseModel):
    """Response for a completed inference request.

    Attributes:
        request_id: Matches the original request.
        result: Model output (e.g., logits, predictions).
        batch_id: Identifier of the batch this request was part of.
        wait_time_ms: Time spent waiting in the batcher queue.
        batch_size: Number of requests in the batch.
        padding_overhead: Fraction of padded elements in this request's contribution to the batch.
    """

    request_id: str
    result: list[float] = Field(default_factory=list)
    batch_id: str = ""
    wait_time_ms: float = 0.0
    batch_size: int = 0
    padding_overhead: float = 0.0


class Batch(BaseModel):
    """A formed batch of inference requests ready for execution.

    Attributes:
        batch_id: Unique identifier for this batch.
        requests: The grouped requests.
        formed_at: Timestamp when the batch was dispatched.
        max_sequence_length: The longest sequence in the batch (determines padding target).
    """

    batch_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    requests: list[InferenceRequest] = Field(default_factory=list)
    formed_at: float = Field(default_factory=time.monotonic)
    max_sequence_length: int = 0

    @property
    def size(self) -> int:
        """Number of requests in the batch."""
        return len(self.requests)

    def compute_padding_waste(self) -> float:
        """Calculate the fraction of padded (wasted) elements in this batch.

        Returns:
            Waste ratio between 0.0 (no waste) and 1.0 (all padding).
            Returns 0.0 for empty batches.
        """
        # TODO: Implement padding waste calculation:
        #   total_capacity = batch_size * max_sequence_length
        #   actual_data = sum of all sequence_lengths
        #   waste = 1 - (actual_data / total_capacity)
        pass
