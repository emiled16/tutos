"""Great Expectations Data Context configuration and setup."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import great_expectations as gx
from great_expectations.data_context import FileDataContext


def get_context(
    project_root: str | Path | None = None,
) -> FileDataContext:
    """Initialize and return a Great Expectations FileDataContext.

    Creates the GX project directory structure if it doesn't exist.

    Args:
        project_root: Root directory for the GX project.
                      Defaults to GX_PROJECT_ROOT env var or "./gx".

    Returns:
        Configured FileDataContext.
    """
    # TODO: Implement
    # - Read project_root from argument, then GX_PROJECT_ROOT env var, then default
    # - Use gx.get_context(mode="file", project_root_dir=str(project_root))
    # - Return the context
    raise NotImplementedError


def add_pandas_datasource(
    context: FileDataContext,
    datasource_name: str = "pandas_datasource",
) -> Any:
    """Add a pandas datasource to the context.

    Args:
        context: The GE Data Context.
        datasource_name: Name for the datasource.

    Returns:
        The configured datasource.
    """
    # TODO: Implement
    # - Use context.sources.add_pandas(datasource_name)
    # - Return the datasource
    raise NotImplementedError


def add_csv_asset(
    datasource: Any,
    asset_name: str,
    file_path: str | Path,
) -> Any:
    """Add a CSV data asset to a datasource.

    Args:
        datasource: The pandas datasource.
        asset_name: Name for this data asset.
        file_path: Path to the CSV file.

    Returns:
        The configured data asset.
    """
    # TODO: Implement
    # - Use datasource.add_csv_asset(name=asset_name, filepath_or_buffer=file_path)
    # - Return the asset
    raise NotImplementedError


def add_dataframe_asset(
    datasource: Any,
    asset_name: str,
) -> Any:
    """Add a DataFrame data asset to a datasource (for in-memory validation).

    Args:
        datasource: The pandas datasource.
        asset_name: Name for this data asset.

    Returns:
        The configured data asset.
    """
    # TODO: Implement
    # - Use datasource.add_dataframe_asset(name=asset_name)
    # - Return the asset
    raise NotImplementedError
