# Data Guide — Interconnection-Queue Risk-Triage Agent (Case 6)

This case uses Lawrence Berkeley National Laboratory’s **Queued Up** project-level interconnection workbook (data through end of 2025). Download locally into `data/raw/` — do **not** commit the Excel file (~15 MB) to GitHub.

---

## Primary Data Source

- **Landing page (always current edition):** https://emp.lbl.gov/queues  
- **2026 edition publication:** https://emp.lbl.gov/publications/queued-2026-edition-characteristics  
- **What:** Cleaned interconnection requests from 7 ISO/RTOs and ~50 non-ISO balancing areas (~98% of U.S. installed generating capacity). Generation and storage seeking **transmission** interconnection only (not distribution / BTM / load interconnection).
- **Workbook contents:** (a) project-level request table, (b) codebook / data dictionary, (c) summary metric tabs.
- **Access:** **No login.** Click the attachment **Queued Up 2026 Data File XLSX (~14.85 MB)** on the landing page.
- **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribute Lawrence Berkeley National Laboratory and GridTracker.

---

## Download Steps

1. Open https://emp.lbl.gov/queues
2. Under **Attachment**, click **Queued Up 2026 Data File XLSX** (about 15 MB).
3. Save the file as `data/raw/lbnl-queues/queued_up_2026.xlsx` (create the folders if needed).

**Windows (PowerShell)** — after the browser download, move it:

```powershell
New-Item -ItemType Directory -Force -Path data\raw\lbnl-queues | Out-Null
Move-Item -Force "$env:USERPROFILE\Downloads\*Queued*2026*.xlsx" data\raw\lbnl-queues\queued_up_2026.xlsx
```

If LBNL posts a new filename, keep the URL above as the source of truth and rename locally to `queued_up_2026.xlsx`.

```
data/
├── README.md
└── raw/
    └── lbnl-queues/
        └── queued_up_2026.xlsx
```

`agent_starter.py` looks for that path. If the workbook is missing it writes **`data/raw/lbnl-queues/demo_queue.csv`** and prints a `[warn]` — synthetic, not LBNL data.

---

## Typical Schema

Open the **codebook** (data dictionary) tab first and map columns. Names vary slightly by edition; after download, align to:

| Logical field | Typical meaning |
|---|---|
| Project / queue ID | Unique request identifier |
| Balancing area / ISO | PJM, MISO, CAISO, ERCOT, SPP, NYISO, ISO-NE, or utility BA |
| State / county | Location of the point of interconnection |
| Resource type | Solar, wind, storage, gas, hybrid, nuclear, other (hybrids may have two MW fields) |
| Capacity (MW) | Requested capacity; hybrids may split MW_1 / MW_2 |
| Queue / IR date | Date the request entered the queue |
| Status / outcome | Active, withdrawn, operational (COD), suspended, etc. |
| Withdrawal date / COD date | Used for labels and duration — **do not use as training features for a model that must score a live request** |

**Label construction (recommended):**

- Positive operational class: status indicates commercial operation / COD.
- Withdrawn class: withdrawn / cancelled.
- Active / suspended: censored for classification; usable in survival models.

**Leakage:** train only on features known at queue entry (or at a declared decision date). Do not feed COD year, IA execution date after the decision, or current status text into a “prediction” of that same status.

---

## Loading Example (Python)

Run from the case folder. Requires `openpyxl` (listed in `requirements.txt`).

```python
import pandas as pd
from pathlib import Path

xlsx = Path("data/raw/lbnl-queues/queued_up_2026.xlsx")
sheets = pd.ExcelFile(xlsx).sheet_names
print(sheets)

# Inspect the codebook tab (name varies — pick the dictionary-like sheet)
for name in sheets:
    if "code" in name.lower() or "dict" in name.lower() or "field" in name.lower():
        print("codebook sheet:", name)
        print(pd.read_excel(xlsx, sheet_name=name).head())

projects = pd.read_excel(xlsx, sheet_name=0)
print(projects.columns.tolist()[:30])
print(len(projects), "rows")
```

Day-one recommendation: one ISO (e.g. **PJM** or **MISO**) plus completed/withdrawn rows only, before modeling the full U.S. workbook.

---

## License & Use Terms

Queued Up Data File. Copyright (c) 2026, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Dept. of Energy) & GridTracker. **CC BY 4.0**.

You may use, share, or adapt the dataset with attribution to **Lawrence Berkeley National Laboratory and GridTracker**.

---

## Suggested Local Layout

This lab already gitignores `**/data/raw/`.

---

## Citation Notes

Rand, J., Cheyette, A., Talley, C., Zhang, S., Gorman, W., Wiser, R. H., Seel, J., Jeong, S., & Kahrl, F. (2026). *Queued Up: 2026 Edition, Characteristics of Power Plants Seeking Transmission Interconnection As of the End of 2025*. Lawrence Berkeley National Laboratory. https://emp.lbl.gov/queues
