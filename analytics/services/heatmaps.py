from __future__ import annotations

import math
import statistics
from collections import defaultdict
from datetime import timedelta
from typing import Dict, List, Literal, Optional

from django.db.models import Count, Min, Max, Q

from ..models import Incident

HeatType = Literal["count", "z_daily", "pct_group", "weekday_delta"]


def calendar_heatmap_data(
    *,
    heat_type: HeatType = "count",
    group_filter: Optional[str] = None,
) -> Dict:
    """Return structured data for the GitHub-style calendar heatmap."""
    if not Incident.objects.exists():
        return {"heat_type": heat_type, "data": []}

    group_filter = (group_filter or "").strip()
    rows = list(
        Incident.objects.values("incident_date")
        .annotate(
            total=Count("id"),
            weekday=Min("day_of_week"),
            group_total=Count(
                "id",
                filter=Q(offense_category__icontains=group_filter)
                | Q(description__icontains=group_filter),
            ),
        )
        .order_by("incident_date")
    )

    start_date = rows[0]["incident_date"]
    totals = [row["total"] for row in rows]
    mean_total = statistics.mean(totals)
    std_total = statistics.pstdev(totals) if len(totals) > 1 else 0

    weekday_buckets: Dict[str, List[int]] = defaultdict(list)
    for row in rows:
        weekday_label = row["weekday"] or row["incident_date"].strftime("%a")
        weekday_buckets[weekday_label].append(row["total"])
    weekday_baseline = {
        label: (sum(values) / len(values)) if values else 0 for label, values in weekday_buckets.items()
    }

    weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    data_points = []
    max_week_index = 0
    for row in rows:
        weekday_label = row["weekday"] or row["incident_date"].strftime("%a")
        value = row["total"]
        if heat_type == "z_daily":
            value = 0 if std_total == 0 else round((row["total"] - mean_total) / std_total, 2)
        elif heat_type == "pct_group":
            value = 0 if row["total"] == 0 else round((row["group_total"] / row["total"]) * 100, 2)
        elif heat_type == "weekday_delta":
            baseline = weekday_baseline.get(weekday_label, 0)
            value = round(row["total"] - baseline, 2)

        week_index = (row["incident_date"] - start_date).days // 7
        weekday_number = row["incident_date"].weekday()
        max_week_index = max(max_week_index, week_index)
        data_points.append(
            {
                "date": row["incident_date"].isoformat(),
                "weekday": weekday_label,
                "weekday_number": weekday_number,
                "week_index": week_index,
                "count": row["total"],
                "value": value,
            }
        )

    return {
        "heat_type": heat_type,
        "group_filter": group_filter or None,
        "mean_total": mean_total,
        "std_total": std_total,
        "weekday_baseline": weekday_baseline,
        "weekday_order": weekday_order,
        "weeks": max_week_index + 1,
        "start_date": start_date.isoformat(),
        "end_date": rows[-1]["incident_date"].isoformat(),
        "data": data_points,
    }


def twenty_four_by_seven(window_key: str = "365d") -> Dict:
    """Return 24x7 heatmap payload leveraging segmentation service."""
    from .segmentation import get_hourly_matrix  # local import to avoid cycle

    matrix = get_hourly_matrix(window_key)
    return {
        "window": window_key,
        **matrix,
    }


def poisson_z_heatmap(
    *,
    window_length: int = 28,
    unit: Literal["beat", "district"] = "beat",
) -> Dict:
    """Return rolling window Poisson-style z-score heatmap data."""
    agg = Incident.objects.aggregate(
        min_date=Min("incident_date"),
        max_date=Max("incident_date"),
    )
    start_date = agg["min_date"]
    end_date = agg["max_date"]
    if not start_date or not end_date:
        return {"window_length_days": window_length, "unit": unit, "windows": []}

    delta = timedelta(days=window_length - 1)
    windows: List[Dict] = []
    current_start = start_date
    idx = 1
    unit_field = "beat" if unit == "beat" else "district"

    while current_start + delta <= end_date:
        current_end = current_start + delta
        previous_start = current_start - timedelta(days=window_length)
        previous_end = current_start - timedelta(days=1)
        if previous_start < start_date:
            current_start = current_end + timedelta(days=1)
            continue

        current_counts = {
            row[unit_field] or "Unknown": row["total"]
            for row in Incident.objects.filter(incident_date__range=(current_start, current_end))
            .values(unit_field)
            .annotate(total=Count("id"))
        }
        previous_counts = {
            row[unit_field] or "Unknown": row["total"]
            for row in Incident.objects.filter(incident_date__range=(previous_start, previous_end))
            .values(unit_field)
            .annotate(total=Count("id"))
        }

        rows_payload = []
        all_units = set(current_counts.keys()) | set(previous_counts.keys())
        for unit_value in sorted(all_units):
            curr = current_counts.get(unit_value, 0)
            prev = previous_counts.get(unit_value, 0)
            if prev <= 0:
                z = 0.0
            else:
                z = round((curr - prev) / math.sqrt(prev), 2)
            rows_payload.append(
                {
                    "unit": unit_value,
                    "current": curr,
                    "past": prev,
                    "z": z,
                }
            )

        windows.append(
            {
                "id": idx,
                "label": f"{current_start:%Y-%m-%d} to {current_end:%Y-%m-%d}",
                "start": current_start.isoformat(),
                "end": current_end.isoformat(),
                "previous_start": previous_start.isoformat(),
                "previous_end": previous_end.isoformat(),
                "rows": rows_payload,
            }
        )
        idx += 1
        current_start = current_end + timedelta(days=1)

    return {
        "window_length_days": window_length,
        "unit": unit,
        "windows": windows,
    }
