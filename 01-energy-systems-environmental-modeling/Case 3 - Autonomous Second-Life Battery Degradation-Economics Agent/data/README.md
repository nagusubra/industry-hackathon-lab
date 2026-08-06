# Data Guide — Second-Life Battery Degradation-Economics Agent (Case 3)

This case uses the **Stanford Energy Control Lab** second-life NMC cell cycling dataset hosted on OSF. Do **not** commit raw archives to GitHub; download locally into `data/raw/` and document your subset.

---

## Dataset: Second-Life Li-ion Grid Storage Cycling (OSF)

- **What:** Cycling data for **6 NMC INR21700-M50T cells** under residential and commercial grid-storage duty cycles — capacity fade, voltage, current, temperature.
- **OSF project:** https://osf.io/8jnr5/
- **DOI:** 10.17605/OSF.IO/8JNR5
- **File:** `SL_Dataset_SECL_INR21700-M50T.zip`
- **License:** **CC-BY 4.0** — cite Khan & Onori (see Citation Notes below).
- **Companion article:** Moy, A., Khan, M., & Onori, S. (2024). Second-life Li-ion grid storage cycling dataset. *Data in Brief*. https://doi.org/10.1016/j.dib.2024.111046

---

## Download Steps

1. **Open** https://osf.io/8jnr5/ in your browser.
2. **Click** **Files** → **Download As Zip** (or download `SL_Dataset_SECL_INR21700-M50T.zip` directly).
3. **Unzip** contents to `data/raw/second-life/`:

```
data/
├── README.md          # this file
└── raw/
    └── second-life/
        └── SL_Dataset_SECL_INR21700-M50T/
            └── ...    # per-cell cycling logs (inspect after unzip)
```

After unzip, **list files and inspect the folder tree** — file names and layout vary by cell and duty cycle. Do not assume a fixed path like `cell_01/cycles.csv`.

---

## Typical Schema (per cell / cycle log)

| Column / Field | Description | Units / Notes |
|---|---|---|
| `cycle_number` | Cycle index | integer |
| `time` | Timestamp within cycle | seconds or datetime |
| `voltage` | Cell terminal voltage | V |
| `current` | Charge/discharge current | A (sign convention varies) |
| `temperature` | Cell temperature | °C |
| `capacity` | Discharge capacity this cycle | Ah or fraction of nominal |
| `soh` / `capacity_retention` | State of health | % or fraction of initial capacity |

Exact file names and column headers vary by cell folder — inspect the unzip tree after download.

---

## Loading Example (Python)

Run from the case folder; paths are relative to the case root as `data/raw/...`.

```python
from pathlib import Path

data_dir = Path("data/raw/second-life")

# List files after unzip — do not assume a fixed filename
for p in sorted(data_dir.rglob("*")):
    if p.is_file():
        print(p.relative_to(data_dir))

# Pick a CSV that contains capacity/SOH columns, then load:
# import pandas as pd
# df = pd.read_csv(chosen_csv)
# print(df.head())
```

---

## Suggested Local Layout

Add a `.gitignore` entry for `data/raw/` in your **submission** repo (this lab already ignores `**/data/raw/` at the root).

---

## Citation Notes

Cite the OSF dataset under **CC-BY 4.0**:

> Khan, M., & Onori, S. Second-Life Li-ion Grid Storage Cycling Dataset. OSF. https://doi.org/10.17605/OSF.IO/8JNR5

Also cite the companion data article when publishing degradation-economics results:

> Moy, A., Khan, M., & Onori, S. (2024). Second-life Li-ion grid storage cycling dataset. *Data in Brief*. https://doi.org/10.1016/j.dib.2024.111046
