"""Unit tests for ML pipeline assets.

Tests asset functions directly as Python functions with mock inputs,
and also tests materialization through Dagster's test utilities.
"""

import numpy as np
import pandas as pd
import pytest
from sklearn.base import BaseEstimator


@pytest.fixture
def sample_raw_data() -> pd.DataFrame:
    """Generate a sample raw DataFrame with some missing values and outliers."""
    np.random.seed(42)
    n = 100
    return pd.DataFrame(
        {
            "user_id": [f"user_{i}" for i in range(n)],
            "timestamp": pd.date_range("2024-01-15", periods=n, freq="h"),
            "feature_1": np.random.normal(10, 2, n),
            "feature_2": np.random.normal(5, 1, n),
            "feature_3": np.random.normal(0, 1, n),
            "label": np.random.choice([0, 1], n),
        }
    )


@pytest.fixture
def sample_raw_data_with_issues(sample_raw_data: pd.DataFrame) -> pd.DataFrame:
    """Create a raw DataFrame with missing values and outliers."""
    df = sample_raw_data.copy()
    df.loc[5, "feature_1"] = np.nan
    df.loc[10, "feature_2"] = np.nan
    df.loc[15, "label"] = np.nan
    df.loc[20, "feature_1"] = 1000.0  # outlier
    return df


@pytest.fixture
def sample_cleaned_data(sample_raw_data: pd.DataFrame) -> pd.DataFrame:
    """A pre-cleaned DataFrame for feature engineering tests."""
    return sample_raw_data.dropna()


@pytest.fixture
def sample_feature_table(sample_cleaned_data: pd.DataFrame) -> pd.DataFrame:
    """A sample feature table with derived features."""
    df = sample_cleaned_data.copy()
    df["feature_1_x_2"] = df["feature_1"] * df["feature_2"]
    df["feature_1_sq"] = df["feature_1"] ** 2
    return df


class TestRawData:
    def test_returns_dataframe(self) -> None:
        """Test that raw_data returns a pandas DataFrame."""
        # TODO: Implement — call the raw_data asset function directly,
        #       assert the result is a pd.DataFrame
        raise NotImplementedError

    def test_has_expected_columns(self) -> None:
        """Test that the raw data has the expected column schema."""
        # TODO: Implement — assert columns include
        #       user_id, timestamp, feature_1, feature_2, feature_3, label
        raise NotImplementedError

    def test_generates_sufficient_rows(self) -> None:
        """Test that at least 100 rows are generated per partition."""
        # TODO: Implement — assert len(result) >= 100
        raise NotImplementedError


class TestCleanedData:
    def test_removes_null_labels(self, sample_raw_data_with_issues: pd.DataFrame) -> None:
        """Test that rows with null labels are removed."""
        # TODO: Implement — pass sample_raw_data_with_issues to cleaned_data,
        #       assert no nulls in the label column
        raise NotImplementedError

    def test_fills_missing_features(self, sample_raw_data_with_issues: pd.DataFrame) -> None:
        """Test that missing feature values are filled."""
        # TODO: Implement — pass sample_raw_data_with_issues to cleaned_data,
        #       assert no nulls in feature columns
        raise NotImplementedError

    def test_removes_outliers(self, sample_raw_data_with_issues: pd.DataFrame) -> None:
        """Test that extreme outliers are removed."""
        # TODO: Implement — pass data with outlier (feature_1=1000),
        #       assert the outlier row is removed
        raise NotImplementedError


class TestFeatureTable:
    def test_creates_interaction_features(self, sample_cleaned_data: pd.DataFrame) -> None:
        """Test that interaction features are created."""
        # TODO: Implement — pass cleaned data to feature_table,
        #       assert interaction columns exist (feature_1_x_feature_2, etc.)
        raise NotImplementedError

    def test_preserves_label_column(self, sample_cleaned_data: pd.DataFrame) -> None:
        """Test that the label column is preserved in the feature table."""
        # TODO: Implement — assert "label" in result.columns
        raise NotImplementedError

    def test_output_has_more_columns_than_input(self, sample_cleaned_data: pd.DataFrame) -> None:
        """Test that feature engineering adds columns."""
        # TODO: Implement — assert result.shape[1] > sample_cleaned_data.shape[1]
        raise NotImplementedError


class TestTrainedModel:
    def test_returns_fitted_estimator(self, sample_feature_table: pd.DataFrame) -> None:
        """Test that trained_model returns a fitted scikit-learn model."""
        # TODO: Implement — pass feature table to trained_model,
        #       assert result is an instance of BaseEstimator
        raise NotImplementedError

    def test_model_can_predict(self, sample_feature_table: pd.DataFrame) -> None:
        """Test that the trained model can generate predictions."""
        # TODO: Implement — train model, then call model.predict(X_test),
        #       assert predictions have the correct shape
        raise NotImplementedError


class TestEvaluationReport:
    def test_contains_expected_metrics(self) -> None:
        """Test that the evaluation report includes standard metrics."""
        # TODO: Implement — call evaluation_report,
        #       assert keys include "accuracy", "precision", "recall", "f1_score"
        raise NotImplementedError

    def test_metrics_in_valid_range(self) -> None:
        """Test that all metric values are between 0 and 1."""
        # TODO: Implement — assert all metric values are in [0.0, 1.0]
        raise NotImplementedError
