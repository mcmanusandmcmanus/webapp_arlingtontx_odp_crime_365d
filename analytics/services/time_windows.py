from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict, Iterable, Optional

from django.db.models import Max, QuerySet
from django.utils import timezone

from ..models import Incident


WINDOW_DEFINITIONS = OrderedDict(
    [
        ("7d", 7),
        ("14d", 14),
        ("28d", 28),
        ("91d", 91),
        ("182d", 182),
        ("365d", 365),
    ]
)


@dataclass
class Window:
    key: str
    label: str
    days: int
    start: date
    end: date

    @property
    def previous_start(self) -> date:
        return self.start - timedelta(days=self.days)

    @property
    def previous_end(self) -> date:
        return self.start - timedelta(days=1)


def _resolve_reference_date(reference_date: Optional[date] = None) -> date:
    if reference_date:
        return reference_date
    max_date = (
        Incident.objects.aggregate(max_date=Max("incident_date")).get("max_date")
    )
    if max_date:
        return max_date
    return timezone.localdate()


def get_time_windows(reference_date: Optional[date] = None) -> Dict[str, Window]:
    """Return dictionary of window metadata keyed by shorthand (7d, 14d, etc.)."""
    ref_date = _resolve_reference_date(reference_date)
    windows: Dict[str, Window] = {}
    for key, days in WINDOW_DEFINITIONS.items():
        start = ref_date - timedelta(days=days - 1)
        windows[key] = Window(
            key=key,
            label=f"Last {days} days",
            days=days,
            start=start,
            end=ref_date,
        )
    return windows


def safe_pct_change(current: int, previous: int) -> float:
    if previous == 0:
        return 0.0 if current == 0 else 100.0
    return round(((current - previous) / previous) * 100.0, 2)


def compute_window_counts(
    queryset: Optional[QuerySet] = None, reference_date: Optional[date] = None
) -> Dict[str, Dict[str, float]]:
    """Return current vs previous counts for each standard window."""
    qs = queryset or Incident.objects.all()
    window_meta = get_time_windows(reference_date)
    results: Dict[str, Dict[str, float]] = {}
    for key, window in window_meta.items():
        current_total = qs.filter(
            incident_date__range=(window.start, window.end)
        ).count()
        previous_total = qs.filter(
            incident_date__range=(window.previous_start, window.previous_end)
        ).count()
        results[key] = {
            "label": window.label,
            "current": current_total,
            "previous": previous_total,
            "absolute_change": current_total - previous_total,
            "percent_change": safe_pct_change(current_total, previous_total),
            "start": window.start,
            "end": window.end,
            "previous_start": window.previous_start,
            "previous_end": window.previous_end,
        }
    return results


def summarize_windows_for_chart(window_keys: Iterable[str]) -> Dict[str, list]:
    """Shape summary data for Chart.js stacked/clustered bars."""
    summary = compute_window_counts()
    labels, current, previous = [], [], []
    for key in window_keys:
        if key not in summary:
            continue
        labels.append(key.upper())
        current.append(summary[key]["current"])
        previous.append(summary[key]["previous"])
    return {
        "labels": labels,
        "current": current,
        "previous": previous,
    }
