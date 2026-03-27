"""Serialization helpers for the Bytewax feature pipeline.

Provides efficient JSON serialization using orjson and optional
Avro encoding utilities.
"""

from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def serialize_json(model: BaseModel) -> bytes:
    """Serialize a Pydantic model to JSON bytes using orjson.

    Args:
        model: A Pydantic model instance to serialize.

    Returns:
        JSON-encoded bytes.
    """
    # TODO: Implement — use orjson.dumps with model.model_dump()
    #       handle datetime serialization (orjson supports it natively)
    raise NotImplementedError


def deserialize_json(data: bytes | str, model_class: type[T]) -> T:
    """Deserialize JSON bytes into a Pydantic model instance.

    Args:
        data: JSON-encoded bytes or string.
        model_class: The Pydantic model class to deserialize into.

    Returns:
        An instance of model_class.

    Raises:
        ValueError: If the data cannot be parsed or validated.
    """
    # TODO: Implement — use orjson.loads to parse, then model_class.model_validate()
    raise NotImplementedError


def serialize_json_line(model: BaseModel) -> str:
    """Serialize a Pydantic model to a single JSON line (for JSONL output).

    Args:
        model: A Pydantic model instance to serialize.

    Returns:
        A JSON string terminated with a newline character.
    """
    # TODO: Implement — serialize to JSON string and append newline
    raise NotImplementedError


def pydantic_to_avro_schema(model_class: type[BaseModel]) -> dict[str, Any]:
    """Convert a Pydantic model schema to an Avro schema representation.

    This is a simplified converter that handles basic types.
    For production use, consider a library like pydantic-avro.

    Args:
        model_class: The Pydantic model class to convert.

    Returns:
        A dictionary representing the Avro schema.
    """
    # TODO: Implement — convert Pydantic model fields to Avro schema:
    #   - str → "string"
    #   - int → "long"
    #   - float → "double"
    #   - datetime → {"type": "long", "logicalType": "timestamp-millis"}
    #   - list[str] → {"type": "array", "items": "string"}
    raise NotImplementedError
