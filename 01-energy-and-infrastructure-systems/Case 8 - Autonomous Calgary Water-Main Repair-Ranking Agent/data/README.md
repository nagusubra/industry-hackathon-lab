# Data Guide — Calgary Water-Main Repair Ranking (Case 8)

A 2016–2026 subset of Open Calgary Water Main Breaks is already in this folder, with a community and consequence band joined for hour one.

---

## Bundled seed

| File | What it is |
|---|---|
| `calgary_water_main_breaks_2016_2026.csv` | ~2,200 break points from 2016 through mid-2026 |

Columns: `break_date`, `break_type`, `status`, `latitude`, `longitude`, `community_name`, `sector`, `srg`, `consequence`.

- **`status`:** `ACTIVE` / `RETIRED` is the City’s asset flag on the record, not “the leak is still open.”
- **`break_type`:** City codes (`A`, `G`, `D`, `CG`, …). There is **no public legend** in this pack. Do not treat letters as pipe diameter.
- **`community_name` / `sector` / `srg`:** nearest Open Calgary community centroid (vertex-average of the community polygon). Good enough to score consequence; not a surveyed address.
- **`consequence`:** a **lab label**, not a City risk model.
  - `high` — downtown core, hospital-adjacent communities, or the Bearspaw–Shaganappi corridor (Bowness, Montgomery, Parkdale, Hillhurst, Shaganappi, …)
  - `medium` — other Established / Complete communities
  - `low` — Developing and the rest

The portal table does **not** include pipe diameter or PCCP wire-break counts. Likelihood in this seed is “how often this cell broke.” Consequence is the band above.

---

## Primary sources

- **Water Main Breaks — Open Calgary:** https://data.calgary.ca/Environment/Water-Main-Breaks/dpcu-jr23  
  Dataset id `dpcu-jr23`.  
  **Licence:** [Open Government Licence — City of Calgary](https://data.calgary.ca/stories/s/Open-Calgary-Terms-of-Use/u45n-7awa)
- Community names: Open Calgary community boundaries (centroids only in this seed).
- Context (not in the CSV): City of Calgary Bearspaw South Feedermain L4 / panel reviews (2024 rupture, 2025 repeat); Water Efficiency Plan (distribution losses rose to ~22% in 2024).

Optional join: [Public Water Main](https://data.calgary.ca/Services-and-Amenities/Public-Water-Main/w6h9-w33i) (`w6h9-w33i`).

Do not commit the 1956–present dump if you re-download it; this seed starts at 2016.

---

## Loading example

```python
import pandas as pd

df = pd.read_csv("data/calgary_water_main_breaks_2016_2026.csv", parse_dates=["break_date"])
print(df["consequence"].value_counts())
print(df["break_date"].dt.year.value_counts().sort_index())
```

---

## Citation

The City of Calgary. Open Calgary — Water Main Breaks. https://data.calgary.ca/Environment/Water-Main-Breaks/dpcu-jr23
