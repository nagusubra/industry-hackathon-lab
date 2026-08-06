# Case 2 — Autonomous Reaction-Condition Optimizer

**Stream:** Materials Science & Chemical Synthesis  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

High-throughput experimentation (HTE) for cross-coupling reactions (Buchwald–Hartwig, Suzuki–Miyaura) produces large tables of ligand / base / solvent / additive combinations with measured yields. The combinatorial space is far too large to screen exhaustively in the lab.

**Your challenge:** Build an **autonomous reaction-optimization agent** that proposes reaction conditions, queries a **hidden yield oracle** (simulating wet-lab measurements), and iteratively refines its search under a fixed experiment budget — an active-learning / bandit loop, **not** supervised regression trained on the full yield table.

---

## Industrial Significance

- Pharmaceutical and fine-chemical manufacturing spend weeks optimizing a single coupling step; HTE + ML can collapse that timeline.
- Landmark Science 2018 studies (Ahneman et al.; Perera et al.) showed that modest HTE datasets enable predictive models — but industrial workflows need **sequential, budgeted** decision-making.
- Iron Mind and rxn_yields consolidate modern HTE yield corpora for benchmarking autonomous optimizers.
- Alberta’s growing advanced-materials and energy-chemicals sector benefits from faster route scouting.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load or stream HTE yield tables (ligand, base, solvent, additive, yield) from Iron Mind / rxn_yields — or a synthetic Buchwald–Hartwig-style table.
2. **Oracle:** Treat yields as **hidden** — the agent may only observe outcomes for conditions it explicitly proposes (no peeking at the full table for training).
3. **Explore / Exploit:** Implement bandit, UCB, Thompson sampling, or Bayesian optimization over categorical reaction descriptors.
4. **Act & Iterate:** Propose the next batch of conditions each round; track best yield, regret, and budget remaining.
5. **Report:** Best conditions found, yield trajectory, and comparison to random / grid baselines.

---

## Recommended Agent Architecture & Starter Code Pointers

```
Propose conditions  ->  Query hidden yield oracle  ->  Update belief / bandit stats  ->  Re-propose
```

**Starter frameworks (open source):**
- [Iron Mind dataset (Hugging Face)](https://huggingface.co/datasets/gomesgroup/iron-mind-data) — [arXiv:2509.00103](https://arxiv.org/abs/2509.00103)
- [rxn_yields data docs](https://rxn4chemistry.github.io/rxn_yields/data/)
- Ahneman et al., *Science* **2018** (Buchwald–Hartwig HTE)
- Perera et al., *Science* **2018** (Suzuki–Miyaura HTE)
- Optional: BoTorch / GPyTorch for Bayesian optimization over mixed categorical spaces

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
| Best yield found | Report max yield within budget vs. random baseline |
| Regret | Cumulative regret vs. oracle optimum (if known offline for eval only) |
| Sample efficiency | Yield ≥ 80% of table max using ≤ 10% of conditions queried |
| Autonomy | Closed loop: propose → measure → update → re-propose for ≥ 3 rounds |
| No cheating | Agent must not fit on unqueried rows during the optimization loop |
| Reproducibility | Seeded oracle + saved query log (JSON/CSV) |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
