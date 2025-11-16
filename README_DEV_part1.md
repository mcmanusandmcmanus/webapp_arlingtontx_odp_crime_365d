You are an expert Django web developer, data scientist, and UX storyteller.

PROJECT CONTEXT
- Repo: https://github.com/mcmanusandmcmanus/webapp_arlingtontx_odp_crime_365d
- Purpose: Build a professional municipal-style web application for analyzing 365 days of crime/incident open data for Arlington, TX (or similar city).
- Audience: COO, command staff, and a Director of Data Science who care about:
  1) Time-Window & Baseline Strategy (core horizons: 7, 14, 28, 91, 182, 365 days)
  2) Segmentation: “Who / Where / When / What” slices that matter operationally
- Future deployment: Render.com (local dev first, Heroku-style deployment later).
- Backend: Django (preferred in municipal space).
- Frontend: Django templates + Tailwind CSS + Chart.js for professional dashboards and charts. Storytelling is as important as raw numbers.

OVERALL GOAL
Turn this repo into a Django-based “COO Dashboard” web app that:
- Loads or connects to a 365-day crime/incident dataset.
- Computes key time-window metrics (7, 14, 28, 91, 182, 365 days).
- Provides baseline / expectation comparisons where possible.
- Presents clean, professional dashboards organized around:
  1) Time-Window & Baseline Strategy
  2) Segmentation (Who / Where / When / What)
- Tells a narrative story: each chart or table should have a small human-readable interpretation below it.

---------------------------------------------------
TECH STACK & STRUCTURE
---------------------------------------------------

Use:
- Python 3.x
- Django (latest stable 4.x/5.x is fine)
- Tailwind CSS for styling
- Chart.js for visualizations
- SQLite for local development DB; later we can swap to PostgreSQL for Render.

If the repo already has a Django project, extend it.
If not, create a project named: `crime_dashboard`
and an app named: `analytics`.

Directory structure goal (simplified):

- crime_dashboard/
  - crime_dashboard/        # project settings
    - settings.py
    - urls.py
  - analytics/              # main app
    - models.py
    - views.py
    - urls.py
    - services/
      - __init__.py
      - time_windows.py     # logic for 7/14/28/91/182/365 day metrics
      - segmentation.py     # helpers for segmenting Who/Where/When/What
      - baseline.py         # (optional) simple baseline expectations
    - templates/analytics/
      - base.html           # shared layout, nav, header, footer
      - dashboard_overview.html
      - dashboard_segments.html
      - dashboard_detail.html
    - static/analytics/
      - css/ (Tailwind build output)
      - js/ (Chart.js configuration)
  - manage.py
- data/
  - crime_365d.csv          # or similar dataset (path placeholder)
- requirements.txt
- Procfile or render.yaml (later)

---------------------------------------------------
DATA & MODEL LAYER
---------------------------------------------------

ASSUME:
- There is a 365-day open data crime/incident CSV somewhere under `data/`.
- Columns will include at least:
  - `incident_datetime` (or similar)
  - `beat` or `zone`
  - `offense_type` or `nibrs_offense`
  - `priority` or severity-like field
  - `location_type` or address-related information

TASKS:

1) MODELS
- In `analytics/models.py`, define a minimal `Incident` model, for example:

  - `incident_datetime` (DateTimeField)
  - `beat` (CharField, nullable)
  - `offense_type` (CharField)
  - `priority` (CharField or IntegerField)
  - `location_type` (CharField, nullable)

- Also define simple lookup/dimension models if useful (e.g., Beat, OffenseType) but keep v1 simple.

2) DATA IMPORT
- Create a Django management command, e.g. `analytics/management/commands/import_incidents.py`, which:
  - Reads `data/crime_365d.csv` (I will adjust the filename/columns).
  - Parses the datetime column.
  - Bulk-creates `Incident` rows.
- Make the import idempotent or safe to re-run (e.g., clear table or use a simple guard).

---------------------------------------------------
TIME-WINDOW & BASELINE STRATEGY (COO CORE HORIZONS)
---------------------------------------------------

