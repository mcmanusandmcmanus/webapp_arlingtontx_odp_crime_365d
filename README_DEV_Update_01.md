# Crime & Intelligence Dashboard – Django Frontend Design Spec (v2)

> **Use this document to “train” the chatbot / AI pair programmer.**  
> The goal is to build a modern, polished, *Django-rendered* web app for crime & intelligence analysis, visually inspired by:
> - Marketing sites like Coca-Cola and Apple  
> - SaaS/pricing layouts like Microsoft Power BI  
> while **staying in Django templates** (no React SPA).

---

## 0. Instructions to the AI Assistant

You are a code assistant working on an existing Django 5.1 project with an `analytics` app.

When you generate or modify code:

1. **Keep Django as the frontend framework.**
   - Use Django templates, template inheritance, and partials.
   - Use HTMX and Alpine.js for interactivity (partial updates, toggles, filters).
2. **Use Tailwind CSS for layout & styling.**
   - Design should feel modern and “product-grade” like Apple/Microsoft.
   - Dark theme base: `bg-slate-950 / bg-slate-900`, accent color like `emerald`.
3. **Use Chart.js + chartjs-matrix + Cal-Heatmap for charts.**
   - Charts are driven by Django JSON endpoints (`/api/...`).
4. **Structure pages as bands/sections**, inspired by:
   - Marketing hero sections (Coca-Cola, Apple).
   - Card grids and pricing cards (Power BI, Apple product tiles).
5. **Write clean, maintainable Django code.**
   - Use template inheritance, `{% include %}` partials, named URL patterns.
   - Keep logic in views/services, not templates.

---

## 1. Purpose & Audience

- **Audience:** Command staff, analysts, and stakeholders in a municipal police department.
- **Goal:** Deliver near-time crime & intelligence insights with:
  - Clear KPIs,
  - Visual patterns (time, day of week, calendar),
  - Narrative summaries,
  - Professional “product” look & feel (not a hobby dashboard).

---

## 2. Tech Stack & Architecture

### 2.1 Backend

- Django 5.1
- `analytics` app with:
  - Views in `analytics/views.py`
  - Services/utilities in `analytics/services.py`
- Database:
  - SQLite in local dev.
  - PostgreSQL in production (Render).

### 2.2 Frontend

- **Templates:** Django template system
- **CSS:** Tailwind CSS (CDN or compiled pipeline)
- **Interactivity:**  
  - HTMX for partial updates (`hx-get`, `hx-target`, `hx-trigger`, etc.)
  - Alpine.js for local UI state (selected horizon, toggles, etc.)
- **Charts:**
  - Chart.js 4 (`chart.umd.min.js`)
  - `chartjs-chart-matrix` for 24×7 heatmaps
  - Cal-Heatmap for calendar heatmaps
- **Static files:**
  - JS in `analytics/static/analytics/js/`
  - CSS in `analytics/static/analytics/css/`

---

## 3. Global Layout & Navigation

### 3.1 `base.html` (Global Shell)

Create/maintain `templates/analytics/base.html` as the core shell:

- Dark background, subtle border lines.
- Top command bar with:
  - App badge (“CA” or logo placeholder).
  - App name: “Crime Analysis Dashboard”.
  - Short tagline: “Operational Insight • Near-Time • Open Data”.
- Right side: global time-window selector (`7d`, `28d`, `365d`, `YTD`) using Alpine.

**Key patterns:**

- Use a 2-column layout in the main area:
  - Left column: filters + navigation (approx. 280px).
  - Right column: main content (dashboard, landing, pricing, etc.).
- Wrap main content in `#dashboard-root` to coordinate HTMX/Alpine events.

**Example skeleton (this is the canonical structure):**

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{% block title %}Crime Dashboard{% endblock %}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- Tailwind -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- HTMX + Alpine -->
  <script src="https://unpkg.com/htmx.org@1.9.12"></script>
  <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>

  <!-- Charts -->
  <script src="{% static 'analytics/js/chart.umd.min.js' %}"></script>
  <script src="{% static 'analytics/js/chartjs-chart-matrix.min.js' %}"></script>
  <script src="{% static 'analytics/js/cal-heatmap.min.js' %}"></script>
  <link rel="stylesheet" href="{% static 'analytics/css/cal-heatmap.css' %}">

  <link rel="stylesheet" href="{% static 'analytics/css/app.css' %}">
  {% block extra_head %}{% endblock %}
