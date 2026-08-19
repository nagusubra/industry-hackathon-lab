# Case 5 — Autonomous OPF Solver-Configuration and Scaling Agent

**Stream:** Software, Cryptography & Computational Math  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Optimal Power Flow (OPF) is the workhorse of market clearing, congestion management, and look-ahead dispatch. The **same network** can take milliseconds or fail to converge depending on formulation (DC vs. linearized AC), solver, tolerances, and warm-start. Grid models that are actually shareable without CEII are **synthetic** — ARPA-E GRID DATA / EPIGRIDS cases from the Texas A&M Electric Grid Test Case Repository.

**Your challenge:** Build an **autonomous agent** that searches OPF **solver configurations**, measures wall-clock time and optimality gap, then **re-tunes as network size grows** (small MATPOWER case → ACTIVSg200 → EPIGRIDS Texas / Midwest). A single default `linprog` call is the baseline, not the submission.

This is the same *search-over-configs* pattern as Stream 3 Case 2 (compiler autotuning), applied to a power-system optimization stack.

---

## Industrial Significance

- ISOs cannot share real EMS models (CEII). ARPA-E GRID DATA funded public synthetic grids so algorithms can be tested at realistic scale.
- DOE Office of Electricity and ARPA-E both treat **tractable OPF at interconnection scale** as a blocking R&D problem (see also the ARPA-E Grid Optimization competition).
- Production stacks (MISO/PJM market engines, vendor EMS) already run config/heuristic switches; agents that close the loop with measured solve stats match operator practice.
- Alberta and WECC planning studies hit the same scaling wall once DC-OPF is replaced by security-constrained or stochastic OPF.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Parse a MATPOWER `.m` case (`mpc.bus`, `mpc.gen`, `mpc.branch`, `mpc.gencost`) from EPIGRIDS or a same-family ACTIVS case.
2. **Solve:** Run a baseline DC-OPF (open-source: `scipy.optimize.linprog`, optional `pandapower` / PYPOWER).
3. **Search:** Autonomously try formulation and solver knobs (DC vs. lossy/iterative DC, solver method, constraint scaling, generator bound tightening).
4. **Scale:** Freeze a config, step up to a larger network, then **re-search** when time or infeasibility blows up.
5. **Evaluate:** Report solve time, objective ($/h), primal feasibility (node balance, line limits), and gap vs. the best feasible config found.

Stretch goals: N-1 contingency subset; warm-start across load snapshots; compare HiGHS vs. interior-point; EPIGRIDS Eastern Network only if you have the RAM.

---

## Recommended Agent Architecture & Starter Code Pointers

```
MATPOWER parser -> Baseline OPF -> Config search -> Larger case -> Re-tune -> Log time/gap
```

**Starter frameworks (open, no CEII):**
- EPIGRIDS catalog: https://electricgrids.engr.tamu.edu/electric-grid-test-cases/
- EPIGRIDS Texas (7,336 bus): https://electricgrids.engr.tamu.edu/electric-grid-test-cases/epigrids-texas/
- Day-one MATPOWER files (BSD): [case9.m](https://raw.githubusercontent.com/MATPOWER/matpower/master/data/case9.m), [case_ACTIVSg200.m](https://raw.githubusercontent.com/MATPOWER/matpower/master/data/case_ACTIVSg200.m)
- Optional: `pandapower`, PYPOWER, HiGHS

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python agent_starter.py --help
```

**Requires Python 3.10+.** The starter DC-OPF uses SciPy only; `pandapower` is optional.

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Optimality / cost | Feasible objective ≤ default-config objective (same network) |
| Solve time | Report wall-clock; beat default on a time–cost Pareto sense at ≥1 size |
| Feasibility | Node balance and line limits within documented tolerance |
| Scaling | At least **two** network sizes (e.g. case9 + ACTIVSg200 or EPIGRIDS) |
| Search efficiency | Best config within N OPF solves (report N) |
| Autonomy | Config policy changes after timeout / infeasible / plateau |
| Reproducibility | Fixed seeds; document which `.m` files were used |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
