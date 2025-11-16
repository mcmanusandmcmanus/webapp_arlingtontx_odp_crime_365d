from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict

from django.conf import settings
from django.contrib import messages
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from . import forms
from .models import EvaluationMetric, Incident, ModelRun
from .services import baseline, segmentation, time_windows

ENTRY_SESSION_KEY = "entry_passcode_verified"
LAB_SESSION_KEY = "lab_passcode_verified"
IMPORT_SESSION_KEY = "import_passcode_verified"

LAB_STAGES = [
    {
        "slug": "eda",
        "title": "Stage 1: Exploratory Data Analysis",
        "description": "Univariate and bivariate summaries, scatterplots, boxplots, histograms.",
        "deliverables": [
            "Distribution cards for the 7→365-day horizons",
            "Calendar heatmap describing temporal cadence",
            "Auto-detected anomalies & narrative callouts",
        ],
    },
    {
        "slug": "feature-lab",
        "title": "Stage 2: Feature Engineering Lab",
        "description": "Derive high-signal predictors (24x7 matrix, lag deltas, segmentation interactions).",
        "deliverables": [
            "Feature catalog with importance ranking",
            "Pattern indicators describing beat-level surges",
        ],
    },
    {
        "slug": "modeling",
        "title": "Stage 3: Modeling & Validation",
        "description": "Multiple algorithms with train/validate/test splits plus cross-validation.",
        "deliverables": [
            "Model comparison table with precision/recall/F1/accuracy",
            "Hyper-parameter tuning summary",
            "Champion vs challenger tracking",
        ],
    },
    {
        "slug": "evaluation",
        "title": "Stage 4: Weekly Evaluation Loop",
        "description": "Compare forecasts vs observed and publish narrative scorecards.",
        "deliverables": [
            "Executive-ready evaluation briefs",
            "Automated alerts when metrics drift",
        ],
    },
]


def _require_entry_access(request: HttpRequest) -> HttpResponse | None:
    if not request.session.get(ENTRY_SESSION_KEY):
        return redirect("analytics:entry_gate")
    return None


def entry_gate(request: HttpRequest) -> HttpResponse:
    form = forms.PasscodeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["passcode"] == settings.ENTRY_PASSCODE:
            request.session[ENTRY_SESSION_KEY] = True
            messages.success(request, "Entry passcode accepted. Welcome to the COO experience.")
            return redirect("analytics:dashboard_overview")
        messages.error(request, "Invalid entry passcode.")
    return render(
        request,
        "analytics/entry_gate.html",
        {"form": form, "page_title": "COO Access Gate"},
    )


def dashboard_overview(request: HttpRequest) -> HttpResponse:
    gate = _require_entry_access(request)
    if gate:
        return gate
    window_keys = ["7d", "14d", "28d", "91d", "182d", "365d"]
    window_summary = time_windows.compute_window_counts()
    chart_payload = time_windows.summarize_windows_for_chart(window_keys)
    kpi_cards = baseline.build_kpi_cards()
    context = {
        "page_title": "Executive Overview",
        "window_summary": window_summary,
        "chart_payload": json.dumps(chart_payload),
        "kpi_cards": kpi_cards,
        "calendar_payload": json.dumps(segmentation.get_calendar_heatmap("365d")),
        "hourly_matrix": json.dumps(segmentation.get_hourly_matrix("28d")),
    }
    return render(request, "analytics/dashboard_overview.html", context)


def dashboard_segments(request: HttpRequest) -> HttpResponse:
    gate = _require_entry_access(request)
    if gate:
        return gate
    form = forms.SegmentFilterForm(request.GET or None)
    if form.is_valid():
        window_key = form.cleaned_data["window"]
        segment_key = form.cleaned_data["segment_field"]
    else:
        window_key = "28d"
        segment_key = "beat"
    summary = segmentation.get_segment_summary(window_key=window_key, segment_key=segment_key)
    context = {
        "page_title": "Segments & Storytelling",
        "form": form,
        "summary": summary,
        "table_rows": summary["rows"],
        "segment_key": segment_key,
        "bar_payload": json.dumps(
            {
                "labels": [row["segment"] for row in summary["rows"]],
                "current": [row["current_count"] for row in summary["rows"]],
                "previous": [row["previous_count"] for row in summary["rows"]],
            }
        ),
    }
    return render(request, "analytics/dashboard_segments.html", context)