</head>
<body class="bg-slate-950 text-slate-100 antialiased">

  <div class="min-h-screen flex flex-col">
    <!-- Top command bar -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between gap-4">
        <!-- Left: logo + title -->
        <div class="flex items-center gap-2">
          <div class="h-8 w-8 rounded-lg bg-emerald-400/10 border border-emerald-400/40 flex items-center justify-center text-xs font-semibold text-emerald-300">
            CA
          </div>
          <div>
            <h1 class="text-sm font-semibold leading-tight">Crime Analysis Dashboard</h1>
            <p class="text-xs text-slate-400">Operational Insight • Near-Time • Open Data</p>
          </div>
        </div>

        <!-- Right: global nav + horizon selector -->
        <div class="flex items-center gap-6">
          <!-- Primary nav like Apple/Microsoft style -->
          <nav class="hidden md:flex items-center gap-4 text-xs text-slate-300">
            <a href="{% url 'home' %}" class="hover:text-slate-50 {% if request.resolver_match.url_name == 'home' %}text-slate-50 border-b-2 border-emerald-400 pb-1{% endif %}">
              Home
            </a>
            <a href="{% url 'analytics:dashboard' %}" class="hover:text-slate-50 {% if request.resolver_match.url_name == 'dashboard' %}text-slate-50 border-b-2 border-emerald-400 pb-1{% endif %}">
              Dashboard
            </a>
            <a href="{% url 'reports' %}" class="hover:text-slate-50 {% if request.resolver_match.url_name == 'reports' %}text-slate-50 border-b-2 border-emerald-400 pb-1{% endif %}">
              Reports
            </a>
            <a href="{% url 'pricing' %}" class="hover:text-slate-50 {% if request.resolver_match.url_name == 'pricing' %}text-slate-50 border-b-2 border-emerald-400 pb-1{% endif %}">
              Pricing
            </a>
          </nav>

          <!-- Global horizon selector controlled by Alpine -->
          <div x-data="{ horizon: '{{ default_horizon|default:"28d" }}' }" class="flex items-center gap-2 text-xs">
            <span class="text-slate-400 hidden sm:inline">Time Window</span>
            <template x-for="h in ['7d', '28d', '365d', 'ytd']" :key="h">
              <button
                class="px-2.5 py-1 rounded-full border text-xs"
                :class="horizon === h
                         ? 'border-emerald-400 bg-emerald-400/10 text-emerald-100'
                         : 'border-slate-700 bg-slate-900 text-slate-300 hover:border-slate-500'"
                x-text="h.toUpperCase()"
                @click="
                  horizon = h;
                  htmx.trigger('#dashboard-root', 'horizonChanged', {detail: {horizon: h}});
                "
              ></button>
            </template>
          </div>
        </div>
      </div>
    </header>

    <!-- Main content area -->
    <div id="dashboard-root"
         class="flex-1 mx-auto max-w-7xl w-full px-4 sm:px-6 lg:px-8 py-6
                grid grid-cols-1 lg:grid-cols-[280px,minmax(0,1fr)] gap-6">

      <!-- Left: sidebar filters / mini nav -->
      <aside class="space-y-6">
        {% block sidebar %}{% endblock %}
      </aside>

      <!-- Right: main content -->
      <main id="main-panel" class="space-y-6">
        {% block content %}{% endblock %}
      </main>
    </div>
  </div>

  {% block scripts %}{% endblock %}
</body>
</html>

document.addEventListener("DOMContentLoaded", () => {
  const mainPanel = document.getElementById("main-panel");
  if (!mainPanel) return;

  initCharts();

  document.body.addEventListener("htmx:afterSwap", (evt) => {
    if (evt.detail.target.id === "main-panel") {
      initCharts();
    }
  });
});

let tsChart, matrixChart, cal;

function initCharts() {
  initTimeSeriesChart();
  initMatrixChart();
  initCalendarHeatmap();
}

function buildUrl(pathSuffix) {
  const base = window.location.pathname.replace(/\/$/, "");
  return `${base}${pathSuffix}${window.location.search}`;
}

