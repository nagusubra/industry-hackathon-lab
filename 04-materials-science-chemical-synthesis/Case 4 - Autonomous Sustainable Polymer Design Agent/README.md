# Case 4 — Autonomous Sustainable Polymer Design Agent

**Stream:** Materials Science & Chemical Synthesis  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Designing sustainable polymers with target **glass-transition temperature (Tg)**, thermal conductivity, radius of gyration (Rg), density, and fractional free volume (FFV) requires navigating a vast SMILES / repeat-unit space under multi-property constraints. Manual iteration in the lab is slow and expensive.

**Your challenge:** Build an **autonomous polymer-design agent** that ingests the NeurIPS Open Polymer Prediction 2025 corpus, scores candidates against multi-objective targets (e.g., high Tg for heat resistance + favorable processability proxies), proposes next repeat units to evaluate, and iteratively refines its search — a closed design loop, not a one-shot property predictor.

---

## Industrial Significance

- Lightweight, heat-resistant, recyclable polymers are critical for EV battery packs, aerospace composites, and circular-economy packaging.
- The NeurIPS 2025 open polymer benchmark provides thousands of labeled repeat units with five key properties — ideal for agentic design under uncertainty.
- Post-competition analysis ([arXiv:2512.08896](https://arxiv.org/abs/2512.08896)) documents state-of-the-art modeling strategies your agent can build on or surpass.
- Alberta’s plastics circularity and advanced-manufacturing initiatives benefit from faster sustainable-materials R&D.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load polymer repeat units (SMILES) and labels: Tg, thermal conductivity, Rg, density, FFV.
2. **Featurize:** Molecular fingerprints (RDKit), hand-crafted descriptors, or learned embeddings.
3. **Search:** Multi-objective ranking toward target Tg / thermal windows with penalty terms for unfavorable FFV or density.
4. **Act & Iterate:** Agent proposes next candidate polymers (genetic / Bayesian / LLM-guided mutations) and re-scores after each batch.
5. **Report:** Pareto shortlist with SMILES, predicted / labeled properties, and design rationale.

---

## Recommended Agent Architecture & Starter Code Pointers

```
Load polymer table  ->  featurize SMILES  ->  multi-objective rank  ->  propose mutations  ->  re-score
```

**Starter frameworks (open source):**
- [NeurIPS Open Polymer Prediction 2025 (Kaggle)](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025)
- Mirror dataset: https://www.kaggle.com/datasets/rathinumesh/neurips-open-polymer-prediction-2025
- Post-competition report: [arXiv:2512.08896](https://arxiv.org/abs/2512.08896)
- Optional: RDKit, Chemprop, Uni-Mol for property models

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python agent_starter.py --help
```

**Requires Python 3.10+.**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Tg target hit rate | Fraction of shortlist within ±20 °C of target Tg |
| Multi-objective Pareto size | Non-dominated set across Tg vs. thermal conductivity |
| Proposal quality | Next-batch candidates improve mean agent score vs. random |
| Autonomy | ≥2 iterations where proposed candidates change based on prior shortlist |
| Model rigor | Cross-validated property models or honest train/hold-out split |
| Reproducibility | Seeded search + saved shortlist CSV |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
