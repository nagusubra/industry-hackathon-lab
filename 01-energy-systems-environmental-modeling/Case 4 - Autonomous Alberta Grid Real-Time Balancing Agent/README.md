# Case 4 — Autonomous Alberta Grid Real-Time Balancing Agent

**Stream:** Energy Systems & Environmental Modeling  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

The Alberta Electric System Operator (AESO) must continuously balance supply and demand across a grid with growing wind, solar, storage, and flexible gas generation. Real-time visibility into Alberta Internal Load (AIL), generation mix, and pool price dynamics is essential — yet operators still rely on manual interpretation of reports and dashboards.

**Your challenge:** Build an **autonomous AI agent** that perceives AESO supply/demand and generation-mix signals, reasons about imbalance and pool-price risk, and iteratively recommends storage / demand-response actions — closing the loop from live grid state → risk assessment → evaluated action, not a static report viewer.

---

## Industrial Significance

- **Local relevance:** Hackathon hosted in Calgary, Alberta — AESO is the balancing authority for the province's electricity market.
- Alberta's grid is transitioning rapidly: wind and solar capacity are growing, storage pilots are launching, and real-time balancing complexity is increasing.
- AESO publishes free Current Supply/Demand reports and historical pool-price data via the Energy Trading System (ETS) — ideal for building industrially grounded balancing agents without proprietary SCADA access.
- Agents that reduce imbalance exposure, improve reserve positioning, or optimize storage/DR dispatch against pool-price volatility have direct economic value for utilities, retailers, and industrial load customers.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Ingest AESO Current Supply/Demand (AIL, wind, solar, storage, gas, imports/exports) and historical pool-price / system marginal price series.
2. **Predict:** Optional short-horizon load and renewable generation forecasts with uncertainty.
3. **Reason:** Compute imbalance risk scores, reserve shortfall indicators, and pool-price volatility proxies.
4. **Act & Iterate:** Recommend storage charge/discharge, DR curtailment, or reserve holds; evaluate actions in a simplified balancing simulation and revise when risk thresholds change.
5. **Explain:** Emit operator-facing summaries: AIL vs. supply gap, renewable share, recommended actions, expected cost/risk reduction.

Stretch goals: couple AESO JSON API for automated ingestion; multi-hour rolling horizon; carbon intensity of marginal generation.

---

## Recommended Agent Architecture & Starter Code Pointers

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Reason     │ -> │  Tool / Sim    │ -> │  Act / Log  │
│ AESO CSD +  │    │ imbalance +  │    │ balancing area │    │ storage/DR  │
│ pool price  │    │ price risk   │    │ sandbox model  │    │ recommend   │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
                              ^                                     |
                              +------------- evaluate --------------+
```

**Starter references (AESO open data):**
- **Current Supply/Demand (no login):** http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet
- **Historical reports (no login):** http://ets.aeso.ca/ets_web/ip/IPHistoricalReportsServlet
- **Optional JSON API (free key):** https://www.aeso.ca/market/market-and-system-reporting/aeso-application-programming-interface-api/

**In this folder:**
- [`agent_starter.py`](agent_starter.py) — perceive / reason / act skeleton wired to local CSV paths
- [`requirements.txt`](requirements.txt) — core Python dependencies
- [`data/README.md`](data/README.md) — verified data access links, schemas, and download steps

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
| Imbalance risk score | Reduce vs. no-action baseline over held-out hours/days |
| Pool-price exposure ($) | Report estimated cost of imbalance under recommended actions |
| Renewable integration | Track wind+solar share vs. AIL; minimize curtailment proxy |
| Reserve adequacy | Zero hard violations of simplified reserve constraints in simulation |
| Agent loop autonomy | ≥ 1 closed-loop iteration (propose → simulate → revise) without human prompts |
| Runtime practicality | End-to-end demo runnable within the 48-hour prototype window |

Judges will prioritize **Alberta grid realism + autonomous tool use** over UI polish alone. See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
