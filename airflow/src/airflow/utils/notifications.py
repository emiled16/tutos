"""Notification helpers for Airflow task callbacks."""

from __future__ import annotations

import json
from typing import Any


def on_failure_callback(context: dict[str, Any]) -> None:
    """Callback triggered when a task fails.

    Sends a notification to Slack with task failure details.

    Args:
        context: Airflow context dictionary containing task instance,
                 execution date, exception info, etc.
    """
    # TODO: Implement failure notification.
    # Extract from context:
    # - task_instance = context["task_instance"]
    # - dag_id = context["dag"].dag_id
    # - task_id = task_instance.task_id
    # - execution_date = context["logical_date"]
    # - exception = context.get("exception", "Unknown error")
    # Format and send Slack message with _send_slack_notification()
    raise NotImplementedError


def on_success_callback(context: dict[str, Any]) -> None:
    """Callback triggered when a DAG run completes successfully.

    Sends a summary notification to Slack.

    Args:
        context: Airflow context dictionary.
    """
    # TODO: Implement success notification.
    raise NotImplementedError


def on_sla_miss_callback(
    dag: Any,
    task_list: str,
    blocking_task_list: str,
    slas: list,
    blocking_tis: list,
) -> None:
    """Callback triggered when tasks miss their SLA.

    Args:
        dag: The DAG object.
        task_list: Comma-separated list of tasks that missed SLA.
        blocking_task_list: Tasks blocking the SLA-missed tasks.
        slas: List of SLA objects.
        blocking_tis: Blocking task instances.
    """
    # TODO: Implement SLA miss notification.
    # - Format a warning message with dag_id, missed tasks, and SLA times
    # - Send via Slack and/or email
    raise NotImplementedError


def _send_slack_notification(
    message: str,
    channel: str = "#ml-pipeline-alerts",
    webhook_url: str | None = None,
) -> bool:
    """Send a notification to Slack via webhook.

    Args:
        message: The message text (supports Slack markdown).
        channel: Target Slack channel.
        webhook_url: Slack webhook URL. If None, reads from Airflow Variable.

    Returns:
        True if the message was sent successfully.
    """
    # TODO: Implement Slack webhook notification.
    # - Get webhook_url from Airflow Variable if not provided
    # - POST to webhook URL with JSON payload
    # - Return True on 200 response, False otherwise
    raise NotImplementedError


def _send_email_notification(
    subject: str,
    body: str,
    to_addresses: list[str],
) -> bool:
    """Send an email notification.

    Args:
        subject: Email subject line.
        body: Email body (HTML supported).
        to_addresses: List of recipient email addresses.

    Returns:
        True if the email was sent successfully.
    """
    # TODO: Implement email notification.
    # - Use Airflow's send_email utility or smtplib
    # - Read SMTP config from environment or Airflow Connection
    raise NotImplementedError