The COO wants fixed standard windows:
- 7 days  – “Last week”
- 14 days – “Last 2 weeks”
- 28 days – “Last 4 weeks / pseudo-month”
- 91 days – “Last ~quarter (13 weeks)”
- 182 days – “Last 6 months”
- 365 days – “Last year”

3) SERVICES: TIME WINDOWS
- In `analytics/services/time_windows.py`, create helpers that:
  - Accept a reference date (default: max incident date in DB).
  - Compute a dictionary of window boundaries for [7, 14, 28, 91, 182, 365] days.
  - Provide reusable functions like:
    - `get_time_windows(reference_date=None)` -> dict of window_name -> (start_date, end_date)
    - `get_counts_by_window()` for entire city
    - `get_counts_by_window_and_segment(segment_field)` (e.g., per beat or offense_type).

- These should use efficient ORM queries (annotate/filter) not row-by-row Python loops.

4) BASELINE (OPTIONAL SIMPLE VERSION)
- For now, implement a simple “baseline” logic:
  - For each window, also compute:
    - The same-length window immediately before it (a “previous period”).
    - e.g., for last 28 days, compare to the prior 28 days.
  - Provide:
    - `current_count`
    - `previous_count`
    - `absolute_change`
    - `percent_change` (with safe divide by zero handling)

- Later we can add real Poisson/NB models, but v1 just needs clean period-over-period comparisons.

---------------------------------------------------
SEGMENTATION: SLICE EVERYTHING THAT MATTERS
---------------------------------------------------

We want a flexible segmentation layer based on the COO thinking:

"Who / Where / When / What"

Examples:
- Who: unit, beat, officer (if available), priority level of call
- Where: beat, zone, neighborhood, location type (residential, commercial, roadway)
- When: day-of-week, time-of-day buckets (Night / Morning / Afternoon / Evening), shift
- What: offense / incident type, NIBRS category, severity

5) SERVICES: SEGMENTATION
- In `analytics/services/segmentation.py`, create helpers that:
  - Given a window (start_date, end_date) and a group-by field (e.g. "beat", "offense_type"),
    compute:
    - counts per segment
    - rank them by count, descending
    - optionally compute change vs previous window for the same segment field
  - Provide a reusable function like:
    - `get_top_segments_by_window(window_name, group_field, top_n=10)`

- Also include a small helper for time-of-day buckets, with buckets such as:
  - Night: [00:00, 06:00)
  - Morning: [06:00, 12:00)
  - Afternoon: [12:00, 18:00)
  - Evening: [18:00, 24:00)

---------------------------------------------------
VIEWS, URLS, AND TEMPLATES
---------------------------------------------------

6) URL ROUTING
- In `crime_dashboard/urls.py`, include the analytics app URLs.
- In `analytics/urls.py`, define at least:
  - `/`                         -> redirect to `/dashboard/`
  - `/dashboard/`              -> citywide COO overview dashboard
  - `/dashboard/segments/`     -> segmentation view (Who/Where/When/What)
  - `/dashboard/detail/<segment_type>/<segment_value>/`
     -> detail page for a specific beat, offense, etc.

7) VIEWS
- In `analytics/views.py`, implement:

  a) `dashboard_overview(request)`:
    - Compute citywide metrics for each standard window:
      - total incidents for 7, 14, 28, 91, 182, 365 days
      - previous period comparison for each window
    - Pass a JSON-ready data structure to the template suitable for Chart.js:
      - e.g., labels = ["7d","14d","28d","91d","182d","365d"]
      - datasets = [current_counts, previous_counts]
    - Also compute a few narrative strings to display under the charts
      (or pass the raw numbers and use template logic to build text).

  b) `dashboard_segments(request)`:
    - Accept query parameters like:
      - `segment_field` (default: "beat")
      - `window` (default: "28d")
    - Use segmentation services to get:
      - Top N segments by volume in the selected window
      - Their change vs the previous same-length window
    - Provide data for:
      - A bar chart (segments vs counts)
      - A small table showing:
        - segment
        - current_count
        - previous_count
        - pct_change

  c) `dashboard_detail(request, segment_type, segment_value)`:
    - For a specific segment (e.g., beat=“450”), show:
      - Time series chart (last 365 days daily counts)
      - Window summary cards for 7/14/28/91/182/365 days
      - A narrative block summarizing:
        - which windows are high/low vs previous period
        - any notable patterns (if we can infer simply)

