"""Partition definitions for the ML pipeline.

Defines daily partitions for incremental data processing.
"""

import dagster as dg

daily_partitions = dg.DailyPartitionsDefinition(
    start_date="2024-01-01",
    timezone="UTC",
)
"""Daily partitions starting from January 1, 2024.

Each partition key is a date string in "YYYY-MM-DD" format.
Assets using this partition process one day of data per materialization.
"""
