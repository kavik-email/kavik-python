"""Bulk job polling helper."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Callable, Optional

from .errors import KavikError

if TYPE_CHECKING:
    from .models import BulkJob, KavikResponse


def poll_bulk_job(
    getter: Callable[[str], KavikResponse[BulkJob]],
    job_id: str,
    interval: float = 5.0,
    timeout: float = 600.0,
    on_progress: Optional[Callable[[BulkJob], None]] = None,
) -> KavikResponse[BulkJob]:
    """Poll a bulk job until it reaches a terminal state.

    Args:
        getter: Function that fetches a bulk job by ID.
        job_id: The bulk job ID to poll.
        interval: Seconds between polls (default: 5).
        timeout: Maximum total wait time in seconds (default: 600).
        on_progress: Called after each poll with the current job state.

    Returns:
        The final job state (completed or failed).

    Raises:
        KavikError: If the job does not complete within the timeout.
    """
    start = time.monotonic()

    while time.monotonic() - start < timeout:
        result = getter(job_id)

        if on_progress is not None:
            on_progress(result.data)

        if result.data.status in ("completed", "failed"):
            return result

        time.sleep(interval)

    raise KavikError(
        f"Bulk job {job_id} did not complete within {timeout}s",
        code="INTERNAL_ERROR",
        status=0,
    )
