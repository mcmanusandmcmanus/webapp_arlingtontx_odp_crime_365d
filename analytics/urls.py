from django.urls import path

from . import views

app_name = "analytics"

urlpatterns = [
    path("access/", views.entry_gate, name="entry_gate"),
    path("dashboard/", views.dashboard_overview, name="dashboard_overview"),
    path("dashboard/segments/", views.dashboard_segments, name="dashboard_segments"),
    path(
        "dashboard/detail/<str:segment_type>/<str:segment_value>/",
        views.dashboard_detail,
        name="dashboard_detail",
    ),
    path("lab/", views.data_science_lab, name="data_science_lab"),
    path("lab/stage/<slug:stage_slug>/", views.lab_stage_detail, name="lab_stage_detail"),
    path("import/", views.import_console, name="import_console"),
    path("api/heatmaps/calendar/", views.calendar_heatmap_api, name="calendar_heatmap_api"),
    path("api/heatmaps/time-of-week/", views.heatmap_24x7_api, name="heatmap_24x7_api"),
    path("api/heatmaps/poisson/", views.poisson_heatmap_api, name="poisson_heatmap_api"),
]
