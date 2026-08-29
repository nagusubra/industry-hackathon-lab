# Data Guide — Calgary Building Retrofit Ranker (Case 2)

A cleaned latest-year extract is already in this folder.

---

## Bundled seed

| File | What it is |
|---|---|
| `calgary_city_buildings_latest_year.csv` | City-owned buildings, latest reporting year in the Open Calgary file (2024 in this seed) |

Columns include `property_name`, `address`, `property_type`, `year_built`, `floor_area_m2`, `site_energy_gj`, `site_eui_gj_per_m2`, `ghg_tco2e`, `energy_star_score`.

Drop rows you cannot score. State any cost assumption (the City file has no retrofit cost column).

---

## Primary source

**City of Calgary-Owned Buildings: Environmental Performance Metrics**

- **Portal:** https://data.calgary.ca/Environment/City-of-Calgary-Owned-Buildings-Environmental-Perf/r5x7-cju4
- **CSV:** `https://data.calgary.ca/api/views/r5x7-cju4/rows.csv?accessType=DOWNLOAD`
- **Licence:** [Open Government Licence — City of Calgary](https://data.calgary.ca/stories/s/Open-Calgary-Terms-of-Use/u45n-7awa)

Optional join: [Corporate Energy Consumption](https://data.calgary.ca/Environment/Corporate-Energy-Consumption/crbp-innf) — that extract is large; do not commit it.

---

## Loading example

```python
import pandas as pd

df = pd.read_csv("data/calgary_city_buildings_latest_year.csv")
print(df.head(3))
print(df["site_eui_gj_per_m2"].describe())
```

---

## Citation

The City of Calgary. Open Calgary — City of Calgary-Owned Buildings: Environmental Performance Metrics. https://data.calgary.ca/Environment/City-of-Calgary-Owned-Buildings-Environmental-Perf/r5x7-cju4
