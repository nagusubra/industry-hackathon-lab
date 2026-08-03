# Data Guide — Structural-Health & Aerodynamic-Design Agent (Stream 2)

---

## Primary Dataset: NASA C-MAPSS Turbofan Engine Degradation

- **Portal:** https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data  
- **Also mirrored on:** IEEE DataPort, Kaggle, Hugging Face community mirrors  
- **Format:** Space-separated text files (`.txt`) inside a zip; 26 columns per row  
- **Subsets:** FD001, FD002, FD003, FD004 (increasing operating-condition / fault-mode complexity)

### Column Schema (per row)

| Index | Field |
|---|---|
| 1 | Unit / engine ID |
| 2 | Time (cycles) |
| 3–5 | Operational settings 1–3 |
| 6–26 | Sensor measurements 1–21 |

Training trajectories run to failure; test trajectories end before failure. True RUL vectors are provided for test engines (`RUL_FD00x.txt`).

### Subset Complexity

| Set | Train / Test engines | Conditions | Fault modes |
|---|---|---|---|
| FD001 | 100 / 100 | 1 (sea level) | 1 (HPC degradation) |
| FD002 | 260 / 259 | 6 | 1 |
| FD003 | 100 / 100 | 1 | 2 (HPC + Fan) |
| FD004 | 248 / 249 | 6 | 2 |

### Download

1. Open the NASA Open Data Portal page: https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data  
2. Download **CMAPSSData.zip** from the dataset resources, then unzip:

```bash
mkdir -p raw/cmapss
# After downloading CMAPSSData.zip locally:
unzip CMAPSSData.zip -d raw/cmapss
```

**Programmatic fallback (community Hugging Face mirror — verify against NASA when possible):**

```bash
pip install datasets
python -c "from datasets import load_dataset; print(load_dataset('SoyVitou/NASA-C-MAPSS-Turbofan-Engine', 'FD001'))"
```

Legacy PCoE turbofan page (may redirect): https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/
### Loading Example

```python
import pandas as pd

cols = ["unit", "cycle"] + [f"op{i}" for i in range(1, 4)] + [f"s{i}" for i in range(1, 22)]
train = pd.read_csv("raw/cmapss/train_FD001.txt", sep=r"\s+", header=None, names=cols)
print(train.head())
```

---

## Stretch Dataset: NVIDIA HiLiftAeroML (NASA CRM High-Lift CFD)

- **Hugging Face:** https://huggingface.co/datasets/nvidia/HiLiftAeroML  
- **Paper:** https://doi.org/10.48550/arxiv.2605.19565  
- **License:** CC-BY-4.0  
- **Content:** 1,800 WMLES samples (180 geometry variants × 10 AoA); geometries + volume/surface fields + integral forces  
- **Warning:** Full repo is on the order of **tens of TB**. For the hackathon, download **only** metadata / `force_mom_*.csv` files.

```bash
pip install huggingface_hub
# Prefer the consolidated force/geometry tables (small) — avoid multi-TB volume fields
hf download nvidia/HiLiftAeroML --repo-type dataset --local-dir raw/hilift \
  --include "force_mom_all.csv" --include "geo_values_all.csv"
```

Force CSVs typically include time-averaged drag, lift, moment, and pressure/viscous coefficient integrals — ideal for surrogate modeling without staging volume fields.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    ├── cmapss/
    └── hilift/   # optional stretch
```
