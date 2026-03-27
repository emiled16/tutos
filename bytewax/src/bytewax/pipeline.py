"""Main Bytewax dataflow definition for the real-time feature pipeline.

Assembles the complete dataflow from source → transforms → sink,
composing all the building blocks defined in other modules.
"""

from pathlib import Path

import bytewax.operators as op
from bytewax.dataflow import Dataflow

from bytewax.models import ClickEvent, SessionFeatures
from bytewax.sinks import FeatureStoreSink, FileSink, StdoutSink
from bytewax.sources import FileReplaySource
from bytewax.transforms import (
    compute_engagement_score,
    filter_short_sessions,
    key_by_user,
    parse_event,
    sessionize,
)
from bytewax.windows import get_event_clock, session_window


def build_pipeline(
    input_dir: Path,
    output_dir: Path | None = None,
    sink_type: str = "stdout",
) -> Dataflow:
    """Build the complete feature engineering dataflow.

    Assembles a Bytewax dataflow that:
    1. Reads clickstream events from JSONL files
    2. Parses and validates events
    3. Keys events by user_id
    4. Applies session windowing with 30-minute gaps
    5. Computes session features
    6. Outputs features to the configured sink

    Args:
        input_dir: Directory containing input JSONL files.
        output_dir: Directory for file output (required if sink_type is "file").
        sink_type: One of "stdout", "file", or "feature_store".

    Returns:
        A configured Bytewax Dataflow ready to be run.
    """
    flow = Dataflow("feature_pipeline")

    # TODO: Step 1 — Add input source using FileReplaySource
    #   source_stream = op.input("input", flow, FileReplaySource(input_dir))

    # TODO: Step 2 — Parse raw JSON into ClickEvent, filtering out None values
    #   parsed = op.filter_map("parse", source_stream, parse_event)

    # TODO: Step 3 — Key events by user_id
    #   keyed = op.map("key_by_user", parsed, key_by_user)

    # TODO: Step 4 — Apply session window and sessionize
    #   Use stateful_map with the sessionize function and session_window
    #   to group events into sessions and compute features

    # TODO: Step 5 — Compute engagement scores for each session
    #   enriched = op.map("engagement", sessions, ...)

    # TODO: Step 6 — Filter out short/trivial sessions
    #   filtered = op.filter("filter_short", enriched, filter_short_sessions)

    # TODO: Step 7 — Add output sink based on sink_type
    #   if sink_type == "stdout":
    #       op.output("output", filtered, StdoutSink())
    #   elif sink_type == "file":
    #       op.output("output", filtered, FileSink(output_dir))
    #   elif sink_type == "feature_store":
    #       op.output("output", filtered, FeatureStoreSink())

    return flow


def run_pipeline(input_dir: str, output_dir: str | None = None, sink: str = "stdout") -> None:
    """Build and run the feature pipeline.

    Args:
        input_dir: Path to the directory containing input JSONL files.
        output_dir: Path to the output directory (for file sink).
        sink: The sink type to use ("stdout", "file", or "feature_store").
    """
    # TODO: Implement — build the pipeline and run it using bytewax.run.cli_main
    #   from bytewax.run import cli_main
    #   flow = build_pipeline(Path(input_dir), Path(output_dir) if output_dir else None, sink)
    #   cli_main(flow)
    raise NotImplementedError


if __name__ == "__main__":
    import sys

    input_path = sys.argv[1] if len(sys.argv) > 1 else "./data"
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    sink_type = sys.argv[3] if len(sys.argv) > 3 else "stdout"

    run_pipeline(input_path, output_path, sink_type)
