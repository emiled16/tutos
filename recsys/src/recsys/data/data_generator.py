"""Generate synthetic user-item interaction data for development and testing."""

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class SyntheticDataConfig:
    """Configuration for synthetic data generation."""

    n_users: int = 500
    n_items: int = 200
    n_interactions: int = 10_000
    n_user_clusters: int = 5
    n_item_genres: int = 8
    n_item_features: int = 20
    rating_scale: tuple[float, float] = (1.0, 5.0)
    noise_std: float = 0.5
    random_seed: int = 42


def generate_user_features(
    n_users: int,
    n_clusters: int,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate synthetic user features with cluster structure.

    Creates users belonging to latent preference clusters, each with
    different genre affinities.

    Args:
        n_users: Number of users to generate.
        n_clusters: Number of latent user preference clusters.
        rng: NumPy random generator for reproducibility.

    Returns:
        DataFrame with user_id and feature columns.
    """
    # TODO: Assign each user to a random cluster
    # TODO: Generate user feature vectors based on cluster membership
    #       (e.g., age group, activity level, genre preferences)
    # TODO: Return DataFrame with user_id and feature columns
    raise NotImplementedError


def generate_item_features(
    n_items: int,
    n_genres: int,
    n_features: int,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate synthetic item features with genre and text-like feature vectors.

    Args:
        n_items: Number of items to generate.
        n_genres: Number of distinct genres.
        n_features: Dimensionality of the TF-IDF-like feature vector per item.
        rng: NumPy random generator.

    Returns:
        DataFrame with item_id, genre, title, description, and feature columns.
    """
    # TODO: Assign each item a primary genre and optional secondary genres
    # TODO: Generate a synthetic TF-IDF-like feature vector per item
    #       (sparse, non-negative, genre-correlated)
    # TODO: Create synthetic title and description strings from genre keywords
    raise NotImplementedError


def generate_interactions(
    n_users: int,
    n_items: int,
    n_interactions: int,
    user_features: pd.DataFrame,
    item_features: pd.DataFrame,
    config: SyntheticDataConfig,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate synthetic user-item interactions driven by latent preferences.

    Users in similar clusters tend to rate similar genres highly. Ratings are
    generated from a latent factor model with added noise.

    Args:
        n_users: Number of users.
        n_items: Number of items.
        n_interactions: Number of interactions to generate.
        user_features: User feature DataFrame.
        item_features: Item feature DataFrame.
        config: Data generation config.
        rng: NumPy random generator.

    Returns:
        DataFrame with columns: user_id, item_id, rating, timestamp.
    """
    # TODO: Create latent preference vectors for each user cluster and item genre
    # TODO: Sample (user, item) pairs — bias toward cluster-genre affinity
    #       so that interactions are not uniformly random
    # TODO: Compute ratings as dot(user_latent, item_latent) + noise, clipped to rating_scale
    # TODO: Generate monotonically increasing timestamps with some randomness
    raise NotImplementedError


def generate_synthetic_dataset(
    config: SyntheticDataConfig | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Generate a complete synthetic dataset.

    Args:
        config: Generation configuration. Uses defaults if None.

    Returns:
        Tuple of (interactions, user_features, item_features) DataFrames.
    """
    if config is None:
        config = SyntheticDataConfig()

    rng = np.random.default_rng(config.random_seed)

    user_features = generate_user_features(config.n_users, config.n_user_clusters, rng)
    item_features = generate_item_features(
        config.n_items, config.n_item_genres, config.n_item_features, rng
    )
    interactions = generate_interactions(
        config.n_users,
        config.n_items,
        config.n_interactions,
        user_features,
        item_features,
        config,
        rng,
    )

    return interactions, user_features, item_features
