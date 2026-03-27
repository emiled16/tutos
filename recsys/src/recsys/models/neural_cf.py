"""Neural Collaborative Filtering (NCF) with learned embeddings."""

from dataclasses import dataclass

import numpy as np
import torch
import torch.nn as nn
from scipy import sparse
from torch.utils.data import DataLoader, Dataset

from recsys.models.base import BaseRecommender


@dataclass
class NCFConfig:
    """Configuration for the Neural Collaborative Filtering model."""

    embedding_dim: int = 64
    mlp_layers: list[int] | None = None
    dropout: float = 0.2
    learning_rate: float = 1e-3
    weight_decay: float = 1e-5
    n_epochs: int = 20
    batch_size: int = 1024
    n_negatives: int = 4

    def __post_init__(self) -> None:
        if self.mlp_layers is None:
            self.mlp_layers = [128, 64, 32]


class InteractionDataset(Dataset):
    """PyTorch Dataset for user-item interactions with negative sampling."""

    def __init__(
        self,
        user_indices: np.ndarray,
        item_indices: np.ndarray,
        labels: np.ndarray,
    ) -> None:
        self.user_indices = torch.LongTensor(user_indices)
        self.item_indices = torch.LongTensor(item_indices)
        self.labels = torch.FloatTensor(labels)

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        return self.user_indices[idx], self.item_indices[idx], self.labels[idx]


class NeuralCF(nn.Module):
    """Neural Collaborative Filtering model combining GMF and MLP pathways.

    Architecture:
        user_id, item_id
          → user_embedding, item_embedding (separate for GMF and MLP)
          → GMF: element-wise product
          → MLP: concatenate → dense layers with ReLU + dropout
          → concatenate GMF and MLP outputs
          → final prediction layer → sigmoid
    """

    def __init__(
        self,
        n_users: int,
        n_items: int,
        config: NCFConfig,
    ) -> None:
        super().__init__()
        self.config = config

        # TODO: Create GMF embedding layers for users and items (embedding_dim each)
        # TODO: Create MLP embedding layers for users and items (embedding_dim each)
        # TODO: Build the MLP as nn.Sequential with layers from config.mlp_layers
        #       Input size = 2 * embedding_dim, each layer: Linear → ReLU → Dropout
        # TODO: Create the final prediction layer:
        #       Linear(embedding_dim + config.mlp_layers[-1], 1) → Sigmoid

        raise NotImplementedError

    def forward(self, user_ids: torch.Tensor, item_ids: torch.Tensor) -> torch.Tensor:
        """Forward pass.

        Args:
            user_ids: Tensor of user indices, shape (batch_size,).
            item_ids: Tensor of item indices, shape (batch_size,).

        Returns:
            Predicted scores, shape (batch_size,).
        """
        # TODO: Look up GMF embeddings and compute element-wise product
        # TODO: Look up MLP embeddings, concatenate, and pass through MLP layers
        # TODO: Concatenate GMF output and MLP output
        # TODO: Pass through final prediction layer and squeeze
        raise NotImplementedError


def sample_negatives(
    interaction_matrix: sparse.csr_matrix,
    n_negatives: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Sample negative (unobserved) user-item pairs for training.

    For each positive interaction, samples n_negatives random items
    that the user has not interacted with.

    Args:
        interaction_matrix: Sparse CSR matrix of positive interactions.
        n_negatives: Number of negative samples per positive.
        rng: NumPy random generator.

    Returns:
        Tuple of (user_indices, item_indices, labels) arrays where
        labels are 1.0 for positive and 0.0 for negative.
    """
    # TODO: Extract positive (user, item) pairs from the interaction matrix
    # TODO: For each positive pair, sample n_negatives random items
    #       that the user hasn't interacted with
    # TODO: Combine positives (label=1) and negatives (label=0)
    # TODO: Shuffle and return
    raise NotImplementedError


class NCFRecommender(BaseRecommender):
    """Recommender wrapping the NeuralCF model with training and inference."""

    def __init__(self, config: NCFConfig | None = None) -> None:
        super().__init__(name="NCF")
        self.config = config or NCFConfig()
        self.model: NeuralCF | None = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.interaction_matrix: sparse.csr_matrix | None = None
        self._user_ids: np.ndarray | None = None
        self._item_ids: np.ndarray | None = None

    def fit(
        self,
        interaction_matrix: sparse.csr_matrix,
        user_ids: np.ndarray,
        item_ids: np.ndarray,
    ) -> "NCFRecommender":
        self.interaction_matrix = interaction_matrix
        self._user_ids = user_ids
        self._item_ids = item_ids

        n_users, n_items = interaction_matrix.shape

        # TODO: Initialize NeuralCF model with n_users, n_items, and config
        # TODO: Move model to self.device
        # TODO: Set up Adam optimizer with config.learning_rate and weight_decay
        # TODO: Use BCELoss as the loss function
        # TODO: For each epoch:
        #   1. Sample negatives using sample_negatives()
        #   2. Create InteractionDataset and DataLoader
        #   3. Train one epoch: forward pass → loss → backward → step
        #   4. Track and optionally log epoch loss
        # TODO: Set self.is_fitted = True

        raise NotImplementedError

    def recommend(
        self,
        user_id: int,
        n: int = 10,
        exclude_seen: bool = True,
    ) -> list[tuple[int, float]]:
        self._check_is_fitted()

        # TODO: Create tensors for the user index repeated n_items times and all item indices
        # TODO: Run model.forward() in eval mode with torch.no_grad()
        # TODO: Optionally exclude seen items
        # TODO: Return top-n (item_id, score) tuples
        raise NotImplementedError

    def predict(self, user_id: int, item_id: int) -> float:
        self._check_is_fitted()

        # TODO: Run model.forward() on the single (user, item) pair
        raise NotImplementedError
