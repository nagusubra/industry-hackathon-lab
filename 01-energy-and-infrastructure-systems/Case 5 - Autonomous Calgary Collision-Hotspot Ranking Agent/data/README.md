# Data Guide — Calgary Collision Hotspots (Case 5)

A 2025 subset of Open Calgary Traffic Incidents is already in this folder.

---

## Bundled seed

| File | What it is |
|---|---|
| `calgary_traffic_incidents_2025.csv` | Reported incidents with coordinates for calendar 2025 |

Columns: `incident_info`, `description`, `start_dt`, `quadrant`, `longitude`, `latitude`, `incident_count`.

Round lat/lon (for example 3–4 decimals) or clean `incident_info` to make a location key. Document the choice. This is the City’s open incident feed, not a complete police collision database.

---

## Primary source

**Traffic Incidents — Open Calgary**

- **Portal:** https://data.calgary.ca/Transportation-Transit/Traffic-Incidents/35ra-9556
- **CSV:** `https://data.calgary.ca/api/views/35ra-9556/rows.csv?accessType=DOWNLOAD`
- **Licence:** [Open Government Licence — City of Calgary](https://data.calgary.ca/stories/s/Open-Calgary-Terms-of-Use/u45n-7awa)

Optional denominator: [Traffic Volumes for 2024](https://data.calgary.ca/dataset/Traffic-Volumes-for-2024/cauu-7hnw).

Do not geocode thousands of rows through a paid API.

---

## Loading example

```python
import pandas as pd

df = pd.read_csv("data/calgary_traffic_incidents_2025.csv", parse_dates=["start_dt"])
print(df.head(2))
```

---

## Citation

The City of Calgary. Open Calgary — Traffic Incidents. https://data.calgary.ca/Transportation-Transit/Traffic-Incidents/35ra-9556
