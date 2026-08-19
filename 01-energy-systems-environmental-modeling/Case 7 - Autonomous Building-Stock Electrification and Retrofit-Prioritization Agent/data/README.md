# Data Guide — Building-Stock Retrofit-Prioritization Agent (Case 7)

This case uses NREL **End-Use Load Profiles / End-Use Savings Shapes** (ResStock). Use **pre-aggregated state-level CSVs** only. Do **not** download individual-building parquet (terabyte-scale). Do **not** commit aggregates to GitHub.

License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## Primary Data Source

- **AWS Open Data:** https://registry.opendata.aws/nrel-pds-building-stock/  
- **S3 bucket (no AWS account):** `s3://oedi-data-lake/nrel-pds-building-stock/`  
- **OpenEI viewer:** https://data.openei.org/submissions/4520  
- **Day-one geography:** Colorado (`state=CO`) — smaller than CA/TX, still a full climate + housing mix.

Two publication trees are useful:

| Tree | Why |
|---|---|
| `.../2021/resstock_amy2018_release_1/` | Baseline 15-min state aggregates (no upgrade packages) |
| `.../2022/resstock_amy2018_release_1/` | End-Use Savings Shapes: baseline **and** numbered upgrade packages |

This case needs **baseline vs. at least one upgrade**. Prefer the **2022** tree. If 2022 paths 404 for your client, start with 2021 baseline files plus the synthetic demo, then add 2022 upgrades.

---

## Download Steps (recommended: 2022 CO, two files)

From the **case folder**. AWS CLI is **not** required. Each 15-min aggregate CSV is ~25 MB — start with **one building type**, not a recursive state dump.

Verified 2022 ResStock AMY2018 upgrade IDs (`upgrades_lookup.json`):

| ID | Package |
|---|---|
| 0 | Baseline |
| 1 | Basic enclosure (recommended day-one upgrade) |
| 2 | Enhanced enclosure |
| 3 | Heat pumps, min-efficiency, electric backup |
| 8 | Whole-home electrification, high efficiency |

Colorado baseline filenames (lowercase `co-`):

- `up00-co-single-family_detached.csv`
- `up00-co-single-family_attached.csv`
- `up00-co-multi-family_with_2_-_4_units.csv`
- `up00-co-multi-family_with_5plus_units.csv`
- `up00-co-mobile_home.csv`

Upgrade 1 uses the same names with `up01-` and prefix `upgrade=1/`.

### 0. Create folders

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Force -Path data\raw\nrel-eulp\baseline, data\raw\nrel-eulp\upgrade | Out-Null
```

**Linux / macOS:**

```bash
mkdir -p data/raw/nrel-eulp/baseline data/raw/nrel-eulp/upgrade
```

### 1. Day-one HTTPS (single-family detached, baseline + basic enclosure)

S3 region is **us-west-2**. No AWS account.

```text
https://oedi-data-lake.s3.us-west-2.amazonaws.com/nrel-pds-building-stock/end-use-load-profiles-for-us-building-stock/2022/resstock_amy2018_release_1/timeseries_aggregates/by_state/upgrade=0/state=CO/up00-co-single-family_detached.csv

https://oedi-data-lake.s3.us-west-2.amazonaws.com/nrel-pds-building-stock/end-use-load-profiles-for-us-building-stock/2022/resstock_amy2018_release_1/timeseries_aggregates/by_state/upgrade=1/state=CO/up01-co-single-family_detached.csv
```

**Windows (PowerShell):**

```powershell
$base = "https://oedi-data-lake.s3.us-west-2.amazonaws.com/nrel-pds-building-stock/end-use-load-profiles-for-us-building-stock/2022/resstock_amy2018_release_1/timeseries_aggregates/by_state"
Invoke-WebRequest -Uri "$base/upgrade=0/state=CO/up00-co-single-family_detached.csv" -OutFile "data\raw\nrel-eulp\baseline\up00-co-single-family_detached.csv"
Invoke-WebRequest -Uri "$base/upgrade=1/state=CO/up01-co-single-family_detached.csv" -OutFile "data\raw\nrel-eulp\upgrade\up01-co-single-family_detached.csv"
```

**Linux / macOS:**

```bash
BASE="https://oedi-data-lake.s3.us-west-2.amazonaws.com/nrel-pds-building-stock/end-use-load-profiles-for-us-building-stock/2022/resstock_amy2018_release_1/timeseries_aggregates/by_state"
curl -L -o data/raw/nrel-eulp/baseline/up00-co-single-family_detached.csv \
  "$BASE/upgrade=0/state=CO/up00-co-single-family_detached.csv"
