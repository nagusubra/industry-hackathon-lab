# Data Guide — Reaction-Condition Optimizer (Stream 4)

---

## Primary Sources

### Iron Mind (recommended starting point)

- **Hugging Face:** https://huggingface.co/datasets/gomesgroup/iron-mind-data  
- **Paper:** [Iron Mind — arXiv:2509.00103](https://arxiv.org/abs/2509.00103)  
- **Content:** Curated HTE yield data including Buchwald–Hartwig and related cross-coupling campaigns  
- **Formats:** Hugging Face `datasets` loader (Parquet/Arrow); export to CSV locally

### rxn_yields (IBM / RXN for Chemistry)

- **Data docs:** https://rxn4chemistry.github.io/rxn_yields/data/  
- **Content:** Yield prediction benchmarks built from published HTE studies (incl. Science 2018 corpora)  
- **Formats:** JSON / CSV per reaction family

### Foundational HTE papers (cite in presentations)

| Study | Reaction | Reference |
|---|---|---|
| Ahneman et al. | Buchwald–Hartwig amination | *Science* **2018** |
| Perera et al. | Suzuki–Miyaura coupling | *Science* **2018** |

---

## Setup — Iron Mind via Hugging Face

### 1. Install loaders

```bash
pip install datasets huggingface_hub
```

### 2. Inspect / download

**Option A — load in Python:**

```python
from datasets import load_dataset

ds = load_dataset("gomesgroup/iron-mind-data")
print(ds)
# Explore splits and columns; export a reaction-family subset to CSV
```

**Option B — CLI download to `raw/iron-mind/`:**

```bash
huggingface-cli download gomesgroup/iron-mind-data --repo-type dataset --local-dir data/raw/iron-mind
```

### 3. Normalize to an HTE table

Typical columns to map (names vary by split):

| Column | Meaning |
|---|---|
| `ligand` / `ligand_id` | Phosphine / NHC ligand identifier |
| `base` | Base (e.g., Cs₂CO₃, K₃PO₄) |
| `solvent` | Solvent system |
| `additive` | Optional additive |
| `yield` | Isolated or normalized yield (%) |

Filter to one reaction family (e.g., Buchwald–Hartwig) before building your oracle.

---

## rxn_yields quick start

Official docs: https://rxn4chemistry.github.io/rxn_yields/data/

1. Open the data page and pick one reaction family (e.g., Buchwald–Hartwig / Science 2018).
2. Download the JSON or CSV files listed for that family.
3. Place them under `data/raw/rxn_yields/<family>/`.
4. Normalize to a single HTE table (ligand, base, solvent, additive, yield) before wiring your oracle.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    ├── iron-mind/          # HF download
    ├── rxn_yields/         # optional IBM corpus
    └── hte_buchwald.csv    # your normalized oracle table (gitignored)
```

---

## Offline Hackathon Fallback

The starter agent **generates** a synthetic Buchwald–Hartwig-style yield table on first run if no cached CSV is present (written under `data/raw/`, which is gitignored). The optimization loop treats yields as a **hidden oracle** — only queried rows are revealed.

---

## License & Redistribution

> **LICENSE NOTE:** License terms are not always explicit on the [Iron Mind Hugging Face dataset card](https://huggingface.co/datasets/gomesgroup/iron-mind-data). Treat Iron Mind and rxn_yields as **research-use** corpora. Cite the original *Science* 2018 papers, the Iron Mind preprint ([arXiv:2509.00103](https://arxiv.org/abs/2509.00103)), and any rxn_yields publications. **Verify license terms before redistribution** or commercial use. Do not commit multi-GB raw dumps to Git.

### Citation

Acknowledge Gomes Group / Iron Mind, IBM RXN, and the original HTE experimental teams when presenting results.
