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

window.DashboardCharts = {
  renderBarChart,
  renderLineChart,
};
