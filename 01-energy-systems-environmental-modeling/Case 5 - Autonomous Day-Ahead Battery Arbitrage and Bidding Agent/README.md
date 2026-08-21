# Case 5 — Autonomous Day-Ahead Battery Arbitrage and Bidding Agent

**Stream:** Energy Systems & Environmental Modeling  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

In PJM, battery operators must submit **day-ahead charge/discharge bids before the real-time (and even day-ahead) price is known**. A persistence or naive “buy below the mean” policy leaves money on the table, over-cycles the pack, or both. This is a forecasting-plus-decision problem, not a chart of historical prices.

**Your challenge:** Build an **autonomous AI agent** that forecasts next-day COMED zonal prices, computes a feasible state-of-charge (SOC) bidding trajectory (power/energy limits, round-trip efficiency, degradation cost), then evaluates **realized arbitrage revenue** against a perfect-foresight upper bound and a naive threshold-bidding baseline — and revises the forecast/policy when capture ratio is weak.

This case is **day-ahead price + storage economics**. It is not real-time load balancing (see Case 4) and does not use the Kaggle hourly PJM *load* dataset referenced in Case 1.

---

## Industrial Significance

- Independent storage operators and aggregators (and ISO market desks) live on this loop: forecast → bid → clear → settle → retrain.
- PJM is the largest U.S. ISO by load; COMED zonal day-ahead prices plus day-ahead load forecasts are a standard North American EPF benchmark.
- DOE Office of Electricity’s 2026 priorities include **affordability** and **scaling storage** into wholesale markets as load grows (data centers, manufacturing). Agents that convert price uncertainty into feasible bids have direct commercial value.
- The epftoolbox PJM series is a published, citable 6-year hourly benchmark (Lago et al., *Applied Energy* 2021).

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load hourly COMED zonal price, PJM system load forecast, and COMED zonal load forecast (2013-01-01 through 2018-12-24).
2. **Forecast:** Produce a 24-hour day-ahead price forecast (persistence, LASSO/LEAR-style, or your own model). Do **not** import the AGPL-licensed `epftoolbox` package — implement your own models.
3. **Optimize:** Given the forecast, solve a battery dispatch/bid trajectory subject to power rating, energy capacity, round-trip efficiency, and a per-MWh degradation cost.
4. **Act & Iterate:** Submit the bid, settle against **realized** prices, compare to perfect-foresight and threshold baselines, then revise forecast features or bid thresholds.
5. **Explain:** Report $/MW-year (or $/day) captured, capture ratio vs. perfect foresight, cycle count, and constraint violations.

Stretch goals: probabilistic forecasts + CVaR bidding; co-optimize energy and ancillary services (simplified); walk-forward Diebold–Mariano tests on forecast residuals **in addition to** the economic loop.

---

## Recommended Agent Architecture & Starter Code Pointers

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Reason     │ -> │  Tool / Sim    │ -> │  Act / Log  │
│ PJM.csv     │    │ 24h price    │    │ battery SOC    │    │ bid & $     │
│ price+load  │    │ forecast     │    │ DP / LP dispatch│    │ vs baselines│
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
                              ^                                     |
                              +------------- evaluate --------------+
```

**Starter references (open data / papers):**
- Dataset: [Zenodo 4624805 — `PJM.csv`](https://zenodo.org/records/4624805) (direct file URL in [`data/README.md`](data/README.md))
- Paper: Lago, Marcjasz, De Schutter, Weron. *Forecasting day-ahead electricity prices…*, Applied Energy 293:116983 (2021). https://doi.org/10.1016/j.apenergy.2021.116983
- PJM Data Miner 2 (optional extra series): https://dataminer2.pjm.com/

**In this folder:**
- [`agent_starter.py`](agent_starter.py) — forecast → dispatch → settle loop (downloads `PJM.csv` or uses labeled synthetic demo data)
- [`requirements.txt`](requirements.txt)
- [`data/README.md`](data/README.md) — download, schema, license (do **not** pip-install `epftoolbox`)

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
| Realized arbitrage revenue ($) | Report vs. naive threshold-bidding baseline over held-out days |
| Capture ratio | Realized $ / perfect-foresight $ (same battery constraints) |
| SOC feasibility | Zero hard violations (energy/power limits, complementary charge/discharge) |
| Degradation | Report equivalent full cycles and $ penalty used |
| Forecast quality | MAE / sMAPE on held-out hours **plus** economic metrics (forecasts alone are not enough) |
| Agent loop autonomy | ≥ 1 closed-loop iteration (forecast → bid → settle → revise) without human prompts |
| Runtime practicality | End-to-end demo runnable within the 48-hour prototype window |

Judges will prioritize **forecast-to-bid decision quality + autonomous revision** over dashboard polish. See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
