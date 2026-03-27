"""Synthetic fraud detection data generator."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class DataGeneratorConfig:
    """Configuration for synthetic data generation."""

    n_users: int = 1000
    n_transactions: int = 50_000
    fraud_rate: float = 0.02
    start_date: datetime = field(
        default_factory=lambda: datetime(2024, 1, 1)
    )
    end_date: datetime = field(
        default_factory=lambda: datetime(2024, 6, 30)
    )
    random_seed: int = 42


def generate_users(config: DataGeneratorConfig) -> pd.DataFrame:
    """Generate synthetic user profiles.

    Creates user records with account creation dates, verification status,
    and country. Fraud-prone users get newer accounts on average.

    Args:
        config: Data generation configuration.

    Returns:
        DataFrame with columns [user_id, account_created_at, email_verified,
        country, timestamp].
    """
    # TODO: Implement
    # - Generate n_users user IDs (e.g., "user_0001" format)
    # - Randomly assign account_created_at dates (some recent, some old)
    # - Set email_verified as boolean (newer accounts less likely verified)
    # - Assign countries from a weighted distribution
    # - Set timestamp to config.end_date for all rows
    raise NotImplementedError


def generate_transactions(
    config: DataGeneratorConfig, users: pd.DataFrame
) -> pd.DataFrame:
    """Generate synthetic transaction data with realistic fraud patterns.

    Normal transactions follow user-specific spending patterns. Fraudulent
    transactions have distinct characteristics: unusual amounts, rapid
    succession, atypical merchants.

    Args:
        config: Data generation configuration.
        users: User profiles DataFrame.

    Returns:
        DataFrame with columns [transaction_id, user_id, amount, merchant_id,
        merchant_category, is_fraud, timestamp].
    """
    # TODO: Implement
    # - Generate n_transactions with random user assignments
    # - Normal transactions: amount ~ LogNormal(mean=50, std=30) per user
    # - Fraudulent transactions (fraud_rate fraction):
    #   - Higher amounts (2-10x user average)
    #   - Clustered in time (multiple within short windows)
    #   - Different merchant categories than user's typical
    # - Assign merchant_ids and categories
    # - Generate timestamps uniformly between start_date and end_date
    # - Sort by timestamp
    raise NotImplementedError


def save_datasets(
    users: pd.DataFrame,
    transactions: pd.DataFrame,
    output_dir: str | Path = "data",
) -> dict[str, Path]:
    """Save generated datasets as parquet files.

    Args:
        users: User profiles DataFrame.
        transactions: Transactions DataFrame.
        output_dir: Directory to save parquet files.

    Returns:
        Dictionary mapping dataset name to file path.
    """
    # TODO: Implement
    # - Create output_dir if it doesn't exist
    # - Save users to output_dir/users.parquet
    # - Save transactions to output_dir/transactions.parquet
    # - Return paths dict
    raise NotImplementedError


def generate_all(
    config: DataGeneratorConfig | None = None,
    output_dir: str | Path = "data",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate all datasets and save to disk.

    Args:
        config: Optional configuration. Uses defaults if None.
        output_dir: Directory to save parquet files.

    Returns:
        Tuple of (users_df, transactions_df).
    """
    # TODO: Implement
    # - Create default config if None
    # - Generate users
    # - Generate transactions
    # - Save datasets
    # - Return (users, transactions)
    raise NotImplementedError


if __name__ == "__main__":
    generate_all()
