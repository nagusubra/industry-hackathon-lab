# Data Guide — Day-Ahead Battery Arbitrage Agent (Case 5)

This case uses the **epftoolbox PJM day-ahead benchmark CSV** published on Zenodo. Download it locally into `data/raw/` — do **not** commit the file to GitHub.

**Do not** `pip install epftoolbox`. That Python package is **AGPL-3.0**. This case uses only the raw CSV via `pandas`.

---

## Primary Data Source

- **Record:** https://zenodo.org/records/4624805  
- **Direct file:** https://zenodo.org/records/4624805/files/PJM.csv  
- **What:** Hourly COMED zonal day-ahead price plus two day-ahead exogenous forecasts, 2013-01-01 00:00 through 2018-12-24 (6 × 364 days; DST already interpolated/averaged by the dataset authors).
- **Access:** **No login.** HTTPS download. File size is ~1 MB. Some scripted clients get HTTP 403 without a browser `User-Agent`; `Invoke-WebRequest` / `curl -L` / the starter script work.
- **Timezone:** Eastern Time (as published).

---

## Download Steps

From the **case folder** (`Case 5 - Autonomous Day-Ahead Battery Arbitrage and Bidding Agent/`):

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Force -Path data\raw\epftoolbox | Out-Null
Invoke-WebRequest -Uri "https://zenodo.org/records/4624805/files/PJM.csv" -OutFile "data\raw\epftoolbox\PJM.csv"
```

**Linux / macOS:**

```bash
mkdir -p data/raw/epftoolbox
curl -L -o data/raw/epftoolbox/PJM.csv "https://zenodo.org/records/4624805/files/PJM.csv"
```

**Python (same URL):**

```python
from pathlib import Path
import pandas as pd

out = Path("data/raw/epftoolbox/PJM.csv")
out.parent.mkdir(parents=True, exist_ok=True)
df = pd.read_csv("https://zenodo.org/records/4624805/files/PJM.csv", skipinitialspace=True)
df.columns = [c.strip() for c in df.columns]
df.to_csv(out, index=False)
print(df.head())
```

Verify: file exists, ~20,656 hourly rows, first timestamp `2013-01-01 00:00:00`.

```
data/
├── README.md
└── raw/
    └── epftoolbox/
        └── PJM.csv
```

`agent_starter.py` will try this download automatically. If the network is blocked it writes **`data/raw/epftoolbox/demo_pjm.csv`** and prints a `[warn]` — that file is synthetic, not the Zenodo benchmark.

---

## Schema

The published header uses these **exact** names (including the original typo `foecast`):

| Column | Meaning | Units |
|---|---|---|
| `Date` | Hour beginning | datetime (ET) |
| `Zonal COMED price` | Day-ahead locational price, COMED zone | $/MWh |
| `System load forecast` | PJM system day-ahead load forecast | MW |
| `Zonal COMED load foecast` | COMED zonal day-ahead load forecast | MW |

When you implement your own models, you may rename internally to `price`, `system_load_da`, `comed_load_da`. Do not assume the epftoolbox names (`Price`, `Exogenous 1`, `Exogenous 2`) unless you rename them yourself.

---

## Loading Example (Python)

Run from the case folder.

```python
import pandas as pd
from pathlib import Path

path = Path("data/raw/epftoolbox/PJM.csv")
df = pd.read_csv(path, parse_dates=["Date"], skipinitialspace=True)
df.columns = [c.strip() for c in df.columns]
df = df.sort_values("Date")
print(df.columns.tolist())
print(df.head())
print(df["Date"].min(), "→", df["Date"].max())
```

Suggested walk-forward split: train on calendar years 2013–2016, test on 2017–2018 (or the last `years_test=2` × 364 days, matching the original paper).

---

## License & Use Terms

- **Zenodo record 4624805** is published as an open-access research dataset (Zenodo default license: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). Attribute the compilers and cite the paper below.
- The compilers **do not own** the underlying market series; they gathered publicly posted PJM / market-operator data. Educational use for this hackathon is appropriate. Commercial redistribution of the raw series may be subject to PJM’s current data terms — check https://www.pjm.com/ if you productize.
- **`epftoolbox` Python library:** AGPL-3.0 — **do not import it** in your submission.

---

## Suggested Local Layout

This lab already gitignores `**/data/raw/`. Keep the Zenodo CSV and any `demo_*.csv` files local.

---

## Citation Notes

Lago, J., Marcjasz, G., De Schutter, B., & Weron, R. (2021). Forecasting day-ahead electricity prices: A review of state-of-the-art algorithms, best practices and an open-access benchmark. *Applied Energy*, 293, 116983. https://doi.org/10.1016/j.apenergy.2021.116983

Dataset: Lago et al. (2021). Open-access benchmark dataset for day-ahead electricity prices. Zenodo. https://doi.org/10.5281/zenodo.4624805
