# Case 4 — Autonomous Binding-Affinity Discovery Agent

**Stream:** Life Sciences & Bio-Engineering  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Structure-based drug discovery depends on ranking ligands by predicted binding affinity to a protein target. Experimental Ki / IC50 measurements exist in public databases, but portfolios are too large to assay exhaustively. Active learning closes a **rank → assay → update** loop against held-out experimental affinities.

**Your challenge:** Build an **autonomous agent** that ranks ligands by predicted binding affinity for a target family, selects the most informative compounds for virtual assay reveal, and iteratively improves rankings — not a single static QSAR without a decision loop.

---

## Industrial Significance

- [BindingDB](https://www.bindingdb.org/) is a FAIR-sharing public repository of measured protein–ligand affinities (Ki, IC50, Kd).
- Lead-optimization teams routinely filter millions of compounds before SPR, ITC, or cellular potency assays.
- Calgary’s life-sciences sector can prototype affinity-discovery agents that scale to real medicinal-chemistry portfolios.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Download BindingDB articles TSV (~17 MB) — not the full 565 MB dump for day one; filter to one UniProt target ID.
2. **Represent:** Featurize ligand SMILES (fingerprints / descriptors); optionally encode target family metadata.
3. **Predict:** Regression or ranking model for pKi / pIC50 from ligand features.
4. **Act & Iterate:** Active-learning loop — acquire uncertain or high-potential ligands for virtual reveal, update model, re-rank.
5. **Report:** Ranked ligand shortlist with predicted affinity, target UniProt ID, and assay type rationale.

---

## Recommended Agent Architecture & Starter Code Pointers

```
BindingDB ligands -> Featurize -> Affinity model -> Acquisition policy -> Next ligands
```

**Starter frameworks (open source):**
- [BindingDB download page](https://www.bindingdb.org/rwd/bind/chemsearch/marvin/Download.jsp) — prefer `BindingDB_BindingDB_Articles_*_tsv.zip` (~17 MB)
- [BindingDB citation](https://www.bindingdb.org/rwd/bind/info.jsp) — cite BindingDB; check terms-of-use for commercial use
- RDKit, DeepChem, sklearn

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python agent_starter.py --help
```

**Requires Python 3.10+.** RDKit is an optional next step (see `requirements.txt`).

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Affinity prediction RMSE / MAE | pKi / pIC50 on held-out BindingDB-style labels |
| Ranking quality | Spearman ρ on ligand ranking vs. ground truth |
| Active learning gain | Improvement vs. random acquisition over iterations |
| Target focus | Demonstrate filtering to ≥1 UniProt target family |
| Autonomy | Closed rank → (virtual) assay → update loop |
| Ethics / safety | Public FAIR data only; no hazardous synthesis instructions |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
