# Case 1 — Autonomous Structural-Health and Aerodynamic-Design Agent

**Stream:** Applied Physics, Aerospace & Electrical Engineering  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Aerospace assets degrade under complex thermo-mechanical and aerodynamic loads. Predicting **Remaining Useful Life (RUL)** for turbofan engines from multi-sensor streams — and optionally coupling that to aerodynamic design feedback — is a classic hard-science PHM (prognostics and health management) problem.

**Your challenge:** Build an **autonomous agent** that monitors engine sensor trajectories, diagnoses degradation modes, predicts RUL, and iteratively proposes maintenance / operating / design actions evaluated against quantitative aerospace metrics — not a static notebook with a single offline fit.

---

## Industrial Significance

- Unplanned engine removals and in-flight shutdowns drive airline cost, safety risk, and fleet availability.
- NASA’s C-MAPSS turbofan datasets are the community benchmark for data-driven prognostics used across industry and academia.
- Combining structural health signals with aerodynamic performance (lift/drag, high-lift behavior) mirrors digital-twin ambitions in aerospace OEMs and MRO providers.
- Alberta’s growing aerospace / UAV / energy-turbomachinery ecosystem benefits from transferable PHM agent patterns.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Ingest NASA C-MAPSS multivariate sensor time series (FD001–FD004) with operational settings.
2. **Diagnose:** Infer health indices / fault progression under one or more operating conditions and fault modes.
3. **Predict:** Estimate RUL on held-out test trajectories with calibrated uncertainty.
4. **Act & Iterate:** Agent proposes inspection thresholds, derate schedules, or (stretch) aerodynamic geometry tweaks; re-evaluate against RUL / performance metrics.
5. **Stretch — Aero:** Use force/moment CSVs from NVIDIA HiLiftAeroML (NASA CRM high-lift) to train a surrogate and let the agent search geometry / AoA trade-offs offline (full volume CFD is too large to download wholesale — use metadata + force files).

---

## Recommended Agent Architecture & Starter Code Pointers

```
Sensors / AoA,geo  ->  Health encoder  ->  RUL / aero surrogate  ->  Action policy
         ^                         |                    |
         +----- re-simulate / re-score after action ----+
```

**Starter frameworks (open source):**
- NASA [C-MAPSS Jet Engine Simulated Data](https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data)
- scikit-learn / PyTorch / [sktime](https://www.sktime.net/) for time-series prognostics
- Stretch aero: [HiLiftAeroML on Hugging Face](https://huggingface.co/datasets/nvidia/HiLiftAeroML) (CC-BY-4.0) — download **force_mom_*.csv** subsets only
- Optional CAD/CFD tools: OpenVSP, XFOIL, SU2 (for teams with aero expertise)

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
| RUL RMSE / MAE (cycles) | Report on FD001 (baseline) and optionally harder FD002–FD004 |
| Prognostic Horizon / Timeliness | Prefer early, calibrated warnings over late overconfident ones |
| Score vs. PHM challenge-style asymmetric penalties | Optional; document if used |
| Aero stretch: force prediction MAE on Cl/Cd | If using HiLiftAeroML force CSVs |
| Autonomy | Closed-loop propose → evaluate → revise on at least one held-out engine |
| Practicality | Demo trains/infers within hackathon compute limits |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
