Here’s a .md you can copy into VS Code and save as something like crime_dashboard_heatmaps.md:

# Crime Dashboard Heatmaps – Design Spec

This document describes the **core heatmaps** for a crime analytics Django web app built on a **366-day incident dataset**.

The goal is to give the coding assistant (VS Code Codex / GitHub Copilot) a **clear spec** for implementing:

1. **Calendar Heat Lab** – GitHub-style yearly calendar heatmap with multiple “heat types”.
2. **24×7 Time-of-Week Heatmap** – Day-of-week × hour grid showing temporal rhythms.
3. **Poisson Z Change Heatmap** – Beat × rolling 28-day windows using the Crime De-Coder Poisson Z-score.

---

## 0. Dataset Assumptions

We assume the incidents CSV has already been ingested into a Django model with fields similar to:

- `date_only` – `DateField`, one per incident (366 distinct days).
- `day_of_week` – integer or string (Mon–Sun).
- `hour` – integer 0–23.
- `District` – string, one of a small set (e.g., EAST, WEST, NORTH, SOUTH).
- `Beat` – string, beat identifier (e.g., N11, S21).
- `Description` – string, offense type/category.
- Optional flags:
  - `Businesshrs_flag` (Business vs Non-Business hours)
  - `weekend_yn`, `weekday_yn`
  - `month_name`, `quarter`, `year_month`
- Data covers a **continuous 366-day span** (one year plus leap day or similar).

In Django, this might be represented as:

