# Case 7 — Autonomous Building-Stock Electrification and Retrofit-Prioritization Agent

**Stream:** Energy Systems & Environmental Modeling  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Utilities, cities, and state energy offices have **finite incentive budgets** and **finite distribution-feeder headroom**. NREL’s ResStock / ComStock End-Use Load Profiles give calibrated 15-minute loads for the U.S. building stock **with and without upgrade packages**. Plotting savings shapes is not the job. The job is to **allocate a constrained retrofit budget across building segments** to maximize peak-load reduction and energy reduction per dollar, subject to a grid-capacity (or coincident-peak) constraint, then revise the allocation when the constraint or package costs change.

**Your challenge:** Build an **autonomous AI agent** that compares baseline vs. upgrade-package load profiles by segment (building type, vintage, climate / state), solves a budgeted allocation, and evaluates it against a greedy “biggest-savings-first” baseline.

---

## Industrial Significance

- Electrification and envelope upgrades shift both **annual kWh** and **coincident peak** — the quantity that drives distribution upgrades and resource adequacy.
- DOE / NREL published the End-Use Load Profiles and End-Use Savings Shapes specifically so planners can value efficiency, demand flexibility, and electrification in time, not just as annual therms.
- Alberta and other cold-climate jurisdictions face the same winter-peak vs. envelope/heat-pump trade-off; the methods transfer even if you start on a U.S. state extract (Colorado is the recommended day-one slice).
- This is capital rationing under physics constraints — the same class of problem IRP and DSM program designers already run, now as an agent loop.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load pre-aggregated state-level 15-minute (or annual) ResStock results for **baseline (upgrade=0)** and **at least one upgrade package** for several building types in one state.
2. **Characterize:** For each segment, compute annual energy reduction, coincident-peak reduction, and a retrofit cost proxy (use NREL package cost assumptions or a documented $/dwelling you choose).
3. **Optimize:** Allocate a budget B across segments (continuous share or integer dwelling counts) to maximize a weighted objective (peak kW saved, kWh saved) subject to budget and an optional remaining-peak cap.
4. **Act & Iterate:** Compare to greedy biggest-savings-first; tighten or shift weights when the peak cap is violated or $/kW is worse than greedy.
5. **Explain:** Which segments get funded, expected peak and energy impact, leftover budget, and constraint slack.

Stretch goals: PUMA-level targeting; combine ResStock + ComStock; demand-flexibility packages vs. envelope-only; carbon intensity of the regional grid.

---

## Recommended Agent Architecture & Starter Code Pointers

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Reason     │ -> │  Tool / Sim    │ -> │  Act / Log  │
│ baseline vs │    │ segment      │    │ budgeted       │    │ mix & peak  │
│ upgrade CSV │    │ kW / kWh / $ │    │ knapsack / LP  │    │ vs greedy   │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
                              ^                                     |
                              +------------- evaluate --------------+
```

**Starter references:**
- Dataset (AWS Open Data, no account): https://registry.opendata.aws/nrel-pds-building-stock/
- OpenEI submission: https://data.openei.org/submissions/4520
- ResStock viewers: https://resstock.nlr.gov/datasets
- Practical access guide: Wilson et al., NREL/TP-5500-83907, https://www.osti.gov/biblio/1909353

**In this folder:**
- [`agent_starter.py`](agent_starter.py) — segment savings + budget allocation loop
- [`requirements.txt`](requirements.txt)
- [`data/README.md`](data/README.md) — exact `aws s3 --no-sign-request` and HTTPS paths

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python agent_starter.py --help
```

**Requires Python 3.10+ (3.11 recommended).** AWS CLI is optional (HTTPS curl works for the day-one files).

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Peak reduction (kW) | Maximize coincident peak cut for budget B vs. greedy baseline |
| Energy reduction (kWh/yr) | Report alongside peak; state the objective weights |
| Cost-effectiveness | $/kW-peak and $/kWh; beat greedy on the stated objective |
| Constraint feasibility | Budget not exceeded; optional peak-cap respected |
| Segment coverage | At least 3 building types (or vintage bins) in one state |
| Agent loop autonomy | ≥ 1 closed-loop iteration (allocate → simulate peak → reweight) |
| Runtime practicality | Demo on **pre-aggregated** files, not the full 900k-building dump |

Judges will prioritize **constrained allocation quality** over a stock-viewer clone. See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
