# Data Guide — Alberta Wind vs Demand (Case 3)

The same 2024 hourly seed as Case 1 is in this folder (`wind_mw` is the column you need).

---

## Bundled seed

| File | What it is |
|---|---|
| `aeso_hourly_2024.csv` | Hourly 2024 AIL, pool price, and summed wind metered MW |

Define a “tight” hour however you can explain it (for example high AIL and low `wind_mw / ail_mw`). Beat yesterday-same-hour persistence.

---

## Primary source

Same AESO hourly metered-volume pack as Case 1:

https://www.aeso.ca/market/market-and-system-reporting/data-requests/hourly-generation-metered-volumes-and-pool-price-and-ail-data-2001-to-july-2025/

Wind in the seed is the sum of CSD **WIND** asset codes present in the 2020–2025 CSV.

---

## Optional: Calgary weather (ECCC)

Hourly climate for Calgary International:

- Portal: https://climate.weather.gc.ca/historical_data/search_historic_data_e.html
- Bulk CSV pattern: `https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=<id>&Year=<Y>&Month=<M>&timeframe=1`

Join on local date-hour. If the join is painful, skip weather; AESO alone is enough.

---

## Loading example

```python
import pandas as pd

df = pd.read_csv("data/aeso_hourly_2024.csv", parse_dates=["timestamp"])
df["wind_share"] = df["wind_mw"] / df["ail_mw"]
print(df[["timestamp", "ail_mw", "wind_mw", "wind_share", "pool_price_cad_per_mwh"]].head())
```

---

## Citation

Alberta Electric System Operator (AESO). Hourly Generation Metered Volumes and Pool Price and AIL.  
Environment and Climate Change Canada. Historical Climate Data — Calgary area stations (if used).
