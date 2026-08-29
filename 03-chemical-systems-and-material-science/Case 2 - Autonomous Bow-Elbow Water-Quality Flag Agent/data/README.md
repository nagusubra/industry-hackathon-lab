# Data Guide — Bow / Elbow Water-Quality Flags (Case 2)

A Bow/Elbow subset plus a starter limit table are already in this folder.

---

## Bundled seed

| File | What it is |
|---|---|
| `watershed_samples.csv` | 2022–2023 grab samples for Bow River and Elbow River sites (E. coli, nitrate, TP, pH, DO, turbidity, temperature) |
| `limits.csv` | Action levels with a `source_note` you must read — some are CCME/Health Canada citations, one TP row is an **illustrative trigger** |

Open Calgary dataset: [Watershed Surface Water Quality Data](https://data.calgary.ca/Environment/Watershed-Surface-Water-Quality-Data/y8as-bmzj) (same City program as DataStream DOI 10.25976/5zzm-z169).

Handle `result_qualifier` (non-detects) explicitly. Normalize parameter names before joining to `limits.csv`. pH uses a range (`limit_value_low` / `limit_value_high`).

---

## Primary sources

- Open Calgary: https://data.calgary.ca/Environment/Watershed-Surface-Water-Quality-Data/y8as-bmzj
- DataStream catalogue: https://datastream.org/en-ca/dataset/5513f4ec-3597-42ac-a994-4dca3efa1aff
- DOI: https://doi.org/10.25976/5zzm-z169

**Licence:** Open Government Licence — City of Calgary.

Do **not** use the ~500 MB Alberta oil-sands State of Environment extract for this case.

If you cannot defend a legal limit in 30 minutes, use a documented internal action level (e.g. 90th percentile of that site’s history) and say so.

---

## Loading example

```python
import pandas as pd

samples = pd.read_csv("data/watershed_samples.csv", parse_dates=["sample_date"])
limits = pd.read_csv("data/limits.csv")
print(samples["parameter"].value_counts())
print(limits)
```

---

## Citation

City of Calgary. Watershed Surface Water Quality Data. Open Calgary / DataStream. https://doi.org/10.25976/5zzm-z169
