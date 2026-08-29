# Data Guide — Alberta Storage Cathode Shortlist (Case 1)

The **story** is Alberta grid storage. The **table** is a labelled literature-typical cathode list so nobody needs a Materials Project API key.

This is **not** a Materials Project dump. The `source` column is `literature_typical_demo`. Do not present these rows as MP `battery_id`s.

---

## Bundled seed

| File | What it is |
|---|---|
| `demo_insertion_electrodes.csv` | 36 intercalation-style chemistries with typical published voltage, capacity, energy, cycle-life proxy, abundance, and volume-change figures |

Beat an energy-only sort. Grid storage often prefers cycle life and abundant metals (LFP-like) over the highest Wh/kg.

If you already have an MP key, you may replace this file with a real insertion-electrode export — cite MP (Jain et al., APL Materials 2013) and https://docs.materialsproject.org/.

---

## Loading example

```python
import pandas as pd

df = pd.read_csv("data/demo_insertion_electrodes.csv")
print(df.sort_values("energy_grav_wh_kg", ascending=False).head(10)[["formula", "energy_grav_wh_kg", "cycle_life_proxy"]])
```

---

## Citation

Typical textbook / review-order-of-magnitude values for named cathode families (LFP, NMC, LMO, Na-ion NASICON, etc.). Not computed in this repository. Optional: Materials Project Battery Explorer if you export your own subset.
