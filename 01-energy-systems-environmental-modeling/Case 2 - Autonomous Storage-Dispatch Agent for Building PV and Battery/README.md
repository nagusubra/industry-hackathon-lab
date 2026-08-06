# Case 2 — Autonomous Storage-Dispatch Agent for Building PV + Battery

**Stream:** Energy Systems & Environmental Modeling  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Commercial and industrial buildings with rooftop PV and behind-the-meter batteries face a daily optimization problem: when should the battery charge, discharge, or idle given uncertain solar production, stochastic load, and time-varying retail buy/sell prices? Poor dispatch leaves money on the table (buying grid power at peak prices) or degrades the battery through unnecessary cycling.

**Your challenge:** Build an **autonomous AI agent** that ingests 15-minute building load, PV production, and price signals, reasons about state-of-charge (SOC) trajectories and price arbitrage opportunities, and iteratively proposes (and evaluates) charge/discharge schedules — not a static rule-of-thumb dashboard.

---

## Industrial Significance

- Behind-the-meter storage is a fast-growing segment for utilities, ESCOs, and building operators seeking demand-charge reduction and price arbitrage.
- Schneider Electric and industry partners hosted the DrivenData **Power Laws** competition on exactly this problem — winning solutions demonstrate real-world dispatch strategies.
- Alberta and Canadian net-zero building codes increasingly couple on-site PV with storage; agents that close the loop from forecast → SOC policy → evaluated cost are directly industrially relevant.
- Optimized dispatch reduces peak grid draw, lowers customer bills, and improves battery asset utilization.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Ingest 15-minute site-level consumption, PV production, and buy/sell price time series (DrivenData Power Laws training data — 11 sites).
2. **Predict:** Optional short-horizon forecasts for load, PV, and prices with uncertainty bands.
3. **Optimize:** Formulate a multi-period battery dispatch problem respecting SOC limits, charge/discharge efficiency, and power ratings.
4. **Act & Iterate:** Implement an agent loop that proposes charge rates, evaluates simulated electricity cost, and revises policies when forecast error or constraint violations appear.
5. **Explain:** Emit operator-facing summaries: daily cost savings vs. baseline, SOC trajectory, peak-shaving impact.

Stretch goals: multi-site fleet dispatch; degradation-aware cycling penalties; coupling with demand-response signals.

---

## Recommended Agent Architecture & Starter Code Pointers

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Reason     │ -> │  Tool / Sim    │ -> │  Act / Log  │
│ load+PV+    │    │ SOC forecast │    │ battery energy │    │ charge rate │
│ price CSV   │    │ + price risk │    │ balance model  │    │ & metrics   │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
                              ^                                     |
                              +------------- evaluate --------------+
```

**Starter references (open source / competition):**
- [DrivenData Power Laws competition](https://www.drivendata.org/competitions/53/optimize-photovoltaic-battery/) — problem definition and leaderboard
- [Schneider Electric Data Exchange rehost](https://data.exchange.se.com/explore/dataset/power-laws-optimizing-demand-side-strategies-training-data/information/) — training CSVs
- [Winning solutions repo](https://github.com/drivendataorg/power-laws-optimization) — reference dispatch strategies

**In this folder:**
- [`agent_starter.py`](agent_starter.py) — perceive / reason / act skeleton wired to local CSV paths
- [`requirements.txt`](requirements.txt) — core Python dependencies
- [`data/README.md`](data/README.md) — verified dataset links, schemas, and download steps

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python agent_starter.py --help
```

**Requires Python 3.10+ (3.11 recommended).**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Electricity cost ($) | Reduce vs. no-battery / naive charge-when-surplus baseline over held-out days |
| Peak grid import (kW) | Minimize while meeting load + SOC constraints |
| SOC feasibility | Zero hard constraint violations (0–100% SOC, power limits) |
| Arbitrage capture | Report savings attributable to buy-low / sell-high timing |
| Agent loop autonomy | ≥ 1 closed-loop iteration (propose → simulate → revise) without human prompts |
| Runtime practicality | End-to-end demo runnable within the 48-hour prototype window |

Judges will prioritize **physics-aware battery dispatch + autonomous tool use** over UI polish alone. See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
