"""Main Definitions object combining all Dagster components.

This is the entry point that `dagster dev` loads. It registers
all assets, resources, IO managers, sensors, and schedules.
"""

import dagster as dg

from assets import (
    cleaned_data,
    evaluation_report,
    feature_stats,
    feature_table,
    model_comparison,
    model_metrics,
    raw_data,
    trained_model,
)
from io_managers.model_io_manager import ModelIOManager
from io_managers.parquet_io_manager import ParquetIOManager
from resources.database import DatabaseResource
from schedules import daily_training_schedule
from sensors.new_data_sensor import new_data_sensor

# TODO: Assemble the Definitions object with all components:
#
defs = dg.Definitions(
    assets=[
        raw_data,
        cleaned_data,
        feature_table,
        feature_stats,
        trained_model,
        model_metrics,
        evaluation_report,
        model_comparison,
    ],
    resources={
        "io_manager": ParquetIOManager(base_path="./data/parquet"),
        "model_io_manager": ModelIOManager(base_path="./data/models"),
        "database": DatabaseResource(),
    },
    sensors=[new_data_sensor],
    schedules=[daily_training_schedule],
)
