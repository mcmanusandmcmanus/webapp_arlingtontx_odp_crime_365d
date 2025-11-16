# Import Console Blueprint (`IMPORT_CONSOLE.md`)

This document tracks the import portal requirements **and** the current code alignment so that we can march toward the full Parse & Preview workflow.

## 0. Implementation Snapshot (2025-11-15)
- DONE: Shared passcode enforced at `/import/` plus CLI management command for deterministic ingest.
- DONE: `ImportBatch` model captures batch date, row counts, and provenance; CLI path bulk loads 16,875 rows from `data/crime_365d.csv`.
- NEXT: File staging + preview table so upload/paste flows can be committed inside the UI (single batch per date).
- NEXT: Automated QA checks (missing beats, duplicates, trend deltas) before commit.
- NEXT: Audit logging when batches are accepted or rejected.

## 1. Goals & Assumptions

- The web application should be updated **daily** by a rotating group of ~10 people.
- Only one person performs the import at a time.
- Source data comes from another **web application** and/or **Excel/CSV** exports.
- There are **4 districts** and **32 beats**.
- The import area is protected by a **single shared passcode** (no per-user accounts).
- Primary goal: support **CSV/Excel upload** as the main method, with optional **copy-paste text** fallback.

## 2. High-Level Import Flow

1. User navigates to `/import/`.
2. Enters **passcode** and **data date**.
3. Chooses one of:
   - Upload one or more **CSV/Excel** files; or
   - Paste table text from the source web app.
4. Clicks **"Parse & Preview"**.
5. Sees a **preview** of parsed records:
   - Sample rows
   - Counts by district/beat
   - Warnings (missing beats, unknown beats, duplicates, etc.)
6. Clicks **"Commit Import"**:
   - A new `ImportBatch` is created.
   - All `Incident` rows are bulk-inserted and linked to that batch.
   - The app ensures only **one committed batch per date**.

CLI fallback (already implemented):
```
python manage.py import_incidents --path data/crime_365d.csv --replace
```

## 3. Simple Authentication (Shared Passcode)

- No user accounts required.
- A single passcode is stored in settings, e.g. `IMPORT_PASSCODE` read from environment.

**View logic (conceptual):**

```python
from django.conf import settings
from django.shortcuts import render

def import_view(request):
    if request.method == "POST":
        passcode = request.POST.get("passcode", "")
        if passcode != settings.IMPORT_PASSCODE:
            return render(request, "import.html", {"error": "Invalid passcode."})
        # If passcode ok: continue with parsing / preview / commit
    else:
        return render(request, "import.html")
```

## 4. Parse & Preview Requirements

- When a file is uploaded or rows are pasted, the backend should parse into structured rows (likely staged in a temporary table or JSON cache keyed by session).
- Run validations:
  - Ensure all 32 beats represented (or flag gaps).
  - Check duplicate case numbers.
  - Compare totals vs previous batch.
- Surface a preview grid plus summary cards before any commit occurs.
- Only after the operator clicks **Commit Import** do we write to `ImportBatch` + `Incident`.

## 5. Future Enhancements

- Webhook or email notifications when a batch is loaded.
- Inline diff vs previous period for quick anomaly detection.
- Ability to tag batches with qualitative notes for Data Science Lab review.
