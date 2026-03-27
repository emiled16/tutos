"""Custom Airflow operator for ML model training."""

from __future__ import annotations

from typing import Any

from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context


class ModelTrainingOperator(BaseOperator):
    """Custom operator that trains an ML model.

    This operator wraps the model training process, handling:
    - Loading training data from a specified path
    - Configuring model hyperparameters
    - Training the model using scikit-learn
    - Saving the model artifact
    - Pushing training metrics to XCom

    Attributes:
        training_data_path: Path to the training dataset.
        model_type: Type of model to train (e.g., "random_forest", "gradient_boosting").
        hyperparameters: Dictionary of model hyperparameters.
        model_output_path: Path to save the trained model artifact.
        test_size: Fraction of data to use for validation.
    """

    template_fields = ("training_data_path", "model_output_path")

    def __init__(
        self,
        training_data_path: str,
        model_type: str = "random_forest",
        hyperparameters: dict[str, Any] | None = None,
        model_output_path: str = "/tmp/model.pkl",
        test_size: float = 0.2,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.training_data_path = training_data_path
        self.model_type = model_type
        self.hyperparameters = hyperparameters or {}
        self.model_output_path = model_output_path
        self.test_size = test_size

    def execute(self, context: Context) -> dict[str, Any]:
        """Execute model training.

        Steps:
        1. Load training data from training_data_path
        2. Split into train/validation sets
        3. Initialize model with hyperparameters
        4. Fit the model
        5. Evaluate on validation set
        6. Save model artifact
        7. Return metrics dict (pushed to XCom automatically)

        Args:
            context: Airflow context dictionary.

        Returns:
            Dictionary with model_path, metrics (accuracy, f1, etc.), and metadata.
        """
        # TODO: Implement model training execution.
        # self.log.info("Loading training data from %s", self.training_data_path)
        # 1. Load data with pandas
        # 2. Split into X_train, X_val, y_train, y_val
        # 3. Create model based on self.model_type
        # 4. Fit model on training data
        # 5. Evaluate on validation data
        # 6. Save model with joblib/pickle
        # 7. Return metrics dict
        raise NotImplementedError

    def _create_model(self) -> Any:
        """Create an sklearn model instance based on model_type.

        Returns:
            An unfitted scikit-learn estimator.

        Raises:
            ValueError: If model_type is not supported.
        """
        # TODO: Implement model factory.
        # Support at least: "random_forest", "gradient_boosting", "logistic_regression"
        # Apply self.hyperparameters as constructor kwargs
        raise NotImplementedError