---------------------------------------------------
TEMPLATES & UI/UX
---------------------------------------------------

8) BASE LAYOUT: `base.html`
- Professional, municipal style:
  - Top navbar with app title, logo placeholder, and nav links:
    - Overview
    - Segments
  - Left sidebar (optional) with quick filters (window selection, segment type).
  - Main content area with responsive cards and charts.
- Include Tailwind classes for:
  - Clean typography
  - Card-like panels
  - Good spacing
- Load Chart.js from a CDN for now.

9) DASHBOARD OVERVIEW UI: `dashboard_overview.html`
- Extends `base.html`.
- Show at least:
  - A top row of KPI cards:
    - Total incidents last 28 days (vs previous 28)
    - Total incidents last 91 days (vs previous 91)
    - Total incidents last 365 days (vs previous 365)
  - A main chart:
    - Bar or line chart comparing the standard windows:
      - Current vs previous counts per window.
  - Under the chart, show a narrative paragraph, for example:
    - “Last 28 days: 312 incidents vs 274 in the prior 28 days (+13.9%).”
    - “Last 91 days: slightly above the prior quarter, driven by [top segment].”

10) SEGMENTS UI: `dashboard_segments.html`
- Extends `base.html`.
- Controls:
  - Dropdown: select window (7d, 14d, 28d, 91d, 182d, 365d)
  - Dropdown: select segment field (beat, offense_type, time_of_day_bucket, etc.)
- Display:
  - A bar chart of top N segments for the chosen window.
  - A table showing:
    - segment
    - current_count
    - previous_count
    - pct_change
  - A short narrative at the top summarizing:
    - “Beats 430, 450, and 610 account for 48% of incidents in the last 28 days, with Beat 450 up 23% vs the previous 28 days.”

11) DETAIL UI: `dashboard_detail.html`
- Extends `base.html`.
- Show:
  - Title: e.g., “Beat 450 – Detail View”
  - Line chart: daily counts for last 365 days.
  - Cards for each window (7/14/28/91/182/365 days):
    - Each card shows current_count, previous_count, pct_change.
  - Narrative:
    - e.g., “In the last 28 days, Beat 450 recorded 22 incidents vs 15 in the prior 28 days (+46.7%). The last 365 days trend shows a gradual upward pattern since May.”

---------------------------------------------------
TAILWIND & CHART.JS INTEGRATION
---------------------------------------------------

12) STYLING
- Integrate Tailwind CSS into the Django project:
  - Use a simple CLI or CDN-based Tailwind setup as appropriate.
- Use Tailwind utility classes to:
  - Style cards, tables, navbars, chart containers.
  - Ensure mobile-friendly (stacked) and desktop-friendly layouts.

13) CHART.JS
- Build small JS snippets in `static/analytics/js/`:
  - One for the overview chart.
  - One for segments chart.
  - One for detail chart.
- Each should read data from:
  - JSON blobs embedded into the template using Django templating (safe JSON).

---------------------------------------------------
RENDER / DEPLOYMENT PREP (SIMPLE)
---------------------------------------------------

14) Add deployment basics (can be placeholders):
- `requirements.txt` with Django, gunicorn, etc.
- `Procfile` or `render.yaml` with:
  - Web service using `gunicorn crime_dashboard.wsgi:application`
- Settings pattern:
  - Use environment variables for DEBUG, SECRET_KEY, and database configuration.
  - Default to SQLite locally; allow PostgreSQL via env vars for Render.

---------------------------------------------------
CODING STYLE & EXPECTATIONS
---------------------------------------------------

- Use clear function and variable names.
- Add docstrings to service functions (time windows, segmentation).
- Keep logic in `services/` where possible; keep views thin.
- Use Django ORM efficiently for aggregation (annotate, values, Count).
- Avoid overengineering; v1 should be understandable and extensible.

WHEN WRITING CODE:
- Follow the structure and intentions above.
- If something is ambiguous (like exact CSV columns), write TODO comments with clear instructions so I can fill in details.
- Prefer incremental, composable functions that can be reused across different dashboards.

End of instructions.
