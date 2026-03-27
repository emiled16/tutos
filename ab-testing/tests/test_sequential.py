"""Tests for sequential testing (SPRT)."""

from __future__ import annotations

import numpy as np
import pytest

from ab_testing.sequential import SPRTDecision, SPRTResult, SequentialTester


class TestSPRTInitialization:
    """Tests for SPRT initialization and boundary computation."""

    def test_boundaries_with_default_params(self) -> None:
        """Verify boundary values with alpha=0.05, beta=0.20."""
        # TODO: Implement test.
        # upper = log((1 - 0.20) / 0.05) = log(16) ≈ 2.773
        # lower = log(0.20 / (1 - 0.05)) = log(0.2105) ≈ -1.558
        raise NotImplementedError

    def test_raises_on_equal_hypotheses(self) -> None:
        """Should raise ValueError when p0 == p1."""
        # TODO: Implement test.
        raise NotImplementedError

    def test_raises_on_invalid_probabilities(self) -> None:
        """Should raise ValueError for p0 or p1 outside (0, 1)."""
        # TODO: Implement test.
        raise NotImplementedError


class TestSPRTUpdate:
    """Tests for processing observations."""

    def test_single_observation_continues(self) -> None:
        """A single observation should almost always result in CONTINUE."""
        # TODO: Implement test.
        raise NotImplementedError

    def test_strong_evidence_rejects_null(self) -> None:
        """Consistent positive observations should eventually reject H0."""
        # TODO: Implement test with many 1s when p1 > p0.
        raise NotImplementedError

    def test_strong_evidence_accepts_null(self) -> None:
        """Consistent negative observations should eventually accept H0."""
        # TODO: Implement test with many 0s when p1 > p0.
        raise NotImplementedError


class TestSPRTBatch:
    """Tests for batch observation processing."""

    def test_batch_matches_sequential(self) -> None:
        """Batch processing should give the same result as sequential."""
        # TODO: Implement test by comparing update_batch with loop of update calls.
        raise NotImplementedError

    def test_early_stopping_in_batch(self) -> None:
        """Batch should stop early when a boundary is crossed mid-batch."""
        # TODO: Implement test verifying that not all observations are processed.
        raise NotImplementedError


class TestSPRTResult:
    """Tests for result generation."""

    def test_result_has_correct_observation_count(self) -> None:
        """Result should report the correct number of processed observations."""
        # TODO: Implement test.
        raise NotImplementedError

    def test_history_length_matches_observations(self) -> None:
        """History list length should equal the number of observations processed."""
        # TODO: Implement test.
        raise NotImplementedError

    def test_reset_clears_state(self) -> None:
        """After reset, the tester should be in its initial state."""
        # TODO: Implement test: process some data, reset, verify clean state.
        raise NotImplementedError