function initTimeSeriesChart() {
  const canvas = document.getElementById("ts-chart");
  if (!canvas) return;
  if (tsChart) tsChart.destroy();

  fetch(buildUrl("/api/time-series/"))
    .then((r) => r.json())
    .then((data) => {
      const ctx = canvas.getContext("2d");
      const gradient = ctx.createLinearGradient(0, 0, 0, 260);
      gradient.addColorStop(0, "rgba(52, 211, 153, 0.25)");
      gradient.addColorStop(1, "rgba(15, 23, 42, 0)");

      tsChart = new Chart(canvas, {
        type: "line",
        data: {
          labels: data.dates,
          datasets: [
            {
              label: "Incidents",
              data: data.counts,
              borderWidth: 2,
              tension: 0.3,
              fill: true,
              backgroundColor: gradient,
              borderColor: "rgba(52, 211, 153, 1)",
              pointRadius: 0,
            },
            {
              label: "Baseline",
              data: data.baseline,
              borderWidth: 1,
              borderDash: [4, 4],
              tension: 0.3,
              borderColor: "rgba(148, 163, 184, 0.9)",
              pointRadius: 0,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              grid: { display: false },
              ticks: {
                maxTicksLimit: 7,
                color: "#64748b",
                font: { size: 10 },
              },
            },
            y: {
              beginAtZero: true,
              grid: { color: "rgba(15, 23, 42, 1)" },
              ticks: {
                color: "#64748b",
                font: { size: 10 },
              },
            },
          },
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                color: "#e5e7eb",
                usePointStyle: true,
                boxWidth: 6,
              },
            },
            tooltip: {
              mode: "index",
              intersect: false,
              callbacks: {
                afterBody(items) {
                  if (!items.length) return;
                  const idx = items[0].dataIndex;
                  const delta = data.delta_percent[idx];
                  const sign = delta >= 0 ? "+" : "";
                  return `Δ vs baseline: ${sign}${delta.toFixed(1)}%`;
                },
              },
            },
          },
          interaction: { mode: "index", intersect: false },
          animation: {
            duration: 600,
            easing: "easeOutQuart",
          },
        },
      });
    });
}

function initMatrixChart() {
  const canvas = document.getElementById("matrix-chart");
  if (!canvas) return;
  if (matrixChart) matrixChart.destroy();

  fetch(buildUrl("/api/matrix/"))
    .then((r) => r.json())
    .then((data) => {
      matrixChart = new Chart(canvas, {
        type: "matrix",
        data: {
          datasets: [
            {
              label: "Incidents",
              data: data.cells, // [{x: hour, y: dow, v: count}, ...]
              width: () => 16,
              height: () => 16,
              backgroundColor: (ctx) => {
                const value = ctx.raw.v || 0;
                const max = data.max || 1;
                const alpha = 0.1 + 0.9 * (value / max);
                return `rgba(52, 211, 153, ${alpha})`;
              },
            },
          ],
        },
        options: {
          maintainAspectRatio: false,
          scales: {
            x: {
              type: "linear",
              position: "bottom",
              ticks: {
                stepSize: 4,
                callback: (v) => `${v}:00`,
                color: "#64748b",
                font: { size: 9 },
              },
              grid: { display: false },
            },
            y: {
              type: "linear",
              ticks: {
                stepSize: 1,
                callback: (v) => data.dow_labels[v] || "",
                color: "#64748b",
                font: { size: 9 },
              },
              grid: { display: false },
            },
          },
          plugins: {
            tooltip: {
              callbacks: {
                title: (items) => {
                  const raw = items[0].raw;
                  return `${data.dow_labels[raw.y]} @ ${raw.x}:00`;
                },
                label: (ctx) => `Incidents: ${ctx.raw.v}`,
              },
            },
            legend: { display: false },
          },
        },
      });
    });
}

function initCalendarHeatmap() {
  const container = document.getElementById("calendar-heatmap");
  if (!container) return;

  if (cal) {
    cal.destroy();
    cal = null;
  }

  cal = new CalHeatmap();
  cal.paint(
    {
      itemSelector: "#calendar-heatmap",
      domain: {
        type: "month",
        gutter: 4,
        label: { position: "top" },
      },
      subDomain: {
        type: "day",
        radius: 2,
        width: 12,
        height: 12,
      },
      range: 4,
      verticalOrientation: true,
      scale: {
        color: {
          type: "linear",
          scheme: "Greens",
          domain: [0, 1],
        },
      },
      data: {
        source: buildUrl("/api/calendar/"),
        x: "date",
        y: "count",
      },
    },
    [
      [
        "Legend",
        {
          label: "Incidents per day",
        },
      ],
    ],
  );
}
