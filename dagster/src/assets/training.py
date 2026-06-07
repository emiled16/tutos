"""Model training assets: trained_model and model_metrics.

Trains a scikit-learn model on the feature table and records
training metrics as a separate asset.
"""

from typing import Any

import dagster as dg
import pandas as pd
from sklearn.base import BaseEstimator

from partitions import daily_partitions


@dg.asset(
    group_name="training",
    partitions_def=daily_partitions,
    io_manager_key="model_io_manager",
    description="Trained scikit-learn model artifact.",
)
def trained_model(
    context: dg.AssetExecutionContext, feature_table: pd.DataFrame
) -> BaseEstimator:
    """Train a machine learning model on the feature table.

    Splits the feature table into train/validation sets, fits a model,
    and returns the trained estimator.

    Args:
        context: Dagster execution context.
        feature_table: DataFrame with features and label column.

    Returns:
        A fitted scikit-learn estimator.
    """
    context.log.info(f"Training model on {len(feature_table)} samples")

    # TODO: Implement model training:
    #   1. Separate features (X) from label (y)
    #   2. Split into train/validation using train_test_split (80/20)
    #   3. Initialize a RandomForestClassifier (or Regressor depending on label type)
    #   4. Fit the model on training data
    #   5. Log training accuracy via context.add_output_metadata()
    #   6. Return the fitted model
    raise NotImplementedError


@dg.asset(
    group_name="training",
    partitions_def=daily_partitions,
    description="Training metrics including loss, accuracy, and convergence info.",
)
def model_metrics(
    context: dg.AssetExecutionContext, trained_model: BaseEstimator, feature_table: pd.DataFrame
) -> dict[str, Any]:
    """Compute and record training metrics for the model.

    Args:
        context: Dagster execution context.
        trained_model: The fitted model estimator.
        feature_table: The feature table used for training.

    Returns:
        A dict of training metrics (accuracy, feature importances, etc.).
    """
    context.log.info("Computing model training metrics")

    # TODO: Implement metric computation:
    #   1. Separate X and y from feature_table
    #   2. Compute training accuracy (model.score(X, y))
    #   3. Extract feature importances if available
    #   4. Record number of training samples
    #   5. Log metrics via context.add_output_metadata()
    #   6. Return metrics as a dict
    raise NotImplementedError
