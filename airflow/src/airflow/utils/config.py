"""Configuration management for the ML pipeline."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Environment(str, Enum):
    """Deployment environment."""

    DEV = "dev"
    STAGING = "staging"
    PRODUCTION = "production"


class DataSourceConfig(BaseModel):
    """Configuration for a data source.

    Attributes:
        name: Identifier for the data source.
        source_type: Type of source ("api", "s3", "database").
        connection_id: Airflow connection ID.
        path_or_table: File path, S3 prefix, or table name.
        schedule: How often to ingest (cron expression or preset).
    """

    name: str
    source_type: str
    connection_id: str
    path_or_table: str
    schedule: str = "@daily"


class ModelConfig(BaseModel):
    """Configuration for model training.

    Attributes:
        model_name: Name for the model in the registry.
        model_type: sklearn model class to use.
        hyperparameters: Model hyperparameters.
        test_size: Fraction of data for validation.
        metric_thresholds: Minimum acceptable metric values.
    """

    model_name: str = "recommendation_model"
    model_type: str = "random_forest"
    hyperparameters: dict[str, Any] = Field(default_factory=dict)
    test_size: float = 0.2
    metric_thresholds: dict[str, float] = Field(
        default_factory=lambda: {"accuracy": 0.80, "f1_score": 0.75}
    )


class PipelineConfig(BaseModel):
    """Top-level pipeline configuration.

    Attributes:
        environment: Current deployment environment.
        data_sources: List of configured data sources.
        model_config: Model training configuration.
        notification_channels: Where to send alerts.
        staging_path: Path for intermediate data storage.
    """

    environment: Environment = Environment.DEV
    data_sources: list[DataSourceConfig] = Field(default_factory=list)
    model_config: ModelConfig = Field(default_factory=ModelConfig)
    notification_channels: list[str] = Field(
        default_factory=lambda: ["slack"]
    )
    staging_path: str = "/tmp/ml_pipeline/staging"


def load_config(environment: str | None = None) -> PipelineConfig:
    """Load pipeline configuration for the given environment.

    Configuration is loaded from Airflow Variables with fallback to defaults.

    Args:
        environment: Environment name. If None, reads from ENVIRONMENT variable.

    Returns:
        PipelineConfig with environment-specific settings.
    """
    # TODO: Implement configuration loading.
    # - Determine environment from argument or Airflow Variable
    # - Load environment-specific overrides from Airflow Variables
    # - Merge with defaults
    # - Return PipelineConfig
    raise NotImplementedError


def get_data_sources(config: PipelineConfig) -> list[DataSourceConfig]:
    """Get the list of configured data sources.

    Args:
        config: Pipeline configuration.

    Returns:
        List of DataSourceConfig objects.
    """
    # TODO: Implement data source retrieval.
    raise NotImplementedError
