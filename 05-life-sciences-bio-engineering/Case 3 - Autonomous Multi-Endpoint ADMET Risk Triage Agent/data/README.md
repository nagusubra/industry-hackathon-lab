# Data Guide — Autonomous Multi-Endpoint ADMET Risk Triage Agent (Stream 5)

---

## 1. ClinTox (clinical trial toxicity)

- **HuggingFace:** https://huggingface.co/datasets/scikit-fingerprints/MoleculeNet_ClinTox  
- **What:** Binary labels — approved drug vs. failed clinical trial due to toxicity.
- **License:** MoleculeNet research-use terms (Wu et al., *Chem. Sci.* 2018).

### Option A — HuggingFace

```bash
pip install datasets pandas
```

```python
from datasets import load_dataset

ds = load_dataset("scikit-fingerprints/MoleculeNet_ClinTox", split="train")
df = ds.to_pandas()
df.to_csv("data/raw/admet/clintox.csv", index=False)
```

### Option B — PyTDC

```bash
pip install PyTDC
```

```python
from tdc.single_pred import Tox

data = Tox(name="ClinTox")
df = data.get_data()
df.to_csv("data/raw/admet/clintox.csv", index=False)
```

---

## 2. SIDER (drug side effects)

- **Source:** MoleculeNet / [PyTDC](https://tdcommons.ai)  
- **What:** Multi-label side-effect profiles for marketed drugs.
- **License:** MoleculeNet research-use terms.

```python
from tdc.single_pred import Tox

data = Tox(name="SIDER")
df = data.get_data()
df.to_csv("data/raw/admet/sider.csv", index=False)
```

---

## 3. hERG Karim (cardiac liability)

- **Source:** [PyTDC](https://tdcommons.ai)  
- **What:** Binary hERG channel blockade labels (Karim et al.).
- **License:** CC BY 4.0 (cite Karim / TDC).

PyTDC dataset name is `hERG` (not `hERG_Karim`):

```python
from tdc.single_pred import Tox

data = Tox(name="hERG")
df = data.get_data()
df.to_csv("data/raw/admet/herg_karim.csv", index=False)
```

---

## Step-by-step setup

1. Install PyTDC **or** use HuggingFace for ClinTox:

```bash
pip install PyTDC pandas
mkdir -p data/raw/admet
```

2. Run the Python snippets above to export small CSVs under `data/raw/admet/`.
3. Point your agent at `data/raw/admet/clintox.csv`, `data/raw/admet/sider.csv`, and `data/raw/admet/herg_karim.csv`.

**Citation:** Wu et al., *Chem. Sci.* 2018 (MoleculeNet); Therapeutics Data Commons (TDC); Karim et al. hERG dataset (CC BY 4.0).

---

## Offline hackathon fallback

If PyTDC or HuggingFace is unavailable on event Wi-Fi, pre-download the three CSVs on Friday and copy them into `data/raw/admet/`. The starter agent synthesizes a toy multi-endpoint table when no CSV is present.

---

## 4. Minimal starter CSV schema (multi-endpoint)

| column | description |
|---|---|
| `compound_id` | Local identifier |
| `smiles` | Chemical structure |
| `endpoint` | `clintox` / `sider` / `herg` |
| `activity` | 1 positive / 0 negative (or multi-label for SIDER) |

The starter agent synthesizes a toy multi-endpoint table for pipeline testing.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    └── admet/
        ├── clintox.csv
        ├── sider.csv
        └── herg_karim.csv
```

### Ethics note

Use public screening datasets only. Do not generate instructions for synthesizing controlled or highly hazardous substances. Focus on multi-endpoint triage and assay prioritization methodology.
