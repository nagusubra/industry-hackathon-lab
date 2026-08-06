# Data Guide — Alberta Grid Real-Time Balancing Agent (Case 4)

This case uses **AESO Energy Trading System (ETS)** public reports and optional API access. Do **not** commit large historical archives to GitHub; download locally into `data/raw/` and document your subset.

---

## Primary Data Sources (AESO)

### 1. Current Supply / Demand Report (real-time snapshot)

- **URL:** https://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet
- **What:** Alberta Internal Load (AIL), generation by fuel type (wind, solar, storage, gas, hydro, etc.), imports/exports, operating reserves.
- **Access:** **No login required** for ETS CSV export.
- **Update frequency:** Near real-time (check AESO for current cadence).

### 2. Historical Reports (pool price, SMP, load, generation)

- **URL:** https://ets.aeso.ca/ets_web/ip/IPHistoricalReportsServlet
- **What:** Historical Pool Price, System Marginal Price (SMP), load, and generation reports.
- **Access:** **No login required** for ETS downloads.
- **Note:** Queries are limited to **≤ 366 days** per request — paginate date ranges for longer histories.

### 3. Optional — AESO JSON API

- **Docs:** https://www.aeso.ca/market/market-and-system-reporting/aeso-application-programming-interface-api/
- **What:** Structured JSON endpoints for market and system data (requires free API key registration).
- **Use:** Automate agent ingestion without manual CSV export.

---

## Download Steps

1. **Current Supply/Demand:** open [CSDReportServlet](https://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet) → click **Submit** → **Save As** CSV → save as `data/raw/aeso/csd_current.csv`.
2. **Pool Price (historical):** open [IPHistoricalReportsServlet](https://ets.aeso.ca/ets_web/ip/IPHistoricalReportsServlet) → select report **Pool Price** → set date range (**≤ 366 days** per request) → click **Submit** → **Save As** CSV → save as `data/raw/aeso/pool_price.csv`. Repeat with paginated date ranges for multi-year history.
3. **Optional — SMP:** same servlet → select **System Marginal Price** → download and save under `data/raw/aeso/` if needed.

```
data/
├── README.md          # this file
└── raw/
    └── aeso/
        ├── csd_current.csv
        └── pool_price.csv
```

---

## Typical Schema

### Current Supply/Demand (CSD)

| Field | Description | Units |
|---|---|---|
| `timestamp` | Report time | datetime |
| `ail_mw` | Alberta Internal Load | MW |
| `wind_mw` | Wind generation | MW |
| `solar_mw` | Solar generation | MW |
| `storage_mw` | Storage net (charge/discharge) | MW |
| `gas_mw` | Gas generation | MW |
| `hydro_mw` | Hydro generation | MW |
| `import_mw` / `export_mw` | Intertie flows | MW |
| `reserve_spin_mw` | Spinning reserve | MW |

Exact column names vary by export — map to the fields above after download.

### Pool Price / SMP Historical

| Field | Description | Units |
|---|---|---|
| `timestamp` | Interval start | datetime |
| `pool_price` | Pool price | $/MWh |
| `smp` | System marginal price | $/MWh |

---

## Loading Example (Python)

Run from the case folder; paths are relative to the case root as `data/raw/...`.

```python
import pandas as pd
from pathlib import Path

csd = Path("data/raw/aeso/csd_current.csv")
df = pd.read_csv(csd)
print(df.head())

price = Path("data/raw/aeso/pool_price.csv")
prices = pd.read_csv(price, parse_dates=["timestamp"])
prices = prices.sort_values("timestamp")
print(prices.tail())
```

---

## License & Use Terms

AESO site terms generally permit **educational and non-commercial** use of publicly published market data — appropriate for this hackathon. **Commercial redistribution or productization** may require explicit permission from AESO; review https://www.aeso.ca/ for current terms.

---

## Suggested Local Layout

Add a `.gitignore` entry for `data/raw/` in your **submission** repo (this lab already ignores `**/data/raw/` at the root).

---

## Citation Notes

When you publish results, cite AESO as the data source and include report timestamps. For API-based ingestion, note the API endpoint and query parameters used.
