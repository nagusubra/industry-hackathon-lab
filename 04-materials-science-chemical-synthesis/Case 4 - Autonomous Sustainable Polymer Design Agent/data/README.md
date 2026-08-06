# Data Guide — Sustainable Polymer Design Agent (Stream 4)

---

## Primary Source: NeurIPS Open Polymer Prediction 2025

- **Kaggle competition:** https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025  
- **Mirror dataset (no competition rules):** https://www.kaggle.com/datasets/rathinumesh/neurips-open-polymer-prediction-2025  
- **Post-competition report:** [arXiv:2512.08896](https://arxiv.org/abs/2512.08896)  
- **Content:** Polymer repeat units (SMILES) with labeled properties  
- **Formats:** CSV (`train.csv`, `test.csv`, etc.)

### Target properties

| Property | Typical units / note |
|---|---|
| `Tg` | Glass-transition temperature (°C or K — check column docs) |
| Thermal conductivity | W/(m·K) |
| `Rg` | Radius of gyration (Å or nm) |
| Density | g/cm³ |
| `FFV` | Fractional free volume (dimensionless) |

Inspect column names in `train.csv` — competition releases may use abbreviated headers.

---

## Setup

### 1. Create a free Kaggle account

https://www.kaggle.com/ — accept [competition rules](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/rules) for the official download.

### 2. Install Kaggle CLI and download

```bash
pip install kaggle
# Place kaggle.json API token in ~/.kaggle/ (see Kaggle docs)

kaggle competitions download -c neurips-open-polymer-prediction-2025 -p data/raw/polymer --unzip
```

**Alternative — mirror dataset (no competition submission):**

```bash
kaggle datasets download -d rathinumesh/neurips-open-polymer-prediction-2025 -p data/raw/polymer --unzip
```

### 3. Quick inspect

```python
import pandas as pd

df = pd.read_csv("data/raw/polymer/train.csv")
print(df.shape, df.columns.tolist())
print(df.head())
```

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    └── polymer/
        ├── train.csv
        ├── test.csv
        └── sample_submission.csv
```

---

## Offline Hackathon Fallback

The starter agent **generates** a synthetic polymer feature table with SMILES-like tokens and Tg labels on first run if no CSV is present (written under `data/raw/`, which is gitignored).

---

## License & Redistribution

> **LICENSE NOTE:** Data is provided under **[Kaggle competition terms](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/rules)** — research and hackathon use is generally permitted, but **check redistribution and commercial-use clauses** before republishing processed datasets. Do not commit full competition dumps to Git; document download steps instead.

### Citation

Acknowledge the NeurIPS 2025 Open Polymer Prediction organizers and cite [arXiv:2512.08896](https://arxiv.org/abs/2512.08896) when referencing benchmark methodology.
