# Case 2 — Autonomous Compiler-Config Search Agent

**Stream:** Software, Cryptography & Computational Math  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

ML accelerators (TPU, GPU) spend significant compile time searching **tiling, layout, and fusion** configurations before a graph runs at peak throughput. Wrong XLA/TPU compiler settings can yield 2–10× runtime regressions on identical models — a high-dimensional, black-box optimization problem over discrete compiler knobs.

**Your challenge:** Build an **autonomous agent** that perceives an ML computation graph plus candidate compiler configs, searches the configuration space using measured (or predicted) runtime, and iteratively refines configs — beyond “guess tile sizes in a spreadsheet.”

---

## Industrial Significance

- Cloud ML inference/training bills are dominated by wall-clock runtime; compiler autotuning directly affects unit economics.
- TpuGraphs (Google Research / NeurIPS 2023) provides real XLA graphs with measured runtimes across thousands of configs — a reproducible benchmark for learned and search-based autotuners.
- Production stacks (XLA, TensorRT, TVM) all rely on config search; agents that close the loop with live measurement mirror industrial MLOps practice.
- Alberta AI/energy sectors running large batch inference benefit from automated compiler tuning pipelines.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load a TpuGraphs subgraph (nodes, edges, op types) and encode compiler config vectors (tile sizes, layout flags).
2. **Search:** Propose configs via random search, evolutionary methods, Bayesian optimization, or learned policies.
3. **Evaluate:** Measure or predict runtime; compare against held-out configs and competition baselines.
4. **Iterate:** Agent revises search strategy when configs plateau or violate hardware constraints.
5. **Generalize:** Demonstrate transfer across at least two graph families (e.g., `tile:xla` subsets).

---

## Recommended Agent Architecture & Starter Code Pointers

```
Graph + config encoder -> Search policy -> Runtime oracle / TPU measure -> Revised search
```

**Starter frameworks (open source):**
- [TpuGraphs dataset](https://github.com/google-research-datasets/tpu_graphs) (Apache 2.0)
- [Kaggle: Predict AI Model Runtime](https://www.kaggle.com/competitions/predict-ai-model-runtime)
- Paper: Phothilimthana et al., *TpuGraphs: A Performance Prediction Dataset on TPUs*, NeurIPS 2023
- Search libraries: [Nevergrad](https://github.com/facebookresearch/nevergrad), Optuna, random / evolutionary baselines

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
| Runtime improvement | ≥10% reduction vs. random-search median on held-out configs |
| Search efficiency | Best config found within N oracle calls (report N) |
| Prediction quality | MAPE / RMSE vs. measured runtime on validation split (if using surrogate) |
| Constraint satisfaction | Zero invalid configs (negative tiles, OOM layouts) |
| Autonomy | Search policy adapts after plateau (budget reallocation, mutation rate) |
| Reproducibility | Fixed seeds; documented graph subset (`tile:xla` recommended) |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
