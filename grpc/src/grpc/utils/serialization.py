"""Numpy array to/from protobuf conversion utilities."""

from __future__ import annotations

import numpy as np


def ndarray_to_proto(array: np.ndarray) -> dict:
    """Convert a numpy array to a protobuf-compatible NDArray dict.

    Serializes the array's shape, raw bytes, and dtype for efficient
    transport over gRPC.

    Args:
        array: Numpy array to serialize.

    Returns:
        Dictionary with keys "shape", "data", "dtype" matching the
        NDArray protobuf message fields.
    """
    # TODO: Implement
    # - Extract shape as list of ints
    # - Serialize data as array.tobytes()
    # - Record dtype as str(array.dtype)
    # - Return {"shape": [...], "data": bytes, "dtype": "float32"}
    raise NotImplementedError


def ndarray_from_proto(proto_dict: dict) -> np.ndarray:
    """Reconstruct a numpy array from a protobuf NDArray message.

    Args:
        proto_dict: Dictionary (or proto object) with shape, data, dtype fields.

    Returns:
        Reconstructed numpy array with original shape and dtype.

    Raises:
        ValueError: If the data size doesn't match shape and dtype.
    """
    # TODO: Implement
    # - Extract shape, data (bytes), and dtype from proto_dict
    # - Use np.frombuffer(data, dtype=dtype)
    # - Reshape to the original shape
    # - Return the array
    raise NotImplementedError


def validate_array_compatibility(
    array: np.ndarray,
    expected_shape: tuple[int, ...] | None = None,
    expected_dtype: np.dtype | None = None,
) -> list[str]:
    """Validate that an array meets expected constraints.

    Args:
        array: Array to validate.
        expected_shape: Expected shape (use -1 for any dimension size).
        expected_dtype: Expected dtype.

    Returns:
        List of validation error messages (empty if valid).
    """
    # TODO: Implement
    # - Check ndim matches len(expected_shape) if provided
    # - Check each dimension matches (skip -1 dimensions)
    # - Check dtype matches if provided
    # - Return list of error strings
    raise NotImplementedError
