"""User/item ID mapping and interaction matrix construction."""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import sparse


@dataclass
class IDMapper:
    """Bidirectional mapping between original IDs and contiguous matrix indices."""

    id_to_idx: dict[int, int]
    idx_to_id: dict[int, int]

    @classmethod
    def from_ids(cls, ids: np.ndarray | pd.Series) -> "IDMapper":
        """Create a mapper from an array of original IDs.

        Args:
            ids: Array of unique original IDs.

        Returns:
            IDMapper with bidirectional mappings.
        """
        # TODO: Build id_to_idx mapping from sorted unique IDs to contiguous 0..N-1 indices
        # TODO: Build the reverse idx_to_id mapping
        raise NotImplementedError

    def map_to_idx(self, original_id: int) -> int:
        """Map an original ID to its matrix index."""
        return self.id_to_idx[original_id]

    def map_to_id(self, idx: int) -> int:
        """Map a matrix index back to the original ID."""
        return self.idx_to_id[idx]

    @property
    def size(self) -> int:
        return len(self.id_to_idx)


@dataclass
class MappedInteractions:
    """Interaction matrix with associated ID mappers."""

    matrix: sparse.csr_matrix
    user_mapper: IDMapper
    item_mapper: IDMapper


def build_interaction_matrix(
    interactions: pd.DataFrame,
    user_col: str = "user_id",
    item_col: str = "item_id",
    value_col: str | None = "rating",
) -> MappedInteractions:
    """Construct a sparse user-item interaction matrix from a DataFrame.

    Args:
        interactions: DataFrame with user, item, and optionally value columns.
        user_col: Column name for user IDs.
        item_col: Column name for item IDs.
        value_col: Column name for interaction values (ratings). If None, use binary (1).

    Returns:
        MappedInteractions containing the sparse CSR matrix and ID mappers.
    """
    # TODO: Create IDMapper for users and items from the interaction DataFrame
    # TODO: Map user and item IDs to contiguous indices
    # TODO: Build a sparse CSR matrix with shape (n_users, n_items)
    #       using the mapped indices and interaction values (or 1s for binary)
    raise NotImplementedError


def binarize_interactions(
    matrix: sparse.csr_matrix,
    threshold: float = 0.0,
) -> sparse.csr_matrix:
    """Convert a rating matrix to binary implicit feedback.

    Args:
        matrix: Sparse matrix of ratings.
        threshold: Values above this threshold become 1, rest become 0.

    Returns:
        Binary sparse CSR matrix.
    """
    # TODO: Create a copy of the matrix where values > threshold become 1, else 0
    # TODO: Eliminate zeros and return as CSR
    raise NotImplementedError
