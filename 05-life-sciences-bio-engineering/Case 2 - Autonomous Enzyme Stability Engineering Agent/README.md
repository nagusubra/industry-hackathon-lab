# Case 2 — Autonomous Enzyme Stability Engineering Agent

**Stream:** Life Sciences & Bio-Engineering  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Industrial biocatalysts must survive harsh process conditions — elevated temperature, pH swings, and long residence times. Directed evolution can improve enzyme stability, but wet-lab screening is expensive and slow. Modern pipelines close a **mutate → predict → select → assay** loop: propose amino-acid mutations, predict melting temperature (Tm), and prioritize the next mutants for experimental validation.

**Your challenge:** Build an **autonomous agent** that proposes mutations on a wildtype enzyme sequence, predicts Tm (and optionally uses AlphaFold structural context), and iteratively selects the next mutants to assay — not a single offline regression without a decision loop.

---

## Industrial Significance

- Novozymes and other enzyme manufacturers rely on stability engineering for detergents, biofuels, food processing, and pharma manufacturing.
- The [Novozymes Enzyme Stability Prediction](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction) Kaggle competition provides real sequence–pH–Tm labels paired with an AlphaFold wildtype structure.
- [Meltome Atlas](https://meltome.org/) catalogs experimentally measured protein thermal stability across organisms — useful for literature context and validation.
- Calgary’s biotech and clean-tech sectors need agents that shrink the design–build–test cycle for biocatalyst portfolios.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load Novozymes `train.csv` (sequence, pH, Tm) and the competition AlphaFold wildtype PDB; optionally cite Meltome Atlas for related stability benchmarks.
2. **Represent:** Encode mutations (sequence deltas, k-mer / composition features) and optional structure-context stubs (residue exposure, distance to active site).
3. **Predict:** Regression model for Tm given sequence + pH (sklearn / gradient boosting / small neural net baselines).
4. **Act & Iterate:** Active-learning loop — propose mutations, predict Tm, acquire uncertain or high-potential variants for “virtual wet-lab” reveal, update model, re-rank.
5. **Report:** Ranked mutant shortlist with predicted ΔTm, mutation rationale, and structure links.

---

## Recommended Agent Architecture & Starter Code Pointers

```
Wildtype + mutations -> Featurize -> Tm model -> Acquisition policy -> Next mutants
```

**Starter frameworks (open source):**
- [Novozymes Kaggle competition](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction) — `train.csv`, test sequences, AlphaFold wildtype PDB
- [Meltome Atlas](https://meltome.org/) — literature-curated thermal stability measurements
- [AlphaFold DB](https://alphafold.ebi.ac.uk/) — predicted structures (CC-BY-4.0)
- BioPython, ESM / protein language models (optional), sklearn / XGBoost

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python agent_starter.py --help
```

**Requires Python 3.10+.** HuggingFace / BioPython are optional next steps (see `requirements.txt`).

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Tm prediction RMSE / MAE | Report on held-out Novozymes-style labels |
| ΔTm ranking | Spearman ρ on mutant ranking vs. ground truth |
| Active learning gain | Improvement vs. random acquisition over iterations |
| Structure linkage | ≥1 demonstrated wildtype PDB / AlphaFold context in the narrative |
| Autonomy | Closed propose → (virtual) assay → update loop |
| Ethics / safety | No hazardous synthesis instructions; public screening data only |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
