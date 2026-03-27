"""Synthetic event log generator for testing process mining algorithms.

Generates event logs with configurable process patterns: sequences,
choices (XOR), parallelism (AND), loops, and noise injection.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from process_mining.event_log import Event, EventLog, Trace


@dataclass
class ActivityConfig:
    """Configuration for a single activity in the process.

    Attributes:
        name: Activity name.
        resources: Pool of resources that can perform this activity.
        min_duration: Minimum service time in seconds.
        max_duration: Maximum service time in seconds.
    """

    name: str
    resources: list[str] = field(default_factory=lambda: ["System"])
    min_duration: float = 60.0
    max_duration: float = 3600.0


@dataclass
class ProcessPattern:
    """A process pattern used to generate traces.

    Supports composition of patterns for building complex processes.
    """

    pass


@dataclass
class SequencePattern(ProcessPattern):
    """Execute activities in order.

    Attributes:
        activities: Ordered list of activity names or sub-patterns.
    """

    activities: list[str | ProcessPattern] = field(default_factory=list)


@dataclass
class ChoicePattern(ProcessPattern):
    """Execute exactly one branch (XOR split).

    Attributes:
        branches: List of alternative activity names or sub-patterns.
        probabilities: Optional probability for each branch (must sum to 1.0).
    """

    branches: list[str | ProcessPattern] = field(default_factory=list)
    probabilities: list[float] | None = None


@dataclass
class ParallelPattern(ProcessPattern):
    """Execute all branches concurrently (AND split, interleaved ordering).

    Attributes:
        branches: List of activity names or sub-patterns to execute in parallel.
    """

    branches: list[str | ProcessPattern] = field(default_factory=list)


@dataclass
class LoopPattern(ProcessPattern):
    """Repeat a body pattern with a configurable redo probability.

    Attributes:
        body: The main pattern to execute.
        redo: The redo pattern (executed before looping back).
        redo_probability: Probability of executing the redo and looping (0.0-1.0).
    """

    body: str | ProcessPattern = ""
    redo: str | ProcessPattern = ""
    redo_probability: float = 0.3


@dataclass
class LogGeneratorConfig:
    """Configuration for synthetic log generation.

    Attributes:
        process_pattern: The process structure to simulate.
        activity_configs: Performance configuration per activity.
        num_cases: Number of cases (traces) to generate.
        start_time: Timestamp for the first event.
        noise_probability: Probability of injecting noise into a trace (0.0-1.0).
        noise_types: Types of noise to inject ('swap', 'skip', 'insert').
        random_seed: Seed for reproducibility.
    """

    process_pattern: ProcessPattern = field(default_factory=SequencePattern)
    activity_configs: dict[str, ActivityConfig] = field(default_factory=dict)
    num_cases: int = 100
    start_time: datetime = field(default_factory=lambda: datetime(2024, 1, 1))
    noise_probability: float = 0.0
    noise_types: list[str] = field(default_factory=lambda: ["swap", "skip", "insert"])
    random_seed: int | None = None


def _generate_trace_activities(
    pattern: str | ProcessPattern,
    rng: random.Random,
) -> list[str]:
    """Recursively generate a list of activities from a process pattern.

    Resolves sequences, choices, parallelism, and loops into a flat
    activity list representing one execution of the process.

    Args:
        pattern: Process pattern (or activity name string) to generate from.
        rng: Random number generator for stochastic choices.

    Returns:
        Ordered list of activity names.
    """
    # TODO: Implement recursive trace generation
    # If pattern is a string: return [pattern]
    # If SequencePattern: concatenate generated activities for each element
    # If ChoicePattern: pick one branch based on probabilities, generate from it
    # If ParallelPattern: generate from each branch, shuffle/interleave the results
    # If LoopPattern: generate body, then with redo_probability, generate redo and loop
    raise NotImplementedError


def _inject_noise(
    activities: list[str],
    noise_types: list[str],
    rng: random.Random,
    all_activities: list[str],
) -> list[str]:
    """Inject noise into a trace's activity list.

    Noise types:
    - 'swap': Swap two adjacent activities
    - 'skip': Remove a random activity
    - 'insert': Insert a random activity at a random position

    Args:
        activities: Original activity list.
        noise_types: Types of noise to potentially apply.
        rng: Random number generator.
        all_activities: Pool of all possible activities (for insertion).

    Returns:
        Modified activity list with noise injected.
    """
    # TODO: Implement noise injection
    # Pick a random noise type
    # Apply the corresponding transformation
    raise NotImplementedError


def generate_event_log(config: LogGeneratorConfig) -> EventLog:
    """Generate a synthetic event log from a process configuration.

    Args:
        config: Generator configuration specifying process structure,
                activity properties, number of cases, and noise settings.

    Returns:
        Generated EventLog with synthetic traces.
    """
    # TODO: Implement synthetic log generation
    # 1. Initialize RNG with config.random_seed
    # 2. For each case (0..num_cases):
    #    a. Generate activity list from process pattern
    #    b. Optionally inject noise (with config.noise_probability)
    #    c. Generate timestamps by accumulating random durations from activity configs
    #    d. Assign random resources from activity configs
    #    e. Create Event objects and build Trace
    # 3. Return EventLog with all traces
    raise NotImplementedError


def generate_simple_sequential_log(
    activities: list[str],
    num_cases: int = 50,
    seed: int | None = None,
) -> EventLog:
    """Convenience function to generate a simple sequential process log.

    Args:
        activities: Ordered list of activity names (e.g., ['A', 'B', 'C']).
        num_cases: Number of cases to generate.
        seed: Random seed for reproducibility.

    Returns:
        EventLog with all traces following the same activity sequence.
    """
    # TODO: Implement simple sequential log generation
    # Create a SequencePattern from activities, use default ActivityConfigs
    raise NotImplementedError


def generate_xor_choice_log(
    before: list[str],
    branches: list[list[str]],
    after: list[str],
    num_cases: int = 100,
    seed: int | None = None,
) -> EventLog:
    """Generate a log with an XOR choice pattern.

    Pattern: before -> (branch1 | branch2 | ...) -> after

    Args:
        before: Activities before the choice.
        branches: List of alternative activity sequences.
        after: Activities after the choice.
        num_cases: Number of cases to generate.
        seed: Random seed.

    Returns:
        EventLog with XOR choice traces.
    """
    # TODO: Implement XOR choice log generation
    raise NotImplementedError


def generate_parallel_log(
    before: list[str],
    parallel_activities: list[str],
    after: list[str],
    num_cases: int = 100,
    seed: int | None = None,
) -> EventLog:
    """Generate a log with parallel (AND) activities.

    Pattern: before -> (act1 AND act2 AND ...) -> after

    Args:
        before: Activities before the parallel block.
        parallel_activities: Activities to execute concurrently.
        after: Activities after the parallel block.
        num_cases: Number of cases to generate.
        seed: Random seed.

    Returns:
        EventLog with interleaved parallel activity traces.
    """
    # TODO: Implement parallel log generation
    raise NotImplementedError
