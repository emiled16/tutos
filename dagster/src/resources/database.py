"""Database resource for data access within the Dagster pipeline.

Provides a configurable database connection that can be injected
into assets and IO managers.
"""

from typing import Any

import pandas as pd
from dagster import ConfigurableResource


class DatabaseResource(ConfigurableResource):
    """Resource providing database connectivity for the ML pipeline.

    In this tutorial, the database is simulated. In production,
    this would wrap a real database connection pool (SQLAlchemy, asyncpg, etc.).

    Attributes:
        connection_string: Database connection URL.
    """

    connection_string: str = "sqlite:///./data/ml_pipeline.db"

    def query(self, sql: str, params: dict[str, Any] | None = None) -> pd.DataFrame:
        """Execute a SQL query and return results as a DataFrame.

        Args:
            sql: The SQL query string.
            params: Optional query parameters.

        Returns:
            Query results as a pandas DataFrame.
        """
        # TODO: Implement database query:
        #   - Use pd.read_sql(sql, connection_string, params=params)
        #   - Handle connection errors gracefully
        #   - For the tutorial, this can return a simulated DataFrame
        raise NotImplementedError

    def write(self, df: pd.DataFrame, table_name: str, if_exists: str = "replace") -> None:
        """Write a DataFrame to a database table.

        Args:
            df: The DataFrame to write.
            table_name: The target table name.
            if_exists: Behavior when table exists ("replace", "append", "fail").
        """
        # TODO: Implement database write:
        #   - Use df.to_sql(table_name, connection_string, if_exists=if_exists, index=False)
        #   - Handle connection errors gracefully
        raise NotImplementedError

    def health_check(self) -> bool:
        """Verify database connectivity.

        Returns:
            True if the database is reachable.
        """
        # TODO: Implement health check:
        #   - Attempt a simple query (SELECT 1)
        #   - Return True on success, False on failure
        raise NotImplementedError
