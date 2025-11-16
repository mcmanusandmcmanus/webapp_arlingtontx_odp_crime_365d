from django.contrib import admin

from .models import EvaluationMetric, ImportBatch, Incident, ModelRun


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("case_number", "incident_datetime", "beat", "district", "offense_category")
    list_filter = ("district", "beat", "offense_category")
    search_fields = ("case_number", "description", "beat", "district")
    date_hierarchy = "incident_datetime"


@admin.register(ImportBatch)
class ImportBatchAdmin(admin.ModelAdmin):
    list_display = ("batch_date", "source_name", "row_count", "created_at")
    list_filter = ("batch_date",)
    search_fields = ("source_name", "notes")


@admin.register(ModelRun)
class ModelRunAdmin(admin.ModelAdmin):
    list_display = ("model_name", "algorithm", "stage", "training_window", "created_at")
    list_filter = ("stage", "algorithm")
    search_fields = ("model_name", "algorithm", "notes")


@admin.register(EvaluationMetric)
class EvaluationMetricAdmin(admin.ModelAdmin):
    list_display = ("week_of", "audience", "metric_name", "expected_value", "observed_value")
    list_filter = ("audience", "week_of")
    search_fields = ("metric_name",)
