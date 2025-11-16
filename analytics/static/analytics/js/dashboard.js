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
  const hue = 200 - ratio * 120; // blue to green
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

async function loadCalendarHeatmap(heatType) {
  const url = new URL('/api/heatmaps/calendar/', window.location.origin);
  url.searchParams.set('heat_type', heatType);
  const payload = await fetchJSON(url.toString());
  renderCalendarHeatmap(payload, heatType);
}

function renderCalendarHeatmap(payload, heatType) {
  const container = document.getElementById('calendarHeatmapGrid');
  const legend = document.getElementById('calendarHeatmapLegend');
  if (!container || !legend) return;
  container.innerHTML = '';
  legend.textContent = '';
  if (!payload.data || payload.data.length === 0) {
    container.textContent = 'No data available yet.';
    return;
  }
  const values = payload.data.map((point) =>
    typeof point.value === 'number' ? point.value : point.count,
  );
  const min = Math.min(...values);
  const max = Math.max(...values);
  const maxAbs = Math.max(...values.map((v) => Math.abs(v)));
  container.style.gridTemplateColumns = `repeat(${payload.weeks || 52}, 14px)`;
  payload.data.forEach((point) => {
    const value = typeof point.value === 'number' ? point.value : point.count;
    const cell = document.createElement('div');
    cell.className = 'heatmap-cell';
    cell.style.gridColumnStart = point.week_index + 1;
    cell.style.gridRowStart = (point.weekday_number || 0) + 1;
    if (heatType === 'count' || heatType === 'pct_group') {
      cell.style.backgroundColor = getSequentialColor(value, min, max);
    } else {
      cell.style.backgroundColor = getDivergingColor(value, maxAbs);
    }
    cell.title = `${point.date}\nValue: ${value}\nCount: ${point.count}`;
    container.appendChild(cell);
  });
  legend.textContent = `Range ${payload.start_date} → ${payload.end_date} (${payload.data.length} days)`;
}

async function loadTimeOfWeekHeatmap() {
  const payload = await fetchJSON('/api/heatmaps/time-of-week/?window=28d');
  const container = document.getElementById('timeOfWeekHeatmap');
  if (!container) return;
  container.innerHTML = '';
  if (!payload.matrix) {
    container.textContent = 'Awaiting data.';
    return;
  }
  const table = document.createElement('table');
  table.className = 'heatmap-table';
  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  headerRow.innerHTML = '<th>Day</th>' + payload.hour_labels.map((hour) => `<th>${hour}</th>`).join('');
  thead.appendChild(headerRow);
  table.appendChild(thead);
  const tbody = document.createElement('tbody');
  const flatValues = payload.matrix.flat();
  const maxValue = Math.max(...flatValues);
  payload.weekday_labels.forEach((label, rowIndex) => {
    const tr = document.createElement('tr');
    const th = document.createElement('th');
    th.textContent = label;
    tr.appendChild(th);
    payload.matrix[rowIndex].forEach((value) => {
      const td = document.createElement('td');
      td.style.backgroundColor = getSequentialColor(value, 0, maxValue || 1);
      td.title = `${label} hour ${payload.hour_labels[td.cellIndex - 1] || ''}: ${value}`;
      td.textContent = value || '';
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
  container.appendChild(table);
}

async function loadPoissonHeatmap(unit, windowLength) {
  const url = new URL('/api/heatmaps/poisson/', window.location.origin);
  url.searchParams.set('unit', unit);
  url.searchParams.set('window_length', windowLength);
  const payload = await fetchJSON(url.toString());
  const container = document.getElementById('poissonHeatmapTable');
  if (!container) return;
  container.innerHTML = '';
  if (!payload.windows || payload.windows.length === 0) {
    container.textContent = 'No windows available.';
    return;
  }
  const latestWindow = payload.windows[payload.windows.length - 1];
  const rows = [...latestWindow.rows].sort(
    (a, b) => Math.abs(b.z) - Math.abs(a.z),
  );
  const topRows = rows.slice(0, 10);
  const table = document.createElement('table');
  table.className = 'heatmap-table';
  table.innerHTML = `
    <thead>
      <tr>
        <th>${payload.unit === 'beat' ? 'Beat' : 'District'}</th>
        <th>Current</th>
        <th>Previous</th>
        <th>Z</th>
      </tr>
    </thead>
  `;
  const tbody = document.createElement('tbody');
  const maxAbs = Math.max(...topRows.map((row) => Math.abs(row.z)), 0);
  topRows.forEach((row) => {
    const tr = document.createElement('tr');
    const nameTd = document.createElement('td');
    nameTd.textContent = row.unit;
    tr.appendChild(nameTd);
    const currentTd = document.createElement('td');
    currentTd.textContent = row.current;
    tr.appendChild(currentTd);
    const previousTd = document.createElement('td');
    previousTd.textContent = row.past;
    tr.appendChild(previousTd);
    const zTd = document.createElement('td');
    zTd.textContent = row.z.toFixed(2);
    zTd.style.backgroundColor = getDivergingColor(row.z, maxAbs || 1);
    tr.appendChild(zTd);
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
  container.appendChild(table);
  const meta = document.createElement('p');
  meta.className = 'text-xs text-slate-500 mt-2';
  meta.textContent = `Window ${latestWindow.label}`;
  container.appendChild(meta);
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
