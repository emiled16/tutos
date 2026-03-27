"""Model evaluation assets: evaluation_report and model_comparison.

Evaluates the trained model on holdout data and compares
performance against previous model versions.
"""

from typing import Any

import dagster as dg
import pandas as pd
from sklearn.base import BaseEstimator

from dagster.partitions import daily_partitions


@dg.asset(
    group_name="evaluation",
    partitions_def=daily_partitions,
    description="Detailed evaluation report with metrics on holdout data.",
)
def evaluation_report(
    context: dg.AssetExecutionContext,
    trained_model: BaseEstimator,
    feature_table: pd.DataFrame,
) -> dict[str, Any]:
    """Evaluate the trained model on a holdout test set.

    Computes classification/regression metrics and generates
    a detailed evaluation report.

    Args:
        context: Dagster execution context.
        trained_model: The fitted model to evaluate.
        feature_table: Full feature table (will split out a test set).

    Returns:
        A dict containing evaluation metrics (accuracy, precision, recall,
        F1, confusion matrix, etc.).
    """
    context.log.info("Evaluating model on holdout data")

    # TODO: Implement model evaluation:
    #   1. Split feature_table into the same train/test split used in training
    #      (use the same random_state for consistency)
    #   2. Generate predictions on the test set
    #   3. Compute metrics: accuracy, precision, recall, f1_score
    #   4. Compute confusion matrix
    #   5. Log summary metrics via context.add_output_metadata()
    #   6. Return the full evaluation report as a dict
    raise NotImplementedError


@dg.asset(
    group_name="evaluation",
    partitions_def=daily_partitions,
    description="Comparison of current model against previous model version.",
)
def model_comparison(
    context: dg.AssetExecutionContext,
    evaluation_report: dict[str, Any],
) -> dict[str, Any]:
    """Compare the current model's performance against the previous version.

    Loads the previous day's evaluation report (if available) and
    computes deltas for key metrics.

    Args:
        context: Dagster execution context.
        evaluation_report: The current model's evaluation metrics.

    Returns:
        A dict containing metric deltas and a recommendation
        (promote, keep previous, or investigate).
    """
    context.log.info("Comparing model against previous version")

    # TODO: Implement model comparison:
    #   1. Attempt to load the previous partition's evaluation_report
    #      (handle the case where no previous report exists)
    #   2. Compute deltas for key metrics (accuracy, f1, etc.)
    #   3. Determine recommendation:
    #      - "promote" if all metrics improved
    #      - "keep_previous" if any metric degraded significantly (>5%)
    #      - "investigate" if mixed results
    #   4. Log comparison via context.add_output_metadata()
    #   5. Return comparison report
    raise NotImplementedError
