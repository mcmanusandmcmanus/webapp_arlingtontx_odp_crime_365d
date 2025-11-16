from __future__ import annotations

from collections import Counter
from typing import Dict, List, Optional, Tuple

from django.db.models import Count

from ..models import EvaluationMetric, Incident, ModelRun
from . import time_windows


def _window_for_key(window_key: str) -> Tuple[str, time_windows.Window]:
    windows = time_windows.get_time_windows()
    if window_key not in windows:
        # default to last 91 days if an unknown key is supplied
        window_key = "91d"
    return window_key, windows[window_key]


def get_eda_payload(
    *,
    window_key: str = "91d",
    top_categories: int = 8,
    max_beats: int = 10,
    max_districts: int = 6,
) -> Dict:
    """Return histogram and matrix payloads for the EDA workspace."""

    window_key, window = _window_for_key(window_key)
    queryset = Incident.objects.filter(incident_date__range=(window.start, window.end))

    hour_counts = [0] * 24
    for row in queryset.values("hour").annotate(total=Count("id")).order_by("hour"):
        hour = row["hour"] or 0
        if 0 <= hour < 24:
            hour_counts[hour] = row["total"]

    category_rows = list(
        queryset.values("offense_category")
        .annotate(total=Count("id"))
        .order_by("-total")[:top_categories]
    )
    category_labels = [
        row["offense_category"] or "Unknown" for row in category_rows
    ]
    category_counts = [row["total"] for row in category_rows]

    beat_rows = list(
        queryset.values("beat")
        .annotate(total=Count("id"))
        .order_by("-total")[:max_beats]
    )
    district_rows = list(
        queryset.values("district")
        .annotate(total=Count("id"))
        .order_by("-total")[:max_districts]
    )
    beats = [row["beat"] or "Unknown" for row in beat_rows]
    districts = [row["district"] or "Unknown" for row in district_rows]
    beat_set = set(beats)
    district_set = set(districts)

    matrix_cells = []
    raw_matrix = queryset.values("district", "beat").annotate(total=Count("id"))
    for row in raw_matrix:
        district_value = row["district"] or "Unknown"
        beat_value = row["beat"] or "Unknown"
        if district_value in district_set and beat_value in beat_set:
            matrix_cells.append(
                {
                    "x": beat_value,
                    "y": district_value,
                    "v": row["total"],
                }
            )

    return {
        "window_key": window_key,
        "window_label": window.label,
        "hours": {
            "labels": list(range(24)),
            "counts": hour_counts,
        },
        "offense_categories": {
            "labels": category_labels,
            "counts": category_counts,
        },
        "district_matrix": {
            "beats": beats,
            "districts": districts,
            "cells": matrix_cells,
        },
    }


def _score_from_metrics(metrics: Dict) -> float:
    for key in ("f1", "f1_score", "recall", "precision", "accuracy"):
        value = metrics.get(key)
        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
    return 0.0


def get_model_comparison(limit: int = 6) -> Dict:
    runs = list(ModelRun.objects.all()[:limit])
    if not runs:
        return {
            "runs": [],
            "chart": {"labels": [], "precision": [], "recall": [], "f1": []},
            "champion": None,
            "stage_breakdown": {},
        }

    chart_payload = {"labels": [], "precision": [], "recall": [], "f1": []}
    table_rows: List[Dict] = []
    champion = None
    champion_score = float("-inf")
    stage_counter: Counter = Counter()

    for run in runs:
        metrics = run.metrics or {}
        precision = metrics.get("precision")
        recall = metrics.get("recall")
        f1 = metrics.get("f1") or metrics.get("f1_score")

        row = {
            "model_name": run.model_name,
            "algorithm": run.algorithm,
            "stage": run.get_stage_display(),
            "run_id": run.run_id,
            "training_window": run.training_window,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "created_at": run.created_at,
        }
        table_rows.append(row)
        stage_counter.update([run.get_stage_display()])

        chart_payload["labels"].append(run.model_name)
        chart_payload["precision"].append(precision)
        chart_payload["recall"].append(recall)
        chart_payload["f1"].append(f1)

        score = _score_from_metrics(metrics)
        if score > champion_score:
            champion_score = score
            champion = row

    return {
        "runs": table_rows,
        "chart": chart_payload,
        "champion": champion,
        "stage_breakdown": dict(stage_counter),
    }


def _delta_pct(expected: Optional[float], observed: Optional[float]) -> float:
    if expected in (None, 0):
        return 0.0
    if observed is None:
        observed = 0.0
    return round(((observed - expected) / expected) * 100.0, 2)


def get_evaluation_payload(
    *,
    audience: Optional[str] = None,
    metric_name: Optional[str] = None,
    weeks: int = 12,
) -> Dict:
    queryset = EvaluationMetric.objects.all()
    audiences = list(
        EvaluationMetric.objects.order_by("audience")
        .values_list("audience", flat=True)
        .distinct()
    )
    metrics = list(
        EvaluationMetric.objects.order_by("metric_name")
        .values_list("metric_name", flat=True)
        .distinct()
    )

    if audience and audience in audiences:
        queryset = queryset.filter(audience=audience)
    if metric_name and metric_name in metrics:
        queryset = queryset.filter(metric_name=metric_name)

    records = list(queryset.order_by("-week_of")[:weeks])
    records.reverse()

    labels: List[str] = []
    expected_values: List[Optional[float]] = []
    observed_values: List[Optional[float]] = []
    delta_values: List[float] = []
    table_records: List[Dict] = []

    for record in records:
        labels.append(record.week_of.strftime("%Y-%m-%d"))
        expected_values.append(record.expected_value)
        observed_values.append(record.observed_value)
        delta = _delta_pct(record.expected_value, record.observed_value)
        delta_values.append(delta)
        table_records.append(
            {
                "week_of": record.week_of,
                "audience": record.audience,
                "metric_name": record.metric_name,
                "expected_value": record.expected_value,
                "observed_value": record.observed_value,
                "delta_pct": delta,
                "narrative": record.narrative,
            }
        )

    latest_delta = delta_values[-1] if delta_values else 0.0
    within_target = 0.0
    if delta_values:
        within_target = round(
            sum(1 for value in delta_values if abs(value) <= 10) / len(delta_values) * 100,
            1,
        )

    summary_text = "Awaiting evaluation metrics."
    if table_records:
        summary_text = (
            f"{within_target}% of the past {len(table_records)} evaluations were within ±10%."
            f" Latest delta: {latest_delta:+.1f}%."
        )

    return {
        "chart": {
            "labels": labels,
            "expected": expected_values,
            "observed": observed_values,
            "delta_pct": delta_values,
        },
        "records": table_records,
        "audiences": audiences,
        "metrics": metrics,
        "selected": {
            "audience": audience or "",
            "metric": metric_name or "",
        },
        "summary": {
            "text": summary_text,
            "latest_delta": latest_delta,
            "within_target": within_target,
        },
    }
