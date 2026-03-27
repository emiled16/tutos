"""Distributed data loading and preprocessing with Ray Data."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import ray.data


class DataFormat(Enum):
    """Supported input data formats."""

    CSV = "csv"
    PARQUET = "parquet"
    JSON = "json"


@dataclass
class DatasetConfig:
    """Configuration for loading and splitting a dataset.

    Attributes:
        path: Local or remote path to the data source.
        format: Data file format.
        target_column: Name of the label / target column.
        train_fraction: Fraction of data used for training.
        batch_size: Batch size for map_batches operations.
        num_workers: Parallelism for read and map operations.
    """

    path: str | Path
    format: DataFormat = DataFormat.PARQUET
    target_column: str = "label"
    train_fraction: float = 0.8
    batch_size: int = 256
    num_workers: int = 4


def load_dataset(config: DatasetConfig) -> ray.data.Dataset:
    """Load a dataset from disk or remote storage.

    Reads data in the format specified by *config.format* and returns a
    :class:`ray.data.Dataset`.

    Args:
        config: Dataset loading configuration.

    Returns:
        A Ray Dataset ready for further transformations.
    """
    # TODO: Dispatch to ray.data.read_csv / read_parquet / read_json based
    #       on config.format, using config.path and config.num_workers for
    #       parallelism
    raise NotImplementedError


def split_dataset(
    ds: ray.data.Dataset,
    train_fraction: float,
) -> tuple[ray.data.Dataset, ray.data.Dataset]:
    """Split a dataset into train and validation sets.

    Args:
        ds: Full dataset.
        train_fraction: Proportion for the training split (0.0–1.0).

    Returns:
        A (train, validation) tuple of Ray Datasets.
    """
    # TODO: Use ds.train_test_split or ds.split_proportionately to create
    #       train/val splits at the given fraction
    raise NotImplementedError


def apply_transforms(
    ds: ray.data.Dataset,
    transforms: list[dict[str, Any]],
    batch_size: int = 256,
) -> ray.data.Dataset:
    """Apply a sequence of batch transforms to a dataset.

    Each entry in *transforms* is a dict describing a single transformation
    (e.g. ``{"name": "normalize", "columns": ["feature_1", "feature_2"]}``).

    Args:
        ds: Input Ray Dataset.
        transforms: Ordered list of transform specifications.
        batch_size: Number of rows per batch in ``map_batches``.

    Returns:
        The transformed dataset.
    """
    # TODO: Iterate over transforms, building a callable for each and applying
    #       it via ds.map_batches with the given batch_size. Support at least
    #       "normalize" and "one_hot" transform types.
    raise NotImplementedError


def dataset_to_torch(
    ds: ray.data.Dataset,
    feature_columns: list[str],
    label_column: str,
) -> Any:
    """Convert a Ray Dataset to a Torch-compatible iterator.

    Args:
        ds: Ray Dataset.
        feature_columns: Columns to include as features.
        label_column: Column to use as the label.

    Returns:
        An iterable yielding (features, labels) tensor batches.
    """
    # TODO: Use ds.iter_torch_batches (or to_torch) specifying
    #       feature_columns and label_column
    raise NotImplementedError
