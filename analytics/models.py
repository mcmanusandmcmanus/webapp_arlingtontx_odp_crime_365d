from django.db import models


class ImportBatch(models.Model):
    """Represents a single ingest of a CSV/Excel export from the upstream system."""

    batch_date = models.DateField(help_text="Logical date of the dataset (usually the most recent incident date).")
    source_name = models.CharField(max_length=255, blank=True)
    row_count = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-batch_date", "-created_at")

    def __str__(self) -> str:
        return f"Import {self.batch_date:%Y-%m-%d} ({self.row_count} rows)"


class Incident(models.Model):
    """Normalized crime / incident record used for dashboards and analytics."""

    import_batch = models.ForeignKey(
        ImportBatch,
        related_name="incidents",
        on_delete=models.CASCADE,
    )
    case_number = models.CharField(max_length=64, blank=True)
    district = models.CharField(max_length=64, blank=True)
    beat = models.CharField(max_length=32, blank=True)
    description = models.CharField(max_length=255, blank=True)
    offense_category = models.CharField(max_length=255, blank=True)
    priority = models.CharField(max_length=64, blank=True)
    location_type = models.CharField(max_length=255, blank=True)
    incident_datetime = models.DateTimeField()
    incident_date = models.DateField()
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    day = models.PositiveSmallIntegerField()
    day_of_week = models.CharField(max_length=16, blank=True)
    hour = models.PositiveSmallIntegerField(default=0)
    minute = models.PositiveSmallIntegerField(default=0)
    iso_week = models.PositiveSmallIntegerField(default=0)
    quarter = models.PositiveSmallIntegerField(default=0)
    time_of_day_label = models.CharField(max_length=32, blank=True)
    business_hours_flag = models.BooleanField(default=False)
    calendar_month_label = models.CharField(max_length=16, blank=True)
    narrative_date = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["incident_date"]),
            models.Index(fields=["beat"]),
            models.Index(fields=["district"]),
            models.Index(fields=["offense_category"]),
        ]
        ordering = ("-incident_datetime",)

    def __str__(self) -> str:
        return f"{self.case_number or self.pk} | {self.incident_datetime:%Y-%m-%d %H:%M}"


class ModelRun(models.Model):
    """Tracks machine learning experiments executed in the Data Science Lab."""

    RUN_STAGE_CHOICES = [
        ("training", "Training"),
        ("validation", "Validation"),
        ("testing", "Testing"),
        ("production", "Production Shadow"),
    ]

    run_id = models.CharField(max_length=64, unique=True)
    model_name = models.CharField(max_length=128)
    algorithm = models.CharField(max_length=128)
    stage = models.CharField(max_length=32, choices=RUN_STAGE_CHOICES, default="training")
    target_variable = models.CharField(max_length=128, default="incidents")
    training_window = models.CharField(max_length=64, blank=True)
    parameters = models.JSONField(default=dict, blank=True)
    metrics = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.model_name} ({self.algorithm})"


class EvaluationMetric(models.Model):
    """Measures how effective the dashboards/forecasts are week over week."""

    week_of = models.DateField(help_text="Week ending or starting date for evaluation.")
    audience = models.CharField(max_length=64, help_text="Executive, Command, Field, Analyst")
    metric_name = models.CharField(max_length=128)
    expected_value = models.FloatField(null=True, blank=True)
    observed_value = models.FloatField(null=True, blank=True)
    narrative = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-week_of", "audience")
        unique_together = ("week_of", "audience", "metric_name")

    def __str__(self) -> str:
        return f"{self.metric_name} ({self.week_of:%Y-%m-%d})"