curl -L -o data/raw/nrel-eulp/upgrade/up01-co-single-family_detached.csv \
  "$BASE/upgrade=1/state=CO/up01-co-single-family_detached.csv"
```

Then copy the same pattern for `co-mobile_home` / `co-single-family_attached` if you want more segments.

### 2. Optional — AWS CLI recursive (all five CO types, ~125 MB per upgrade)

```bash
aws s3 cp --no-sign-request \
  s3://oedi-data-lake/nrel-pds-building-stock/end-use-load-profiles-for-us-building-stock/2022/resstock_amy2018_release_1/timeseries_aggregates/by_state/upgrade=0/state=CO/ \
  data/raw/nrel-eulp/baseline/ --recursive
```

Browse: [OpenEI S3 viewer — CO baseline](https://data.openei.org/s3_viewer?bucket=oedi-data-lake&prefix=nrel-pds-building-stock/end-use-load-profiles-for-us-building-stock/2022/resstock_amy2018_release_1/timeseries_aggregates/by_state/upgrade=0/state=CO/)

### 3. Fallback — 2021 baseline-only

```text
https://oedi-data-lake.s3.us-west-2.amazonaws.com/nrel-pds-building-stock/end-use-load-profiles-for-us-building-stock/2021/resstock_amy2018_release_1/timeseries_aggregates/by_state/state=CO/co-single-family_detached.csv
```

2021 files are **baseline only**. Add a 2022 `up01-` extract for the upgrade side, or use the labeled synthetic demo until then.

```
data/
├── README.md
└── raw/
    └── nrel-eulp/
        ├── upgrades_lookup.json      # optional
        ├── baseline/                 # upgrade=0 CSVs
        └── upgrade/                  # chosen package CSVs
```

If no real CSVs are present, `agent_starter.py` writes **`data/raw/nrel-eulp/demo_segments.csv`** and prints `[warn]`.

---

## Typical Schema (timeseries aggregates)

Each CSV is 15-minute energy for **one geography × one building type × one upgrade**. Column names are documented in `data_dictionary.tsv` in the same S3 prefix. After download, find:

| Logical field | How to find it |
|---|---|
| Timestamp | `timestamp` or first datetime column |
| Electricity (kWh per interval) | column containing `electricity` and `total` / `energy_consumption` |
| Other fuels | gas / propane / fuel oil columns if present (optional) |

Convert 15-min kWh to kW with `kW = kWh / 0.25`. Coincident peak = max of the electricity kW series (or max of baseline+upgrade aligned timestamps).

Annual results CSVs (optional, often easier for $/dwelling):

`.../metadata_and_annual_results/by_state/state=CO/csv/`

---

## Loading Example (Python)

Run from the case folder.

```python
from pathlib import Path
import pandas as pd

def load_eulp(path: Path) -> pd.Series:
    df = pd.read_csv(path)
    tcol = next(c for c in df.columns if "time" in c.lower() or "timestamp" in c.lower())
    df[tcol] = pd.to_datetime(df[tcol])
    ecol = next(
        c for c in df.columns
        if "electricity" in c.lower() and ("total" in c.lower() or "energy" in c.lower())
    )
    kw = df.set_index(tcol)[ecol].astype(float) / 0.25  # kWh/15min → kW
    return kw.sort_index()

base = Path("data/raw/nrel-eulp/baseline")
up = Path("data/raw/nrel-eulp/upgrade")
print("baseline files:", list(base.glob("*.csv"))[:5])
print("upgrade files:", list(up.glob("*.csv"))[:5])
```

Match baseline/upgrade pairs by building-type token in the filename.

---

## License & Use Terms

End-Use Load Profiles for the U.S. Building Stock — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cite NREL / DOE as below. No login for S3 `--no-sign-request` or the public HTTPS objects.

---

## Suggested Local Layout

This lab already gitignores `**/data/raw/`.

---

## Citation Notes

Wilson, E., et al. (2022). *End-Use Load Profiles for the U.S. Building Stock: Practical Guidance on Accessing and Using the Data*. NREL/TP-5500-83907. https://www.osti.gov/biblio/1909353

Dataset: End-Use Load Profiles for the U.S. Building Stock, accessed from https://registry.opendata.aws/nrel-pds-building-stock (OEDI `oedi-data-lake/nrel-pds-building-stock/`).
