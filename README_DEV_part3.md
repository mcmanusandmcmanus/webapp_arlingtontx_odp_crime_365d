# Data Science Lab & Evaluation Playbook

This guide translates the True North directives (README_ROADMAP_part0) into concrete engineering tasks for the Data Science Lab, machine learning workflow, and weekly effectiveness tracking.

## 1. Personas and Expectations
- **Executives (City Manager, Council):** want crisp narratives summarizing whether the data science program is delivering on safety outcomes.
- **Police Command / COO:** need the 7/14/28/91/182/365 day comparisons plus creative storytelling as they drill down.
- **Field Patrols:** care about clear signals (what matters vs noise) and recall-friendly metrics.
- **Analysts / Data Science team:** expect transparent EDA, feature engineering, model benchmarking, and a monitoring loop.

## 2. Lab Stages (mirrors the `/lab/` UI)
1. **Stage 1 - Exploratory Data Analysis (EDA)**
   - Extensive univariate/bivariate exploration across key fields (beat, district, offense, time).
   - Scatter plots, boxplots, histograms, rolling line charts for each COO window.
   - Calendar and 24x7 heatmaps (see `README_DEV_part4.md`) surface cadence and anomalies.

2. **Stage 2 - Feature Engineering Lab**
   - Derive time-based features (lag deltas, moving averages, period-over-period change).
   - Build 24x7 buckets, business hours flags, weekend indicators, offense category groupings.
   - Catalog each feature with importance scores and narrative notes that command staff can act on.

3. **Stage 3 - Modeling & Validation**
   - Split into train/test/validation, then run cross-validation.
   - Train multiple model families (baseline counts, ARIMA/Prophet-style, tree ensembles, classification if predicting thresholds).
   - Track hyper-parameters, scoring metrics (precision, recall, F1, accuracy, MAE/MAPE depending on task).
   - Store runs in `ModelRun` (already scaffolded) with metrics JSON for comparison.

4. **Stage 4 - Evaluation Loop**
   - Weekly comparison of forecasts/expectations vs observed incidents.
   - Persist to `EvaluationMetric` with audience labels (Executive, Command, Field, Analyst).
   - Generate narratives: "Beat 450 forecast 22 incidents, observed 24 (+9%)."
   - Feed results back into dashboards and send alerts when drift exceeds thresholds.

## 3. Implementation Checklist

### 3.1 Data Science Infrastructure
- [ ] Create notebooks or scripts that read from Django ORM (or replica CSV) and push results back via management commands.
- [ ] Extend `ModelRun` to capture validation strategy, dataset span, and champion/challenger flags.
- [ ] CLI utility: `python manage.py log_model_run --run-id ... --metrics '{"precision":0.91}'`.

### 3.2 Feature Store Lite
- [ ] Build `analytics/services/features.py` to compute feature sets used in modeling (re-usable between notebooks and API endpoints).
- [ ] Persist feature catalog (JSON) describing each engineered column, source fields, and operational meaning.

### 3.3 Evaluation Automation
- [ ] Scheduled job (Celery beat or cron) calculates expectation vs observed weekly and logs to `EvaluationMetric`.
- [ ] Add `/lab/evaluations/` endpoint with charts/tables summarizing latest effectiveness.
- [ ] Provide download/export (CSV) for command staff briefings.

### 3.4 Access Gates
- Entry gate already implemented; add stage-specific messaging so analysts understand what data is available (EDA vs Modeling vs Evaluation).
- Consider logging lab access requests (simple table) to support "site visitors can request access to admin group" per True North doc.

## 4. Metrics to Track
- **Recall/F1/Precision/Accuracy** for classification tasks (e.g., predicting if a beat will exceed threshold).
- **MAE/MAPE/RMSE** for regression/forecasting tasks (e.g., counts per beat).
- **Top drivers/features** via SHAP or permutation importance.
- **Operational KPIs** such as percent of deployments that matched forecast hot spots.

## 5. Roadmap Hooks
- Integrate the heatmap work (README_DEV_part4.md) into Stage 1 dashboards.
- Tie import QA summaries to Stage 4 so we know if data quality impacted forecasts.
- Document success stories weekly so executives see the value of open-source analytics.
