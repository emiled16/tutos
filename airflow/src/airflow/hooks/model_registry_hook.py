"""Custom Airflow hook for interacting with a model registry."""

from __future__ import annotations

from typing import Any

from airflow.hooks.base import BaseHook


class ModelRegistryHook(BaseHook):
    """Hook for interacting with a model registry service.

    Manages the connection to a model registry API (e.g., MLflow, custom
    service) and provides methods for registering, retrieving, and
    promoting model versions.

    The hook uses Airflow's connection system to manage credentials.
    Configure a connection with:
        - conn_id: "model_registry_default"
        - host: Registry API URL
        - password: API key/token
    """

    conn_name_attr = "model_registry_conn_id"
    default_conn_name = "model_registry_default"
    conn_type = "http"
    hook_name = "Model Registry"

    def __init__(
        self,
        model_registry_conn_id: str = default_conn_name,
    ) -> None:
        super().__init__()
        self.model_registry_conn_id = model_registry_conn_id
        self._session: Any = None

    def get_conn(self) -> Any:
        """Get or create a connection to the model registry.

        Returns:
            A requests.Session configured with base URL and auth headers.
        """
        # TODO: Implement connection setup.
        # - Use self.get_connection(self.model_registry_conn_id) to get credentials
        # - Create a requests.Session with base_url and auth headers
        # - Cache the session in self._session
        raise NotImplementedError

    def register_model(
        self,
        model_name: str,
        model_path: str,
        metrics: dict[str, float],
        parameters: dict[str, Any] | None = None,
        tags: dict[str, str] | None = None,
    ) -> str:
        """Register a new model version in the registry.

        Args:
            model_name: Name of the model in the registry.
            model_path: Path to the serialized model artifact.
            metrics: Training/evaluation metrics.
            parameters: Model hyperparameters.
            tags: Additional metadata tags.

        Returns:
            The registered model version identifier.

        Raises:
            AirflowException: If registration fails.
        """
        # TODO: Implement model registration.
        # - POST to /api/models/{model_name}/versions
        # - Include model_path, metrics, parameters, tags in the request body
        # - Return the version ID from the response
        raise NotImplementedError

    def get_latest_version(self, model_name: str) -> dict[str, Any]:
        """Get the latest version of a model from the registry.

        Args:
            model_name: Name of the model.

        Returns:
            Dictionary with version info (version_id, metrics, status, etc.).
        """
        # TODO: Implement latest version retrieval.
        # - GET /api/models/{model_name}/versions/latest
        # - Return parsed response
        raise NotImplementedError

    def promote_model(
        self,
        model_name: str,
        version_id: str,
        stage: str = "production",
    ) -> bool:
        """Promote a model version to a deployment stage.

        Args:
            model_name: Name of the model.
            version_id: Version to promote.
            stage: Target stage ("staging", "production", "archived").

        Returns:
            True if promotion was successful.
        """
        # TODO: Implement model promotion.
        # - PUT /api/models/{model_name}/versions/{version_id}/stage
        # - Include {"stage": stage} in the request body
        raise NotImplementedError

    def compare_models(
        self,
        model_name: str,
        version_a: str,
        version_b: str,
    ) -> dict[str, Any]:
        """Compare metrics between two model versions.

        Args:
            model_name: Name of the model.
            version_a: First version ID.
            version_b: Second version ID.

        Returns:
            Dictionary with side-by-side metric comparison.
        """
        # TODO: Implement model comparison.
        # - Retrieve metrics for both versions
        # - Return a comparison dict with differences and relative improvements
        raise NotImplementedError