```python
class Incident(models.Model):
    date_only = models.DateField()
    day_of_week = models.CharField(max_length=10)  # or IntegerField 0-6
    hour = models.IntegerField()  # 0-23
    district = models.CharField(max_length=10)
    beat = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    # plus optional flags/fields


All heatmaps should be driven by aggregated data exposed through JSON API endpoints.

1. Calendar Heat Lab – GitHub-Style Daily Calendar Heatmap
1.1 Purpose

Create a GitHub-style yearly calendar heatmap where:

Each square = one day in the 366-day range.

X-axis ≈ weeks of year (columns).

Y-axis = day of week (rows).

Color = “heat” based on user-selectable metric (heat type).

This is the “Year-at-a-glance” view.

1.2 Heat Types (Metrics)

Implement a dropdown to switch heat type. All use the same grid layout.

Heat Type A – Activity (Daily Count)

Metric per day: count_all

Definition: count_all(d) = number of incidents on date d

Color: sequential scale (light = low, dark = high).

Heat Type B – Daily Z vs Year Baseline

Metric per day: Z-score relative to year’s daily mean/stdev:

mu = mean(daily counts over all 366 days)
sigma = std(daily counts over all 366 days)
Z_d = (count_all(d) - mu) / sigma


Color: diverging scale centered at 0.

Neutral around Z≈0.

Hot colors for positive Z (unusually busy).

Cool colors for negative Z (unusually quiet).

Heat Type C – Category Mix (Percent of a Group)

Example: proportion of person crimes.

Metric per day:

pct_person(d) = person_incidents(d) / all_incidents(d)


More generally, user selects a group (Person, Property, Drugs, etc.).

Color: sequential scale from low % to high %.

Heat Type D – Weekday vs Expected Profile

Step 1: compute baseline average for each weekday:

avg_weekday[w] = average daily count for all days with day_of_week = w


Step 2: per day:

expected_d = avg_weekday[day_of_week(d)]
delta_d = count_all(d) - expected_d


Color: diverging scale on delta_d.

Shows days that were unusually hot/quiet for that weekday, not just overall.

NOTE: Implementation should support adding more heat types later with minimal changes.

1.3 Backend API (Example)

Create a Django view like /api/calendar_heatmap that:

Accepts query params:

heat_type ∈ {count, z_daily, pct_group, weekday_delta}

district (optional filter, default = ALL)

offense_group (optional filter, default = ALL)

start & end date (optional; default = last 365/366 days)

Returns JSON:

{
  "heat_type": "count",
  "start": "2024-01-01",
  "end": "2024-12-31",
  "days": [
    {
      "date": "2024-01-01",
      "weekday": 1,        // Monday=1 ... Sunday=7
      "week_index": 0,     // 0-based week offset from start
      "value": 23,         // metric for the selected heat_type
      "count_all": 23,     // raw daily count (optional)
      "extra": {
        "pct_person": 0.32,
        "z_daily": 1.1,
        "weekday_delta": 5.4
      }
    },
    ...
  ]
}


The frontend uses weekday and week_index to place each square.

1.4 Frontend Behavior

Use D3.js, Cal-Heatmap, or a custom SVG to render:

7 rows (one per weekday).

Columns for each week (week_index).

Each rect:

x = week_index * (tile_size + tile_padding)

y = weekday * (tile_size + tile_padding)

fill = colorScale(value)

Add:

Month labels above columns (approx at first week of each month).

Weekday labels on the left (e.g., Mon, Wed, Fri).

Tooltip on hover:

Date

Value + explanation:

Example for Z: 34 incidents (Z = 1.3, above yearly average)

Example for pct: 18 incidents (44% Person crimes)

Optional click behavior:

Clicking a day opens a detail panel (modal or side panel) with:

Breakdown by district

Breakdown by offense category

Daily 24×7 pattern for that date (future enhancement).

2. 24×7 Time-of-Week Heatmap
2.1 Purpose

Show the typical weekly rhythm of incidents:

Rows = day_of_week (Mon–Sun).

Columns = hour (0–23).

Cell value = incident count (or rate) over the selected period.

This is the “When does it happen?” view.

2.2 Metrics

Main metric: aggregated count for the selected filter and time range.

Optionally support:

All incidents.

Filter by District, Beat, offense_group.

Filter by Businesshrs_flag (business vs non-business hours).

2.3 Backend API (Example)

Endpoint: /api/heatmap_24x7

Params:

start, end date

district, beat, offense_group

Returns:

{
  "start": "2024-01-01",
  "end": "2024-12-31",
  "matrix": [
    {
      "day_of_week": "Mon",
      "hour": 0,
      "count": 3
    },
    {
      "day_of_week": "Mon",
      "hour": 1,
      "count": 5
    }
    // one entry per (day_of_week, hour)
  ],
  "marginals": {
    "by_hour": [
      {"hour": 0, "count": 34},
      {"hour": 1, "count": 52}
    ],
    "by_day": [
      {"day_of_week": "Mon", "count": 140},
      {"day_of_week": "Tue", "count": 155}
    ]
  }
}

2.4 Frontend Behavior

Render a 7×24 heatmap (rows = days, columns = hours).

Use a sequential color scale on count.

Add marginal bar charts:

Top: total incidents by hour.

Right: total incidents by day of week.

Interaction:

Hover over a cell:

Show day_of_week, hour, and count.

Filters (district, offense group, business hours) should trigger a re-fetch and re-render.

3. Poisson Z Change Heatmap (Crime De-Coder)
3.1 Purpose

Show statistically meaningful changes between consecutive time windows using the Crime De-Coder Poisson Z-score.

This is a Beat × Time-Window grid:

Rows = beats (or districts).

Columns = rolling or sequential time windows (e.g., 28-day periods).

Cell value = Poisson Z comparing current window vs past window for that beat.

3.2 Poisson Z Formula

For each beat and each window:

Current = incident count in current window
Past    = incident count in previous window

If Past == 0 and Current == 0:
    Z = 0  (no activity)
If Past == 0 and Current > 0:
    Z = special "new hotspot" case (can be None or very large)
Else:
    Z = 2 * (sqrt(Current) - sqrt(Past))


Interpretation:

|Z| ≈ 0 → no meaningful change (within Poisson noise).

Z ≥ +3 → strong evidence of an increase.

Z ≤ −3 → strong evidence of a decrease.

3.3 Window Definition

Use 28-day windows across the 366-day span:

Example:

Window 1: days 1–28

Window 2: days 29–56

...

For window k, compare to k-1.

Support:

Citywide view (aggregated).

District or Beat view (per-row).

3.4 Backend API (Example)

Endpoint: /api/poisson_z_heatmap

Params:

window_length (default 28 days)

unit ∈ {beat, district} (row dimension)

Optional filters on offense group, etc.

Response shape:

{
  "window_length_days": 28,
  "units": "beat",
  "windows": [
    {
      "id": 2,
      "label": "2024-02-01 to 2024-02-28",
      "start": "2024-02-01",
      "end": "2024-02-28",
      "rows": [
        {
          "unit": "N11",
          "current": 23,
          "past": 10,
          "z": 2.6
        },
        {
          "unit": "N12",
          "current": 7,
          "past": 7,
          "z": 0.0
        }
      ]
    },
    ...
  ]
}


The frontend will convert this into a matrix:

X = window index (id)

Y = unit (unit)

3.5 Frontend Behavior

Render a heatmap:

Columns = windows (label or short ID).

Rows = beats or districts.

Color = diverging around Z = 0; stronger colors beyond |Z| ≥ 3.

Tooltip:

Unit name

Window date range

Current, Past, and Z value

Optional:

Click a cell to:

Open a detail panel showing:

Offense breakdown for that unit and window.

Link to calendar or 24×7 view restricted to that subset.

4. Integration Notes

All heatmaps should:

Use shared filters for date range, district, and offense group where feasible.

Use consistent color scales and legends.

The Calendar Heat Lab and Poisson Z Heatmap can live on the same page as separate tabs:

Tab 1: Calendar Heat (daily metrics).

Tab 2: Poisson Z Change (window-level change detection).

The 24×7 heatmap can be linked from:

The overview page.

Drilldowns from calendar or Poisson Z views.

5. TODOs for Implementation

 Implement Incident model and load the 366-day CSV.

 Create API endpoints:

 /api/calendar_heatmap

 /api/heatmap_24x7

 /api/poisson_z_heatmap

 Implement aggregation logic in Django views or dedicated service layer.

 Implement frontend rendering:

 Calendar heatmap (GitHub-style).

 24×7 heatmap with marginal charts.

 Poisson Z Beat × Window heatmap.

 Add filters (District, Beat, offense group, business vs non-business).

 Add tooltips and legends for each heatmap.

 Add tests for aggregation and Poisson Z calculations.


::contentReference[oaicite:0]{index=0}