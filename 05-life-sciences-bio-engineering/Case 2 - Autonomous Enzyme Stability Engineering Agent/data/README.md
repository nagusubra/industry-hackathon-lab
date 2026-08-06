# Data Guide — Autonomous Enzyme Stability Engineering Agent (Stream 5)

---

## 1. Novozymes Enzyme Stability Prediction (Kaggle)

- **Competition:** https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction  
- **What:** Amino-acid sequences with experimental melting temperature (Tm) at specified pH; includes AlphaFold wildtype structure files in the competition bundle.
- **Key files:** `train.csv` (sequence, pH, tm), `test.csv`, wildtype PDB from AlphaFold (in competition download).
- **License:** Kaggle competition terms — research / non-commercial use; **flag for your team** before commercial deployment.

### Kaggle API credentials

1. Create a **free Kaggle account** at https://www.kaggle.com/ and accept the competition rules.
2. Open **Account → API → Create New Token** — this downloads `kaggle.json`.
3. Place the token at `~/.kaggle/kaggle.json` (Linux/macOS) or `%USERPROFILE%\.kaggle\kaggle.json` (Windows).
4. Install the CLI and download:

```bash
pip install kaggle
mkdir -p data/raw/novozymes
kaggle competitions download -c novozymes-enzyme-stability-prediction -p data/raw/novozymes --unzip
```

5. Point your agent at:
   - `data/raw/novozymes/train.csv` — labeled sequences with `sequence`, `pH`, `tm` columns
   - Wildtype structure file(s) included in the competition bundle (AlphaFold PDB)

**Citation:** Novozymes Enzyme Stability Prediction Kaggle competition; see competition data page for full attribution.

---

## 2. Meltome Atlas (literature context)

- **Portal:** https://meltome.org/  
- **What:** Curated database of protein thermal stability measurements (Tm, Tagg) across organisms and conditions.
- **Use:** Cross-reference stability benchmarks, literature validation, and feature engineering ideas.
- **License:** Public web resource for **research use**; cite Meltome Atlas in your README / poster. Do not bulk-redistribute scraped content.

---

## 3. AlphaFold wildtype structure

The Novozymes competition bundle includes an AlphaFold-predicted wildtype structure. You can also fetch related entries from:

- **AlphaFold DB UI:** https://alphafold.ebi.ac.uk/  
- **Bulk:** Google Cloud `gs://public-datasets-deepmind-alphafold-v4` (CC-BY-4.0)

**Hackathon tip:** Use the competition-provided PDB under `data/raw/novozymes/` for day one; do not mirror the full AlphaFold database.

---

## 4. Minimal starter CSV schema (mutant–stability)

| column | description |
|---|---|
| `mutant_id` | Local identifier (e.g. `MUT_0042`) |
| `sequence` | Amino-acid sequence (single-letter code) |
| `pH` | Assay pH |
| `tm` | Melting temperature (°C) |
| `n_mutations` | Count of substitutions vs. wildtype |

The starter agent synthesizes a toy table for pipeline testing; swap in real Novozymes labels when ready.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    ├── novozymes/
    │   ├── train.csv
    │   └── (wildtype PDB from competition)
    └── toy_enzyme_stability.csv
```

### Ethics note

Use public screening and competition data only. Do not generate instructions for hazardous protein expression, pathogen engineering, or controlled-substance synthesis. Focus on in silico triage and stability ranking methodology.
