# Data Guide — Calgary Snow / Delivery Routing (Case 2)

A 22-stop inner-city table (depot + community centroids) is already in this folder. You do not need GeoJSON on hour one.

---

## Bundled seed

| File | What it is |
|---|---|
| `stops.csv` | `stop_id`, `name`, `lat`, `lon`, `priority` |

- `stop_id=0` is **Depot (downtown civic)** at 51.0447, -114.0719 (stated downtown point, not a City yard geocode).
- Other rows are centroids of Open Calgary **residential community** polygons (inner-city cluster).
- `priority` 1–3 is a snow-class-style hint for scoring, not an official City route class.

Distance: haversine in kilometres. Do not call a commercial routing API unless you already have a key.

---

## Primary sources (if you rebuild the table)

- Communities (Open Calgary): used for names and polygon centroids.
- Optional: [Snow and Ice Clearing Priority Routes](https://data.calgary.ca/Health-and-Safety/Snow-and-Ice-Clearing-Priority-Routes/4v8s-3kss) — line geometries; sample vertices if you want official plow lines.

**Licence:** Open Government Licence — City of Calgary.

---

## Loading example

```python
import pandas as pd

stops = pd.read_csv("data/stops.csv")
print(stops)
```

---

## Citation

The City of Calgary. Open Calgary community boundaries / snow-clearing datasets as used.
