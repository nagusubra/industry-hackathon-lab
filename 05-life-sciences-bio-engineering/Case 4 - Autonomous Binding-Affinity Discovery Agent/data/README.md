# Data Guide — Autonomous Binding-Affinity Discovery Agent (Stream 5)

---

## 1. BindingDB (measured protein–ligand affinities)

- **Download page:** https://www.bindingdb.org/rwd/bind/chemsearch/marvin/Download.jsp  
- **What:** Ki, IC50, Kd, and related measurements linked to protein targets and ligand structures (SMILES / InChI).
- **License:** BindingDB is a public FAIR-sharing resource; free downloads. **Cite BindingDB** and review the [terms of use](https://www.bindingdb.org/rwd/bind/info.jsp) for commercial restrictions.

### Step-by-step download

1. Open the download page above (no login observed for TSV downloads).
2. Download **`BindingDB_BindingDB_Articles_*_tsv.zip`** (~17 MB) — **prefer this** over `BindingDB_All_*` (~565 MB) for hackathon day one.
3. Unzip to `data/raw/bindingdb/`:

```bash
mkdir -p data/raw/bindingdb
# Linux/macOS:
unzip BindingDB_BindingDB_Articles_*_tsv.zip -d data/raw/bindingdb/
# Windows (PowerShell):
Expand-Archive BindingDB_BindingDB_Articles_*_tsv.zip -DestinationPath data\raw\bindingdb
```

4. Filter to **one target UniProt ID** for experiments:

```python
import pandas as pd
from pathlib import Path

# Prefer the articles-only TSV (~17 MB). Filenames include a YYYYMM date stamp.
tsv = next(Path("data/raw/bindingdb").glob("BindingDB_BindingDB_Articles_*_tsv/*.tsv"), None) \
      or next(Path("data/raw/bindingdb").glob("*.tsv"))
df = pd.read_csv(tsv, sep="\t", low_memory=False)
# Column names may vary slightly by release — inspect df.columns if needed.
target_col = [c for c in df.columns if "UniProt" in c and "Primary" in c][0]
target_uniprot = "P00533"  # example: EGFR — pick your target
subset = df[df[target_col] == target_uniprot]
subset.to_csv("data/raw/bindingdb/target_P00533.csv", index=False)
```

**Hackathon tip:** Start with the articles-only TSV; expand to the full dump only if you need broader coverage.

---

## 2. Minimal starter CSV schema (ligand–affinity)

| column | description |
|---|---|
| `ligand_id` | Local identifier (e.g. `LIG_0042`) |
| `smiles` | Ligand SMILES |
| `target_uniprot` | UniProt accession for the protein target |
| `affinity_type` | `Ki` / `IC50` / `Kd` |
| `affinity_nM` | Measured affinity in nM |
| `paffinity` | −log10(affinity in M) for modeling |

The starter agent synthesizes a toy table for pipeline testing; swap in real BindingDB labels when ready.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    └── bindingdb/
        ├── BindingDB_BindingDB_Articles_*.tsv
        └── target_<UNIPROT>.csv
```

### Ethics note

Use public FAIR screening data only. Do not generate instructions for synthesizing controlled or highly hazardous substances. Focus on in silico affinity ranking and assay prioritization methodology.
