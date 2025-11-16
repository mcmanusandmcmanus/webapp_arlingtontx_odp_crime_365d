# Arlington ODP Crime 365 – COO Dashboard

Professional, municipal-grade Django web application that showcases how open data, modern analytics, and storytelling can guide Arlington’s executive, command, field, and analyst audiences. The build follows the “True North” roadmap (`README_ROADMAP_part0.docx`) plus the DEV briefs and targets Render deployment after local hardening.

## Stack Overview
- **Backend:** Django 5.1, SQLite (local) with `dj-database-url` for easy Render/Postgres swaps
- **Data Science:** pandas, NumPy, SciKit-Learn, Matplotlib/Seaborn for offline EDA + modeling
- **Frontend:** Django templates, Tailwind utility classes, Chart.js modules, custom JS helpers
- **Data Flow:** Consolidated CSV (`data/crime_365d.csv`) → management command → `Incident` model → COO dashboards, segmentation suites, Data Science Lab

Directory highlights
```
analytics/
  ├─ management/commands/import_incidents.py   # CSV/Excel ingestion
  ├─ models.py                                 # Incident, ImportBatch, ModelRun, EvaluationMetric
  ├─ services/                                 # Time windows, segmentation, baseline cards
  ├─ templates/analytics/                      # Municipal-grade UI shells
  └─ static/analytics/                         # Tailwind-friendly CSS + Chart.js helpers
crime_dashboard/                               # Project settings + URLs
data/crime_365d.csv                            # Consolidated WEBAPP dataset (copy of WEBAPP CSV)
templates/analytics/base.html                  # Shared layout, nav, and scripts
requirements.txt                               # Django + DS stack
```

## Getting Started
```bash
pip install -r requirements.txt
python manage.py migrate
# copy the latest consolidated extract into data/crime_365d.csv
python manage.py import_incidents --replace
python manage.py runserver
```

Environment variables (`.env`) you can override:
```
DJANGO_SECRET_KEY=super-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.onrender.com
CRIME_DATA_PATH=/full/path/to/consolidated_extract_WEBAPP.csv
ENTRY_PASSCODE=welcome
DS_LAB_PASSCODE=labpass
IMPORT_PASSCODE=importpass
```

## Multi-layer Access Controls
1. **Entry Gate (`/access/`)** – protects COO dashboard experience (ENTRY_PASSCODE).
2. **Data Science Lab (`/lab/`)** – second passcode (DS_LAB_PASSCODE) unlocks EDA/modeling artifacts.
3. **Import Console (`/import/`)** – importer passcode (IMPORT_PASSCODE) plus upload/paste form; CLI `import_incidents` is the authoritative ingest path today.

Session flags keep the UX smooth for authenticated visitors, while the public MIT-licensed content can be shared once leadership grants initial access.

## Dashboards & Lab
- **Executive Overview (`/dashboard/`)** – KPI cards for 28/91/365, Chart.js bar comparing the six standard windows, data payloads for calendar heatmap + 24×7 grid, narrative summary deck.
- **Segments (`/dashboard/segments/`)** – dynamic window + segment dropdowns, Chart.js “current vs previous” bar chart, storytelling table with % change + share + detail CTAs.
- **Detail (`/dashboard/detail/<segment>/<value>/`)** – 365-day line chart, per-window comparisons, narrative checklist for command staff.
- **Data Science Lab (`/lab/`)** – four Netflix-level stages (EDA, Feature Lab, Modeling, Evaluation), recent `ModelRun` metrics, weekly `EvaluationMetric` log.
- **Import Console (`/import/`)** – instructions + upload/paste shell to prep future preview/commit flow defined in `README_DEV_part3.md`.

## Data Import Command
```
python manage.py import_incidents --path data/crime_365d.csv --replace
```
- Safely re-runs by deleting existing `ImportBatch` for the detected/max incident date unless `--replace` specified.
- Auto-normalizes datetime components, time-of-day labels, ISO weeks, quarter, and stores relationships to the batch for provenance.

## Next Steps (Roadmap hooks)
1. **Visual polish:** wire Tailwind CLI/TW plugin builds, drop in production-grade calendar + 24×7 heatmap components (see `README_DEV_part4.md`).
2. **Data Science Lab tooling:** add notebooks/scripts to log `ModelRun` entries and evaluation metrics; expose download endpoints for analysts.
3. **Importer UI:** connect upload form to a staging table, surface preview counts, and trigger the management command via Celery task or admin action.
4. **Testing/QA:** add pytest suite for services (`analytics/services/*`) plus smoke tests for passcode gating.
5. **Render deployment:** add `render.yaml`/Procfile + environment secrets; enable WhiteNoise static serving already configured in settings.

See the detailed blueprints across `README_DEV_part1-4.md` and `README_ROADMAP_part0.docx` for persona stories, UX choreography, and heatmap expectations.
