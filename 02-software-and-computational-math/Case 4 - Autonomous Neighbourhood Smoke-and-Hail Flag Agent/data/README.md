# Data Guide — Neighbourhood Smoke and Hail Flags (Case 4)

Two small tables are already in this folder.

---

## Bundled seeds

| File | What it is |
|---|---|
| `calgary_air_quality_seed.csv` | Open Calgary near-real-time readings for **Air Quality Health Index** and **Fine Particulate Matter** (three Calgary stations) |
| `neighbourhoods_hail_scenario.csv` | Community centroids plus a `hail_track` band for an **Aug 2024-style** north-Calgary hail path |

`hail_track` values: `high` (named in public coverage of the 5 Aug 2024 north / airport corridor), `medium` (adjacent north / northeast / inner-north), `low` (sample of the rest of the city).

This is **not** a CatIQ claims file and **not** an official City hail map. Treat it as a labelled scenario so you can combine smoke and hail in one flag.

Community centroids are vertex averages of Open Calgary community polygons, good enough for nearest-station assignment.

---

## Primary sources

- **Air Quality Data (near real time) — Open Calgary:** https://data.calgary.ca/Environment/Air-Quality-Data-near-real-time-/g9s5-qhu5  
  **Licence:** [Open Government Licence — City of Calgary](https://data.calgary.ca/stories/s/Open-Calgary-Terms-of-Use/u45n-7awa)
- **Community boundaries — Open Calgary** (centroids only in this seed)
- Hail path: reconstructed from public reporting of the 5 August 2024 Calgary hailstorm (north city / airport corridor). Do not claim you have insurer microdata.

---

## Loading example

```python
import pandas as pd

aq = pd.read_csv("data/calgary_air_quality_seed.csv", parse_dates=["readingdate"])
neigh = pd.read_csv("data/neighbourhoods_hail_scenario.csv")
print(aq["parameter"].value_counts())
print(neigh["hail_track"].value_counts())
```

---

## Citation

The City of Calgary. Open Calgary — Air Quality Data (near real time). https://data.calgary.ca/Environment/Air-Quality-Data-near-real-time-/g9s5-qhu5
