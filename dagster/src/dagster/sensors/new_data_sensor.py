"""Sensor that watches for new data files and triggers pipeline runs.

Monitors a directory for new CSV/Parquet files and creates
RunRequests for each detected file.
"""

from pathlib import Path

import dagster as dg


@dg.sensor(
    description="Monitors for new data files and triggers ingestion pipeline.",
    minimum_interval_seconds=30,
)
def new_data_sensor(context: dg.SensorEvaluationContext) -> dg.SensorResult:
    """Check for new data files and trigger pipeline runs.

    Uses a cursor to track which files have already been processed,
    preventing duplicate runs for the same file.

    Args:
        context: Sensor evaluation context with cursor state.

    Returns:
        A SensorResult with RunRequests for each new file detected.
    """
    data_dir = Path("./data/incoming")

    # TODO: Implement the sensor logic:
    #   1. Load the cursor (last processed timestamp or set of processed files)
    #      last_processed = context.cursor or ""
    #
    #   2. Scan data_dir for new .csv or .parquet files
    #      new_files = [f for f in data_dir.glob("*.csv") if f.name > last_processed]
    #
    #   3. For each new file, create a RunRequest:
    #      run_requests = []
    #      for file in sorted(new_files):
    #          run_requests.append(
    #              dg.RunRequest(
    #                  run_key=file.name,
    #                  run_config={"ops": {"raw_data": {"config": {"file_path": str(file)}}}},
    #              )
    #          )
    #
    #   4. Update the cursor to the latest processed file
    #      new_cursor = sorted(new_files)[-1].name if new_files else last_processed
    #
    #   5. Return SensorResult with run_requests and cursor
    #      return dg.SensorResult(run_requests=run_requests, cursor=new_cursor)
    raise NotImplementedError
