"""Data loading, cleaning, and formatting into instruction/response pairs.

Transforms raw domain-specific conversations (e.g., technical support logs)
into a structured instruction-tuning dataset.
"""

from pathlib import Path
from typing import Any

from datasets import Dataset


INSTRUCTION_TEMPLATE = """### Instruction: {instruction}
### Input: {input}
### Response: {response}"""


def load_raw_data(path: str | Path) -> list[dict[str, Any]]:
    """Load raw conversation data from a JSONL file.

    Each line should be a JSON object with at least "messages" or
    "conversation" fields.

    Args:
        path: Path to the JSONL data file.

    Returns:
        List of raw conversation dicts.

    Raises:
        FileNotFoundError: If the data file does not exist.
        ValueError: If the file format is invalid.
    """
    # TODO: Implement
    # 1. Read the JSONL file line by line
    # 2. Parse each line as JSON
    # 3. Validate required fields exist
    # 4. Return the list of parsed dicts
    raise NotImplementedError


def clean_conversation(conversation: dict[str, Any]) -> dict[str, Any] | None:
    """Clean a single conversation record.

    Removes PII patterns, normalizes whitespace, filters out
    conversations that are too short or too long.

    Args:
        conversation: A raw conversation dict.

    Returns:
        The cleaned conversation dict, or None if it should be filtered out.
    """
    # TODO: Implement
    # 1. Strip leading/trailing whitespace from all text fields
    # 2. Remove email addresses and phone numbers (PII)
    # 3. Filter out conversations shorter than a minimum turn count
    # 4. Filter out conversations longer than a maximum token estimate
    # 5. Return cleaned dict or None
    raise NotImplementedError


def format_as_instruction_pair(
    conversation: dict[str, Any],
) -> dict[str, str]:
    """Convert a conversation into an instruction/input/response triple.

    Extracts the user's question as the instruction/input and the
    agent's response as the target output.

    Args:
        conversation: A cleaned conversation dict.

    Returns:
        Dict with keys "instruction", "input", "response".
    """
    # TODO: Implement
    # 1. Extract the user's query from the conversation turns
    # 2. Extract the agent's response
    # 3. Format into the instruction template
    raise NotImplementedError


def apply_chat_template(
    example: dict[str, str],
    tokenizer: Any,
) -> str:
    """Format an instruction pair using the model's chat template.

    Args:
        example: Dict with "instruction", "input", "response".
        tokenizer: The HuggingFace tokenizer (with chat_template).

    Returns:
        The formatted string ready for tokenization.
    """
    # TODO: Implement
    # 1. Construct messages list [{role: ..., content: ...}, ...]
    # 2. Apply tokenizer.apply_chat_template()
    # 3. Return the formatted string
    raise NotImplementedError


def prepare_dataset(
    data_path: str | Path,
    tokenizer: Any,
    test_size: float = 0.1,
    val_size: float = 0.1,
    seed: int = 42,
) -> dict[str, Dataset]:
    """Full data preparation pipeline: load, clean, format, split.

    Args:
        data_path: Path to the raw JSONL data.
        tokenizer: The HuggingFace tokenizer.
        test_size: Fraction of data for the test split.
        val_size: Fraction of data for the validation split.
        seed: Random seed for reproducibility.

    Returns:
        Dict with keys "train", "validation", "test", each a HuggingFace Dataset.
    """
    # TODO: Implement
    # 1. Load raw data
    # 2. Clean each conversation (filter None results)
    # 3. Format as instruction pairs
    # 4. Apply chat template
    # 5. Create HuggingFace Dataset
    # 6. Split into train/validation/test
    raise NotImplementedError
