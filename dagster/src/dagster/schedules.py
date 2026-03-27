"""Schedule definitions for automatic pipeline execution.

Defines a daily schedule that materializes all assets
for the previous day's partition.
"""

import dagster as dg

from dagster.partitions import daily_partitions


@dg.schedule(
    cron_schedule="0 6 * * *",
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
    # TODO: Implement the schedule:
    #   1. Compute the previous day's partition key:
    #      partition_key = (context.scheduled_execution_time - timedelta(days=1)).strftime("%Y-%m-%d")
    #   2. Return a RunRequest with that partition_key:
    #      return dg.RunRequest(partition_key=partition_key)
    raise NotImplementedError
