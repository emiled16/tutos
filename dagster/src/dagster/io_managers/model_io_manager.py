"""Custom IO manager for persisting ML model artifacts.

Uses joblib for serialization with metadata tracking.
"""

from pathlib import Path
from typing import Any

from dagster import ConfigurableIOManager, InputContext, OutputContext


class ModelIOManager(ConfigurableIOManager):
    """IO manager that serializes ML models using joblib.

    Models are stored as:
        {base_path}/{asset_name}/{partition_key}.joblib

    Attributes:
        base_path: Root directory for model artifact storage.
    """

    base_path: str = "./data/models"

    def _get_path(self, context: OutputContext | InputContext) -> Path:
        """Compute the file path for a model artifact.

        Args:
            context: The output or input context.

        Returns:
            The full Path to the joblib file.
        """
        # TODO: Implement path computation (similar to ParquetIOManager):
        #   Return Path(self.base_path) / asset_name / f"{partition_key}.joblib"
        raise NotImplementedError

    def handle_output(self, context: OutputContext, obj: Any) -> None:
        """Serialize and persist a model artifact.

        Args:
            context: Output context with asset metadata.
            obj: The model object to serialize (any scikit-learn estimator).
        """
        # TODO: Implement model serialization:
        #   1. Compute the file path
        #   2. Create parent directories
        #   3. Use joblib.dump(obj, path) to serialize
        #   4. Log the path and model type (type(obj).__name__)
        #   5. Add metadata: model_type, file_size, path
        raise NotImplementedError

    def load_input(self, context: InputContext) -> Any:
        """Deserialize and load a model artifact.

        Args:
            context: Input context with asset metadata.

        Returns:
            The deserialized model object.

        Raises:
            FileNotFoundError: If the model file doesn't exist.
        """
        # TODO: Implement model loading:
        #   1. Compute the file path
        #   2. Use joblib.load(path) to deserialize
        #   3. Log the path and model type
        raise NotImplementedError
