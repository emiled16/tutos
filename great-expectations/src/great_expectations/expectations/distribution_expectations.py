"""Custom expectations for distribution checks (KS test, PSI)."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from scipy import stats


def compute_ks_statistic(
    reference: pd.Series, current: pd.Series
) -> tuple[float, float]:
    """Compute the two-sample Kolmogorov-Smirnov test statistic and p-value.

    Args:
        reference: Reference distribution values.
        current: Current distribution values.

    Returns:
        Tuple of (ks_statistic, p_value).
    """
    # TODO: Implement
    # - Use scipy.stats.ks_2samp(reference, current)
    # - Return (statistic, p_value)
    raise NotImplementedError


def compute_psi(
    reference: pd.Series,
    current: pd.Series,
    n_bins: int = 10,
    epsilon: float = 1e-4,
) -> float:
    """Compute the Population Stability Index between two distributions.

    PSI = Σ (p_i - q_i) × ln(p_i / q_i)

    where p_i and q_i are the proportions of values in bin i for the
    reference and current distributions respectively.

    Args:
        reference: Reference distribution values.
        current: Current distribution values.
        n_bins: Number of bins for discretization.
        epsilon: Small value added to avoid log(0).

    Returns:
        PSI value. < 0.1 indicates no shift, 0.1-0.2 moderate, > 0.2 significant.
    """
    # TODO: Implement
    # - Create n_bins equal-width bins from the reference distribution range
    # - Compute proportion of reference values in each bin (p_i)
    # - Compute proportion of current values in each bin (q_i)
    # - Add epsilon to both to avoid division by zero
    # - Compute PSI = sum((p_i - q_i) * ln(p_i / q_i))
    raise NotImplementedError


class DistributionValidator:
    """Validates feature distributions against a reference dataset.

    Stores a reference dataset and provides methods to check if new data
    follows similar distributions.
    """

    def __init__(
        self,
        reference_data: pd.DataFrame,
        ks_threshold: float = 0.05,
        psi_threshold: float = 0.2,
    ) -> None:
        """Initialize with reference data and thresholds.

        Args:
            reference_data: Reference DataFrame to compare against.
            ks_threshold: p-value threshold for KS test (below = drift).
            psi_threshold: PSI threshold (above = significant shift).
        """
        self.reference_data = reference_data
        self.ks_threshold = ks_threshold
        self.psi_threshold = psi_threshold

    def check_column_drift(
        self, current_data: pd.DataFrame, column: str
    ) -> dict[str, Any]:
        """Check a single column for distribution drift.

        Args:
            current_data: Current DataFrame to validate.
            column: Column name to check.

        Returns:
            Dictionary with ks_statistic, ks_p_value, psi, has_drift.
        """
        # TODO: Implement
        # - Get the column from reference and current data
        # - Compute KS statistic and p-value
        # - Compute PSI
        # - Determine has_drift based on thresholds
        # - Return results dict
        raise NotImplementedError

    def check_all_numeric_columns(
        self, current_data: pd.DataFrame
    ) -> dict[str, dict[str, Any]]:
        """Check all numeric columns for distribution drift.

        Args:
            current_data: Current DataFrame to validate.

        Returns:
            Dictionary mapping column names to drift check results.
        """
        # TODO: Implement
        # - Identify numeric columns in reference_data
        # - Call check_column_drift for each
        # - Return {column_name: drift_results, ...}
        raise NotImplementedError

    def get_drifted_columns(
        self, current_data: pd.DataFrame
    ) -> list[str]:
        """Get list of columns that have drifted.

        Args:
            current_data: Current DataFrame to validate.

        Returns:
            List of column names with detected drift.
        """
        # TODO: Implement
        # - Call check_all_numeric_columns
        # - Filter for columns where has_drift is True
        raise NotImplementedError
