from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List

from django.db.models import Count, F
from django.db.models.functions import ExtractHour, ExtractWeekDay

from ..models import Incident
from . import time_windows

SEGMENT_FIELD_MAP = {
    "beat": "beat",
    "district": "district",
    "offense_category": "offense_category",
    "day_of_week": "day_of_week",
    "time_of_day_label": "time_of_day_label",
}

DEFAULT_WEEKDAY_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _resolve_segment_field(segment_key: str) -> str:
    if segment_key not in SEGMENT_FIELD_MAP:
        raise ValueError(f"Unsupported segment field: {segment_key}")
    return SEGMENT_FIELD_MAP[segment_key]


def get_segment_summary(
    *,
    window_key: str = "28d",
    segment_key: str = "beat",
    top_n: int = 10,
) -> Dict[str, List[Dict]]:
    """Return top segments for the selected window plus change vs previous window."""
    windows = time_windows.get_time_windows()
    if window_key not in windows:
        raise ValueError(f"Unknown window: {window_key}")
    window = windows[window_key]
    field_name = _resolve_segment_field(segment_key)

    current_qs = Incident.objects.filter(
        incident_date__range=(window.start, window.end)
    )
    aggregated = (
        current_qs.values(field_name)
        .annotate(current_count=Count("id"))
        .order_by("-current_count")
    )
    aggregated = list(aggregated[:top_n])
    total_current = sum(item["current_count"] for item in aggregated) or 1
    previous_counts = defaultdict(int)
    previous_rows = (
        Incident.objects.filter(
            incident_date__range=(window.previous_start, window.previous_end)
        )
        .values(field_name)
        .annotate(previous_count=Count("id"))
    )
    for row in previous_rows:
        segment_value = row[field_name] or "Unknown"
        previous_counts[segment_value] = row["previous_count"]

    rows: List[Dict] = []
    for item in aggregated:
        segment_value = item[field_name] or "Unknown"
        previous_total = previous_counts[segment_value]
        rows.append(
            {
                "segment": segment_value,
                "current_count": item["current_count"],
                "previous_count": previous_total,
                "pct_change": time_windows.safe_pct_change(
                    item["current_count"], previous_total
                ),
                "share": round(item["current_count"] / total_current * 100, 1),
            }
        )

    return {
        "window": window,
        "segment_key": segment_key,
        "rows": rows,
    }


def get_calendar_heatmap(window_key: str = "365d") -> Dict[str, int]:
    """Returns {date_iso: total_incidents} for the requested window."""
    windows = time_windows.get_time_windows()
    window = windows[window_key]
    qs = Incident.objects.filter(incident_date__range=(window.start, window.end))
    return {
        row["incident_date"].isoformat(): row["total"]
        for row in qs.values("incident_date").annotate(total=Count("id"))
    }


def get_hourly_matrix(window_key: str = "28d") -> Dict[str, Iterable]:
    """Return 24x7 matrix for heatmap visualizations."""
    windows = time_windows.get_time_windows()
    window = windows[window_key]
    qs = Incident.objects.filter(incident_date__range=(window.start, window.end))
    rows = (
        qs.annotate(
            annotated_hour=ExtractHour("incident_datetime"),
            annotated_weekday=ExtractWeekDay("incident_datetime"),
        )
        .values("annotated_hour", "annotated_weekday")
        .annotate(total=Count("id"))
    )
    matrix = [[0 for _ in range(24)] for _ in range(7)]
    for row in rows:
        hour = row["annotated_hour"] or 0
        weekday_index = ((row["annotated_weekday"] or 1) + 5) % 7  # Convert Sunday=1 to Monday=0 ordering
        matrix[weekday_index][hour] = row["total"]
    return {
        "weekday_labels": DEFAULT_WEEKDAY_ORDER,
        "hour_labels": list(range(24)),
        "matrix": matrix,
    }
