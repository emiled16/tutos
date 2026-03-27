"""Custom IO manager for persisting DataFrames as Parquet files.

Handles partitioned storage with a directory-per-asset structure.
"""

from pathlib import Path

import pandas as pd
from dagster import ConfigurableIOManager, InputContext, OutputContext


class ParquetIOManager(ConfigurableIOManager):
    """IO manager that reads and writes pandas DataFrames as Parquet files.

    Files are organized as:
        {base_path}/{asset_name}/{partition_key}.parquet

    Attributes:
        base_path: Root directory for Parquet file storage.
    """

    base_path: str = "./data/parquet"

    def _get_path(self, context: OutputContext | InputContext) -> Path:
        """Compute the file path for a given asset and partition.

        Args:
            context: The output or input context containing asset metadata.

        Returns:
            The full Path to the Parquet file.
        """
        # TODO: Implement path computation:
        #   - Extract asset_key from context (context.asset_key.path[-1])
        #   - Extract partition_key from context (context.partition_key or "unpartitioned")
        #   - Return Path(self.base_path) / asset_name / f"{partition_key}.parquet"
        raise NotImplementedError

    def handle_output(self, context: OutputContext, obj: pd.DataFrame) -> None:
        """Write a DataFrame to a Parquet file.

        Creates parent directories if they don't exist.

        Args:
            context: Output context with asset and partition metadata.
            obj: The DataFrame to persist.
        """
        # TODO: Implement output handling:
        #   1. Compute the file path
        #   2. Create parent directories (path.parent.mkdir(parents=True, exist_ok=True))
        #   3. Write DataFrame to Parquet (obj.to_parquet(path, index=False))
        #   4. Log the file path and row count
        #   5. Add metadata: context.add_output_metadata({"path": str(path), "rows": len(obj)})
        raise NotImplementedError

    def load_input(self, context: InputContext) -> pd.DataFrame:
        """Read a DataFrame from a Parquet file.

        Args:
            context: Input context with asset and partition metadata.

        Returns:
            The loaded DataFrame.

        Raises:
            FileNotFoundError: If the Parquet file doesn't exist.
        """
        # TODO: Implement input loading:
        #   1. Compute the file path
        #   2. Read and return pd.read_parquet(path)
        #   3. Log the path and row count
        raise NotImplementedError
