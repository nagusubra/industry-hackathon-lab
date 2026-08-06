# Case 4 — Autonomous Battery Health and RUL Agent

**Stream:** Applied Physics, Aerospace & Electrical Engineering  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Lithium-ion batteries degrade through charge/discharge cycling and calendar aging. Predicting **State of Health (SOH)** and **Remaining Useful Life (RUL)** from cycling, impedance, and EIS data — and proposing **duty-cycle derate policies** — is a core hard-science energy-storage PHM problem.

**Your challenge:** Build an **autonomous agent** that tracks capacity fade, predicts RUL, and iteratively proposes operating adjustments evaluated against quantitative battery-health metrics — not a static notebook with a single offline fit.

---

## Industrial Significance

- Battery degradation drives EV range anxiety, grid-storage economics, and aerospace / UAV mission planning.
- NASA’s **PCoE Li-ion Battery Aging** datasets are the community benchmark for data-driven battery prognostics.
- Closed-loop derate policies mirror BMS (battery management system) strategies in automotive and stationary storage.
- Alberta’s EV, grid-storage, and remote-energy sectors benefit from transferable battery-health agent patterns.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Ingest charge/discharge voltage–current cycles and capacity fade from NASA `.mat` files — or synthetic capacity-fade trajectories.
2. **Diagnose:** Estimate SOH from cycle features (voltage curves, internal resistance proxies).
3. **Predict:** Forecast RUL (cycles to end-of-life threshold, e.g. 70% rated capacity).
4. **Act & Iterate:** Agent proposes derate / charge-rate limits; re-evaluate RUL error and safety margin.
5. **Stretch:** EIS impedance features, multi-cell fleet ranking, or uncertainty-aware prognostics.

---

## Recommended Agent Architecture & Starter Code Pointers

```
Cycle / EIS data  ->  Health encoder  ->  RUL regressor  ->  Derate policy
         ^                      |                  |
         +----- re-simulate fade after policy change -----+
```

**Starter frameworks (open source):**
- [NASA Li-ion Battery Aging Datasets](https://data.nasa.gov/dataset/li-ion-battery-aging-datasets)
- Direct zip: https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip
- License: Public domain / US Government Works
- Optional variety: [Randomized Battery Usage on Zenodo](https://zenodo.org/records/10668737)
- scikit-learn / PyTorch for prognostics

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
| RUL MAE / RMSE (cycles) | Report on held-out cells |
| SOH estimation error | MAE on capacity fade trajectory |
| Prognostic horizon | Early, calibrated end-of-life warnings |
| Derate policy impact | Simulated capacity-life extension vs. baseline |
| Autonomy | Closed-loop propose → evaluate → revise on held-out cell |
| Practicality | Demo trains/infers within hackathon compute limits |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
