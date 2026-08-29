# Data Guide — Street-Light 311 Dispatch (Case 6)

A filtered lighting ticket seed is already in this folder.

---

## Bundled seed

| File | What it is |
|---|---|
| `street_lights_311.csv` | 800 Open Calgary 311 streetlight **maintenance/damage** tickets (Feb–Aug 2026 in this seed; not pedestrian/signal lights) |

Filter used: `Roads - Streetlight Maintenance`, `Roads - Streetlight Damage`, and related streetlight names from the current-year 311 feed.

---

## Primary sources

- **Current year:** https://data.calgary.ca/Services-and-Amenities/311-Service-Requests-Current-Year/arf6-qysm  
  CSV: `https://data.calgary.ca/api/views/arf6-qysm/rows.csv?accessType=DOWNLOAD`
- **All years:** https://data.calgary.ca/Services-and-Amenities/311-Service-Requests/iahh-g8bj

**Licence:** [Open Government Licence — City of Calgary](https://data.calgary.ca/stories/s/Open-Calgary-Terms-of-Use/u45n-7awa)

Do not commit the multi-million-row 311 dump.

---

## Loading example

```python
import pandas as pd

df = pd.read_csv("data/street_lights_311.csv", parse_dates=["requested_date"])
print(df["service_name"].value_counts())
```

---

## Citation

The City of Calgary. Open Calgary — 311 Service Requests. https://data.calgary.ca/Services-and-Amenities/311-Service-Requests/iahh-g8bj
