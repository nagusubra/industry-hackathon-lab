# Data Guide — Building PV + Battery Storage-Dispatch Agent (Case 2)

This case uses the **DrivenData Power Laws** competition training data (rehosted on Schneider Electric Data Exchange). Do **not** commit raw CSV archives to GitHub; download locally into `data/raw/` and document your subset.

---

## Dataset: Power Laws — Optimizing Demand-Side Strategies

- **What:** 15-minute time series for **11 commercial/industrial sites** with building consumption, PV production, and buy/sell electricity prices.
- **Competition page:** https://www.drivendata.org/competitions/53/optimize-photovoltaic-battery/
- **Data rehost (Schneider Electric Data Exchange):** https://data.exchange.se.com/explore/dataset/power-laws-optimizing-demand-side-strategies-training-data/information/
- **Winning solutions (reference implementations):** https://github.com/drivendataorg/power-laws-optimization
- **License:** Competition / research use; **free account signup required** (DrivenData or Schneider Electric Data Exchange). Review competition rules: https://www.drivendata.org/competitions/53/optimize-photovoltaic-battery/rules/
- **Formats:** CSV per site (15-minute resolution)

---

## Download Steps

1. **Create a free account** on the [Schneider Electric Data Exchange](https://data.exchange.se.com/) **OR** register on the [DrivenData competition page](https://www.drivendata.org/competitions/53/optimize-photovoltaic-battery/) and accept the competition rules.
2. **Download the training CSVs** (11 site files). Choose one path:
   - **Schneider Electric Data Exchange:** open the [dataset page](https://data.exchange.se.com/explore/dataset/power-laws-optimizing-demand-side-strategies-training-data/information/) → **Export** → **CSV** → download the archive or individual site files.
   - **DrivenData:** open the [competition Data tab](https://www.drivendata.org/competitions/53/optimize-photovoltaic-battery/data/) → download the training-data zip (requires competition registration and rules acceptance).
3. **Place files under** `data/raw/power-laws/` (create the folder if needed):

```
data/
├── README.md          # this file
└── raw/
    └── power-laws/
        ├── site_001.csv
        ├── site_002.csv
        └── ...        # up to 11 site CSVs
```

---

## Typical Schema (per site CSV)

| Column | Description | Units / Notes |
|---|---|---|
| `timestamp` | 15-minute interval start | ISO datetime or pandas-parseable |
| `consumption` | Building load | **kW** — mean power over the 15-min interval |
| `production` | PV generation | **kW** — mean power over the 15-min interval |
| `buy_price` | Retail import price | $/kWh |
| `sell_price` | Export / feed-in price | $/kWh |

**Energy conversion:** energy (kWh) over one interval = kW × 0.25 (15 min = 0.25 h).

Additional columns (site ID, temperature, etc.) may appear in some exports — consult the competition data dictionary on DrivenData.

---

## Loading Example (Python)

Run from the case folder; paths are relative to the case root as `data/raw/...`.

```python
import pandas as pd
from pathlib import Path

site_csv = Path("data/raw/power-laws/site_001.csv")
df = pd.read_csv(site_csv, parse_dates=["timestamp"])
df = df.sort_values("timestamp").set_index("timestamp")
print(df[["consumption", "production", "buy_price", "sell_price"]].head())
```

---

## Suggested Local Layout

Add a `.gitignore` entry for `data/raw/` in your **submission** repo (this lab already ignores `**/data/raw/` at the root).

---

## Citation Notes

When you publish results, cite the DrivenData Power Laws competition and Schneider Electric Data Exchange dataset. Review winning solution approaches at https://github.com/drivendataorg/power-laws-optimization for benchmarking ideas.
