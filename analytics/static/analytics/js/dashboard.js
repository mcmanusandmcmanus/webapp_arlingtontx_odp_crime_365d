(function () {
  let windowComparisonChart;
  let calendarHeatmapInstance;
  let timeOfWeekChart;
  let poissonHeatmapChart;
  let labHourChart;
  let labCategoryChart;
  let labMatrixChart;
  let labModelComparisonChart;
  let labEvaluationChart;

  function resolveContext(canvasId) {
    const canvas = typeof canvasId === "string" ? document.getElementById(canvasId) : canvasId;
    if (!canvas) return null;
    return canvas.getContext("2d");
  }

  function renderWindowComparisonChart(canvasId, payload) {
    const ctx = resolveContext(canvasId);
    if (!ctx || !payload || !payload.labels) return;
    if (windowComparisonChart) {
      windowComparisonChart.destroy();
    }
    const gradient = ctx.createLinearGradient(0, 0, 0, 260);
    gradient.addColorStop(0, "rgba(16, 185, 129, 0.45)");
    gradient.addColorStop(1, "rgba(15, 23, 42, 0)");
    windowComparisonChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: payload.labels,
        datasets: [
          {
            label: "Current",
            data: payload.current,
            backgroundColor: gradient,
            borderRadius: 8,
          },
          {
            label: "Previous",
            data: payload.previous,
            backgroundColor: "rgba(148, 163, 184, 0.35)",
            borderRadius: 8,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: {
              color: "#cbd5f5",
              usePointStyle: true,
            },
          },
          tooltip: {
            mode: "index",
            intersect: false,
          },
        },
        scales: {
          x: {
            ticks: { color: "#94a3b8" },
            grid: { display: false },
          },
          y: {
            ticks: { color: "#94a3b8" },
            grid: { color: "rgba(148, 163, 184, 0.1)" },
            beginAtZero: true,
          },
        },
      },
    });
  }

  function renderBarChart(canvasId, payload) {
    const ctx = resolveContext(canvasId);
    if (!ctx || !payload) return;
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: payload.labels,
        datasets: [
          {
            label: "Current",
            data: payload.current,
            backgroundColor: "rgba(14, 165, 233, 0.7)",
          },
          {
            label: "Previous",
            data: payload.previous,
            backgroundColor: "rgba(99, 102, 241, 0.5)",
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true },
        },
      },
    });
  }

  function renderLineChart(canvasId, payload) {
    const ctx = resolveContext(canvasId);
    if (!ctx || !payload) return;
    new Chart(ctx, {
      type: "line",
      data: {
        labels: payload.labels,
        datasets: [
          {
            label: "Incidents per day",
            data: payload.counts,
            borderColor: "rgb(59, 130, 246)",
            backgroundColor: "rgba(59, 130, 246, 0.15)",
            tension: 0.25,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true },
        },
      },
    });
  }

  async function fetchJSON(url) {
    const response = await fetch(url, {
      headers: { Accept: "application/json" },
      credentials: "same-origin",
    });
    if (!response.ok) {
      throw new Error(`Request failed (${response.status})`);
    }
    return response.json();
  }

  function getSequentialColor(value, min, max) {
    if (max === min) return "rgba(37, 99, 235, 0.3)";
    const ratio = (value - min) / (max - min);
    const hue = 200 - ratio * 120;
    return `hsl(${hue}, 70%, ${65 - ratio * 25}%)`;
  }

  function getDivergingColor(value, maxAbs) {
    if (maxAbs === 0) return "rgba(148, 163, 184, 0.5)";
    const ratio = Math.min(Math.abs(value) / maxAbs, 1);
    const lightness = 65 - ratio * 30;
    return value >= 0 ? `hsl(12, 85%, ${lightness}%)` : `hsl(210, 80%, ${lightness}%)`;
  }

  function renderCalendarHeatmap(payload, heatType) {
    const legend = document.getElementById("calendarHeatmapLegend");
    if (!payload || !legend) return;
    if (!payload.data || payload.data.length === 0) {
      legend.textContent = "No data available yet.";
      return;
    }
    const dataset = payload.data.map((point) => ({
      date: new Date(point.date),
      value: typeof point.value === "number" ? point.value : point.count,
      count: point.count,
    }));
    const values = dataset.map((d) => d.value);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const maxAbs = Math.max(...values.map((v) => Math.abs(v)));
    if (!calendarHeatmapInstance) {
      calendarHeatmapInstance = new CalHeatmap();
    }
    calendarHeatmapInstance.paint({
      itemSelector: "#calendarHeatmapGrid",
      theme: "dark",
      animationDuration: 400,
      data: {
        source: dataset,
        x: (d) => d.date,
        y: (d) => d.value,
      },
      range: Math.max(1, Math.ceil(dataset.length / 7)),
      domain: {
        type: "month",
        gutter: 4,
        label: { text: "MMM yyyy", position: "top" },
      },
      subDomain: {
        type: "day",
        width: 16,
        height: 16,
        radius: 4,
        gutter: 3,
      },
      scale: {
        color:
          heatType === "count" || heatType === "pct_group"
            ? {
                type: "linear",
                domain: [min, max],
                range: ["#134e4a", "#2dd4bf", "#a7f3d0"],
              }
            : {
                type: "linear",
                domain: [-maxAbs, 0, maxAbs],
                range: ["#f43f5e", "#e2e8f0", "#0ea5e9"],
              },
      },
      tooltip: {
        text: (timestamp, value) => {
          const day = new Date(timestamp);
          return `${day.toLocaleDateString(undefined, {
            weekday: "short",
            month: "short",
            day: "numeric",
          })}<br/>Value: ${value ?? 0}`;
        },
      },
    });
    legend.textContent = `Range ${payload.start_date} - ${payload.end_date} (${payload.data.length} days)`;
  }

  async function loadCalendarHeatmap(heatType) {
    const url = new URL("/api/heatmaps/calendar/", window.location.origin);
    url.searchParams.set("heat_type", heatType);
    const payload = await fetchJSON(url.toString());
    renderCalendarHeatmap(payload, heatType);
  }

  function setupCalendarHeatmapControl() {
    const calendarSelect = document.getElementById("calendarHeatType");
    if (!calendarSelect) return;
    const handler = () =>
      loadCalendarHeatmap(calendarSelect.value).catch((err) =>
        console.error("Calendar heatmap error", err),
      );
    calendarSelect.addEventListener("change", handler);
  }

  function renderTimeOfWeekHeatmap(payload) {
    const canvas = document.getElementById("timeOfWeekHeatmapCanvas");
    if (!canvas || !payload?.matrix) return;
    const ctx = canvas.getContext("2d");
    const data = [];
    const flatValues = payload.matrix.flat();
    const maxValue = Math.max(...flatValues, 1);
    payload.weekday_labels.forEach((day, rowIndex) => {
      payload.matrix[rowIndex].forEach((value, colIndex) => {
        data.push({
          x: payload.hour_labels[colIndex],
          y: day,
          v: value,
        });
      });
    });
    if (timeOfWeekChart) {
      timeOfWeekChart.destroy();
    }
    timeOfWeekChart = new Chart(ctx, {
      type: "matrix",
      data: {
        datasets: [
          {
            label: "Incidents",
            data,
            backgroundColor: (context) => {
              const value = context.raw.v || 0;
              return getSequentialColor(value, 0, maxValue);
            },
            width: () => 18,
            height: () => 18,
            borderWidth: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          tooltip: {
            callbacks: {
              title: (items) => {
                const item = items[0];
                return `${item.raw.y}, hour ${item.raw.x}`;
              },
              label: (item) => `Incidents: ${item.raw.v}`,
            },
          },
          legend: { display: false },
        },
        scales: {
          x: {
            type: "category",
            labels: payload.hour_labels,
            grid: { display: false },
            ticks: { color: "#94a3b8", autoSkip: true, maxTicksLimit: 12 },
            title: { display: true, text: "Hour of Day", color: "#cbd5f5" },
          },
          y: {
            type: "category",
            labels: payload.weekday_labels,
            grid: { display: false },
            reverse: true,
            ticks: { color: "#94a3b8" },
            title: { display: true, text: "Day of Week", color: "#cbd5f5" },
          },
        },
      },
    });
  }

  async function loadTimeOfWeekHeatmap() {
    const payload = await fetchJSON("/api/heatmaps/time-of-week/?window=28d");
    renderTimeOfWeekHeatmap(payload);
  }

  async function loadPoissonHeatmap(unit, windowLength) {
    const url = new URL("/api/heatmaps/poisson/", window.location.origin);
    url.searchParams.set("unit", unit);
    url.searchParams.set("window_length", windowLength);
    const payload = await fetchJSON(url.toString());
    const canvas = document.getElementById("poissonHeatmapCanvas");
    const meta = document.getElementById("poissonHeatmapMeta");
    if (!canvas || !payload.windows || payload.windows.length === 0) return;
    const ctx = canvas.getContext("2d");
    const windows = payload.windows.slice(-8);
    const windowLabels = windows.map((w) => `W${w.id}`);
    const unitSet = new Set();
    windows.forEach((w) => w.rows.forEach((row) => unitSet.add(row.unit)));
    const units = Array.from(unitSet).sort();
    const data = [];
    let maxAbs = 0;
    windows.forEach((window, windowIndex) => {
      units.forEach((unitName) => {
        const row = window.rows.find((r) => r.unit === unitName) || { current: 0, past: 0, z: 0 };
        maxAbs = Math.max(maxAbs, Math.abs(row.z));
        data.push({
          x: windowLabels[windowIndex],
          windowLabel: window.label,
          y: unitName,
          v: row.z,
          current: row.current,
          past: row.past,
        });
      });
    });
    if (poissonHeatmapChart) {
      poissonHeatmapChart.destroy();
    }
    poissonHeatmapChart = new Chart(ctx, {
      type: "matrix",
      data: {
        datasets: [
          {
            label: "Z-score",
            data,
            backgroundColor: (context) => {
              const value = context.raw.v;
              return getDivergingColor(value, maxAbs || 1);
            },
            borderWidth: 0,
            width: () => 28,
            height: () => 24,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          tooltip: {
            callbacks: {
              title: (items) => {
                const raw = items[0].raw;
                return `${raw.y} | ${raw.windowLabel}`;
              },
              label: (item) => {
                const raw = item.raw;
                return [`Z: ${raw.v.toFixed(2)}`, `Current: ${raw.current}`, `Previous: ${raw.past}`];
              },
            },
          },
          legend: { display: false },
        },
        scales: {
          x: {
            type: "category",
            labels: windowLabels,
            grid: { display: false },
            title: { display: true, text: "Rolling Windows", color: "#cbd5f5" },
          },
          y: {
            type: "category",
            labels: units,
            grid: { display: false },
            title: {
              display: true,
              text: payload.unit === "beat" ? "Beat" : "District",
              color: "#cbd5f5",
            },
          },
        },
      },
    });
    if (meta) {
      meta.textContent = `Latest window: ${windows[windows.length - 1].label} | Unit: ${payload.unit}`;
    }
  }

  function initPoissonHeatmapControls() {
    const unitSelect = document.getElementById("poissonUnitSelect");
    const windowSelect = document.getElementById("poissonWindowSelect");
    if (!unitSelect || !windowSelect) return;
    const reload = () =>
      loadPoissonHeatmap(unitSelect.value, windowSelect.value).catch((err) =>
        console.error("Poisson heatmap error", err),
      );
    reload();
    unitSelect.addEventListener("change", reload);
    windowSelect.addEventListener("change", reload);
  }

  function initHeatmaps() {
    const calendarSelect = document.getElementById("calendarHeatType");
    if (calendarSelect) {
      loadCalendarHeatmap(calendarSelect.value).catch((err) =>
        console.error("Calendar heatmap error", err),
      );
      setupCalendarHeatmapControl();
    }
    loadTimeOfWeekHeatmap().catch((err) => console.error("24x7 heatmap error", err));
    initPoissonHeatmapControls();
  }

  function hydrateJsonScript(id) {
    const el = document.getElementById(id);
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch (error) {
      console.warn(`Failed to parse JSON in script#${id}`, error);
      return null;
    }
  }

  function initOverview(config) {
    if (!config) return;
    if (config.windowChart) {
      renderWindowComparisonChart("windowComparisonChart", config.windowChart);
    }
    if (config.calendarPayload) {
      renderCalendarHeatmap(config.calendarPayload, config.calendarPayload.heat_type || "count");
    } else {
      loadCalendarHeatmap("count").catch((err) => console.error("Calendar heatmap error", err));
    }
    setupCalendarHeatmapControl();
    if (config.matrixPayload) {
      renderTimeOfWeekHeatmap(config.matrixPayload);
    } else {
      loadTimeOfWeekHeatmap().catch((err) => console.error("24x7 heatmap error", err));
    }
    initPoissonHeatmapControls();
  }

  function renderLabHourChart(payload) {
    const ctx = resolveContext("labHourChart");
    if (!ctx || !payload?.hours) return;
    if (labHourChart) labHourChart.destroy();
    labHourChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: payload.hours.labels,
        datasets: [
          {
            label: `${payload.window_label} incidents`,
            data: payload.hours.counts,
            borderColor: "#34d399",
            backgroundColor: "rgba(52, 211, 153, 0.15)",
            tension: 0.3,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            ticks: { color: "#94a3b8", callback: (v) => `${v}:00` },
            grid: { display: false },
          },
          y: {
            ticks: { color: "#94a3b8" },
            grid: { color: "rgba(148, 163, 184, 0.1)" },
            beginAtZero: true,
          },
        },
        plugins: {
          legend: { display: false },
        },
      },
    });
  }

  function renderLabCategoryChart(payload) {
    const ctx = resolveContext("labCategoryChart");
    if (!ctx || !payload?.offense_categories) return;
    if (labCategoryChart) labCategoryChart.destroy();
    labCategoryChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: payload.offense_categories.labels,
        datasets: [
          {
            label: "Incidents",
            data: payload.offense_categories.counts,
            backgroundColor: "rgba(129, 140, 248, 0.7)",
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: "y",
        scales: {
          x: {
            ticks: { color: "#94a3b8" },
            grid: { color: "rgba(148, 163, 184, 0.1)" },
            beginAtZero: true,
          },
          y: {
            ticks: { color: "#94a3b8" },
            grid: { display: false },
          },
        },
        plugins: {
          legend: { display: false },
        },
      },
    });
  }

  function renderLabMatrix(payload) {
    const ctx = resolveContext("labDistrictMatrix");
    if (!ctx || !payload?.district_matrix?.cells?.length) return;
    if (labMatrixChart) labMatrixChart.destroy();
    const cells = payload.district_matrix.cells;
    const maxValue = Math.max(...cells.map((cell) => cell.v || 0), 1);
    labMatrixChart = new Chart(ctx, {
      type: "matrix",
      data: {
        datasets: [
          {
            label: "Incidents",
            data: cells,
            backgroundColor: (context) => {
              const value = context.raw.v || 0;
              return getSequentialColor(value, 0, maxValue);
            },
            width: (ctx) => {
              const area = ctx.chart.chartArea || { width: 0 };
              const length = Math.max(payload.district_matrix.beats.length, 1);
              return Math.max(area.width / length - 4, 6);
            },
            height: (ctx) => {
              const area = ctx.chart.chartArea || { height: 0 };
              const length = Math.max(payload.district_matrix.districts.length, 1);
              return Math.max(area.height / length - 4, 6);
            },
            borderWidth: 0,
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              title: (items) => {
                const raw = items[0].raw;
                return `${raw.y} | ${raw.x}`;
              },
              label: (item) => `Incidents: ${item.raw.v}`,
            },
          },
        },
        scales: {
          x: {
            type: "category",
            labels: payload.district_matrix.beats,
            grid: { display: false },
            ticks: { color: "#94a3b8" },
          },
          y: {
            type: "category",
            labels: payload.district_matrix.districts,
            grid: { display: false },
            ticks: { color: "#94a3b8" },
          },
        },
      },
    });
  }

  function renderModelComparisonChart(payload) {
    const ctx = resolveContext("modelComparisonChart");
    if (!ctx || !payload?.labels?.length) return;
    if (labModelComparisonChart) labModelComparisonChart.destroy();
    labModelComparisonChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: payload.labels,
        datasets: [
          {
            label: "Precision",
            data: payload.precision,
            backgroundColor: "rgba(59, 130, 246, 0.7)",
            borderRadius: 6,
          },
          {
            label: "Recall",
            data: payload.recall,
            backgroundColor: "rgba(16, 185, 129, 0.7)",
            borderRadius: 6,
          },
          {
            label: "F1",
            data: payload.f1,
            backgroundColor: "rgba(249, 115, 22, 0.7)",
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            ticks: { color: "#94a3b8" },
            grid: { display: false },
          },
          y: {
            ticks: { color: "#94a3b8" },
            grid: { color: "rgba(148, 163, 184, 0.1)" },
            beginAtZero: true,
            suggestedMax: 1,
          },
        },
        plugins: {
          legend: {
            labels: { color: "#cbd5f5" },
          },
        },
      },
    });
  }

  function renderEvaluationChart(payload) {
    const ctx = resolveContext("evaluationChart");
    if (!ctx || !payload?.labels?.length) return;
    if (labEvaluationChart) labEvaluationChart.destroy();
    labEvaluationChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: payload.labels,
        datasets: [
          {
            type: "line",
            label: "Expected",
            data: payload.expected,
            borderColor: "#38bdf8",
            backgroundColor: "rgba(56, 189, 248, 0.2)",
            tension: 0.3,
            fill: false,
            yAxisID: "y",
          },
          {
            type: "line",
            label: "Observed",
            data: payload.observed,
            borderColor: "#fbbf24",
            backgroundColor: "rgba(251, 191, 36, 0.2)",
            tension: 0.3,
            fill: false,
            yAxisID: "y",
          },
          {
            type: "bar",
            label: "Delta %",
            data: payload.delta_pct,
            backgroundColor: (ctx) => {
              const value = ctx.raw || 0;
              return value >= 0 ? "rgba(16, 185, 129, 0.6)" : "rgba(248, 113, 113, 0.6)";
            },
            borderRadius: 4,
            yAxisID: "y1",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            position: "left",
            grid: { color: "rgba(148, 163, 184, 0.1)" },
            ticks: { color: "#94a3b8" },
            beginAtZero: false,
          },
          y1: {
            position: "right",
            grid: { display: false },
            ticks: { color: "#94a3b8", callback: (value) => `${value}%` },
          },
          x: {
            ticks: { color: "#94a3b8" },
            grid: { display: false },
          },
        },
        plugins: {
          tooltip: {
            mode: "index",
            intersect: false,
          },
          legend: {
            labels: { color: "#cbd5f5" },
          },
        },
      },
    });
  }

  function initLab(config) {
    if (!config) return;
    if (config.edaPayload) {
      renderLabHourChart(config.edaPayload);
      renderLabCategoryChart(config.edaPayload);
      renderLabMatrix(config.edaPayload);
    }
    if (config.modelChart) {
      renderModelComparisonChart(config.modelChart);
    }
    if (config.evaluationChart) {
      renderEvaluationChart(config.evaluationChart);
    }
  }

  window.DashboardCharts = {
    renderBarChart,
    renderLineChart,
    initHeatmaps,
  };

  window.CrimeDashboard = {
    initOverview,
    initLab,
    hydrateJsonScript,
    renderWindowComparison: renderWindowComparisonChart,
    renderCalendarFromPayload: (payload) => renderCalendarHeatmap(payload, payload?.heat_type || "count"),
    renderMatrixFromPayload: renderTimeOfWeekHeatmap,
  };
})();
