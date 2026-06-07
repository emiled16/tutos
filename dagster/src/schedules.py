"""Schedule definitions for automatic pipeline execution.

Defines a daily schedule that materializes all assets
for the previous day's partition.
"""

from datetime import timedelta

import dagster as dg

from partitions import daily_partitions


@dg.schedule(
    cron_schedule="0 6 * * *",
    target=dg.AssetSelection.all(),
    description="Daily retraining schedule - runs at 6 AM UTC for the previous day's data.",
)
def daily_training_schedule(context: dg.ScheduleEvaluationContext) -> dg.RunRequest:
    """Generate a RunRequest for the previous day's partition.

    Triggers a full pipeline run (ingestion → features → training → evaluation)
    for the most recent complete day of data.

    Args:
        context: Schedule evaluation context with timing info.

    Returns:
        A RunRequest targeting the previous day's partition.
    """
    execution_time = context.scheduled_execution_time
    if execution_time is None:
        return dg.SkipReason("No scheduled execution time available.")

    partition_key = (execution_time - timedelta(days=1)).strftime("%Y-%m-%d")
    if not daily_partitions.has_partition_key(partition_key):
        return dg.SkipReason(f"Partition {partition_key} is outside partition bounds.")

    return dg.RunRequest(partition_key=partition_key)
