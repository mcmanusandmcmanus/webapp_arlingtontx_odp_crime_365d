# Django Import Console Design (`IMPORT_CONSOLE.md`)

## 1. Goals & Assumptions

- The web application should be updated **daily** by a rotating group of ~10 people.
- At any given time, **only one person** will perform the import.
- Source data currently comes from another **web application** and/or **Excel/CSV** exports.
- There are **4 districts** and **32 beats**.
- To keep things simple, the import area is protected by a **single shared passcode** (no per-user accounts).
- Primary goal: support **CSV/Excel upload** as the main import method, with optional **copy-paste text** as a fallback.

---

## 2. High-Level Import Flow

1. User navigates to `/import/`.
2. Enters **passcode** and **data date**.
3. Chooses **one of**:
   - Upload one or more **CSV/Excel** files; or
   - Paste table text from the source web app.
4. Clicks **“Parse & Preview”**.
5. Sees a **preview** of parsed records:
   - Sample rows
   - Counts by district/beat
   - Warnings (missing beats, unknown beats, duplicates, etc.)
6. Clicks **“Commit Import”**:
   - A new `ImportBatch` is created.
   - All `Incident` rows are bulk-inserted and linked to that batch.
   - The app ensures only **one committed batch per date**.

---

## 3. Simple Authentication (Shared Passcode)

- No user accounts required.
- A single passcode is stored in settings, e.g. `IMPORT_PASSCODE` read from environment.

**View logic (conceptual):**

```python
# settings.py
IMPORT_PASSCODE = os.environ.get("IMPORT_PASSCODE", "changeme")


# views.py (concept)
from django.conf import settings
from django.shortcuts import render

def import_view(request):
    if request.method == "POST":
        passcode = request.POST.get("passcode", "")
        if passcode != settings.IMPORT_PASSCODE:
            return render(request, "import.html", {
                "error": "Invalid passcode.",
            })
        # If passcode ok: continue with parsing / preview / commit
    else:
        return render(request, "import.html")
