"""Custom data collator for causal language model training.

Handles padding, attention masks, and label construction for
instruction-tuning where we only compute loss on the response tokens.
"""

from dataclasses import dataclass
from typing import Any

import torch
from transformers import PreTrainedTokenizerBase


@dataclass
class CausalLMDataCollator:
    """Data collator for causal LM instruction tuning.

    Pads sequences to the same length within a batch, constructs
    attention masks, and creates labels that mask out instruction
    tokens (only compute loss on response tokens).

    Attributes:
        tokenizer: The tokenizer used for padding.
        max_length: Maximum sequence length.
        pad_to_multiple_of: Pad to a multiple of this value for hardware efficiency.
        response_template: The string token(s) marking the start of the response.
    """

    tokenizer: PreTrainedTokenizerBase
    max_length: int = 2048
    pad_to_multiple_of: int | None = 8
    response_template: str = "### Response:"

    def __call__(self, features: list[dict[str, Any]]) -> dict[str, torch.Tensor]:
        """Collate a batch of examples into padded tensors.

        Args:
            features: List of tokenized examples, each with "input_ids"
                      and optionally "attention_mask".

        Returns:
            Dict with "input_ids", "attention_mask", and "labels" tensors.
        """
        # TODO: Implement
        # 1. Extract input_ids from each feature
        # 2. Pad sequences to the longest in the batch (or max_length)
        # 3. Create attention masks (1 for real tokens, 0 for padding)
        # 4. Create labels: copy of input_ids with padding tokens set to -100
        # 5. Mask instruction tokens in labels (set to -100 so loss is only on response)
        # 6. Return the batch dict
        raise NotImplementedError

    def _find_response_start(self, input_ids: list[int]) -> int:
        """Find the token index where the response begins.

        Locates the response_template tokens in the input_ids to determine
        which tokens are instruction (masked) vs response (trained on).

        Args:
            input_ids: The tokenized sequence.

        Returns:
            The index of the first response token.
        """
        # TODO: Implement
        # 1. Tokenize the response_template
        # 2. Search for this subsequence in input_ids
        # 3. Return the index after the template tokens
        raise NotImplementedError