def dashboard_detail(request: HttpRequest, segment_type: str, segment_value: str) -> HttpResponse:
    gate = _require_entry_access(request)
    if gate:
        return gate
    if segment_type not in segmentation.SEGMENT_FIELD_MAP:
        messages.error(request, "Unsupported segment.")
        return redirect("analytics:dashboard_segments")
    field_name = segmentation.SEGMENT_FIELD_MAP[segment_type]
    filter_kwargs = {field_name: segment_value}
    qs = Incident.objects.filter(**filter_kwargs)
    if not qs.exists():
        messages.warning(request, "No incidents found for that segment.")
        return redirect("analytics:dashboard_segments")
    series_window = time_windows.get_time_windows()["365d"]
    series = (
        qs.filter(incident_date__range=(series_window.start, series_window.end))
        .values("incident_date")
        .annotate(total=Count("id"))
        .order_by("incident_date")
    )
    window_cards = baseline.build_kpi_cards(
        window_keys=time_windows.WINDOW_DEFINITIONS.keys(),
        queryset=qs,
    )
    segment_window_summary = time_windows.compute_window_counts(queryset=qs)
    context = {
        "page_title": f"{segment_type.title()} Detail",
        "segment_type": segment_type,
        "segment_value": segment_value,
        "series_payload": json.dumps(
            {
                "labels": [row["incident_date"].isoformat() for row in series],
                "counts": [row["total"] for row in series],
            }
        ),
        "window_cards": window_cards,
        "segment_window_summary": segment_window_summary,
    }
    return render(request, "analytics/dashboard_detail.html", context)


def data_science_lab(request: HttpRequest) -> HttpResponse:
    gate = _require_entry_access(request)
    if gate:
        return gate
    if not request.session.get(LAB_SESSION_KEY):
        form = forms.PasscodeForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            if form.cleaned_data["passcode"] == settings.DS_LAB_PASSCODE:
                request.session[LAB_SESSION_KEY] = True
                messages.success(request, "Data Science Lab unlocked.")
                return redirect("analytics:data_science_lab")
            messages.error(request, "Invalid Data Science Lab passcode.")
        return render(
            request,
            "analytics/lab_gate.html",
            {"form": form, "page_title": "Data Science Lab Passcode"},
        )

    recent_models = ModelRun.objects.all()[:5]
    evaluations = EvaluationMetric.objects.all()[:8]
    context = {
        "page_title": "Data Science Lab",
        "stages": LAB_STAGES,
        "recent_models": recent_models,
        "evaluations": evaluations,
    }
    return render(request, "analytics/lab_home.html", context)


def lab_stage_detail(request: HttpRequest, stage_slug: str) -> HttpResponse:
    gate = _require_entry_access(request)
    if gate:
        return gate
    if not request.session.get(LAB_SESSION_KEY):
        return redirect("analytics:data_science_lab")
    stage = next((stage for stage in LAB_STAGES if stage["slug"] == stage_slug), None)
    if not stage:
        messages.error(request, "Unknown lab stage.")
        return redirect("analytics:data_science_lab")
    context = {
        "page_title": stage["title"],
        "stage": stage,
    }
    return render(request, "analytics/lab_stage_detail.html", context)


def import_console(request: HttpRequest) -> HttpResponse:
    gate = _require_entry_access(request)
    if gate:
        return gate
    if not request.session.get(IMPORT_SESSION_KEY):
        form = forms.PasscodeForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            if form.cleaned_data["passcode"] == settings.IMPORT_PASSCODE:
                request.session[IMPORT_SESSION_KEY] = True
                messages.success(request, "Importer authenticated.")
                return redirect("analytics:import_console")
            messages.error(request, "Incorrect import passcode.")
        return render(
            request,
            "analytics/import_gate.html",
            {"form": form, "page_title": "Importer Access"},
        )

    form = forms.ImportUploadForm()
    context = {
        "page_title": "Import Console",
        "form": form,
        "instructions": [
            "Upload or paste the four district workbooks exported from the upstream app.",
            "Review the automated preview (counts by district/beat, anomaly flags).",
            "Commit the batch to lock in a single source of truth per date.",
            "If necessary, run the CLI command `python manage.py import_incidents --path data/crime_365d.csv`.",
        ],
    }
    return render(request, "analytics/import_console.html", context)
