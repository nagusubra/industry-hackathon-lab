# Case 3 — Autonomous Multi-Endpoint ADMET Risk Triage Agent

**Stream:** Life Sciences & Bio-Engineering  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Early drug discovery must triage thousands of candidates across **multiple toxicology and ADMET endpoints** — not just a single Tox21 assay. ClinTox flags clinical trial failures; SIDER catalogs drug side effects; hERG blockade predicts cardiac liability. Teams need agents that decide **which endpoint deserves the next expensive follow-up assay**.

**Your challenge:** Build an **autonomous agent** that loads multi-endpoint toxicity labels (ClinTox, SIDER, hERG), trains per-endpoint models, and iteratively selects which compounds and endpoints to evaluate next — not a single binary classifier without endpoint-aware acquisition.

---

## Industrial Significance

- ADMET attrition drives >40% of late-stage drug failures; multi-endpoint triage is standard in pharma portfolios.
- [MoleculeNet](https://moleculenet.org/) (Wu et al., *Chem. Sci.* 2018) standardized benchmark datasets including ClinTox and SIDER.
- [Therapeutics Data Commons (TDC)](https://tdcommons.ai/) provides unified Python loaders for hERG (Karim et al., CC BY 4.0) and other ADMET tasks.
- Calgary health-innovation teams can prototype agents that generalize to real medicinal-chemistry workflows.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load ClinTox (HuggingFace or MoleculeNet), SIDER, and hERG via PyTDC (`Tox(name="hERG")`); save compact CSVs under `data/raw/admet/`.
2. **Represent:** Featurize SMILES (fingerprints / descriptors) shared across endpoints.
3. **Predict:** Per-endpoint classifiers (ClinTox, SIDER, hERG) with calibrated risk scores.
4. **Act & Iterate:** Acquisition policy chooses the **most uncertain endpoint–compound pair** for virtual assay reveal; update models; re-rank portfolio risk.
5. **Report:** Multi-endpoint risk dashboard with recommended follow-up assays and rationale.

---

## Recommended Agent Architecture & Starter Code Pointers

```
SMILES -> Shared featurizer -> Per-endpoint models -> Endpoint-aware acquisition -> Next assays
```

**Starter frameworks (open source):**
- [MoleculeNet ClinTox on HuggingFace](https://huggingface.co/datasets/scikit-fingerprints/MoleculeNet_ClinTox)
- [PyTDC](https://tdcommons.ai/) — `from tdc.single_pred import Tox` for SIDER, `Tox(name="hERG")`, etc.
- [MoleculeNet paper](https://pubs.rsc.org/en/content/articlehtml/2018/sc/c7sc02664a) — Wu et al., *Chem. Sci.* 2018
- RDKit, DeepChem, sklearn (optional)

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python agent_starter.py --help
```

**Requires Python 3.10+.** PyTDC is optional for real data (see `requirements.txt`).

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Per-endpoint AUROC / AUPRC | ClinTox, SIDER, hERG held-out performance |
| Endpoint selection quality | Acquisition picks high-information pairs vs. random |
| Active learning gain | Portfolio risk ranking improves over iterations |
| Multi-endpoint coverage | ≥3 distinct endpoints integrated |
| Autonomy | Closed perceive → predict → acquire → update loop |
| Ethics / safety | Public screening data only; no hazardous synthesis instructions |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
