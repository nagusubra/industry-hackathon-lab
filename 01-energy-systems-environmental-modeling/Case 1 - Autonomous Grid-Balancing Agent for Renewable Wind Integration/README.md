# Case 1 — Autonomous Grid-Balancing Agent for Renewable Wind Integration

**Stream:** Energy Systems & Environmental Modeling  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Modern power grids must continuously balance supply and demand while absorbing highly variable wind generation. Forecast errors, ramp events, and transmission constraints create real operational risk: curtailment of renewables, expensive peaker plant dispatch, and — in extreme cases — frequency instability.

**Your challenge:** Build an **autonomous AI agent** that ingests wind resource / power forecasts and load time series, reasons about grid imbalance risk, and iteratively proposes (and evaluates) dispatch / storage / curtailment actions against a physics-aware power system model — not a chat wrapper over a static dashboard.

---

## Industrial Significance

- Wind variability is a first-order bottleneck for high-renewable grids in Alberta and across North America.
- Grid operators (ISOs / utilities) already consume NREL-class meteorological and forecast products; agents that close the loop from forecast → action are industrially relevant.
- Alberta’s electricity system and Canadian net-zero pathways depend on reliable renewable integration with storage and flexible loads.
- Solutions that reduce imbalance penalties, curtailment, or reserve requirements have direct economic and environmental value.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Ingest open wind and load datasets (NREL WIND Toolkit subsets and/or NREL PERFORM Phase II ISO forecasts; optional PJM hourly load for demand-side experiments).
2. **Predict:** Produce short-horizon wind power and net-load forecasts with uncertainty estimates.
3. **Optimize:** Formulate a dispatch / storage schedule (e.g., via PyPSA linear optimal power flow or a simplified balancing-area model) that respects capacity and energy constraints.
4. **Act & Iterate:** Implement an agent loop that proposes actions, evaluates them in simulation, and revises plans when forecast error or constraint violations appear.
5. **Explain:** Emit operator-facing summaries: imbalance risk, recommended reserve, curtailment vs. storage trade-offs.

Stretch goals: couple OpenFAST / turbine physics for site-specific power curves; multi-zone balancing with transmission limits; carbon intensity of the resulting dispatch.

---

## Recommended Agent Architecture & Starter Code Pointers

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Reason     │ -> │  Tool / Sim    │ -> │  Act / Log  │
│ wind+load   │    │ forecast +   │    │ PyPSA / reV /  │    │ dispatch &  │
│ time series │    │ risk policy  │    │ OpenFAST tools │    │ metrics     │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
                              ^                                     |
                              +------------- evaluate --------------+
```

**Starter frameworks (open source):**
- [PyPSA](https://github.com/PyPSA/pypsa) — Python for Power System Analysis (network + LOPF optimization)
- [OpenFAST](https://github.com/OpenFAST/openfast) — NREL whole-turbine aero-hydro-servo-elastic simulation
- NREL [WIND Toolkit on AWS](https://registry.opendata.aws/nrel-pds-wtk/) — meteorological + power estimates
- [PERFORM Forecasts documentation](https://github.com/PERFORM-Forecasts/documentation) — ISO load/wind/solar actuals + probabilistic forecasts
- Optional: NREL `reV` for renewable potential modeling

**In this folder:**
- [`agent_starter.py`](agent_starter.py) — perceive / reason / act skeleton wired to a local CSV path
- [`requirements.txt`](requirements.txt) — core Python dependencies
- [`data/README.md`](data/README.md) — verified dataset links, schemas, and download commands

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
| Net-load forecast MAE or RMSE | Report vs. naive persistence baseline |
| Imbalance energy (MWh) | Reduce vs. no-control / greedy baseline over a held-out week |
| Curtailment fraction | Minimize while meeting demand + reserve constraints |
| Storage SOC feasibility | Zero hard constraint violations in the simulated horizon |
| Agent loop autonomy | ≥ 1 closed-loop iteration (propose → simulate → revise) without human prompts |
| Runtime practicality | End-to-end demo runnable within the 48-hour prototype window |

Judges will prioritize **hard-science grid physics + autonomous tool use** over UI polish alone. See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
