# Data Guide — Alberta Peak-Price Load-Shift (Case 1)

A seed file is already in this folder. You can start without downloading the multi-year AESO archive.

---

## Bundled seed

| File | What it is |
|---|---|
| `aeso_hourly_2024.csv` | Calendar year 2024, hourly Alberta pool price, Alberta Internal Load (AIL), and summed wind metered volume |

Columns: `timestamp` (AESO `Date_Begin_Local`), `pool_price_cad_per_mwh`, `ail_mw`, `wind_mw`.

`wind_mw` is the sum of AESO plant codes listed as **WIND** on the Current Supply Demand report (29 Aug 2026 snapshot). A few newer assets may be missing in early-2024 hours; treat wind as a useful signal, not a settlement-quality total.

---

## Primary source (full archive)

**AESO — Hourly Generation Metered Volumes and Pool Price and AIL, 2001 to July 2025**

- **Page:** https://www.aeso.ca/market/market-and-system-reporting/data-requests/hourly-generation-metered-volumes-and-pool-price-and-ail-data-2001-to-july-2025/
- **2020–Jul 2025 CSV:** `https://www.aeso.ca/assets/Uploads/data-requests/Hourly_Metered_Volumes_and_Pool_Price_and_AIL_2020-Jul2025.csv`
- **Access:** No login. Educational / personal use under AESO site terms. Do not scrape ETS in a way that overloads it.

Do **not** commit the full ~50 MB file to GitHub. Extra years belong in `data/raw/` (gitignored).

---

## Loading example

```python
import pandas as pd

df = pd.read_csv("data/aeso_hourly_2024.csv", parse_dates=["timestamp"])
print(df.head())
print(df["pool_price_cad_per_mwh"].describe())
```

---

## Citation

Alberta Electric System Operator (AESO). Hourly Generation Metered Volumes and Pool Price and AIL data. https://www.aeso.ca/
