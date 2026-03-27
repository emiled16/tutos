"""Report generation for A/B test results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy import stats as sp_stats

from ab_testing.bayesian import BayesianResult
from ab_testing.experiment import Experiment
from ab_testing.statistics import TestResult


class ABTestReporter:
    """Generates HTML and JSON reports for A/B test experiments.

    The reporter takes experiment data and statistical results, then produces
    formatted reports with visualizations of distributions, confidence intervals,
    and time series of key metrics.
    """

    def __init__(self, experiment: Experiment) -> None:
        self.experiment = experiment
        self._figures: list[go.Figure] = []

    def plot_distributions(
        self,
        control_data: np.ndarray,
        treatment_data: np.ndarray,
    ) -> go.Figure:
        """Create a histogram/KDE plot comparing control and treatment distributions.

        Args:
            control_data: Observations from the control group.
            treatment_data: Observations from the treatment group.

        Returns:
            Plotly Figure with overlaid distributions.
        """
        # TODO: Implement distribution comparison plot.
        # - Create overlaid histograms for both groups
        # - Add vertical lines for means
        # - Add legend and title
        raise NotImplementedError

    def plot_confidence_intervals(
        self, results: list[TestResult]
    ) -> go.Figure:
        """Create a forest plot of confidence intervals for each metric.

        Args:
            results: List of TestResult objects from different metrics.

        Returns:
            Plotly Figure with confidence interval visualization.
        """
        # TODO: Implement forest plot.
        # - For each result, draw a horizontal line from CI lower to CI upper
        # - Add a point at the estimated difference
        # - Add a vertical dashed line at 0 (no effect)
        raise NotImplementedError

    def plot_bayesian_posteriors(
        self,
        posterior_a: tuple[float, float],
        posterior_b: tuple[float, float],
    ) -> go.Figure:
        """Plot the posterior Beta distributions for both variants.

        Args:
            posterior_a: (alpha, beta) parameters for control posterior.
            posterior_b: (alpha, beta) parameters for treatment posterior.

        Returns:
            Plotly Figure with overlaid posterior distributions.
        """
        # TODO: Implement posterior distribution plot.
        # - Generate x values from 0 to 1
        # - Compute Beta PDF for both posteriors
        # - Plot as filled area charts
        # - Add shaded credible intervals
        raise NotImplementedError

    def generate_json_report(
        self,
        frequentist_result: TestResult | None = None,
        bayesian_result: BayesianResult | None = None,
    ) -> dict[str, Any]:
        """Generate a JSON-serializable report dictionary.

        Args:
            frequentist_result: Result from frequentist analysis.
            bayesian_result: Result from Bayesian analysis.

        Returns:
            Dictionary containing experiment summary, statistical results,
            and metadata.
        """
        # TODO: Implement JSON report generation.
        # Include:
        # - experiment summary (name, status, durations, sample sizes)
        # - frequentist results (if provided): test name, p-value, CI, effect size
        # - bayesian results (if provided): prob_b_beats_a, expected losses, credible intervals
        # - metadata: timestamp, analysis parameters
        raise NotImplementedError

    def generate_html_report(
        self,
        frequentist_result: TestResult | None = None,
        bayesian_result: BayesianResult | None = None,
        output_path: Path | None = None,
    ) -> str:
        """Generate a complete HTML report with embedded visualizations.

        Args:
            frequentist_result: Result from frequentist analysis.
            bayesian_result: Result from Bayesian analysis.
            output_path: File path to save the HTML report. If None, returns HTML string.

        Returns:
            HTML string of the complete report.
        """
        # TODO: Implement HTML report generation.
        # - Build HTML template with CSS styling
        # - Embed experiment summary table
        # - Embed statistical results
        # - Embed Plotly figures as interactive charts
        # - Save to file if output_path is provided
        raise NotImplementedError
