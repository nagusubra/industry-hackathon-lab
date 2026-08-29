# Case 2 — Autonomous Calgary Building Retrofit-Prioritization Agent

**Stream:** Energy and Infrastructure Systems  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

The City of Calgary owns offices, rec centres, fire halls, and more. Some buildings use far more energy per square metre than others. The retrofit budget **cannot** fix every building this year.

This is the same job a corporate energy manager does with a spreadsheet — except your program should **re-rank** after you change the budget or the goal (save kWh vs save dollars vs cut emissions).

**Your challenge:** Rank City buildings so a limited dollar budget (you pick a number and state it) cuts the most energy use. Beat “fix the biggest building first.” Then change the budget or the scoring rule once and show how the funded list changes.

---

## Industrial Significance

- Calgary has published environmental performance for City-owned buildings and corporate energy consumption on Open Calgary — the same class of data building operators use in ENERGY STAR / BenchmarkYYC programs.
- **Who would use this:** City of Calgary Corporate Properties, Community Energy Programs, or a contractor bidding retrofit packages. **What is sold:** more kWh (or GHG) saved per dollar of public money.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load Open Calgary building energy / emissions / floor-area fields. Clean missing rows; do not invent numbers.
2. **Reason:** Score each building (for example kWh per m², or $/year, or GHG). State the formula in one sentence.
3. **Act:** Given budget `B`, pick a set of buildings (simple knapsack: take next-best until money runs out). Assume a retrofit cost if the City file has no cost — **state the assumption** (e.g. $50 / m²).
4. **Iterate:** Change `B` or switch from “energy first” to “emissions first” and re-run.
5. **Explain:** Which buildings got funded, estimated savings, leftover budget.

Stretch: join [Corporate Energy Consumption](https://data.calgary.ca/Environment/Corporate-Energy-Consumption/crbp-innf) if it adds a time trend.

---

## Recommended Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Score      │ -> │  Fill budget   │ -> │  Re-rank    │
│ Open Calgary│    │ kWh per $    │    │ greedy vs your │    │ new budget  │
│ buildings   │    │ or GHG per $ │    │ rule           │    │ or weights  │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
```

Run [`agent_starter.py`](agent_starter.py). See [`data/README.md`](data/README.md).

**Requires Python 3.10+ (3.11 recommended).**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Baseline | Greedy “largest kWh first” (or largest floor area) under the same budget |
| Your list | Higher estimated kWh or GHG saved per dollar, or same savings at lower spend — report both |
| Feasibility | Do not spend more than `B`; no duplicate buildings |
| Loop | ≥ 1 re-rank after changing budget or weights |
| Demo | Table of funded buildings + leftover $ |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
