# Data Guide — 311 Work-Order Dispatch (Case 1)

A mixed 200-ticket sample is already in this folder.

---

## Bundled seed

| File | What it is |
|---|---|
| `311_dispatch_sample.csv` | ~200 Open Calgary 311 tickets with coordinates: potholes, ice/snow, waste, signs, debris, streetlights |

Use this as the day-plan demo. You may pull more rows from the portal if you need a larger day.

---

## Primary sources

- **Current year:** https://data.calgary.ca/Services-and-Amenities/311-Service-Requests-Current-Year/arf6-qysm
- **All years:** https://data.calgary.ca/Services-and-Amenities/311-Service-Requests/iahh-g8bj

**Licence:** Open Government Licence — City of Calgary.

Do not commit the multi-million-row dump.

---

## Loading example

```python
import pandas as pd

df = pd.read_csv("data/311_dispatch_sample.csv", parse_dates=["requested_date"])
print(df["service_name"].value_counts())
```

---

## Citation

The City of Calgary. Open Calgary — 311 Service Requests.
