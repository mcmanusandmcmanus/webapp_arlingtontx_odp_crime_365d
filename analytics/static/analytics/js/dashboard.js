function renderBarChart(canvasId, payload) {
  const ctx = document.getElementById(canvasId);
  if (!ctx || !payload) return;
  const { labels, current, previous } = payload;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Current',
          data: current,
          backgroundColor: 'rgba(14, 165, 233, 0.7)',
        },
        {
          label: 'Previous',
          data: previous,
          backgroundColor: 'rgba(99, 102, 241, 0.5)',
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}

function renderLineChart(canvasId, payload) {
  const ctx = document.getElementById(canvasId);
  if (!ctx || !payload) return;
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: payload.labels,
      datasets: [
        {
          label: 'Incidents per day',
          data: payload.counts,
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: 'rgba(59, 130, 246, 0.15)',
          tension: 0.25,
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}

async function fetchJSON(url) {
  const response = await fetch(url, {
    headers: {
      'Accept': 'application/json',
    },
    credentials: 'same-origin',
  });
  if (!response.ok) {
    throw new Error(`Request failed (${response.status})`);
  }
  return response.json();
}

function getSequentialColor(value, min, max) {
  if (max === min) return 'rgba(37, 99, 235, 0.3)';
  const ratio = (value - min) / (max - min);
  const hue = 200 - ratio * 120;
  return `hsl(${hue}, 70%, ${65 - ratio * 25}%)`;
}

function getDivergingColor(value, maxAbs) {
  if (maxAbs === 0) return 'rgba(148, 163, 184, 0.5)';
  const ratio = Math.min(Math.abs(value) / maxAbs, 1);
  const lightness = 65 - ratio * 30;
  return value >= 0
    ? `hsl(12, 85%, ${lightness}%)`
    : `hsl(210, 80%, ${lightness}%)`;
}

let calendarHeatmapInstance;

async function loadCalendarHeatmap(heatType) {
  const url = new URL('/api/heatmaps/calendar/', window.location.origin);
  url.searchParams.set('heat_type', heatType);
  const payload = await fetchJSON(url.toString());
  renderCalendarHeatmap(payload, heatType);
}

function renderCalendarHeatmap(payload, heatType) {
  const legend = document.getElementById('calendarHeatmapLegend');
  if (!legend) return;
  if (!payload.data || payload.data.length === 0) {
    legend.textContent = 'No data available yet.';
    return;
  }

  const dataset = payload.data.map((point) => ({
    date: new Date(point.date),
    value: typeof point.value === 'number' ? point.value : point.count,
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
    itemSelector: '#calendarHeatmapGrid',
    theme: 'light',
    animationDuration: 400,
    data: {
      source: dataset,
      x: (d) => d.date,
      y: (d) => d.value,
    },
    date: {
      start: dataset[0].date,
      end: dataset[dataset.length - 1].date,
    },
    range: Math.ceil(dataset.length / 7),
    domain: {
      type: 'month',
      gutter: 4,
      label: { text: 'MMM yyyy', position: 'top' },
    },
    subDomain: {
      type: 'day',
      width: 16,
      height: 16,
      radius: 4,
      gutter: 3,
      label: (value) => value.toLocaleDateString(undefined, { day: 'numeric' }),
    },
    scale: {
      color: heatType === 'count' || heatType === 'pct_group'
        ? {
            type: 'linear',
            domain: [min, max],
            range: ['#bae6fd', '#0284c7'],
          }
        : {
            type: 'linear',
            domain: [-maxAbs, 0, maxAbs],
            range: ['#f43f5e', '#e2e8f0', '#0ea5e9'],
          },
    },
    tooltip: {
      text: (timestamp, value) => {
        const day = new Date(timestamp);
        return `${day.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}<br>
            Value: ${value ?? 0}`;
      },
    },
  });
  legend.textContent = `Range ${payload.start_date} → ${payload.end_date} (${payload.data.length} days)`;
}

let timeOfWeekChart;

async function loadTimeOfWeekHeatmap() {
  const payload = await fetchJSON('/api/heatmaps/time-of-week/?window=28d');
  const canvas = document.getElementById('timeOfWeekHeatmapCanvas');
  if (!canvas || !payload.matrix) return;
  const ctx = canvas.getContext('2d');
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
    type: 'matrix',
    data: {
      datasets: [
        {
          label: 'Incidents',
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
          type: 'category',
          labels: payload.hour_labels,
          grid: { display: false },
          title: { display: true, text: 'Hour of Day' },
        },
        y: {
          type: 'category',
          labels: payload.weekday_labels,
          grid: { display: false },
          reverse: true,
          title: { display: true, text: 'Day of Week' },
        },
      },
    },
  });
}

let poissonHeatmapChart;

async function loadPoissonHeatmap(unit, windowLength) {
  const url = new URL('/api/heatmaps/poisson/', window.location.origin);
  url.searchParams.set('unit', unit);
  url.searchParams.set('window_length', windowLength);
  const payload = await fetchJSON(url.toString());
  const canvas = document.getElementById('poissonHeatmapCanvas');
  const meta = document.getElementById('poissonHeatmapMeta');
  if (!canvas || !payload.windows || payload.windows.length === 0) return;
  const ctx = canvas.getContext('2d');
  const windows = payload.windows.slice(-8);
  const windowLabels = windows.map((w) => `W${w.id}`);
  const unitSet = new Set();
  windows.forEach((w) => w.rows.forEach((row) => unitSet.add(row.unit)));
  const units = Array.from(unitSet).sort();
  const data = [];
  let maxAbs = 0;
  windows.forEach((window, windowIndex) => {
    units.forEach((unitName) => {
      const row =
        window.rows.find((r) => r.unit === unitName) ||
        { current: 0, past: 0, z: 0 };
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
    type: 'matrix',
    data: {
      datasets: [
        {
          label: 'Z-score',
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
              return [
                `Z: ${raw.v.toFixed(2)}`,
                `Current: ${raw.current}`,
                `Previous: ${raw.past}`,
              ];
            },
          },
        },
        legend: { display: false },
      },
      scales: {
        x: {
          type: 'category',
          labels: windowLabels,
          grid: { display: false },
          title: { display: true, text: 'Rolling Windows' },
        },
        y: {
          type: 'category',
          labels: units,
          grid: { display: false },
          title: { display: true, text: payload.unit === 'beat' ? 'Beat' : 'District' },
        },
      },
    },
  });
  if (meta) {
    meta.textContent = `Latest window: ${windows[windows.length - 1].label} • unit: ${payload.unit}`;
  }
}

function initHeatmaps() {
  const calendarSelect = document.getElementById('calendarHeatType');
  if (calendarSelect) {
    loadCalendarHeatmap(calendarSelect.value).catch((err) =>
      console.error('Calendar heatmap error', err),
    );
    calendarSelect.addEventListener('change', () => {
      loadCalendarHeatmap(calendarSelect.value).catch((err) =>
        console.error('Calendar heatmap error', err),
      );
    });
  }
  loadTimeOfWeekHeatmap().catch((err) =>
    console.error('24x7 heatmap error', err),
  );
  const unitSelect = document.getElementById('poissonUnitSelect');
  const windowSelect = document.getElementById('poissonWindowSelect');
  if (unitSelect && windowSelect) {
    const reload = () =>
      loadPoissonHeatmap(unitSelect.value, windowSelect.value).catch((err) =>
        console.error('Poisson heatmap error', err),
      );
    reload();
    unitSelect.addEventListener('change', reload);
    windowSelect.addEventListener('change', reload);
  }
}

window.DashboardCharts = {
  renderBarChart,
  renderLineChart,
  initHeatmaps,
};
