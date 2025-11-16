from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from analytics.models import ImportBatch, Incident


class Command(BaseCommand):
    help = "Import incidents from the consolidated CSV extract."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            help="Path to CSV/Excel export. Defaults to settings.CRIME_DATA_PATH.",
        )
        parser.add_argument(
            "--batch-date",
            type=str,
            help="Override the logical batch date (YYYY-MM-DD). Defaults to max incident date.",
        )
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Replace existing batch with the same batch date.",
        )

    def handle(self, *args, **options):
        csv_path = Path(options.get("path") or settings.CRIME_DATA_PATH)
        if not csv_path.exists():
            raise CommandError(f"File not found: {csv_path}")
        self.stdout.write(f"Loading data from {csv_path} ...")
        df = self._read_dataframe(csv_path)
        if df.empty:
            raise CommandError("The provided dataset is empty.")

        datetime_column = None
        for candidate in ["Date/Time Occurred", "incident_datetime", "Datetime"]:
            if candidate in df.columns:
                datetime_column = candidate
                break
        if not datetime_column:
            raise CommandError("Could not locate a datetime column in the dataset.")

        df["incident_datetime"] = pd.to_datetime(df[datetime_column])
        df = df.dropna(subset=["incident_datetime"])
        df["incident_date"] = df["incident_datetime"].dt.date
        df["year"] = df["incident_datetime"].dt.year
        df["month"] = df["incident_datetime"].dt.month
        df["day"] = df["incident_datetime"].dt.day
        df["hour"] = df["incident_datetime"].dt.hour
        df["minute"] = df["incident_datetime"].dt.minute
        df["iso_week"] = df["incident_datetime"].dt.isocalendar().week
        df["quarter"] = df["incident_datetime"].dt.quarter

        batch_date = (
            datetime.strptime(options["batch_date"], "%Y-%m-%d").date()
            if options.get("batch_date")
            else df["incident_date"].max()
        )

        with transaction.atomic():
            if options.get("replace"):
                ImportBatch.objects.filter(batch_date=batch_date).delete()
            elif ImportBatch.objects.filter(batch_date=batch_date).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"Batch {batch_date} already exists. Use --replace to overwrite."
                    )
                )
                return

            batch = ImportBatch.objects.create(
                batch_date=batch_date,
                source_name=csv_path.name,
                row_count=0,
                notes="Imported via management command.",
            )
            incidents = self._build_incident_objects(df, batch)
            Incident.objects.bulk_create(incidents, batch_size=1000)
            batch.row_count = len(incidents)
            batch.save(update_fields=["row_count"])
        self.stdout.write(self.style.SUCCESS(f"Imported {batch.row_count} rows."))

    def _read_dataframe(self, path: Path) -> pd.DataFrame:
        if path.suffix.lower() in {".xls", ".xlsx"}:
            return pd.read_excel(path)
        return pd.read_csv(path)

    def _build_incident_objects(self, df: pd.DataFrame, batch: ImportBatch) -> List[Incident]:
        incidents: List[Incident] = []

        def bool_from_value(value: Optional[str]) -> bool:
            if isinstance(value, str):
                return value.strip().lower().startswith("business")
            return bool(value)

        for record in df.to_dict(orient="records"):
            incident_datetime = record.get("incident_datetime")
            if pd.isna(incident_datetime):
                continue
            dt = incident_datetime.to_pydatetime()
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt, timezone.get_default_timezone())
            incident = Incident(
                import_batch=batch,
                case_number=record.get("Case_Number", "") or "",
                district=record.get("District", "") or "",
                beat=str(record.get("Beat", "") or ""),
                description=record.get("Description", "") or "",
                offense_category=record.get("Description", "") or record.get("Offense", ""),
                priority=str(record.get("priority", "") or record.get("Priority", "")),
                location_type=record.get("location_type", "") or record.get("Location_Type", ""),
                incident_datetime=dt,
                incident_date=record.get("incident_date"),
                year=int(record.get("year") or record.get("Year") or 0),
                month=int(record.get("month") or record.get("month_num") or 0),
                day=int(record.get("day") or 0),
                day_of_week=record.get("day_of_week", "") or record.get("Day_of_week", ""),
                hour=int(record.get("hour") or 0),
                minute=int(record.get("minute") or 0),
                iso_week=int(record.get("iso_week") or 0),
                quarter=int(record.get("quarter") or 0),
                time_of_day_label=record.get("timeofday_label", ""),
                business_hours_flag=bool_from_value(record.get("Businesshrs_flag")),
                calendar_month_label=record.get("month_name", "") or record.get("month_txt", ""),
                narrative_date=record.get("date_summary", ""),
            )
            incidents.append(incident)
        return incidents
