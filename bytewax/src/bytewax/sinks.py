"""Output sinks for the Bytewax feature pipeline.

Provides sinks for writing computed features to various destinations:
stdout, files, and a simulated feature store.
"""

from pathlib import Path
from typing import Any

from bytewax.outputs import DynamicSink, StatelessSinkPartition

from bytewax.models import SessionFeatures


class StdoutSinkPartition(StatelessSinkPartition[SessionFeatures]):
    """Sink partition that prints session features to stdout."""

    def write_batch(self, batch: list[SessionFeatures]) -> None:
        """Write a batch of session features to stdout.

        Args:
            batch: List of computed session features to print.
        """
        # TODO: Implement — iterate over batch and print each SessionFeatures
        #       in a human-readable format (consider using model_dump_json)
        raise NotImplementedError


class StdoutSink(DynamicSink[SessionFeatures]):
    """Sink that writes session features to stdout for debugging."""

    def build(self, step_id: str, worker_index: int, worker_count: int) -> StdoutSinkPartition:
        """Build a stdout sink partition.

        Args:
            step_id: The dataflow step identifier.
            worker_index: Index of this worker.
            worker_count: Total number of workers.

        Returns:
            A StdoutSinkPartition instance.
        """
        # TODO: Implement — return a StdoutSinkPartition
        raise NotImplementedError


class FileSinkPartition(StatelessSinkPartition[SessionFeatures]):
    """Sink partition that writes session features to a JSONL file."""

    def __init__(self, output_path: Path, worker_index: int) -> None:
        """Initialize the file sink partition.

        Args:
            output_path: Directory to write output files to.
            worker_index: Worker index for naming the output file.
        """
        self._output_path = output_path
        self._worker_index = worker_index
        # TODO: Open an output file for writing (e.g., features_worker_{worker_index}.jsonl)

    def write_batch(self, batch: list[SessionFeatures]) -> None:
        """Write a batch of session features to the output file as JSONL.

        Args:
            batch: List of computed session features to write.
        """
        # TODO: Implement — serialize each SessionFeatures to JSON and write
        #       one per line, flush after each batch
        raise NotImplementedError

    def close(self) -> None:
        """Close the output file handle."""
        # TODO: Implement — close the file handle
        raise NotImplementedError


class FileSink(DynamicSink[SessionFeatures]):
    """Sink that writes session features to JSONL files."""

    def __init__(self, output_dir: Path) -> None:
        """Initialize the file sink.

        Args:
            output_dir: Directory to write output files to.
        """
        self._output_dir = output_dir

    def build(self, step_id: str, worker_index: int, worker_count: int) -> FileSinkPartition:
        """Build a file sink partition for this worker.

        Args:
            step_id: The dataflow step identifier.
            worker_index: Index of this worker.
            worker_count: Total number of workers.

        Returns:
            A FileSinkPartition instance.
        """
        # TODO: Implement — ensure output_dir exists, return a FileSinkPartition
        raise NotImplementedError


class FeatureStoreSinkPartition(StatelessSinkPartition[SessionFeatures]):
    """Sink partition that writes features to a simulated feature store.

    The feature store is implemented as an in-memory dict keyed by
    (user_id, session_start) for simplicity.
    """

    def __init__(self, store: dict[tuple[str, str], dict[str, Any]]) -> None:
        """Initialize with a reference to the shared feature store.

        Args:
            store: The dictionary acting as the feature store.
        """
        self._store = store

    def write_batch(self, batch: list[SessionFeatures]) -> None:
        """Write computed features to the feature store.

        Args:
            batch: List of computed session features to store.
        """
        # TODO: Implement — for each feature, create a key of (user_id, session_start)
        #       and store the feature dict in self._store
        raise NotImplementedError


class FeatureStoreSink(DynamicSink[SessionFeatures]):
    """Sink that writes session features to a simulated in-memory feature store."""

    def __init__(self) -> None:
        self.store: dict[tuple[str, str], dict[str, Any]] = {}

    def build(self, step_id: str, worker_index: int, worker_count: int) -> FeatureStoreSinkPartition:
        """Build a feature store sink partition.

        Args:
            step_id: The dataflow step identifier.
            worker_index: Index of this worker.
            worker_count: Total number of workers.

        Returns:
            A FeatureStoreSinkPartition instance.
        """
        # TODO: Implement — return a FeatureStoreSinkPartition with self.store
        raise NotImplementedError
