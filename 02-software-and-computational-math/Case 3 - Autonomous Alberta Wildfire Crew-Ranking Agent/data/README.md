# Data Guide — Alberta Wildfire Crew Ranking (Case 3)

A 2023–2025 subset of Alberta’s historical wildfire table is already in this folder.

---

## Bundled seed

| File | What it is |
|---|---|
| `alberta_wildfires_2023_2025.csv` | All size-class C/D/E fires from 2023–2025 plus a sample of A/B fires (~850 rows) |

Useful columns: `YEAR`, `FIRE_NUMBER`, `CURRENT_SIZE`, `SIZE_CLASS`, `LATITUDE`, `LONGITUDE`, `GENERAL_CAUSE`, `FIRE_START_DATE`, `DISPATCHED_RESOURCE`, `FIRE_SPREAD_RATE`, `TEMPERATURE`, `RELATIVE_HUMIDITY`, `WIND_SPEED`, `FUEL_TYPE`.

Hectares can be 0.1 for class A. Missing weather is real — drop or impute, and say which.

---

## Primary source

**Historical wildfire data 2006–2025 — Government of Alberta**

- **Portal:** https://open.alberta.ca/opendata/wildfire-data
- **CSV used for this seed:** `fp-historical-wildfire-data-2006-2025.csv` from the Open Alberta dataset
- **Licence:** [Open Government Licence — Alberta](https://open.alberta.ca/licence)

Do not commit the full 2006–2025 dump if you re-download it (~10 MB is fine; keep the lab seed small).

---

## Loading example

```python
import pandas as pd

df = pd.read_csv("data/alberta_wildfires_2023_2025.csv", parse_dates=["FIRE_START_DATE"])
print(df["SIZE_CLASS"].value_counts())
print(df["YEAR"].value_counts().sort_index())
```

---

## Citation

Government of Alberta. Historical wildfire data. Open Alberta.
