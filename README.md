# Arlington ODP Crime 365 - COO Dashboard

Professional, municipal-grade Django web application that showcases how open data, modern analytics, and storytelling can guide Arlington's executive, command, field, and analyst audiences. The build follows the True North roadmap (`README_ROADMAP_part0.docx`) along with the DEV design briefs and targets Render deployment after local hardening.

## Documentation Map
| File | Purpose |
| --- | --- |
| `README_ROADMAP_part0.docx` | True North narrative, personas, and security gates |
| `README_DEV_part1.md` | Core architecture, time-window strategy, segmentation services |
| `README_DEV_part2.md` | Import console blueprint plus current implementation status |
| `README_DEV_part3.md` | Data Science Lab stages, ML expectations, evaluation loop |
| `README_DEV_part4.md` | Heatmap (calendar, 24x7, Poisson Z) specification |

## Stack Overview
- **Backend:** Django 5.1, SQLite (local) with `dj-database-url` for easy Render/Postgres swaps
- **Data Science:** pandas, NumPy, scikit-learn, matplotlib, seaborn for offline EDA and modeling
- **Frontend:** Django templates, Tailwind utility classes, Chart.js modules, custom JS helpers
- **Data Flow:** Consolidated CSV (`data/crime_365d.csv`) -> management command -> `Incident` model -> COO dashboards, segmentation suites, Data Science Lab

Directory highlights
```
analytics/
  - management/commands/import_incidents.py   # CSV/Excel ingestion & provenance
  - models.py                                 # Incident, ImportBatch, ModelRun, EvaluationMetric
  - services/                                 # Time windows, segmentation, baseline cards
  - templates/analytics/                      # Municipal-grade UI shells
crime_dashboard/                               # Project settings + URLs
data/crime_365d.csv                            # Consolidated WEBAPP dataset
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
1. **Entry Gate (`/access/`)** - protects the COO dashboard experience (ENTRY_PASSCODE).
2. **Data Science Lab (`/lab/`)** - second passcode (DS_LAB_PASSCODE) unlocks EDA/modeling artifacts.
3. **Import Console (`/import/`)** - importer passcode (IMPORT_PASSCODE) plus upload/paste form; CLI `import_incidents` is the authoritative ingest path today.

Session flags keep the UX smooth for authenticated visitors, while the public MIT-licensed content can be shared once leadership grants initial access.

## Dashboards and Lab
- **Executive Overview (`/dashboard/`)** - KPI cards for 28/91/365, Chart.js bar comparing the six standard windows, JSON payloads for calendar heatmap and 24x7 grid, narrative summary deck.
- **Segments (`/dashboard/segments/`)** - dynamic window and segment dropdowns, Chart.js current vs previous bar chart, storytelling table with percent change, share, and detail CTAs.
- **Detail (`/dashboard/detail/<segment>/<value>/`)** - 365-day line chart, per-window comparisons, narrative checklist for command staff.
- **Data Science Lab (`/lab/`)** - four stages (EDA, Feature Lab, Modeling, Evaluation), recent `ModelRun` metrics, weekly `EvaluationMetric` log.
- **Import Console (`/import/`)** - instructions plus upload/paste shell to prep the preview/commit flow defined in the import console spec.

## Data Import Command
```
python manage.py import_incidents --path data/crime_365d.csv --replace
```
- Safely re-runs by deleting existing `ImportBatch` for the detected/max incident date unless `--replace` is specified.
- Auto-normalizes datetime components, time-of-day labels, ISO weeks, quarter, and stores relationships to the batch for provenance.

## Path to Version 1.0.0
| Track | MVP (done) | Next (0.9.x) | 1.0.0 Goal |
| --- | --- | --- | --- |
| **Data foundation** | Incident + ImportBatch models, CSV import command | Import preview service, automated QA checks, nightly refresh hooks | Fully automated ingest (upload + CLI), validation dashboards |
| **COO dashboards** | KPI cards, segmentation, detail view | Calendar/24x7 heatmaps wired per `README_DEV_part4.md`, narrative generator | Executive-ready storytelling with drill downs, A/B baseline comparisons |
| **Data Science Lab** | Stage navigation, ModelRun/EvaluationMetric scaffolding | Notebook/CLI utilities logging metrics, experiment registry, feature catalog | Repeatable ML workflow (train/val/test/cv), hyperparameter search history, download APIs |
| **Import console** | Passcode gate + form shell, CLI fallback | File staging, Parse & Preview UI, single-commit enforcement | Web-first ingestion with audit logs, user notifications |
| **Evaluation & telemetry** | Weekly evaluation model, manual entry | Auto comparison of expectation vs observed, alert hooks | Self-monitoring analytics with board-ready scorecards |
| **Deployment** | Django + WhiteNoise config, `.env` support | Tailwind build pipeline, render.yaml/Procfile, smoke tests | Render deployment with CI, CDN-backed static assets, monitoring |

## Next Steps
1. **Visual polish:** wire Tailwind CLI build, drop in production-grade calendar and 24x7 heatmap components (see `README_DEV_part4.md`).
2. **Data Science Lab tooling:** add notebooks/scripts to log `ModelRun` entries and evaluation metrics; expose download endpoints for analysts.
3. **Importer UI:** connect upload form to a staging table, surface preview counts, and trigger the management command via Celery task or admin action.
4. **Testing/QA:** add pytest suite for services (`analytics/services/*`) plus smoke tests for passcode gating and import workflows.
5. **Render deployment:** add `render.yaml` or Procfile plus environment secrets; enable static builds during deploy.

Stay aligned with the DEV briefs and the roadmap documents to keep every persona (executive, command, field, analyst) delighted through v1.0.0 and beyond.

## Render Deployment
1. Ensure `render.yaml` exists on `main` (already added) and push your latest code.
2. In Render, **New + Blueprint** ➜ point to this repo (branch `main`).
3. Render automatically provisions:
   - **Web service:** `arlingtontx_odp_crime_365d` (Python env) with build `pip install … && python manage.py collectstatic --noinput`, **pre-deploy** `python manage.py migrate --noinput`, and start `gunicorn crime_dashboard.wsgi:application`.
   - **Database:** `arlingtontx_odp_crime_db` (Free Postgres) and injects `DATABASE_URL`.
4. Adjust environment variables in the Render UI if you need different passcodes or additional secrets (e.g., `DJANGO_SECRET_KEY`, `ENTRY_PASSCODE`, etc.).
5. Upload the latest `data/crime_365d.csv` to the `/opt/render/project/src/data/` path (Render shell) or ingest via the management command + importer console once deployed.
6. Trigger a deploy; after the first successful deploy run `python manage.py import_incidents --replace` via Render shell or hook the Import Console to load fresh data.
