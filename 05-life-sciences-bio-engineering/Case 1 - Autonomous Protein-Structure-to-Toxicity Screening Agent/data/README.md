# Data Guide — Protein-Structure-to-Toxicity Screening Agent (Stream 5)

---

## 1. EPA Tox21 / ToxCast (bioactivity)

- **ToxCast exploring page:** https://www.epa.gov/comptox-tools/exploring-toxcast-data  
- **Downloadable computational toxicology data:** https://www.epa.gov/comptox-tools/downloadable-computational-toxicology-data  
- **Tox21 program:** https://tox21.gov/data-and-tools/  
- **What:** High-throughput screening bioactivity for thousands of chemicals across many assays; `invitrodb` MySQL + `tcpl` R package for advanced users; flat-file releases also available.
- **Formats:** CSV / TSV flat files; MySQL dumps; API access via EPA CTX Bioactivity APIs
- **License:** EPA open data (free for commercial and non-commercial use per EPA open-data statements)

```bash
mkdir -p raw/toxcast
# Download the latest recommended ToxCast / Tox21 flat files from the EPA pages above.
# Prefer current invitrodb-linked releases for new work; legacy zips remain available.
```

**PubChem:** Tox21 assay records are also browsable via PubChem BioAssay for compound-centric pulls.

---

## 2. RCSB Protein Data Bank (experimental structures)

- **Portal:** https://www.rcsb.org/  
- **Format:** PDB / mmCIF  
- **REST example:**

```bash
mkdir -p raw/pdb
# Download hemoglobin structure 1A3N as an example
curl -L -o raw/pdb/1A3N.pdb https://files.rcsb.org/download/1A3N.pdb
```

Python:

```python
from Bio.PDB import PDBList
pdbl = PDBList()
pdbl.retrieve_pdb_file("1A3N", pdir="raw/pdb", file_format="pdb")
```

---

## 3. AlphaFold Protein Structure Database

- **UI:** https://alphafold.ebi.ac.uk/  
- **Bulk:** Google Cloud `gs://public-datasets-deepmind-alphafold-v4` (CC-BY-4.0)  
- **GitHub access notes:** https://github.com/google-deepmind/alphafold/tree/main/afdb  
- **Formats:** PDB / mmCIF predicted coordinates + confidence metrics (pLDDT, PAE)
- **Hackathon tip:** Download **individual** predictions for a few UniProt accessions — do not mirror hundreds of millions of structures.

Example (website download for a single prediction) or GCS for scripted pulls when cloud tooling is available.

---

## 4. Minimal starter CSV schema (compound–assay)

If EPA flat files are heavy for day-one setup, begin with a compact derived table:

| column | description |
|---|---|
| `compound_id` | Local or DSSTox / CAS identifier |
| `smiles` | Chemical structure |
| `assay_id` | Tox21/ToxCast assay identifier |
| `activity` | 1 active / 0 inactive (or continuous AC50) |

The starter agent can synthesize a toy table for pipeline testing, then you swap in real Tox21 labels.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    ├── toxcast/
    ├── pdb/
    ├── alphafold/
    └── toy_tox21.csv
```

### Ethics note

Use public screening datasets only. Do not attempt to generate instructions for producing controlled or highly hazardous substances. Focus on ranking / triage methodology.
