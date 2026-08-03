# Data Guide — Battery Cathode Discovery Agent (Stream 4)

---

## Primary Source: Materials Project Insertion Electrodes

- **API getting started:** https://docs.materialsproject.org/downloading-data/using-the-api/getting-started  
- **Battery Explorer (UI):** https://next-gen.materialsproject.org/  
- **Endpoint used in docs/community:** `materials.insertion_electrodes` via `mp_api.client.MPRester`  
- **Scale:** On the order of **6,800+** battery / insertion-electrode entries exposed through the Battery Explorer / API (count evolves with MP releases)  
- **Formats:** JSON documents via API (convertible to CSV/Parquet locally); structures as CIF / pymatgen `Structure`

### Important fields (typical)

| Field | Meaning | Units (typical) |
|---|---|---|
| `battery_id` / material ids | MP identifiers | — |
| `average_voltage` | Average voltage | V |
| `capacity_grav` | Gravimetric capacity | mAh/g |
| `capacity_vol` | Volumetric capacity | mAh/cm³ |
| `energy_grav` | Specific energy | Wh/kg |
| `energy_vol` | Energy density | Wh/L |
| `working_ion` | e.g. Li, Na, Mg | — |
| stability / framework fields | Stability proxies | MP-specific |

Exact field names can vary slightly by client version — inspect returned documents and select `fields=[...]` explicitly.

### Setup

1. Create a free account at https://next-gen.materialsproject.org/  
2. Copy your API key from the dashboard  
3. Export it:

```bash
export MP_API_KEY="YOUR_KEY"
```

### Download / query example

```python
from mp_api.client import MPRester
import pandas as pd
import os

with MPRester(os.environ["MP_API_KEY"], use_document_model=False) as mpr:
    docs = mpr.materials.insertion_electrodes.search(
        working_ion="Li",
        # optional filters, e.g. average_voltage=(3.0, 4.5)
    )

df = pd.DataFrame(docs)
df.to_csv("raw/mp_li_insertion_electrodes.csv", index=False)
print(len(df), "electrodes cached")
```

Community snippet (full pull — can be large/slow):

```python
with MPRester(use_document_model=False) as mpr:
    elec_docs = mpr.materials.insertion_electrodes.search()
```

---

## Offline Hackathon Fallback

If API access is limited during the event, cache a filtered CSV on Saturday morning and commit **only** a small sample (tens–hundreds of rows) plus the download script. Do not commit the entire MP dump.

The starter agent **generates** a tiny synthetic electrode table on first run if no API key / CSV is present (written under `data/raw/`, which is gitignored).

---

## Related Structure Data

For composition/structure featurization, query materials by `material_ids` returned on electrode docs and load structures through pymatgen:

```python
from pymatgen.core import Structure
# structure = mpr.get_structure_by_material_id("mp-XXXX")
```

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    ├── mp_li_insertion_electrodes.csv
    └── sample_electrodes.csv   # optional tiny cache
```

### Citation

Acknowledge the Materials Project and cite relevant MP / pymatgen publications when presenting.
