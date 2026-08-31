# Data Guide — Calgary Development-Permit Triage (Case 7)

A housing-focused sample of Open Calgary Development Permits is already in this folder.

---

## Bundled seed

| File | What it is |
|---|---|
| `calgary_housing_development_permits.csv` | ~2,000 rows with `category` starting with `Residential`: open-queue statuses plus a 2024+ Released sample |

Columns: `permitnum`, `address`, `category`, `description`, `statuscurrent`, `applieddate`, `decisiondate`, `communityname`, `ward`, `quadrant`, `latitude`, `longitude`, `srg`, `sector`.

`srg` is joined from Open Calgary community boundaries (Established / Developing / Complete). Use it for the “established areas wait longer” story. A few rows have no match — drop or keep as unknown.

GeoJSON / WKT location blobs from the portal are **not** in this seed on purpose.

For the ranking, filter to files that are still in the queue (`Released` / `Cancelled` are history — useful if you want a completed-time check, not the live list).

---

## Primary sources

- **Development Permits — Open Calgary:** https://data.calgary.ca/Government/Development-Permits/6933-unw5  
  **Licence:** [Open Government Licence — City of Calgary](https://data.calgary.ca/stories/s/Open-Calgary-Terms-of-Use/u45n-7awa)
- Community `srg` / sector: Open Calgary community boundaries.

Do not commit the full permit dump (it includes huge geometry columns).

---

## Loading example

```python
import pandas as pd

df = pd.read_csv("data/calgary_housing_development_permits.csv", parse_dates=["applieddate", "decisiondate"])
print(df["statuscurrent"].value_counts())
print(df["srg"].value_counts(dropna=False))
print(df["category"].value_counts().head())
```

---

## Citation

The City of Calgary. Open Calgary — Development Permits. https://data.calgary.ca/Government/Development-Permits/6933-unw5
