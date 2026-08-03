# Data Guide — Grid-Balancing Agent (Stream 1)

This case uses **real, open-access** energy datasets. Do **not** commit multi-GB raw archives to GitHub; download locally into this folder (or a sibling `raw/` directory) and document your subset.

---

## Primary Datasets

### 1. NREL Wind Integration National Dataset (WIND) Toolkit

- **What:** Meteorological fields + estimated turbine power for 100,000+ CONUS sites (2007–2013 era toolkit; long-term ensemble / LED extensions available).
- **Host:** AWS Open Data — `s3://nrel-pds-wtk/`
- **Docs:** https://registry.opendata.aws/nrel-pds-wtk/  
  Overview: https://nlr.gov/grid/wind-toolkit
- **Formats:** HDF5 / NetCDF-style scientific arrays on S3; derived CSV/parquet subsets commonly used in ML pipelines
- **License:** DOE Open Energy Data Initiative (public)

**List bucket (no AWS account required):**

```bash
aws s3 ls --no-sign-request s3://nrel-pds-wtk/
```

**Example: download a small site subset (adjust keys after listing):**

```bash
mkdir -p raw/wtk
aws s3 cp --no-sign-request s3://nrel-pds-wtk/ raw/wtk/ --recursive --exclude "*" --include "*README*"
# Then select a specific site/year HDF5 path from the listing for your agent pipeline.
```

**Typical fields (site power / met subsets):** timestamp, wind speed / direction at hub height (e.g., 100 m), temperature, pressure, estimated power (MW), forecast horizons (1 h / 4 h / 6 h / 24 h where forecast products are available).

### 2. NREL PERFORM Phase II — Solar, Wind, and Load Forecasts (MISO, NYISO, SPP)

- **What:** Time-coincident load, wind, and solar **actuals** and **probabilistic forecasts** for three U.S. ISOs (actuals ~2018–2019; forecasts primarily 2019).
- **Docs / access:** https://github.com/PERFORM-Forecasts/documentation  
  Technical report: https://doi.org/10.2172/2335360
- **Formats:** CSV / structured time-series packages documented in the PERFORM repo
- **Spatial scales:** site-level, zone-level, system (balancing area) level
- **Why useful:** Perfect for agent experiments that couple renewable forecasts with system load.

```bash
git clone https://github.com/PERFORM-Forecasts/documentation.git raw/perform-docs
# Follow the documentation README for dataset download URLs and directory layout.
```

### 3. Kaggle — Hourly Energy Consumption (PJM / related ISO load series)

- **What:** Convenient hourly load CSVs for rapid prototyping of demand-side imbalance models.
- **URL:** https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption
- **Format:** CSV (`Datetime`, regional load MW columns)
- **Use:** Pair with a wind power series (WTK or PERFORM) as a lightweight balancing sandbox if full ISO PERFORM packages are too large for day-one setup.

```bash
# Requires Kaggle API credentials (~/.kaggle/kaggle.json)
kaggle datasets download -d robikscube/hourly-energy-consumption -p raw/pjm --unzip
```

### 4. Optional Kaggle — Feature-Engineered Wind Time Series (WTK-LED derived)

- **URL:** https://www.kaggle.com/datasets/muratiik/feature-engineered-wind-time-series-data-2015-23
- **Format:** CSV (~hourly, engineered shear/veer/regime labels + estimated power)
- **License:** CC BY 4.0
- **Use:** Fast ML baseline when you cannot stage multi-TB WTK HDF5 locally during the hackathon.

---

## Suggested Local Layout

```
data/
├── README.md          # this file
└── raw/               # gitignored downloads
    ├── wtk/
    ├── perform/
    └── pjm/
```

Add a `.gitignore` entry for `data/raw/` in your **submission** repo (this lab already ignores `**/data/raw/` at the root).

---

## Loading Example (Python)

```python
import pandas as pd

# After placing a CSV subset next to this folder:
df = pd.read_csv("raw/pjm/AEP_hourly.csv", parse_dates=["Datetime"])
df = df.sort_values("Datetime").set_index("Datetime")
print(df.head())
```

For WTK HDF5 site files, use `h5py` / `xarray` after downloading a specific object from `s3://nrel-pds-wtk/`.

---

## Citation Notes

When you publish results, cite NREL WIND Toolkit / PERFORM documentation DOIs and Kaggle dataset pages as appropriate. Keep license attribution for CC-BY materials.
